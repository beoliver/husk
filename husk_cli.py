#!/usr/bin/env python3

import argparse
import inspect
import json
import os
import sqlite3
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

#####################################################################
# UTILS
#####################################################################


def user_confirmation(message, implicit_yes=False):
    if implicit_yes:
        return implicit_yes
    selection = input("{}\nProceed? [y/N]: ".format(message))
    return selection.lower() == "y"


#####################################################################
# CONFIG
#####################################################################


def husk_config_dir() -> Path:
    return Path.home() / ".config" / "husk"


def husk_config_file() -> Path:
    return husk_config_dir() / "config.json"


def write_json_config(config: Any, force=False):
    dot_config = Path.home() / ".config"
    if not dot_config.exists():
        if not force:
            raise Exception("{} does not exist".format(dot_config))
        dot_config.mkdir()
    husk_dir = dot_config / "husk"
    husk_dir.mkdir(exist_ok=force)
    with open(husk_dir / "config.json", "w+") as f:
        f.write(json.dumps(config))


def read_json_config():
    with open(husk_config_file(), "r+") as f:
        return json.loads(f.read())


def set_default_config_context(name):
    c = read_json_config()
    c["default_context"] = name
    write_json_config(c, force=True)


def unset_default_config_context():
    c = read_json_config()
    if c.get("default_context"):
        del c["default_context"]
    write_json_config(c, force=True)


#####################################################################
# PERSISTENCE
#####################################################################


HUSK_DATABASE_TABLES = {
    "contexts": [
        "context_id INTEGER PRIMARY KEY AUTOINCREMENT",
        "context_name TEXT NOT NULL UNIQUE",
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
        "context_path TEXT UNIQUE",
    ],
    "tags": [
        "tag_id INTEGER PRIMARY KEY AUTOINCREMENT",
        "tag_name TEXT NOT NULL UNIQUE",
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
    ],
    "context_tags": [
        "context_id INTEGER NOT NULL",
        "tag_id INTEGER NOT NULL",
        "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (context_id) REFERENCES contexts (context_id)",
        "FOREIGN KEY (tag_id) REFERENCES contexts (tag_id)",
        "UNIQUE(context_id, tag_id)",
    ],
}


def create_table_statement(name, fields):
    return "CREATE TABLE {} ({});".format(name, ",".join(fields))


def insert_context_statement(context_name, context_path=None):
    return (
        "INSERT INTO contexts (context_name, context_path) VALUES (?, ?)",
        (context_name, context_path),
    )


def insert_tag_statement(tag):
    return ("INSERT INTO tags (tag_name) VALUES (?)", (tag,))


def insert_context_tag_statement(context_id, tag_id):
    return (
        "INSERT INTO context_tags (context_id, tag_id) VALUES (?,?)",
        (context_id, tag_id),
    )


def insert_tags(db_context, context, tags):
    with db_context as db:
        cursor = db.connection.cursor()
        # make sure that the context exists
        cursor.execute(
            "SELECT context_id FROM contexts WHERE context_name = ?", (context,)
        )
        result = cursor.fetchone()
        # if no context then just return
        if not result:
            return
        (context_id,) = result
        # insert the tags into the tags table
        for tag in tags:
            # make sure that there are no user errors with duplicate tags.
            # collect the ids that were inserted
            try:
                cursor.execute(*insert_tag_statement(tag))
                tag_id = cursor.lastrowid
                cursor.execute(*insert_context_tag_statement(context_id, tag_id))
            except sqlite3.IntegrityError:
                pass
        db.connection.commit()


def write_empty_database(db_path, default_context="HUSK"):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    for (table_name, table_fields) in HUSK_DATABASE_TABLES.items():
        cursor.execute(create_table_statement(table_name, table_fields))
    connection.execute(*insert_context_statement(default_context))
    connection.commit()
    connection.close()


class DB_Context(object):
    def __init__(self, config):
        self.path = config.get("db")

    def __enter__(self):
        self.connection = sqlite3.connect(self.path)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.close()


#####################################################################
# CONTEXT
#####################################################################

HUSK_CONTEXT_FILENAME = ".husk_context"


def read_context(dir):
    path = Path(dir) / HUSK_CONTEXT_FILENAME
    with open(path, "r") as f:
        return json.loads(f.read())


