import pandas as pd
import numpy as np

np.random.seed(42)

rows = 10000

# Generate realistic scores
tech_score = np.random.randint(40, 100, rows)
exp_score = np.random.randint(30, 100, rows)
comm_score = np.random.randint(30, 100, rows)

# Create weighted realistic final score with some noise
final_score = (
    (tech_score * 0.5) +
    (exp_score * 0.3) +
    (comm_score * 0.2) +
    np.random.normal(0, 5, rows)  # slight noise
)

df = pd.DataFrame({
    "tech_score": tech_score,
    "exp_score": exp_score,
    "comm_score": comm_score,
    "final_score": final_score
})

df.to_csv("training_data.csv", index=False)

print("Dataset with 10,000 rows created successfully!")