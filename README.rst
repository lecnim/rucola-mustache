===============
rucola-mustache
===============

.. image:: https://travis-ci.org/lecnim/rucola-mustache.svg
    :target: https://travis-ci.org/lecnim/rucola-mustache

A Rucola plugin used to render Mustache templates.

Installation
------------

You can install using ``pip``: ::

    $ pip install rucola-mustache

Dependencies
~~~~~~~~~~~~

The plugin requires a `pystache <https://pypi.python.org/pypi/pystache/>`_
package. If you use ``pip``, it will automatically install it for you.

Usage
-----

A plugin contains three useful items: `Mustache`_, `MustacheLayouts`_
and `render_mustache()`_. Also look at `Using with other plugins`_

``Mustache``
~~~~~~~~~~~~

If you use ``Mustache`` class without arguments it will render
a content of each ``html`` file using it metadata
as a template context.

For example, we have a file ``src/dog.html``:

.. code-block:: html

    <p>{{ title }}</p>

And the python script:

.. code-block:: python

    from rucola_mustache import Mustache

    app = Rucola('.')

    file = app.get('dog.html')
    file['title'] = 'Wow'

    app.use(
        Mustache()   # same as: Mustache('**/*.html')
    )
    app.build()

Result of ``build/dog.html``:

.. code-block:: html

    <p>Wow</p>


Options
#######

pattern:
    Mustache renders all files that matches a pattern. Default is ``**/*.html``

metadata (default: ``None``):
    A file is rendered using it metadata and a metadata from this parameter.
    For example:

    .. code-block:: python

        app.create('about.html', content='{{ author }}')
        app.use(
            Mustache(metadata={'author': 'Me'})
        )

    Result of ``build/about.html``: ::

        Me

partials (default: ``None``):
    A partials directory relative to the rucola working directory
    or a dict like object.

    An example project directory::

        partials/
            header.html
            footer.mustache
        src/
            page.html
        script.py

    Content of ``script.py``:

    .. code-block:: python

        app.use(
            Mustache(partials='partials')
        )

    No you can use ``{{> header }}`` or ``{{> footer }}`` tags in ``page.html``.

    Also you can use a ``dict`` like object like this:

    .. code-block:: python

        app.use(
            Mustache(partials={'header': '<h1>Welcome</h1>',
                               'footer': 'Author: Me'})
        )



``MustacheLayouts``
~~~~~~~~~~~~~~~~~~~

If you use ``MustacheLayouts`` class without arguments it will render
each ``html`` file. As a template it will use ``layout`` key from metadata,
value of this key should points to a layout file in the ``./layouts`` directory.

Our example project directory: ::

    layouts/
        main.html
    src/
        fruit.html
    script.py

An example layout file ``layouts/main.html``:

.. code-block:: html

    <h1>{{ title }}</h1>
    <p>{{ content }}</p>

And the python ``script.py``:

.. code-block:: python

    from rucola_mustache import MustacheLayouts

    app = Rucola('.')

    file = app.get('fruit.html')
    file['title'] = 'Banana'
    file['content'] = 'Yellow fruit!'
    file['layout'] = 'main.html'

    app.use(
        MustacheLayouts()
    )
    app.build()

Result of ``build/fruit.html``:

.. code-block:: html

    <h1>Banana</h1>
    <p>Yellow fruit!</p>


Options
#######

pattern:
    Apply layouts to all files that matches a pattern. Default is ``**/*.html``

source (default: ``layouts``)
    A layouts directory, relative to the rucola working directory.

partials (default: ``None``)
    A partials directory relative to the rucola working directory. Works the same
    as ``partials`` in the ``Mustache`` class.

default (default: ``None``)
    A default layout filename. Plugin use it if ``File`` instance has no
    ``layout`` key in metadata.

metadata_key (default: 'layout')
    A metadata key where the plugin looks for a layout filename.


``render_mustache()``
~~~~~~~~~~~~~~~~~~~~~

You can use the ``render_mustache()`` function to render the given template string.

.. code-block:: pycon

    >>> from rucola_mustache import render_mustache
    >>> render_mustache('{{ foo }}', context={'foo': 'Hello!'})
    Hello!

It also accepts ``File`` instances:

.. code-block:: pycon

    >>> from rucola import File
    >>> f = File('/hello', content='Hi {{ foo }}')
    >>> render_mustache(f, context={'foo': 'Banana!'})
    Hi Banana!


Using with other plugins
~~~~~~~~~~~~~~~~~~~~~~~~

It is good to use ``Mustache`` and ``MustacheLayouts`` with other plugins, for
example like `YamlContext <https://github.com/lecnim/rucola-yamlfm/>`_.
Let's see:

Content of file ``src/fruit.html``:

.. code-block:: html

    """
    title: Banana
    """

    Hello this page is about: {{ title }}

And the python ``script.py``:

.. code-block:: python

    from rucola_yamlfm import YamlFrontmatter
    from rucola_mustache import Mustache

    app = Rucola('.')
    app.use(
        YamlFrontmatter(),
        Mustache()
    )
    app.build()

Result of ``build/fruit.html``:

.. code-block:: html

    Hello this page is about: Banana


License
-------

MIT