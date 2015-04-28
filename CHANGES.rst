.. _changelog:

Changelog
=========


v1.0.0 (2015-04-28)
-------------------

- Add ``APNS_DEFAULT_BATCH_SIZE=100`` config option.
- Pin ``pushjack`` dependency version to ``>=1.0.0``. (**breaking change**)
- Remove ``send_bulk`` method as bulk sending is now accomplished by the ``send`` function. (**breaking change**)
- Remove ``APNS_HOST``, ``APNS_PORT``, ``APNS_FEEDBACK_HOST``, and ``APNS_FEEDBACK_PORT`` config options. These are now determined by whether ``APNS_SANDBOX`` is ``True`` or not.
- Remove ``APNS_MAX_NOTIFICATION_SIZE`` as config option.
- Remove ``GCM_MAX_RECIPIENTS`` as config option.
- Rename ``APNS_ERROR_TIMEOUT`` config option to ``APNS_DEFAULT_ERROR_TIMEOUT``. (**breaking change**)


v0.1.1 (2015-04-14)
-------------------

- Pin ``pushjack`` dependency version to ``>=0.1.0, <0.3.0`` due to an breaking changes in ``pushjack``.


v0.1.0 (2015-03-26)
-------------------

- First release.
