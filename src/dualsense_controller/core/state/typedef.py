from __future__ import annotations

from typing import Any, Callable, TypeVar, TypeAlias, Unpack, TypeVarTuple

from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.state.enum import MixedStateName
from dualsense_controller.core.state.read_state.enum import ReadStateName
from dualsense_controller.core.state.write_state.enum import WriteStateName

StateValue = TypeVar('StateValue')
AdditionalArgs = TypeVarTuple("AdditionalArgs")
MappedStateValue = TypeVar('MappedStateValue')
StateName = ReadStateName | WriteStateName | MixedStateName | str

_StChCb0 = Callable[[], None]
_StChCb1 = Callable[[Any], None]
_StChCb2 = Callable[[Any, int | None], None]
_StChCb3 = Callable[[Any, Any, int | None], None]
_StChCb4 = Callable[[StateName, Any, Any, int | None], None]
StateChangeCallback = _StChCb0 | _StChCb1 | _StChCb2 | _StChCb3 | _StChCb4

Number = int | float
CompareResult = tuple[bool, StateValue]
_WrappedCompareFn: TypeAlias = Callable[[StateValue, StateValue, Unpack[AdditionalArgs]], CompareResult[StateValue]]
_CompareFn: TypeAlias = Callable[[StateValue, StateValue], CompareResult[StateValue]]
Ts = TypeVarTuple("Ts")
WrappedCompareFn: TypeAlias = Callable[[StateValue, StateValue, *Ts], CompareResult[StateValue]]
CompareFn: TypeAlias = _WrappedCompareFn[StateValue] | _CompareFn[StateValue]
StateValueFn: TypeAlias = Callable[[InReport, Unpack[AdditionalArgs]], StateValue]

def default_compare_fn(before: StateValue, after: StateValue) -> CompareResult[StateValue]:
    return (True, after) if before != after else (False, after)
