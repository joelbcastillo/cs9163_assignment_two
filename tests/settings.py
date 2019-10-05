"""Settings module for test app."""
import os

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TMP_PATH = os.path.join(PROJECT_ROOT, "tmp")

ENV = "development"
TESTING = True
if os.name == "nt":
    SQLALCHEMY_DATABASE_URI = "sqlite:///{db_path}".format(
        db_path=os.path.join(TMP_PATH, "tmp.db")
    )
else:
    SQLALCHEMY_DATABASE_URI = "sqlite://{db_path}".format(
        db_path=os.path.join(TMP_PATH, "tmp.db")
    )
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = (
    4
)  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
DEBUG_TB_ENABLED = False
CACHE_TYPE = "simple"
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False  # Allows form testing
