#include "hid_device_info.h"
#include "hid_device.h"

#ifdef _WIN32
    #include <hidapi.h>
#else
    #include <hidapi/hidapi.h>
#endif

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

    py::class_<HidDeviceInfo>(m, "HidDeviceInfo")
        .def(py::init<>())
        .def_property("path", &HidDeviceInfo::get_path, &HidDeviceInfo::set_path, "Platform-specific device path")
        .def_property("vendor_id", &HidDeviceInfo::get_vendor_id, &HidDeviceInfo::set_vendor_id, "Device Vendor ID")
        .def_property("product_id", &HidDeviceInfo::get_product_id, &HidDeviceInfo::set_product_id, "Device Product ID")
        .def_property("serial_number", &HidDeviceInfo::get_serial_number, &HidDeviceInfo::set_serial_number, "Serial Number")
        .def_property("release_number", &HidDeviceInfo::get_release_number, &HidDeviceInfo::set_release_number, "Device Release Number in binary-coded decimal")
        .def_property("manufacturer_string", &HidDeviceInfo::get_manufacturer_string, &HidDeviceInfo::set_manufacturer_string, "Manufacturer String")
        .def_property("product_string", &HidDeviceInfo::get_product_string, &HidDeviceInfo::set_product_string, "Product String")
        .def_property("usage_page", &HidDeviceInfo::get_usage_page, &HidDeviceInfo::set_usage_page, "Usage Page for this Device/Interface")
        .def_property("usage", &HidDeviceInfo::get_usage, &HidDeviceInfo::set_usage, "Usage for this Device/Interface")
        .def_property("interface_number", &HidDeviceInfo::get_interface_number, &HidDeviceInfo::set_interface_number, "USB interface which this logical device represents")
        .def_property("next", &HidDeviceInfo::get_next, &HidDeviceInfo::set_next, "Next device")
        .def_property("bus_type", &HidDeviceInfo::get_bus_type, &HidDeviceInfo::set_bus_type, "Underly bus type")
        .def("has", &HidDeviceInfo::has, "Check if the device info is valid")
        .def("has_next", &HidDeviceInfo::has_next, "Check if there is a next device");

    py::class_<HidDevice>(m, "HidDevice")
        .def(py::init<unsigned short, unsigned short, const wchar_t *, bool>(),
             py::arg("vendor_id"), py::arg("product_id"), py::arg("serial_number"), py::arg("blocking") = true)
        .def(py::init<const char *, bool>(), py::arg("path"), py::arg("blocking") = true)
        .def(py::init<HidDeviceInfo &, bool>(), py::arg("device_info"), py::arg("blocking") = true)
        .def("close", &HidDevice::close)
        .def("write", py::overload_cast<std::string &>(&HidDevice::write), py::arg("data"), "Write string data to the device")
        .def("write", py::overload_cast<py::bytes &>(&HidDevice::write), py::arg("data"), "Write bytes data to the device")
        .def("read", py::overload_cast<size_t, int, bool>(&HidDevice::read), py::arg("length"), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("read", py::overload_cast<int, bool>(&HidDevice::read), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("read", py::overload_cast<py::bytearray &, int, bool>(&HidDevice::read), py::arg("buffer"), py::arg("timeout_ms") = 0, py::arg("blocking") = false)
        .def("set_nonblocking", &HidDevice::set_nonblocking)
        .def("send_feature_report", &HidDevice::send_feature_report)
        .def("get_feature_report", &HidDevice::get_feature_report)
        .def("get_error", &HidDevice::get_error)
        .def("is_opened", &HidDevice::is_opened);

    m.def("hid_init", &hid_init, "Initialize the HIDAPI library");
    m.def("hid_exit", &hid_exit, "Finalize the HIDAPI library");
    m.def("hid_enumerate", [](unsigned short vendor_id, unsigned short product_id)
          { return HidDeviceInfo(hid_enumerate(vendor_id, product_id)); }, py::arg("vendor_id"), py::arg("product_id"), "Enumerate HID devices");
    m.def("hid_free_enumeration", [](HidDeviceInfo &device_info)
          { return hid_free_enumeration(device_info.get_device_info()); }, py::arg("device_info"), "Free enumeration results");
}