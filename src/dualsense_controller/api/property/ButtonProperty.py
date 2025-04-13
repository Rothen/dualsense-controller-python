from typing import Callable
from dualsense_controller.api.property.base import BoolProperty


class ButtonProperty(BoolProperty):

    def on_down(self, callback: Callable[[], None]):
        self._on_true(callback)

    def on_up(self, callback: Callable[[], None]):
        self._on_false(callback)

    @property
    def pressed(self) -> bool:
        return self._get_value()