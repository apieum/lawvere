from .morphism import Morphism
from .curry import Curry
from .typify import typify, typed, typedef
from .dispatcher import dispatcher
from .stack import composable, compose_with, compose_with_self

morphism = typify(Morphism)
arrow = dispatcher(Morphism)
curry = dispatcher(Curry)
