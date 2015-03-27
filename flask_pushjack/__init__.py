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

from flask import current_app
from pushjack import (
    APNSClient,
    GCMClient,
    create_apns_sandbox_config,
    create_apns_config,
    create_gcm_config
)


__all__ = (
    'FlaskAPNS',
    'FlaskGCM',
)


class FlaskPushjack(object):
    """Base class for Flask push notification client extensions."""
    client_class = None
    _config_prefix = None
    _extension_name = 'pushjack'

    def __init__(self, app=None):
        self.app = app

        if app is not None:  # pragma: no cover
            self.init_app(app)

    def init_app(self, app):
        """Initialize extension with application configuration."""
        self.init_config(app)

        # pylint: disable=not-callable
        client = self.client_class(app.config)

        if not hasattr(app, 'extensions'):  # pragma: no cover
            app.extensions = {}

        app.extensions[self._extension_name] = {
            'client': client
        }

    def init_config(self, app):  # pragma: no cover
        """Initialize configuration specifically for client."""
        raise NotImplementedError

    @property
    def client(self):
        """Return push notification client associated with current app."""
        return current_app.extensions[self._extension_name]['client']

    @property
    def enabled(self):
        """Return whether client is enabled."""
        return current_app.config.get(self._config_prefix + 'ENABLED')

    def send(self, registration_id, alert, **options):
        """Send push notification to single recipient."""
        if self.enabled:
            return self.client.send(registration_id, alert, **options)

    def send_bulk(self, registration_ids, alert, **options):
        """Send push notification to multiple recpients."""
        if self.enabled:
            return self.client.send_bulk(registration_ids, alert, **options)


class FlaskAPNS(FlaskPushjack):
    """Flask extension for APNS client."""
    client_class = APNSClient
    _config_prefix = 'APNS_'
    _extension_name = 'pushjack.apns'

    def init_config(self, app):
        """Initialize client configuration."""
        app.config.setdefault('APNS_ENABLED', True)
        app.config.setdefault('APNS_SANDBOX', False)

        if app.config['APNS_SANDBOX']:
            create_config = create_apns_sandbox_config
        else:
            create_config = create_apns_config

        app.config.update(create_config(app.config))

    def get_expired_tokens(self):
        """Return expired tokens."""
        if self.enabled:
            return self.client.get_expired_tokens()


class FlaskGCM(FlaskPushjack):
    """Flask extension for GCM client."""
    client_class = GCMClient
    _config_prefix = 'GCM_'
    _extension_name = 'pushjack.gcm'

    def init_config(self, app):
        """Initialize client configuration."""
        app.config.setdefault('GCM_ENABLED', True)
        app.config.update(create_gcm_config(app.config))
