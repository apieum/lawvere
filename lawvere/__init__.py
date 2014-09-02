from .morphism import Morphism
from .curry import Curry
from .arrow import Arrow, typedef
from .dispatcher import dispatch
from .stack import composable, compose_with, compose_with_self

morphism = Arrow.wrap(Morphism)
arrow = Arrow.wrap(dispatch(Morphism))
curry = dispatch(Curry)
