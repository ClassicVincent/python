#!/usr/bin/python

import os
import sys

print(sys.path)
print(os.getenv("PYTHONPATH"))
for path in os.getenv("PYTHONPATH").split(";"):
    sys.path.append(path)

print(sys.path)

from config import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD, DB_NAME

print(DB_HOST)
a=['5.1.17']
print(a[0])
