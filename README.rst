===============
rucola-mustache
===============

A Rucola plugin used to render Mustache templates.

Installation
------------

Install with a ``pip`` command:

::

    $ pip install rucola-mustache

Dependencies
~~~~~~~~~~~~

Plugin requires ``pystache`` package.

Usage
-----

A plugin used without arguments will render all ``html`` files using their metadata.

For example, we have a file ``dog.html``:

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
~~~~~~~

pattern:
    Mustache renders all files that matches a pattern. Default is ``**/*.html``

metadata (default: ``None``):
    File will be rendered using it metadata and a metadata from this parameter.
    For example:

    ``page.html``

    .. code-block:: html

        {{ author }}

    Code:

    .. code-block:: python

        app.use(
            Mustache(metadata={'author': 'Me'})
        )

    Result ``build/page.html``::

        Me

partials (default: ``None``):
    Partials directory relative to app path or dict like object.

    Project directory structure::

        - partials/
            - header.html
            - footer.mustache
        - src/
            - page.html

    Script:

    .. code-block:: python

        app.use(
            Mustache(partials='partials')
        )

    No you can use ``{{> header }}`` or ``{{> footer }}`` tags in ``page.html``.



    Also you can used ``dict`` like object like this:

    .. code-block:: python

        app.use(
            Mustache(partials={'header': '<h1>Welcome</h1>',
                               'footer': 'Author: Me'})
        )


License
-------

MIT