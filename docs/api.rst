.. _api:

*************
API Reference
*************

The APNS and GCM Flask clients are thin wrappers around the pushjack APNS and GCM clients. For further details, see the `pushjack documentation <http://pushjack.readthedocs.org>`_.


APNS
====

.. autoclass:: flask_pushjack.FlaskAPNS
    :members: init_app, client, enabled, send, get_expired_tokens


GCM
===

.. autoclass:: flask_pushjack.FlaskGCM
    :members: init_app, client, enabled, send
