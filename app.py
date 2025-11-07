"""Example of flask main file."""
import os
import io

from flask import Flask, jsonify


app = Flask(__name__)


# Load application.properties from the config directory (mounted ConfigMap)
# Default mount path is /config, but can be overridden with CONFIG_DIR env var.
def _load_application_properties():
    config_dir = os.environ.get('CONFIG_DIR', '/config')
    prop_path = os.path.join(config_dir, 'application.properties')
    try:
        with io.open(prop_path, 'r', encoding='utf-8') as file_handle:
            content = file_handle.read()
            # store the raw content in app.config under the dotted key
            app.config['application.properties.from.configmap'] = content
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
            app.config['application.secret.properties.from.secret'] = content
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
    app_prop = app.config.get('application.properties.from.configmap')
    if app_prop is not None:
        env_vars['application.properties.from.configmap'] = app_prop
    secret_prop = app.config.get('application.secret.properties.from.secret')
    if secret_prop is not None:
        env_vars['application.secret.properties.from.secret'] = secret_prop
    return jsonify(env_vars)


if __name__ == '__main__':
    app.run()
