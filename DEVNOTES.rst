******************
Development Notes
******************
*Intent to explain choices on design.*

--------------------------------------------------------------------


Features:
    * Composition (circle and pipe)
    * Currying
    * Type checking on functions signatures

Constraints:
    * should use features independantly from each others
    * should extend lib with proper objects (Stacks, Signatures)
    * should be compatible with and syntax specific to python >= 2.7 and 3.x versions.


===========
Version 0.1
===========

I hate the design of this first release, but haven't found a sufficient good idea to improve it.

The main matter is having py version syntax specific functions like dispatch.register
In one case (2.x) it is called with domain and codomain and on the other case with function.
This pattern is practical for api usage but has a crapy implementation.

Other things I would remove:
 * Morphism.check_domain and Morphism.check_codomain: required to avoid checking on function call for composed functions
 * getattr on Stacks... which returns first item attribute.
 * overuse of @property
 * globally dispatch implementation


That's why I've not documented the complete api wich is:
    * Morphism, Curry, (base classes, constructed with a function and a *Signature* object)
    * typify, typed, typedef, (utils to add type annotations)
    * dispatcher, (transform class like Morphism in dispatcher)
    * composable, compose_with, compose_with_self, (class decorators to make composables objects with Stack or other stack types)
    * morphism, arrow, curry (typed or dispatched versions of Curry and Morphism)

**Details:**
    * *Curry* is composable with Stack, (No type checking)
    * *Morphism* extends Curry (it add func signature type checking) and is composable with *MorphismStack* (which add composition type checking, and deactivate func signature type checking between each composed function)
    * *typedef* is a simple function decorator that add domain and codomain to function annotations.
    * *typify* is an alias of *typed.wrap*
    * *typed* wraps a callable with typedef and manage version specific syntax
    * *dispatcher* use *typify.MultipleWrap* via *typed* to override *__call__* (dispatch) and add *register* method to a callable.
    * *compose_with* make a class of composable with specifi Stack.
    * *morphism* is the typified version of *Morphism* (*arrow* without dispatcher)
    * *arrow* is a dispatched *Morphism*
    * *curry* is a dispatched *Curry*: do not check type annotations, but parameters names and length





