PaintLog
========

Colored log formatter for Python.

How to Use:
-----------

Source code:

    import logging
    import paintlog      

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)#

    # Create Colored Formatter like normal formatter
    formatter = paintlog.ColoredFormatter(
                   '%(asctime)s [%(levelname)-8s] %(message)s',
                   datefmt='%Y-%m-%dT%H:%M:%S'.
                   INFO={'levelname': (paintlog.Fore.CYAN, paintlog.Style.RESET_ALL)}
                )

    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Info Message")

Output:

<div style='background-color:black;color:white;font-family:Courier New;'>
2018-12-04T12:02:45 [<span style='color:cyan;'>INFO</span>] Info Message<br/>
</div>