:orphan:
.. versionadded : 0.4.5:
.. _logging_setup:


Logging for debugging and advanced stuff
########################################

Logging is a very useful feature for debugging. It is also a way to "log" your bot actions.
Logging is highly recommended by EpikCord since it helps to debug and simplify things

Here is a simple example to implement logging:

.. code-block:: python

    import logging
    logger = logging.getLogger('EpikCord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='./logs.log', encoding='utf-8', mode='w')   
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

The first line ``import logging`` is obvious. It imports the module ``logging``

The second line sets the logger to "subscribe" to ``log`` events (i.e. How you get notifications from a YT channel you subscribed)

The third line sets the logger to only report warnings higher or similar than DEBUG

The fourth line sets an log handler which reports the logs to a specific filename

The fifth line sets the formatter:
*. The Formatter sets the format of the logs that get written to the log file.
*. The format given above is the most recommended format

The 6th line sets the handler

There is an extremely simple but not pythonic way to log items