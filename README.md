# husk

#### English

The outer covering of a grain or a seed.

- Synonyms: rind, shell, hull, covering

#### Norwegian

Imperative form of the the verb _huske_ - to remember or recollect

1.  [init](#init)
    1. [husk](#init_husk)
    2. [context](#init_context)
2.  [show](#show)
    1. [contexts](#show_contexts)
    2. [tags](#show_tags)
3.  [add](#add)
    1. [tag](#add_tag)
    1. [url](#add_url)

# `init` <a name="init"></a>

## `init husk` <a name="init_husk"></a>

```sh
husk init husk <path>
```

Create a new `husk.db`

## `init context` <a name="init_context"></a>

1. Create a `.husk_context` file in the indicated directory.
2. Adds context information to the `husk.db`

A context is a namespace.

By default the basepath of the current working directory is used as the `<name>` and the current working directory is used as the `<path>`.

```sh
husk init context [--name NAME] [--path PATH]
```

### Examples <a name="init_context_examples"></a>

The following examples assume that your current working directory is `/Users/yourname/Documents/foo`.

```
$ husk init context
This will perform the following action:
Initialize context 'foo' in directory '/Users/yourname/Documents/foo'
Proceed? [y/N]
```

```
$ husk init context --name bar
This will perform the following action:
Initialize context 'bar' in directory '/Users/yourname/Documents/foo'
Proceed? [y/N]
```

```
$ husk init context --path ~/Documents
This will perform the following action:
Initialize context 'foo' in directory '/Users/yourname/Documents'
Proceed? [y/N]
```

```
$ husk init context --name bar --path ~/Documents
This will perform the following action:
Initialize context 'bar' in directory '/Users/yourname/Documents'
Proceed? [y/N]
```

# `show` <a name="show"></a>

## `show contexts` <a name="show_contexts"></a>

Provides an overview of the different contexts that you have created.

```
husk show contexts [-p] [-c] [-A] [--in CONTEXT]
```

When called with no arguments the current working context is used as the default argument to `--in`.

| Flag   | Action                                                                           |
| ------ | -------------------------------------------------------------------------------- |
| `-A`   | Show **A**LL contexts. Equivalent to `husk show contexts -c --in <root-context>` |
| `-p`   | Include all **p**arent contexts                                                  |
| `-c`   | Include all **c**hild contexts                                                   |
| `--in` | Use a specified context                                                          |

### Examples <a name="init_context_examples"></a>

The following examples assume that your current working directory is `/Users/yourname/Documents/foo`.

```
$ husk show contexts
Context     Parent   Path
*foo        yourname /Users/yourname/Documents/foo
```

```
$ husk show contexts -p
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
```

```
$ husk show contexts -c
Context     Parent   Path
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
```

```
$ husk show contexts -pc
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
```

```
$ husk show contexts -A
Context     Parent   Path
yourname    -        /Users/yourname/
*foo        yourname /Users/yourname/Documents/foo
foo-tasks   foo      /Users/yourname/Documents/foo/tasks
bar         yourname /Users/yourname/Documents/bar
bar-ideas   bar      /Users/yourname/Documents/bar/ideas
```

```
$ husk show contexts -c --in bar
Context     Parent   Path
bar         yourname /Users/yourname/Documents/bar
bar-ideas   bar      /Users/yourname/Documents/bar/ideas
```

## `show tags` <a name="show_tags"></a>

```
husk show tags  [-p] [-c] [-A] [--in CONTEXT]
```

| Flag   | Action                                                                   |
| ------ | ------------------------------------------------------------------------ |
| `-A`   | Show **A**LL tags. Equivalent to `husk show tags -c --in <root-context>` |
| `-p`   | Include all tags defined within **p**arent contexts                      |
| `-c`   | Include all tags defined within **c**hild contexts                       |
| `--in` | Use a specified context                                                  |

# `add` <a name="add"></a>

## `add tag` <a name="add_tag"></a>

```
husk add tag NAME [-G] [--in CONTEXT]
```

| Flag   | Action                                                                        |
| ------ | ----------------------------------------------------------------------------- |
| `-G`   | Create a **G**lobal tag. Equivalent to `husk add tag TAG --in <root-context>` |
| `--in` | Create the tag in a specified context                                         |

## `add url` <a name="add_url"></a>

```
husk add url URL [-G] [--in CONTEXT] [--tags TAGS] [--note TEXT]
```

| Flag     | Action                                                                                         |
| -------- | ---------------------------------------------------------------------------------------------- |
| `-G`     | Create a **G**lobal bookmark for the URL. Equivalent to `husk add url URL --in <root-context>` |
| `--in`   | Create the URL bookmark in a specified context                                                 |
| `--tags` | Comma separated list of tags                                                                   |
| `--note` | An Optional description                                                                        |
