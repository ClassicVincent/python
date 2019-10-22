# -*- coding=gbk -*-
# file:manage.py.py
# time:2019/9/14{10:05}
# author:Vincent
# note:

from application import app, manager
from flask_script import Server
import www

manager.add_command("runserver",
                    Server(host=app.config['SERVER_HOST'],
                           port=app.config['SERVER_PORT'],
                           use_debugger=app.config['USE_DEBUGGER'],
                           use_reloader=app.config['USE_RELOADER']))

def main():
    manager.run()

if __name__ == "__main__":
    try:
        import sys

        sys.exit(main())
    except Exception as e:
        import traceback

        traceback.print_exc()
