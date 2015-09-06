===============
rucola-mustache
===============

A Rucola plugin used to load YAML front matters from files.

Installation
------------

Install with a ``pip`` command:

::

    $ pip install rucola-mustache

Dependencies
~~~~~~~~~~~~

Plugin requires ``pyyaml`` package.

Usage
-----

We have an example file ``post.md`` with a frontmatter::

    ---
    title: Hello badger
    ---
    Lorem ipsum dolor sit amet

Next we load a yaml frontmatter from all ``.md`` files:

.. code-block:: python

    from rucola_yamlfm import YamlFrontmatter

    app = Rucola('.')
    app.use(
        YamlFrontmatter()   # same as: YamlFrontmatter('**/*.md')
    )

    # Frontmatter variables are available in the file:

    file = app.get('post.md')
    file['title']   # Hello badger
    file['content'] # Lorem ipsum dolor sit amet


Load a frontmatter from all files that matches a pattern:

.. code-block:: python

    app.use(
        YamlFrontmatter('path/to/file')     # only 'path/to/file'
        YamlFrontmatter('path/to/dir/*.md') # all .md files in 'path/to/dir'
    )


Options
~~~~~~~

pattern:
    Try to load frontmatter from all files that matches a pattern. Default is ``**/*.md``

limiter:
    Frontmatter limiter. Default is ``---``


License
-------

MIT