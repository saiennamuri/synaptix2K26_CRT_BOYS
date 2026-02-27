from flask import Flask, render_template, request, redirect
from config import Config
import mysql.connector
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config.from_object(Config)


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"]
    )

def send_email(to_email, subject, body):
     try:
        msg = MIMEMultipart()
        msg["From"] = app.config["EMAIL_USER"]
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(
            app.config["EMAIL_USER"],
            app.config["EMAIL_PASSWORD"]
        )

        server.sendmail(
            app.config["EMAIL_USER"],
            to_email,
            msg.as_string()
        )

        server.quit()

        print("Email sent successfully to", to_email)

     except Exception as e:
        print("EMAIL ERROR:", str(e))
# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("home.html")


# ---------------- CANDIDATE REGISTER ----------------

@app.route("/candidate/register", methods=["GET", "POST"])
def candidate_register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        technical_skills = request.form.get("technical_skills")
        communication_skill = int(request.form.get("communication_skill"))
        experience = int(request.form.get("experience"))
        graduation = request.form.get("graduation")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("""
                INSERT INTO candidates
                (name, email, technical_skills, communication_skill, experience, graduation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, technical_skills,
                  communication_skill, experience, graduation))

            connection.commit()

        except Exception as e:
            connection.rollback()
            print("Database error:", e)

        finally:
            cursor.close()
            connection.close()

        # SEND EMAIL (only inside POST)
        try:
            email_body = f"""
Dear {name},

Your registration on Skill Match Platform was successful.

Regards,
Skill Match Team
"""
            send_email(
                email,
                "Registration Successful - Skill Match Platform",
                email_body
            )

        except Exception as e:
            print("Email sending error:", e)

        return render_template(
            "candidate_register.html",
            message="Registration Successful!"
        )

    return render_template("candidate_register.html")

# ---------------- DASHBOARD ----------------
from werkzeug.security import check_password_hash

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        password = request.form["password"]

        if password == app.config["ADMIN_PASSWORD"]:
            return redirect("/admin/dashboard")
        else:
            return render_template(
                "admin_login.html",
                error="Invalid Password"
            )

    return render_template("admin_login.html")
@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


# ---------------- CREATE PROJECT + SCORING ----------------

@app.route("/admin/create-project", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        project_name = request.form["project_name"]
        required_skills = request.form["required_skills"]
        required_experience = int(request.form["required_experience"])

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Insert project
        cursor.execute("""
            INSERT INTO projects (project_name, required_skills, required_experience)
            VALUES (%s, %s, %s)
        """, (project_name, required_skills, required_experience))

        connection.commit()
        project_id = cursor.lastrowid

        # Fetch candidates
        cursor.execute("SELECT * FROM candidates")
        candidates = cursor.fetchall()

        required_skill_list = [s.strip().lower() for s in required_skills.split(",")]

        for candidate in candidates:

            # ---------------- Candidate Skill List ----------------
            candidate_skill_list = [
                skill.strip().lower()
                for skill in candidate["technical_skills"].split(",")
            ]

            # ---------------- SKILL BREAKDOWN ----------------
            skill_analysis = {}
            matched_skills = []
            missing_skills = []

            for skill in required_skill_list:
                if skill in candidate_skill_list:
                    skill_analysis[skill] = 100
                    matched_skills.append(skill)
                else:
                    skill_analysis[skill] = 0
                    missing_skills.append(skill)

            # Technical Score
            tech_score = (
                sum(skill_analysis.values()) / len(required_skill_list)
                if required_skill_list else 0
            )

            # ---------------- EXPERIENCE MATCH ----------------
            if candidate["experience"] >= required_experience:
                exp_score = 100
            else:
                exp_score = (
                    (candidate["experience"] / required_experience) * 100
                    if required_experience > 0 else 0
                )

            # ---------------- COMMUNICATION MATCH ----------------
            comm_score = (candidate["communication_skill"] / 10) * 100

            # ---------------- FINAL WEIGHTED SCORE ----------------
            final_score = (
                (tech_score * 0.5) +
                (exp_score * 0.3) +
                (comm_score * 0.2)
            )

            # ---------------- SUGGESTIONS ----------------
            suggestions = []

            if missing_skills:
                suggestions.append(
                    f"Improve skills in: {', '.join(missing_skills)}"
                )

            if candidate["experience"] < required_experience:
                suggestions.append(
                    "Gain more real-world project experience"
                )

            if candidate["communication_skill"] < 6:
                suggestions.append(
                    "Improve communication and presentation skills"
                )

            if not suggestions:
                suggestions.append(
                    "Excellent fit for this project. Highly recommended."
                )

            # ---------------- EXPLANATION TEXT ----------------
            explanation = f"""
Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}

Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

