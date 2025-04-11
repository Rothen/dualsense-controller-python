import threading
from threading import Thread
from typing import Final

import pyee

from dualsense_controller.core.core.Lockable import Lockable
from dualsense_controller.core.enum import ConnectionType, EventType
from dualsense_controller.core.exception import InvalidDeviceIndexException, InvalidInReportLengthException
from dualsense_controller.core.hidapi import HidDevice, HidDeviceInfo, get_all_device_infos
from dualsense_controller.core.log import Log
from dualsense_controller.core.report.in_report.Bt01InReport import Bt01InReport
from dualsense_controller.core.report.in_report.Bt31InReport import Bt31InReport
from dualsense_controller.core.report.in_report.InReport import InReport
from dualsense_controller.core.report.in_report.Usb01InReport import Usb01InReport
from dualsense_controller.core.report.in_report.enum import InReportLength
from dualsense_controller.core.report.in_report.typedef import InReportCallback
from dualsense_controller.core.report.out_report.Bt01OutReport import Bt01OutReport
from dualsense_controller.core.report.out_report.Bt31OutReport import Bt31OutReport
from dualsense_controller.core.report.out_report.OutReport import OutReport
from dualsense_controller.core.report.out_report.Usb01OutReport import Usb01OutReport
from dualsense_controller.core.typedef import ExceptionCallback


class HidControllerDevice:
    VENDOR_ID: Final[int] = 0x054c
    PRODUCT_ID: Final[int] = 0x0ce6

    @staticmethod
    def enumerate_devices() -> list[HidDeviceInfo]:
        return get_all_device_infos(HidControllerDevice.VENDOR_ID, HidControllerDevice.PRODUCT_ID)

    @property
    def connection_type(self) -> ConnectionType:
        return self._connection_type

    @property
    def out_report(self) -> OutReport | None:
        return self._out_report_lockable.value

    @property
    def is_opened(self) -> bool:
        return self._hid_device.is_opened()

    def __init__(self, device_index_or_device_info: int | HidDeviceInfo | None = 0):
        self._connection_type: ConnectionType = ConnectionType.UNDEFINED
        self._event_emitter: Final[pyee.EventEmitter] = pyee.EventEmitter()
        self._loop_thread = Thread(
            target=self._loop,
            daemon=True,
        )
        self._stop_thread_event: threading.Event = threading.Event()
        self._thread_started_event: threading.Event = threading.Event()

        device_info: HidDeviceInfo
        if device_index_or_device_info is None or isinstance(device_index_or_device_info, int):
            device_index: int = device_index_or_device_info if device_index_or_device_info is not None else 0
            hid_device_infos: list[HidDeviceInfo] = HidControllerDevice.enumerate_devices()
            num_hid_device_infos: int = len(hid_device_infos)
            if num_hid_device_infos < device_index + 1:
                raise InvalidDeviceIndexException(device_index)
            device_info = hid_device_infos[device_index]
        else:
            device_info = device_index_or_device_info

        self._serial_number: Final[str] = device_info.serial_number
        self._path: Final[str] = device_info.path
        self._bus_type: HidDevice = HidDevice(path=self._path)
        self._hid_device: HidDevice = HidDevice(path=self._path)

        self._in_report_length: int = InReportLength.DUMMY
        self._in_report_lockable: Final[Lockable[InReport]] = Lockable()
        self._out_report_lockable: Final[Lockable[OutReport]] = Lockable()

    def open(self):
        assert self._hid_device.is_opened() is False, "Device already opened"
        self._hid_device.open()
        self._detect()
        self._start_loop_thread()

    def close(self) -> None:
        assert self._hid_device.is_opened() is True, "Device not opened"
        self._stop_loop_thread()
        self._hid_device.close()

    def write(self) -> None:
        out_report_value = self._out_report_lockable.value

        if out_report_value is None:
            raise Exception("Out report not initialized")

        data = out_report_value.to_bytes()
        Log.verbose(data.hex(' '))
        self._hid_device.write(data)

    def on_exception(self, callback: ExceptionCallback) -> None:
        self._event_emitter.on(EventType.EXCEPTION, callback)

    def on_in_report(self, callback: InReportCallback) -> None:
        self._event_emitter.on(EventType.IN_REPORT, callback)

    def _detect(self) -> None:
        buffer = bytearray(100)
        self._in_report_length = self._hid_device.read(buffer)
        match self._in_report_length:
            case InReportLength.USB_01:
                self._connection_type = ConnectionType.USB_01
                self._in_report_lockable.value = Usb01InReport()
                self._out_report_lockable.value = Usb01OutReport()
            case InReportLength.BT_31:
                self._connection_type = ConnectionType.BT_31
                self._in_report_lockable.value = Bt31InReport()
                self._out_report_lockable.value = Bt31OutReport()
            case InReportLength.BT_01:
                self._connection_type = ConnectionType.BT_01
                self._in_report_lockable.value = Bt01InReport()
                self._out_report_lockable.value = Bt01OutReport()
            case _:
                raise InvalidInReportLengthException

    def _start_loop_thread(self) -> None:
        self._loop_thread.start()
        while not self._thread_started_event.is_set():
            pass

    def _stop_loop_thread(self) -> None:
        self._stop_thread_event.set()
        self._loop_thread.join()

    def _loop(self) -> None:
        if not self._thread_started_event.is_set():
            self._thread_started_event.set()
        try:
            while not self._stop_thread_event.is_set():
                buffer: bytes = self._hid_device.read()
                value = self._in_report_lockable.value
                if value is not None:
                    value.update(buffer)
                self._event_emitter.emit(EventType.IN_REPORT, value)
        except Exception as exception:
            self._event_emitter.emit(EventType.EXCEPTION, exception)
