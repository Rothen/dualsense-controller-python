#include "hid_device.h"

#include <hidapi/hidapi.h>

#include <string>
#include <locale>
#include <codecvt>

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(hidapi_py, m) {
    m.doc() = "HIDAPI C++ bindings";

    py::enum_<hid_bus_type>(m, "HidBusType")
        .value("UNKNOWN", HID_API_BUS_UNKNOWN)
        .value("USB", HID_API_BUS_USB)
        .value("BLUETOOTH", HID_API_BUS_BLUETOOTH)
        .value("I2C", HID_API_BUS_I2C)
        .value("SPI", HID_API_BUS_SPI);

    py::class_<hid_device_info>(m, "HidDeviceInfo")
        .def(py::init<>())
        .def_readwrite("path", &hid_device_info::path, "Platform-specific device path")
        .def_readwrite("vendor_id", &hid_device_info::vendor_id, "Device Vendor ID")
        .def_readwrite("product_id", &hid_device_info::product_id, "Device Product ID")
        .def_readwrite("serial_number", &hid_device_info::serial_number, "Serial Number")
        .def_readwrite("release_number", &hid_device_info::release_number, "Device Release Number in binary-coded decimal")
        .def_readwrite("manufacturer_string", &hid_device_info::manufacturer_string, "Manufacturer String")
        .def_readwrite("product_string", &hid_device_info::product_string, "Product String")
        .def_readwrite("usage_page", &hid_device_info::usage_page, "Usage Page for this Device/Interface")
        .def_readwrite("usage", &hid_device_info::usage, "Usage for this Device/Interface")
        .def_readwrite("interface_number", &hid_device_info::interface_number, "USB interface which this logical device represents")
        .def_readwrite("next", &hid_device_info::next, "Next device")
        .def_readwrite("bus_type", &hid_device_info::bus_type, "Underly bus type");

    py::class_<HidDevice>(m, "HidDevice")
        .def(py::init<unsigned short, unsigned short, const wchar_t *, bool>(), 
            py::arg("vendor_id"), py::arg("product_id"), py::arg("serial_number"), py::arg("blocking") = true)
        .def(py::init<const char *, bool>(), py::arg("path"), py::arg("blocking") = true)
        .def(py::init<hid_device_info *, bool>(), py::arg("device_info"), py::arg("blocking") = true)
        .def("close", &HidDevice::close)
        .def("write", &HidDevice::write)
        .def("read", &HidDevice::read)
        .def("set_nonblocking", &HidDevice::set_nonblocking)
        .def("send_feature_report", &HidDevice::send_feature_report)
        .def("get_feature_report", &HidDevice::get_feature_report)
        .def("get_error", &HidDevice::get_error);

    m.def("hid_init", &hid_init, "Initialize the HIDAPI library");
    m.def("hid_exit", &hid_exit, "Finalize the HIDAPI library");
    m.def("hid_enumerate", &hid_enumerate, "Enumerate HID devices");
    m.def("hid_free_enumeration", &hid_free_enumeration, "Free enumeration results");
}