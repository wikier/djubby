# -*- coding: utf-8 -*-

# python logging trick for django, based on http://stackoverflow.com/questions/342434/python-logging-in-django

import sys
import logging

logInitDone = False
if not logInitDone:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s", stream=sys.stdout)
    logInitDone = True

