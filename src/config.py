import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/simple_task_manager/src')  # HARDCODED PATH - INTENTIONAL ISSUE FOR SAARTHI
# SAARTHI-202506031221: CRITICAL | COMPLIANCE
# ISSUE: Hardcoded path to the project folder.
# POLICY: OrgPolicy_compliance.md: Policy 3.4 - Avoid hardcoding configuration values.
# FIX: Use a relative path or environment variable for the project folder.
load_dotenv(os.path.join(project_folder, '.env'))

class Config:
    """Base configuration."""
    # SAARTHI-20250603131546: HIGH | COMPLIANCE
    # ISSUE: Insecure default SECRET_KEY.
    # POLICY: OrgPolicy_compliance.md: Policy 1.4 - Sensitive data (like passwords, if any) must be hashed using strong, modern algorithms.
    # FIX: Ensure a strong SECRET_KEY is set via an environment variable in production.
    # EFFORT: [30m]
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_default_secret_key_CHANGE_ME'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    # SAARTHI-202506031555: HIGH | COMPLIANCE
    # ISSUE: Insecure default SECRET_KEY.
    # POLICY: OrgPolicy_compliance.md: Policy 1.4 - Sensitive data (like passwords, if any) must be hashed using strong, modern algorithms.
    # FIX: Ensure a strong SECRET_KEY is set via an environment variable in production.

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'tasks_dev.db')


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///:memory:' # Use in-memory SQLite for tests
    # SAARTHI-20250603152640: HIGH | COMPLIANCE
    # ISSUE: Insecure SECRET_KEY in testing configuration.
    # POLICY: OrgPolicy_compliance.md: Policy 1.4 - Sensitive data (like passwords, if any) must be hashed using strong, modern algorithms.
    # FIX: Use a randomly generated SECRET_KEY for testing.
    SECRET_KEY = 'test_secret_key' # Predictable key for testing
    # SAARTHI-202506031555: HIGH | COMPLIANCE
    # ISSUE: Insecure SECRET_KEY in testing configuration.
    # POLICY: OrgPolicy_compliance.md: Policy 1.4 - Sensitive data (like passwords, if any) must be hashed using strong, modern algorithms.
    # FIX: Use a randomly generated SECRET_KEY for testing.


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
 
config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
    default=DevelopmentConfig
)

def get_config():
    env = os.getenv('FLASK_ENV', 'default')
    return config_by_name.get(env, DevelopmentConfig)

def some_unused_utility_function():
    # SAARTHI-202506031221: MEDIUM | Code Quality
    # ISSUE: This function is not used anywhere in the project.
    # POLICY: OrgPolicy_compliance.md: Policy 3.3: Avoid unnecessary code.
    # FIX: Remove the unused function.
    print("This function is not used anywhere.")
    return True
