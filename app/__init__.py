import logging
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev-secret-key-change-later'

    from app.routes import main
    app.register_blueprint(main)

    # Catches anything our own routes didn't handle explicitly — e.g. a URL
    # that doesn't match any route at all, or an unexpected exception in
    # our own code. Without these, Flask would show its raw debug traceback
    # (fine while developing, unacceptable in a demo or in front of anyone
    # else — it leaks file paths and source code).
    @app.errorhandler(404)
    def handle_not_found(error):
        return render_template('error.html', code=404, heading='Not Found',
                                message="The page you're looking for doesn't exist."), 404

    @app.errorhandler(403)
    def handle_forbidden(error):
        return render_template('error.html', code=403, heading='Access Denied',
                                message="You don't have permission to view this page."), 403

    @app.errorhandler(500)
    def handle_server_error(error):
        # Log the real error to the console/log file for debugging, but never
        # show the user (or a viva panel) the raw traceback.
        app.logger.error(f"Unhandled server error: {error}")
        return render_template('error.html', code=500, heading='Something Went Wrong',
                                message="An unexpected error occurred. Please try again."), 500

    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    return app