def write_context(name, path):
    with open(path, "w+") as f:
        f.write(json.dumps({"context_name": name, "context_path": path}))


def parent_context_on_path(path):
    while True:
        (next_path, _) = os.path.split(path)
        with os.scandir(path) as dir:
            file = next(
                filter(
                    lambda entry: entry.is_file()
                    and entry.name == HUSK_CONTEXT_FILENAME,
                    dir,
                ),
                None,
            )
        if file:
            context = read_context(path)
            return context.get("context_name")
        else:
            if path == next_path:
                return None
            else:
                path = next_path


def infer_context(invocation_path, config=None):
    # a "global_context" **MAY** be set in the config
    global_context = config.get("default_context") if config else None
    if global_context:
        return global_context
    return parent_context_on_path(invocation_path)


def create_context(db_context, name, dir=None):
    with db_context as db:
        db.connection.execute(*insert_context_statement(name, dir))
        if dir:
            path = Path(dir) / HUSK_CONTEXT_FILENAME
            with open(path, "w+") as f:
                f.write(json.dumps({"context_name": name, "context_path": str(dir)}))
        db.connection.commit()


def valid_context_name(name):
    if name == "":
        return False
    return True


def ensure_valid_context_name(name):
    if not valid_context_name(name):
        raise Exception("'{}' is not a valid context name".format(name))
    return name


#####################################################################
# HANDLERS
#####################################################################


def valid_tag_name(name):
    if name == "":
        return False
    return True


def ensure_valid_tag_name(name):
    if not valid_tag_name(name):
        raise Exception("'{}' is not a valid tag name".format(name))
    return name


#####################################################################
# HANDLERS
#####################################################################


class Handler(ABC):
    @property
    @abstractmethod
    def about(self):
        pass

    @property
    @abstractmethod
    def interface(self):
        pass

    @abstractmethod
    def execute(self, args):
        pass


#####################################################################
# INIT HANDLER
#####################################################################


def default_install_dir() -> Path:
    return Path.home()


class InitHandler(Handler):
    about = {"description": "Initialize husk", "help": "Initialize husk"}
    interface = [
        {
            "args": ["-f", "--force"],
            "kwargs": {
                "action": "store_true",
                "help": "Use force. This will overwrite any existing databases and configurations",
            },
        },
        {
            "args": ["--path"],
            "kwargs": {
                "type": str,
                "metavar": "PATH",
                "help": "Dir to create top level '.husk' dir. Defaults to $HOME",
            },
        },
    ]

    def execute(self, force=False, path=None):
        install_dir = Path(path) if path else default_install_dir()
        husk_dir = install_dir / ".husk"
        husk_dir.mkdir(exist_ok=force)
        db_path = husk_dir / "husk.db"
        if db_path.exists() and not force:
            raise Exception("Database already exists")
        config = {"root": str(husk_dir), "db": str(db_path)}
        write_empty_database(db_path)
        write_json_config(config, force)


#####################################################################
# CONTEXT HANDLERS
#####################################################################


class ContextHandler(Handler):
    about = {"description": "Context stuff", "help": "Context stuff"}
    interface = []

    def execute(self, **kwargs):
        None


#####################################################################
## CONTEXT INIT HANDLER
#####################################################################


class ContextInitHandler(Handler):
    about = {"description": "Initialize a context", "help": "Initialize a context"}
    interface = [
        {
            "args": ["--virtual"],
            "kwargs": {
                "action": "store_true",
                "help": "Create a virtual context that is not tied to your filesystem.",
            },
        },
        {
            "args": ["--name"],
            "kwargs": {
                "type": str,
                "help": "Name of the context. By default the name of the current working diretory",
            },
        },
        {
            "args": ["--path"],
            "kwargs": {
                "type": str,
                "metavar": "PATH",
                "help": "Path to context root directory. By default the path to the current working directory. This flag is ignored when creating a virtual context.",
            },
        },
    ]

    def execute(self, virtual=False, name=None, path=None):
        context_type = "VIRTUAL" if virtual else "FILE"
        path = path if path else os.getcwd()
        name = name if name else os.path.basename(path)
        ensure_valid_context_name(name)
        actions = [
            "This will perform the following actions:",
            "1. Add '{}' to the husk database as a '{}' context.".format(
                name, context_type
            ),
        ]
        if not virtual:
            actions.append(
                "2. Create a '{}' file in the directory '{}'.".format(
                    HUSK_CONTEXT_FILENAME, path
                )
            )
        if user_confirmation("\n".join(actions)):
            config = read_json_config()
            create_context(DB_Context(config), name, path)


