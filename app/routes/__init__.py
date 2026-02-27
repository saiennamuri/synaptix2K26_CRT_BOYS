# app/routes/__init__.py

from .candidate_routes import candidate_bp
from .project_routes import project_bp
from .match_routes import match_bp
from .admin_routes import admin_bp

# Optional: export all blueprints in one place
all_blueprints = [
    candidate_bp,
    project_bp,
    match_bp,
    admin_bp
]