from typing import Any, Callable

from dualsense_controller.core.state.typedef import Number

FromToTuple = tuple[Number, Number, Number, Number]
MapFn = Callable[[Any], Any]

def empty_map_fn(x: Any) -> Any:
    return x
