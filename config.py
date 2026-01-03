import os


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///canciones.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GITHUB_OWNER = os.environ.get("GITHUB_OWNER", "ucbtrigales")
    GITHUB_REPO = os.environ.get("GITHUB_REPO", "acordes")
    GITHUB_PATH = os.environ.get("GITHUB_PATH", "Chordpro")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


CONFIG_BY_NAME = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}


def get_config():
    env = os.environ.get("APP_ENV", "dev").lower()
    return CONFIG_BY_NAME.get(env, DevelopmentConfig)
