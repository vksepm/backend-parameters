"""Example of flask main file."""
import os
import io

from flask import Flask, jsonify


app = Flask(__name__)

# Keys exposed by the /env endpoint. Define as constants to avoid duplication
APPLICATION_PROPERTIES_KEY = 'application.properties.from.configmap'
APPLICATION_SECRET_KEY = 'application.secret.properties.from.secret'


# Load application.properties from the config directory (mounted ConfigMap)
# Default mount path is /config, but can be overridden with CONFIG_DIR env var.
def _load_application_properties():
    config_dir = os.environ.get('CONFIG_DIR', '/config')
    prop_path = os.path.join(config_dir, 'application.properties')
    try:
        with io.open(prop_path, 'r', encoding='utf-8') as file_handle:
            content = file_handle.read()
            # store the raw content in app.config under the dotted key
            app.config[APPLICATION_PROPERTIES_KEY] = content
    except (FileNotFoundError, OSError):
        # If file doesn't exist or can't be read, leave the config unset
        return


_load_application_properties()


def _load_application_secret():
    """Load application.secret.properties from the secret mount path.

    Default mount path is /secret-config but can be overridden with
    the `SECRET_CONFIG_DIR` environment variable.
    """
    secret_dir = os.environ.get('SECRET_CONFIG_DIR', '/secret-config')
    secret_path = os.path.join(secret_dir, 'application.secret.properties')
    try:
        with io.open(secret_path, 'r', encoding='utf-8') as file_handle:
            content = file_handle.read()
            app.config[APPLICATION_SECRET_KEY] = content
    except (FileNotFoundError, OSError):
        return


_load_application_secret()


@app.route('/api/hello')
def hello_world():
    """Returns Hello, EDP!"""
    return 'Hello, EDP!'


@app.route('/env')
def env():
    """Return all environment variables as JSON."""
    # Include environment variables plus the application.properties content
    env_vars = dict(os.environ.items())
    # application.properties content is stored in app.config under the key
    # 'application.properties.from.configmap'. Expose it in the env output
    # with the dotted key requested.
    app_prop = app.config.get(APPLICATION_PROPERTIES_KEY)
    if app_prop is not None:
        env_vars[APPLICATION_PROPERTIES_KEY] = app_prop
    secret_prop = app.config.get(APPLICATION_SECRET_KEY)
    if secret_prop is not None:
        env_vars[APPLICATION_SECRET_KEY] = secret_prop
    return jsonify(env_vars)


if __name__ == '__main__':
    app.run()