Experience: {candidate['experience']} years (Required: {required_experience})

Communication Skill: {candidate['communication_skill']}/10

Suggestions:
- {'\n- '.join(suggestions)}
"""

            # Convert skill breakdown to JSON
            skill_analysis_json = json.dumps(skill_analysis)

            # ---------------- INSERT INTO SCORES ----------------
            cursor.execute("""
                INSERT INTO scores
                (candidate_id, project_id, match_score, explanation,
                 tech_score, exp_score, comm_score, skill_breakdown)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                candidate["id"],
                project_id,
                round(final_score, 2),
                explanation,
                round(tech_score, 2),
                round(exp_score, 2),
                round(comm_score, 2),
                skill_analysis_json
            ))

        connection.commit()
        cursor.close()
        connection.close()

        return render_template(
            "create_project.html",
            message="Project Created & Scores Generated Successfully!"
        )

    return render_template("create_project.html")
# ---------------- SELECT PROJECT ----------------

@app.route("/admin/results")
def view_projects():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT p.id, p.project_name, p.required_skills,
               COUNT(s.id) AS total_candidates
        FROM projects p
        LEFT JOIN scores s ON p.id = s.project_id
        GROUP BY p.id
    """)

    projects = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("select_project.html", projects=projects)


# ---------------- PROJECT RESULTS ----------------

@app.route("/admin/results/<int:project_id>")
def project_results(project_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.id AS score_id,
               c.name,
               c.email,
               s.match_score
        FROM scores s
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.project_id = %s
        ORDER BY s.match_score DESC
    """, (project_id,))

    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("results.html", results=results)


# ---------------- CANDIDATE DETAIL ----------------

@app.route("/admin/result/<int:score_id>")
def candidate_detail(score_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.id AS score_id,
               s.match_score,
               s.explanation,
               s.project_id,
               s.tech_score,
               s.exp_score,
               s.comm_score,
               s.skill_breakdown,
               c.name,
               c.email
        FROM scores s
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.id = %s
    """, (score_id,))

    result = cursor.fetchone()
    cursor.close()
    connection.close()

    import json
    if result and result["skill_breakdown"]:
        result["skill_breakdown"] = json.loads(result["skill_breakdown"])
    else:
        result["skill_breakdown"] = {}

    return render_template("candidate_detail.html", result=result)
@app.route("/admin/send-email/<int:score_id>", methods=["POST"])
def send_result_email(score_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.match_score,
               s.explanation,
               c.name,
               c.email
        FROM scores s
        JOIN candidates c ON s.candidate_id = c.id
        WHERE s.id = %s
    """, (score_id,))

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        email_body = f"""
Dear {result['name']},

Your project evaluation is complete.

Final Match Score: {result['match_score']}%

Detailed Explanation:
{result['explanation']}

Regards,
Skill Match Platform
"""

        send_email(
            result["email"],
            "Your Evaluation Result - Skill Match Platform",
            email_body
        )

    return redirect(request.referrer)
if __name__ == "__main__":
    app.run(debug=True)