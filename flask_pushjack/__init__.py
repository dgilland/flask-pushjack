# -*- coding: utf-8 -*-
"""Flask-Pushjack module.
"""

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)

from functools import wraps

from flask import current_app
from pushjack import (
    APNSClient,
    APNSSandboxClient,
    GCMClient,
    apns
)


__all__ = (
    'FlaskAPNS',
    'FlaskGCM',
)


def enable(func):
    """Decorator that only executes class method if `self.enabled` is True."""
    @wraps(func)
    def decorated(self, *args, **kargs):
        if self.enabled:
            return func(self, *args, **kargs)
    return decorated


class FlaskPushjack(object):
    """Base class for Flask push notification client extensions."""
    client_class = None
    _config_prefix = None
    _extension_name = 'pushjack'

    def __init__(self, app=None):
        self.app = app

        if app is not None:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):  # pragma: no cover
        """Initialize extension with application configuration."""
        raise NotImplementedError

    def store_client(self, app, client):
        """Store reference to client on app.extensions."""
        app.extensions[self._extension_name] = {
            'client': client
        }

    @property
    def client(self):
        """Return push notification client associated with current app."""
        return current_app.extensions[self._extension_name]['client']

    @property
    def enabled(self):
        """Return whether client is enabled."""
        return current_app.config.get(self._config_prefix + 'ENABLED')

    @enable
    def send(self, ids, message, **options):
        """Send push notification to single or multiple recipients."""
        return self.client.send(ids, message, **options)


class FlaskAPNS(FlaskPushjack):
    """Flask extension for APNS client."""
    client_class = APNSClient
    client_sandbox_class = APNSSandboxClient

    _config_prefix = 'APNS_'
    _extension_name = 'pushjack.apns'

    def __init__(self, app=None):
        self.app = app

        if app is not None:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):
        """Initialize extension with application configuration."""
        config = app.config
        config.setdefault('APNS_ENABLED', True)
        config.setdefault('APNS_SANDBOX', False)
        config.setdefault('APNS_DEFAULT_ERROR_TIMEOUT',
                          apns.APNS_DEFAULT_ERROR_TIMEOUT)
        config.setdefault('APNS_DEFAULT_EXPIRATION_OFFSET',
                          apns.APNS_DEFAULT_EXPIRATION_OFFSET)
        config.setdefault('APNS_DEFAULT_BATCH_SIZE',
                          apns.APNS_DEFAULT_BATCH_SIZE)

        client_class = (self.client_class if not config['APNS_SANDBOX']
                        else self.client_sandbox_class)

        client = client_class(
            config['APNS_CERTIFICATE'],
            default_error_timeout=config['APNS_DEFAULT_ERROR_TIMEOUT'],
            default_expiration_offset=config['APNS_DEFAULT_EXPIRATION_OFFSET'],
            default_batch_size=config['APNS_DEFAULT_BATCH_SIZE'])

        self.store_client(app, client)

        if hasattr(app, 'teardown_appcontext'):
            # 0.9 and later
            teardown = app.teardown_appcontext
        elif hasattr(app, 'teardown_request'):  # pragma: no cover
            # 0.7 to 0.8
            teardown = app.teardown_request
        else:  # pragma: no cover
            # Older Flask versions
            teardown = app.after_request

        @teardown
        def close_client(response_or_exc):
            self.client.close()
            return response_or_exc

    @enable
    def get_expired_tokens(self):
        """Return expired tokens."""
        return self.client.get_expired_tokens()


class FlaskGCM(FlaskPushjack):
    """Flask extension for GCM client."""
    client_class = GCMClient

    _config_prefix = 'GCM_'
    _extension_name = 'pushjack.gcm'

    def init_app(self, app):
        """Initialize extension with application configuration."""
        app.config.setdefault('GCM_ENABLED', True)

        client = self.client_class(app.config['GCM_API_KEY'])

        self.store_client(app, client)
