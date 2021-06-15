========
Dotstrap
========


.. contents::

.. image:: //img.shields.io/pypi/v/dotstrap.svg
    :target: https://pypi.org/project/dotstrap/

.. image:: //img.shields.io/pypi/pyversions/dotstrap.svg
    :target: https://pypi.org/project/dotstrap/

About
-----

Dotstrap is a simiple Python based command line tool that acts as a git wrapper for simplifying dotfile management via bare git repository.

Dotstrap is directly inspired by Nicola Paolucci (Twitte: @durdn) and Fabien Dubosson (GitHub: StreakyCobra).

It was created as an alternative to using shell aliases with the goal of simplifying bootstrapping a clean machine down to just two commands (or three if git isn't pre-instaled).

Dotstrap simplifies the most common git operations (such as adding, commiting and then pushing a dotfile) when using a git bare repository approach to dotfile handling.

To understand how and why it works, read Nicola Paolucci's tutorial:
`https://www.atlassian.com/git/tutorials/dotfiles <https://www.atlassian.com/git/tutorials/dotfiles>`_

---

Install on first system
-----------------------

Just install via pip:

.. code:: shell

    $ pip install dotstrap


Next create an empty repo on e.g. github for your dotfiles.

Initialize dotstrap repository with your own repo URL:

.. code:: shell

    $ dotstrap init https://github.com/nitwit-se/dotfiles.git
    # TODO: output

Then start adding files to your repo. Dotstrap will automatically commit and sync upstream:

.. code:: shell

    $ dotstrap add ~/.emacs
    # TODO: output

Dotstrap second system
----------------------

Again, install via pip:

.. code:: shell

    $ pip install dotstrap


Then clone with your own repop URL:

.. code:: shell

    $ dotstrap clone https://github.com/nitwit-se/dotfiles.git
    # TODO: output

Done! (Well, best-case scenario).
