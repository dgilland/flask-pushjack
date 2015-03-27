**************
Flask-Pushjack
**************

|version| |travis| |coveralls| |license|

Flask extension for push notifications on APNS (iOS) and GCM (Android).


Links
=====

- Project: https://github.com/dgilland/flask-pushjack
- Documentation: http://flask-pushjack.readthedocs.org
- PyPi: https://pypi.python.org/pypi/flask-pushjack/
- TravisCI: https://travis-ci.org/dgilland/flask-pushjack


Quickstart
==========

Whether using ``APNS`` or ``GCM``, Flask-Pushjack provides a common API interface for each.


APNS
----

.. code-block:: python

    from flask import Flask
    from flask_pushjack import FlaskAPNS

    config = {
        'APNS_CERTIFICATE': '<path/to/certificate.pem>'
    }

    app = Flask(__name__)
    app.config.update(config)

    client = FlaskAPNS()
    client.init_app(app)

    with app.app_context():
        # Send to single device.
        client.send(token, alert, **options)

        # Send to multiple devices.
        client.send_bulk(tokens, alert, **options)

        # Get expired tokens.
        expired = client.get_expired_tokens()


GCM
---

.. code-block:: python

    from flask import Flask
    from flask_pushjack import FlaskGCM

    config = {
        'GCM_API_KEY': '<api key>'
    }

    app = Flask(__name__)
    app.config.update(config)

    client = FlaskGCM()
    client.init_app(app)

    with app.app_context():
        # Send to single device.
        client.send(token, alert, **options)

        # Send to multiple devices.
        client.send_bulk(tokens, alert, **options)


Configuration
-------------

APNS
++++

==================================  ===
``APNS_ENABLED``                    Whether to enable sending. Default ``True``
``APNS_SANDBOX``                    Whether to use default sandbox settings. Default: ``False``
``APNS_CERTIFICATE``                File path to certificate PEM file (**must be set**). Default: ``None``
``APNS_HOST``                       APNS push server host. Default: ``'gateway.push.apple.com'``
``APNS_PORT``                       APNS push server port. Default: ``2195``
``APNS_FEEDBACK_HOST``              APNS feedback server host. Default: ``'feedback.push.apple.com'``
``APNS_FEEDBACK_PORT``              APNS feedback server port. Default: ``2196``
``APNS_ERROR_TIMEOUT``              Socket error timeout. Default: ``0.5``
``APNS_DEFAULT_EXPIRATION_OFFSET``  Message expiration (secs) from now. Default: ``2592000`` (1 month)
``APNS_MAX_NOTIFICATION_SIZE``      Maximum length of message. Default: ``2048``
==================================  ===


GCM
+++

======================  ===
``GCM_ENABLED``         Whether to enable sending. Default ``True``
``GCM_API_KEY``         API key (**must be set**). Default: ``None``
``GCM_URL``             GCM send URL. Default: ``'https://android.googleapis.com/gcm/send'``
``GCM_MAX_RECIPIENTS``  Max recipients per bulk send. Default: ``1000``
======================  ===


.. |version| image:: http://img.shields.io/pypi/v/flask-pushjack.svg?style=flat-square
    :target: https://pypi.python.org/pypi/flask-pushjack/

.. |travis| image:: http://img.shields.io/travis/dgilland/flask-pushjack/master.svg?style=flat-square
    :target: https://travis-ci.org/dgilland/flask-pushjack

.. |coveralls| image:: http://img.shields.io/coveralls/dgilland/flask-pushjack/master.svg?style=flat-square
    :target: https://coveralls.io/r/dgilland/flask-pushjack

.. |license| image:: http://img.shields.io/pypi/l/flask-pushjack.svg?style=flat-square
    :target: https://pypi.python.org/pypi/flask-pushjack/
