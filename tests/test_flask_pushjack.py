
import flask
import mock
import pytest

from flask_pushjack import FlaskAPNS, FlaskGCM


parametrize = pytest.mark.parametrize


def issubset(subset, superset):
    return all(item in superset.items() for item in subset.items())


@pytest.fixture(scope='function')
def app(request):
    """Provide instance for basic Flask app."""
    app = flask.Flask(__name__)
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    return app


@parametrize('extension_class,base_config,expected', [
    (FlaskAPNS,
     {'APNS_CERTIFICATE': None},
     {'APNS_ENABLED': True,
      'APNS_SANDBOX': False,
      'APNS_CERTIFICATE': None,
      'APNS_DEFAULT_ERROR_TIMEOUT': 10,
      'APNS_DEFAULT_EXPIRATION_OFFSET': 60 * 60 * 24 * 30,
      'APNS_DEFAULT_BATCH_SIZE': 100}),
    (FlaskAPNS,
     {'APNS_CERTIFICATE': None, 'APNS_SANDBOX': True},
     {'APNS_ENABLED': True,
      'APNS_SANDBOX': True,
      'APNS_CERTIFICATE': None,
      'APNS_DEFAULT_ERROR_TIMEOUT': 10,
      'APNS_DEFAULT_EXPIRATION_OFFSET': 60 * 60 * 24 * 30,
      'APNS_DEFAULT_BATCH_SIZE': 100}),
    (FlaskGCM,
     {'GCM_API_KEY': None},
     {'GCM_API_KEY': None})
])
def test_default_configuration(app, extension_class, base_config, expected):
    app.config.update(base_config)
    client = extension_class()
    client.init_app(app)
    assert issubset(expected, app.config)


@parametrize('extension_class,config,method,send_object,args', [
    (FlaskAPNS,
     {'APNS_CERTIFICATE': None},
     'send',
     'pushjack.apns.APNSClient.send',
     ([], 'hello')),
    (FlaskAPNS,
     {'APNS_CERTIFICATE': None},
     'get_expired_tokens',
     'pushjack.apns.APNSClient.get_expired_tokens',
     ()),
    (FlaskGCM,
     {'GCM_API_KEY': None},
     'send',
     'pushjack.gcm.GCMClient.send',
     ([], 'hello')),
])
def test_client_methods(app,
                        extension_class,
                        config,
                        method,
                        send_object,
                        args):
    with mock.patch(send_object) as patched:
        app.config.update(config)
        client = extension_class()
        client.init_app(app)

        with app.app_context():
            getattr(client, method)(*args)

        assert patched.called
        send_args = list(args)
        patched.assert_called_with(*send_args)
