
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


@parametrize('extension_class,expected', [
    (FlaskAPNS, {'APNS_ENABLED': True,
                 'APNS_SANDBOX': False,
                 'APNS_CERTIFICATE': None,
                 'APNS_HOST': 'gateway.push.apple.com',
                 'APNS_PORT': 2195,
                 'APNS_FEEDBACK_HOST': 'feedback.push.apple.com',
                 'APNS_FEEDBACK_PORT': 2196,
                 'APNS_ERROR_TIMEOUT': 0.5,
                 'APNS_DEFAULT_EXPIRATION_OFFSET': 60 * 60 * 24 * 30,
                 'APNS_MAX_NOTIFICATION_SIZE': 2048}),
    (FlaskAPNS, {'APNS_ENABLED': True,
                 'APNS_SANDBOX': True,
                 'APNS_CERTIFICATE': None,
                 'APNS_HOST': 'gateway.sandbox.push.apple.com',
                 'APNS_PORT': 2195,
                 'APNS_FEEDBACK_HOST': 'feedback.sandbox.push.apple.com',
                 'APNS_FEEDBACK_PORT': 2196,
                 'APNS_ERROR_TIMEOUT': 0.5,
                 'APNS_DEFAULT_EXPIRATION_OFFSET': 60 * 60 * 24 * 30,
                 'APNS_MAX_NOTIFICATION_SIZE': 2048}),
    (FlaskGCM, {'GCM_API_KEY': None,
                'GCM_URL': 'https://android.googleapis.com/gcm/send',
                'GCM_MAX_RECIPIENTS': 1000})
])
def test_default_configuration(app, extension_class, expected):
    app.config.update(expected)
    client = extension_class()
    client.init_app(app)
    assert issubset(expected, app.config)


@parametrize('extension_class,method,send_object,args', [
    (FlaskAPNS, 'send', 'pushjack.apns.send', ([], 'hello')),
    (FlaskAPNS, 'send_bulk', 'pushjack.apns.send_bulk', ([], 'hello')),
    (FlaskAPNS, 'get_expired_tokens', 'pushjack.apns.get_expired_tokens', ()),
    (FlaskGCM, 'send', 'pushjack.gcm.send', ([], 'hello')),
    (FlaskGCM, 'send_bulk', 'pushjack.gcm.send_bulk', ([], 'hello')),
])
def test_client_methods(app, extension_class, method, send_object, args):
    with mock.patch(send_object) as patched:
        client = extension_class()
        client.init_app(app)

        with app.app_context():
            getattr(client, method)(*args)

        assert patched.called
        send_args = list(args) + [app.config]
        patched.assert_called_with(*send_args)