#####################################################################
## CONTEXT INFO HANDLER
#####################################################################


class ContextInfoHandler(Handler):
    about = {
        "description": "Show information about the current context",
        "help": "Show information about the current context",
    }
    interface = [
        {
            "args": ["-v", "--verbose"],
            "kwargs": {"action": "store_true", "help": "Verbose output",},
        },
    ]

    def execute(self, verbose=False):
        config = read_json_config()
        context = infer_context(os.getcwd(), config)
        if context:
            if verbose:
                print("verbose: {}".format(context))
            else:
                print(context)


#####################################################################
## CONTEXT LIST HANDLER
#####################################################################


class ContextListHandler(Handler):
    about = {"description": "Show all contexts", "help": "Show all contexts"}
    interface = [
        {"args": ["-G"], "kwargs": {"action": "store_true", "help": "All contexts",},},
        {"args": ["--name"], "kwargs": {"type": str, "help": "Name of the context",},},
    ]

    def execute(self, G=False, name=None):
        global_search = G
        config = read_json_config()
        context = name if name else infer_context(os.getcwd(), config)
        if context is None and not global_search:
            return

        with DB_Context(config) as husk:
            headers = [
                "context_name",
                "created_at",
                "context_path",
            ]
            base_query = "SELECT {} FROM contexts".format(",".join(headers))
            query = (
                base_query
                if global_search
                else "{} WHERE context_name = '{}'".format(base_query, context)
            )

            results = list(husk.connection.execute(query))

            # calc padding based on either 16 chars default or the longest
            # string in the column.

            padding = list(
                map(
                    lambda col: max(
                        12, 1 + max(map(lambda row_item: len(str(row_item)), col))
                    ),
                    zip(*results),
                )
            )

            print(
                "".join(
                    str(x).ljust(pad)
                    for (x, pad) in zip(["CONTEXT", "CREATED", "PATH",], padding)
                )
            )
            print(sum(padding) * "-")
            for row in results:
                print("".join(str(x).ljust(pad) for (x, pad) in zip(row, padding)))


#####################################################################
## CONTEXT SET HANDLER
#####################################################################


class ContextSetHandler(Handler):
    about = {
        "description": "Set a global VIRTUAL context to work in",
        "help": "Set a global VIRTUAL context to work in",
    }
    interface = [
        {
            "args": ["name"],
            "kwargs": {
                "type": str,
                "metavar": "NAME",
                "help": "Name of the VIRTUAL context",
            },
        },
    ]

    def execute(self, name=None):
        if name:
            config = read_json_config()
            with DB_Context(config) as db:
                cursor = db.connection.execute(
                    "SELECT * FROM contexts WHERE context_name = ? AND context_path IS NULL",
                    (name,),
                )
                if cursor.fetchone():
                    set_default_config_context(name)
                else:
                    print("No virtual context '{}' exists.".format(name))


#####################################################################
## CONTEXT UNSET HANDLER
#####################################################################


class ContextUnsetHandler(Handler):
    about = {
        "description": "Un-set any current global VIRTUAL context",
        "help": "Un-set any current global VIRTUAL context",
    }
    interface = []

    def execute(self):
        unset_default_config_context()


#####################################################################
# TAG HANDLERS
#####################################################################


class TagHandler(Handler):
    about = {"description": "Tag stuff", "help": "Tag stuff"}
    interface = []

    def execute(self, **kwargs):
        None


#####################################################################
# TAG ADD HANDLERS
#####################################################################


class TagAddHandler(Handler):
    about = {"description": "Add a Tag", "help": "Add a Tag"}
    interface = [
        {
            "args": ["tags"],
            "kwargs": {
                "type": str,
                "metavar": "TAGS",
                "help": "Comma separated list of tags",
            },
        },
        {
            "args": ["-G"],
            "kwargs": {
                "action": "store_true",
                "help": "Create a global tag 'add --context HUSK'",
            },
        },
        {
            "args": ["--context"],
            "kwargs": {
                "type": str,
                "metavar": "NAME",
                "help": "Explicit context to create the tag in",
            },
        },
    ]

    def execute(self, tags="", G=False, context=None):
        config = read_json_config()
        context = context if context else infer_context(os.getcwd(), config)
        tags = [ensure_valid_tag_name(tag.strip()) for tag in tags.split(",")]
        insert_tags(DB_Context(config), context, tags)


