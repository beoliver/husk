# husk

#### English

The outer covering of a grain or a seed.

- Synonyms: rind, shell, hull, covering

#### Norwegian

Imperative form of the the verb _huske_ - to remember or recollect

1.  [Initializing](#init)
2.  [Contexts](#context)
    1.  [init](#context_init)
    2.  [info](#context_info)
    3.  [list](#context_show)
    4.  [set](#context_set)
    5.  [unset](#context_unset)
3.  [Tags](#tag)

    1. [add](#add_tag)
    2. [list](#show_tags)
    3. [clean](#clean_tags)

4.  [Bookmarks](#bookmarks)

    1. [add](#add_bookmark)
    1. [list](#find_bookmark)

5.  [Notes](#notes)
    1. [add](#add_bookmark)
    1. [list](#find_bookmark)

# Initializing <a name="init"></a>

```sh
husk init <path> [--with-context NAME]
```

| Flag             | Action                                 |
| ---------------- | -------------------------------------- |
| `--with-context` | Provide a custom **root context** name |

Create a new `~/.husk.db` and a `.husk` file in your home folder `~/`. If a custom `context` name is not passed then the default `<username>` is used.

Note that both `HUSK` is a reserved context name. You can use it as an argument to `--name` to specify the top level user filesystem context that is created when running then `init` command.

# Contexts <a name="context"></a>

Contexts are a fundamental abstraction used by `husk`.

A context (abbreviated to `ctx`) is a namespace that lets you take notes, store bookmarks, add tags etc using `husk <op> add`. From any context you can find the context (and related notes, bookmarks, tags etc that belong to it) for the parent (recursive) and its children.
Contexts are a lot like implicit `tags` - in the sense that whatever you save **MUST HAVE** an associated context.

## Motivation

If you use your machine for both work and play you might find that you have two directories `~/Documents/work` and `~/Documents/play`. If you are in the subdirectory `~/Documents/work/foo/src`, then you are in the **file system context** of `work`. However, if you are in `~/Documents`, then depending on how you look at it - either you are in the context of **both** `work` and `play` or you are in **neither**.
It is also entirely reasonable for you to be thinking about `play` while in the `~/Documents/work` directory. In this case your **mental context** is `play` while your "physical" (filesystem) context is `work`.

## File system and Virtual Contexts

### File system Contexts

`husk` lets you create a **file system context** in any directory.

The file system contexts have the following properties (TODO: decide on handling of symlinks).

1. A **file system context** can have 0 or 1 "parent" **file system contexts**.
2. A **file system context** can have 0 or many "ancestor" **file system contexts**.
3. A **file system context** can have 0 or many "child" **file system contexts**.
4. A **file system context** can have 0 or many "decendant" **file system contexts**.

Given a file path `.../a/.../b/.../c/...`

Assume a context `c_a` was initialized in directory `a` and a context `c_b` was initialized in directory `b` and `c_c` was initialized in directory `c`.

1. The contents of contexts `c_a` and `c_b` are "accessable" to context `c_c` when using the `--ancestors` (`-a`) flag.
2. The contents of contexts `c_b` and `c_c` are "accessable" to context `c_a` when using the `--descendants` (`-d`) flag.

### Virtual Contexts

Virtual contexts are not tied to the file system. This means that a virtual context can have multiple parents.
When creating a virtual context - it has `HUSK` as the parent

```
V1 -> HUSK
```

## `ctx init` <a name="context_init"></a>

The `ctx init` command is used to initiate a new context.

```sh
husk ctx init [--virtual] [--name NAME] [--path PATH]
```

| Flag        | Action                                                        |
| ----------- | ------------------------------------------------------------- |
| `--virtual` | Create a virtual context that is not tied to your filesystem. |
| `--name`    | Name of the context.                                          |
| `--path`    | Path to context root directory                                |

By default a **context** is mapped to your current working directory. For example if we were in `~/Documents/work` and run the following:

```
$ husk ctx init
```

Then two operations would be performed.

1. A `.husk` file is created in the current directory.
2. The context name and path information are added to the `husk.db`.

If we wanted to create a **virtual** context then we would use the following:

```
$ husk ctx init --virtual --name lol
```

In this case the following operation would be performed.

1. The context name is added to the `husk.db`.

## `ctx info` <a name="context_info"></a>

The `ctx info` command is provides information about the current context.

```sh
husk ctx info [-v] [-t] [--name CONTEXT]
```

| Flag     | Action                                    |
| -------- | ----------------------------------------- |
| `-v`     | Verbose                                   |
| `-t`     | Shorthand for `husk ctx info --name HUSK` |
| `--name` | Name of the context.                      |

If no `--name` is provided then `husk` will attempt to calculate your current **context**.

```
$ husk ctx info
```

If you want to find information about a virtual context that has not been [set](#context_set), then you must use the `--name` flag.

```
$ husk ctx info --name lol
```

## `ctx set` <a name="context_set"></a>

```
husk ctx set VIRUAL_CONTEXT
```

Set virual context for the entire filesystem. This means that `VIRUAL_CONTEXT` will used whenever a context is not **explicily** set using a command line flag.

## `ctx unset` <a name="context_unset"></a>

```
husk ctx unset
```

Unsets the virual context for the entire filesystem if active.

## `ctx list` <a name="context_show"></a>

Provides an overview of the different contexts that you have created.

```
husk ctx list [-G] [-a] [-d] [--name CONTEXT]
```

When called with no arguments the current working context or the current [set virtual context](#context_set) is used as the default argument to `--name`.

| Flag     | Action                                                        |
| -------- | ------------------------------------------------------------- |
| `-G`     | List all contexts. Equivalent to `husk ctx list -d --in HUSK` |
| `-a`     | Include all **a**nscestor contexts                            |
| `-d`     | Include all **d**escendant contexts                           |
| `--name` | Use a specified context                                       |

# Tags

## `tag add` <a name="add_tag"></a>

```
husk tag add TAGS [-G] [--name CONTEXT]
```

Where `TAGS` is a comma separated list of tags

| Flag     | Action                                                                |
| -------- | --------------------------------------------------------------------- |
| `-G`     | Create a **G**lobal tag. Equivalent to `husk tag add TAG --name HUSK` |
| `--name` | Create the tag in a specified context                                 |

### Examples

Add a single tag `foo` to the current context.

```
$ husk tag add foo
```

Add the tags `foo`, `bar` and `baz` to the global context.

```
$ husk tag add -G foo,bar,baz
```

## `tag list` <a name="show_tags"></a>

```
husk tag list [-G] [-a] [-d] [--name CONTEXT] [--pattern REGEX]
```

| Flag        | Action                                                      |
| ----------- | ----------------------------------------------------------- |
| `-G`        | List all tags. Equivalent to `husk tag list -d --name HUSK` |
| `-a`        | Include all tags defined within **a**nscestor contexts      |
| `-d`        | Include all tags defined within **d**escendant contexts     |
| `--name`    | Use a specified context                                     |
| `--pattern` | A regex pattern to marth against the tag                    |

Notice that the same tag may appear in different contexts.

## `tag clean` <a name="clean_tags"></a>

Removes any tags that are not used

```
husk tag clean [-G] [-a] [-d] [--name CONTEXT] [--dry-run]
```

| Flag        | Action                                                                  |
| ----------- | ----------------------------------------------------------------------- |
| `-G`        | Clean all tags. Equivalent to `husk tag clean -c --name <root-context>` |
| `-a`        | Include all tags defined within **a**nscestor contexts                  |
| `-d`        | Include all tags defined within **d**escendant contexts                 |
| `--name`    | Use a specified context                                                 |
| `--dry-run` | Show which tags would be deleted                                        |

# Bookmarks <a name="bookmarks"></a>

Bookmarks are references to "external" documents.

## `bm add` <a name="add_bookmark"></a>

```
husk bm add PATH [-G] [--name CONTEXT] [--tags TAGS] [--meta TEXT]
```

Where `PATH` is either a `URL` or a local file on disk.

| Flag     | Action                                                                                 |
| -------- | -------------------------------------------------------------------------------------- |
| `-G`     | Create a **G**lobal bookmark for the URL. Equivalent to `husk bm add PATH --name HUSK` |
| `--name` | Create the URL bookmark in a specified context                                         |
| `--tag`  | Comma separated list of tags                                                           |
| `--meta` | An Optional description                                                                |

When creating a bookmark, any tags supplied will be created within the desired context. This means that you can use the same value for a `tag` in multiple contexts.

## `bm list` <a name="show_bookmark"></a>

```
husk bm list [-G] [-a] [-d] [--name CONTEXT] [--tags TAGS] [--pattern REGEX]
```

| Flag        | Action                                                              |
| ----------- | ------------------------------------------------------------------- |
| `-G`        | List all all bookmarks. Equivalent to `husk bm list -d --name HUSK` |
| `-a`        | Include all bookmarks defined within **a**nscestor contexts         |
| `-d`        | Include all bookmarks defined within **d**escendant contexts        |
| `--name`    | Create the URL bookmark in a specified context                      |
| `--tag`     | Comma separated list of tags fo filter by                           |
| `--pattern` | A regex pattern to marth against the link                           |

# Notes <a name="notes"></a>

Notes are blocks of text that you want to store

## `note add` <a name="add_note"></a>

```
husk note add [-G] [--name CONTEXT] [--tags TAGS]
```

Opens your default editor for the note
