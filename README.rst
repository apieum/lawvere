********
Lawvere
********

.. image:: https://pypip.in/v/lawvere/badge.png
        :target: https://pypi.python.org/pypi/lawvere

---------------------------------------------------------------------

**What ?**

Functionnal Tool: (de)composition with type checking, multiple dispatch.

**Why ?**

There is a lot of functionnal tools in python: toolz, funcy, fn.py, Pymonads...

They are great but none of them do type checking which, in my opinion, is a big loss from functionnal paradigm view.

**How ?**

With a complex and unmaintenable api: a single decorator called *"arrow"*.

For a *technical* explanation of arrows you can look at: `Understanding arrows <http://en.wikibooks.org/wiki/Haskell/Understanding_arrows>`_

For a *theorical* explanation: *"Conceptual Mathematics: A First Introduction to Categories"* [F. William Lawvere, Stephen H. Schanuel] is good start.


**Prerequisites**

I strongly recommand to have at least notions about:
  * lambda calculi (Currying)
  * tuples in algebra notations (e.g. `signatures <http://en.wikipedia.org/wiki/Signature_%28logic%29>`_)
  * basics of graph theory (related to category theory - morphisms, domain, codomain...)


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

------------
Quick start:
------------
  for impatients

**arrow** take only two optionnal arguments:
  * the *domain* or *source*: it's a tuple of types (or just a type in case of 1-tuple)
  * the codomain or *target*: (a single type)

It returns a function decorator.

Syntax is compatible for python 2.7 to 3.x..
In case you target 3.x versions only you can use annotations instead of "*arrow*" arguments.
"*arrow*" arguments override annotations.


**Code compatible with 2.x and 3.x python versions.**

  .. code-block:: python

    from lawvere import arrow

    # obviously you don't need to use named parameters
    # it's just to illustrate their meaning.
    @arrow(domain=(int, int), codomain=int)
    def add(x, y):
      return x + y

    # currying:
    add2 = add(2)

    assert add2(3) == 5
    assert add(1)(2) == 3 # successive calls

    # composition (pipe):
    # pass the result of first function to second
    add4 = add2 >> add2
    assert add4(1) == 5
    # composition (circle):
    # pass result of add(1) into add4
    add5 = add4 << add(1)
    assert add5(5) == 10

    # composed functions are tuples:
    assert isinstance(add4, tuple)
    assert add5[1] == add4

    # equality is checked over signatures:
    assert add(1) == add(1)
    assert add5 == add(1) >> add2 >> add2

    # operator precedence:
    assert add5 == add(1) >> (add2 << add2)
    assert add5 == add2 >> add2 << add(1)

    # Type Checking:
    type_checked = False
    try:
      add('a', 'b') == 'ab'
    except TypeError:
      type_checked = True

    assert type_checked, 'add should not exists for str types'


    # dispatch register
    # concat inherit arrow properties
    @add.register((str, str), str)
    def concat(x, y):
      return "%s %s" %(x, y)

    # can still call/curry... concat
    assert concat('a')('b') == 'a b'
    # add with str call concat
    assert add('a') == concat('a')

    # Concat is only defined for str
    type_checked = False
    try:
      assert concat(1, 2) == 3
    except TypeError:
      type_checked = True

    assert type_checked, 'concat should not exists for int types'

    # Type Checking when composing:
    try:
      add >> concat(y='b')
    except TypeError as exc:
      message = str(exc)
    # hope message is clear :)
    assert message == "Cannot compose add -> int with concat(x:str=Undefined, y:str=b)"
    # if composition was circle message would be:
    # ... concat -> str with add(x:int=Undefined, y:int=Undefined)



**Code compatible with 3.x versions only.**

  .. code-block:: python

    from lawvere import arrow

    @arrow
    def add(x:int, y:int) -> int:
      return x + y

    # identical use as Python 2 #

    # Type Checking:
    type_checked = False
    try:
      add('a', 'b') == 'ab'
    except TypeError:
      type_checked = True

    assert type_checked, 'add should not exists for str types'

    # dispatch
    @add.register
    def concat(x:str, y:str) -> str:
      return "%s %s" %(x, y)

    assert concat('a', 'b') == 'a b'
    # now add exists for str types:
    assert add('a', 'b') == 'a b'

    # type is also checked when composing... see python 2 ex.






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
