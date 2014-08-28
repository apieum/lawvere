from .morphism import Morphism
from .curry import Curry
from .arrow import ArrowType
from .dispatcher import dispatch
from .stack import composable, compose_with, compose_with_self

morphism = ArrowType(Morphism)
arrow = ArrowType(dispatch(Morphism))
curry = dispatch(Curry)
