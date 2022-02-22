Logging for debuging and advanced stuff
=======================================

Logging is a very useful feature for debugging. It is also a way to "log" your bot actions.

Here is a simple example to implement logging:

.. code-block:: python

    import logging
    logger = logging.getLogger('EpikCord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='.\\epik.log', encoding='utf-8', mode='w')   
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)