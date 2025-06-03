from flask import Flask
from flask_migrate import Migrate
from .models import db
from .routes import api_bp
from .config import get_config 
import logging

def create_app(config_name=None):

    app = Flask(__name__)
    if config_name is None:
        app_config = get_config()
    else:
        from .config import config_by_name
        app_config = config_by_name.get(config_name, config_by_name['default'])
    
    app.config.from_object(app_config)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(api_bp)

# SAARTHI-20250603142700: MEDIUM | COMPLIANCE
# ISSUE: Logging might contain sensitive data.
# POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
# FIX: Review all logging statements and ensure no sensitive data is logged.
    # SAARTHI-20250603131546: MEDIUM | COMPLIANCE
    # ISSUE: Logging might contain sensitive data.
    # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
    # FIX: Review all logging statements and ensure no sensitive data is logged.
    # EFFORT: [1h]
    logging.basicConfig(level=app.config.get('LOG_LEVEL', 'INFO'),
                        format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

    app.logger.info(f"Task Manager App created with env: {config_name or 'default'}")

    @app.route('/health')
    def health_check():
        """
        Health check endpoint.
        """
        # SAARTHI-202506031220: LOW | LINTING
        # ISSUE: There is a space after the colon in the dictionary definition.
        # POLICY: PEP 8 recommends no spaces around colons in dictionaries.
        # FIX: Remove the space after the colon.
        return {"status": "healthy", "message": "API is up and running!"}, 200


    return app


if __name__ == '__main__':
    # SAARTHI-20250603152603: MEDIUM | COMPLIANCE
    # ISSUE: Hardcoded environment configuration.
    # POLICY: OrgPolicy_compliance.md: Policy 3.4 - Avoid hardcoding configuration values.
    # FIX: Use an environment variable to configure the environment.
    app = create_app('dev')
    app.run(debug=True)
