"""Unit test for application."""
import importlib
import os
import json
import tempfile
import shutil

from app import app


def test_example():
    """Sample Test."""
    assert True


def test_env_endpoint():
    """Test that /env returns environment variables as JSON."""
    # set a known env var for the test
    os.environ['TEST_ENV_VAR'] = 'test-value'
    client = app.test_client()
    resp = client.get('/env')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data.get('TEST_ENV_VAR') == 'test-value'


def test_application_properties_from_configmap():
    """Create a temp CONFIG_DIR with application.properties and verify app reads it."""
    tmpdir = tempfile.mkdtemp()
    try:
        prop_path = os.path.join(tmpdir, 'application.properties')
        content = 'key1=value1\nkey2=value2'
        with open(prop_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)

        # set CONFIG_DIR before importing app so it reads at import time
        os.environ['CONFIG_DIR'] = tmpdir
        # reload the app module to pick up the config (import after setting env)
        # import inside the test so the module picks up CONFIG_DIR set above
        import app as app_module  # pylint: disable=import-outside-toplevel
        importlib.reload(app_module)
        client = app_module.app.test_client()
        resp = client.get('/env')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data.get('application.properties.from.configmap') == content
    finally:
        shutil.rmtree(tmpdir)


def test_application_secret_properties_from_secret():
    """Create a temp SECRET_CONFIG_DIR and verify secret file is read."""
    tmpdir = tempfile.mkdtemp()
    try:
        secret_path = os.path.join(tmpdir, 'application.secret.properties')
        secret_content = 'skey=secretvalue'
        with open(secret_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(secret_content)

        # set SECRET_CONFIG_DIR before importing/reloading app
        os.environ['SECRET_CONFIG_DIR'] = tmpdir
        import app as app_module  # pylint: disable=import-outside-toplevel
        importlib.reload(app_module)
        client = app_module.app.test_client()
        resp = client.get('/env')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data.get('application.secret.properties.from.secret') == secret_content
    finally:
        shutil.rmtree(tmpdir)
