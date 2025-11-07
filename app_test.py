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
    """Temp CONFIG_DIR; verify application.properties is read."""
    tmpdir = tempfile.mkdtemp()
    try:
        prop_path = os.path.join(tmpdir, 'application.properties')
        content = 'key1=value1\nkey2=value2'
        with open(prop_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)

        # set CONFIG_DIR before importing app so it reads at import time
        os.environ['CONFIG_DIR'] = tmpdir
        # reload the app module to pick up the config
        # import inside test so module picks up CONFIG_DIR
        import app as app_module  # pylint: disable=import-outside-toplevel
        importlib.reload(app_module)
        client = app_module.app.test_client()
        resp = client.get('/env')
        assert resp.status_code == 200
        data = json.loads(resp.data)
        key = 'application.properties.from.configmap'
        assert data.get(key) == content
    finally:
        shutil.rmtree(tmpdir)


def test_application_secret_properties_from_secret():
    """Temp SECRET_CONFIG_DIR; verify secret file is read."""
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
        secret_key = 'application.secret.properties.from.secret'
        assert data.get(secret_key) == secret_content
    finally:
        shutil.rmtree(tmpdir)
