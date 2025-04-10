from __future__ import annotations  # Enables forward references for type hints
import threading
from typing import Generic, Final

from dualsense_controller.core.typedef import LockableValue


class Lockable(Generic[LockableValue], object):
    __slots__ = ['_value', '_lock']

    @property
    def value(self) -> LockableValue | None:
        with self._lock:
            return self._value

    @value.setter
    def value(self, value: LockableValue | None) -> None:
        with self._lock:
            self._value = value

    def __init__(self, lock: threading.Lock | None = None, value: LockableValue | None = None):
        self._lock: Final[threading.Lock] = lock or threading.Lock()
        self._value: LockableValue | None = value
