import os
from tinydb import TinyDB
from cement.utils import fs
from .controllers.items import Items

def extend_tinydb(app):
    app.log.info('extending todo application with tinydb')
    db_file = app.config.get('todo', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.info('tinydb database file is: %s' % db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))


from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import TodoError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('todo')
CONFIG['todo']['db_file'] = '~/.todo/db.json'
CONFIG['todo']['foo'] = 'bar'
CONFIG['todo']['email'] = 'avinash.kumar@ladybirdweb.com'


class Todo(App):
    """My TODO Application primary application."""

    class Meta:
        label = 'todo'

        # configuration defaults
        config_defaults = CONFIG

        hooks = [
            ('post_setup', extend_tinydb),
        ]

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base,
            Items
        ]


class TodoTest(TestApp, Todo):
    """A sub-class of Todo that is better suited for testing."""

    class Meta:
        label = 'todo'


def main():
    with Todo() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except TodoError as e:
            print('TodoError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