#####################################################################
# TAG LIST HANDLER
#####################################################################


class TagListHandler(Handler):
    about = {"description": "List Tags", "help": "List Tags"}
    interface = [
        {"args": ["-G"], "kwargs": {"action": "store_true", "help": "All contexts",},},
        {
            "args": ["--context"],
            "kwargs": {"type": str, "help": "Name of the context",},
        },
    ]

    def execute(self, G=False, context=None):
        global_search = G
        config = read_json_config()
        context = context if context else infer_context(os.getcwd(), config)
        if context is None and not global_search:
            return

        with DB_Context(config) as husk:
            headers = ["tag_name", "context_name", "context_tags.created_at"]
            base_query = "SELECT {} FROM context_tags INNER JOIN tags ON context_tags.tag_id = tags.tag_id INNER JOIN contexts".format(
                ",".join(headers)
            )
            query = (
                base_query
                if global_search
                else "{} WHERE context_name = '{}'".format(base_query, context)
            )

            results = list(husk.connection.execute(query))
            # calc padding based on either 16 chars default or the longest
            # string in the column.

            padding = list(
                map(
                    lambda col: max(
                        12, 1 + max(map(lambda row_item: len(str(row_item)), col))
                    ),
                    zip(*results),
                )
            )

            print(
                "".join(
                    str(x).ljust(pad)
                    for (x, pad) in zip(["TAG", "CONTEXT", "CREATED",], padding)
                )
            )
            print(sum(padding) * "-")
            for row in results:
                print("".join(str(x).ljust(pad) for (x, pad) in zip(row, padding)))


#####################################################################
# ARG PARSER
#####################################################################


def wrapped_handler(handler):
    # see https://stackoverflow.com/questions/26515595/how-does-one-ignore-unexpected-keyword-arguments-passed-to-a-function
    # For insiration on how to expose they correct kwargs
    # 1. Find the kwargs for the execute method of the handler
    sig = inspect.signature(handler.execute)
    filter_keys = [
        param.name
        for param in sig.parameters.values()
        if param.kind == param.POSITIONAL_OR_KEYWORD
    ]
    # returned handler function
    def handle(namespace):
        # convert the argparse namespace into a dict
        args = vars(namespace)
        # remove any args that should not be passed to `handler.execute`
        filtered_args = {filter_key: args[filter_key] for filter_key in filter_keys}
        handler.execute(**filtered_args)

    return handle


def build_arg_parser_rec(routes, subparsers):
    for command, v in routes.items():
        handler = v.get("handler")()
        command_parser = subparsers.add_parser(command, **handler.about)
        for argument in handler.interface:
            args = tuple(argument.get("args", []))
            kwargs = argument.get("kwargs", {})
            command_parser.add_argument(*args, **kwargs)
        command_parser.set_defaults(func=wrapped_handler(handler))
        sub_routes = v.get("routes")
        if sub_routes:
            build_arg_parser_rec(sub_routes, command_parser.add_subparsers())


def build_arg_parser(routes):
    parser = argparse.ArgumentParser(
        prog="husk", description="Remember things in context."
    )
    build_arg_parser_rec(routes, parser.add_subparsers())
    return parser


#####################################################################
# ARG PARSER ROUTES
#####################################################################

ROUTES = {
    "init": {"handler": InitHandler},
    "context": {
        "handler": ContextHandler,
        "routes": {
            "init": {"handler": ContextInitHandler},
            "info": {"handler": ContextInfoHandler},
            "list": {"handler": ContextListHandler},
            "set": {"handler": ContextSetHandler},
            "unset": {"handler": ContextUnsetHandler},
        },
    },
    "tag": {
        "handler": TagHandler,
        "routes": {
            "add": {"handler": TagAddHandler},
            "list": {"handler": TagListHandler},
        },
    },
}

#####################################################################
# ARG PARSER
#####################################################################

parser = build_arg_parser(ROUTES)

#####################################################################
# ENTRY POINT
#####################################################################


def run():
    args = parser.parse_args()
    args.func(args)
