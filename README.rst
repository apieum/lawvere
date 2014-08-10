********
Lawvere
********

.. image:: https://pypip.in/v/lawvere/badge.png
        :target: https://pypi.python.org/pypi/lawvere

Functionnal Tools.

---------------------------------------------------------------------

**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


=============
Installation
=============

Install it from pypi::

  pip install lawvere

or from sources::

  git clone git@github.com:apieum/lawvere.git
  cd lawvere
  python setup.py install

=====
Usage
=====


===========
Development
===========

Your feedback, code review, improvements or bugs, and help to document is appreciated.
You can contact me by mail: apieum [at] gmail [dot] com

Test recommended requirements::

  pip install -r dev-requirements.txt

Sometimes --spec-color doesn't function. Uninstall nosespec and nosecolor then reinstall nosecolor and nosespec separatly in this order (nosecolor first).

Launch tests::

  git clone git@github.com:apieum/lawvere.git
  cd lawvere
  nosetests --with-spec --spec-color ./lawvere
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./lawvere



.. image:: https://secure.travis-ci.org/apieum/lawvere.png?branch=master
   :target: https://travis-ci.org/apieum/lawvere
