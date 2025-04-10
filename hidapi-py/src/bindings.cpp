#include <hidapi/hidapi.h>

#include <string>
#include <locale>
#include <codecvt>

#include <pybind11/pybind11.h>

namespace py = pybind11;

std::string wchar_to_string(const wchar_t* wstr) {
    // Use a wide character to UTF-8 conversion
    std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
    return converter.to_bytes(wstr);
}

std::wstring string_to_wchar(const std::string& str) {
    // Use a UTF-8 to wide character conversion
    std::wstring_convert<std::codecvt_utf8<wchar_t>> converter;
    return converter.from_bytes(str);
}

class HidDeviceInfo {
public:
    HidDeviceInfo() : hid_device_info_ptr(nullptr) {}
    ~HidDeviceInfo() { }
    
    std::string get_path() {return hid_device_info_ptr->path;}
    void set_path(std::string &path) { std::memcpy(hid_device_info_ptr->path, path.c_str(), path.size() * sizeof(char)); }

    unsigned short get_vendor_id() { return hid_device_info_ptr->vendor_id; }
    void set_vendor_id(unsigned short vencor_id) { hid_device_info_ptr->vendor_id = vencor_id; }

    unsigned short get_product_id() { return hid_device_info_ptr->product_id; }
    void set_product_id(unsigned short product_id) { hid_device_info_ptr->product_id = product_id; }

    std::string get_serial_number() { return wchar_to_string(hid_device_info_ptr->serial_number); }
    void set_serial_number(std::string &serial_number) { std::memcpy(hid_device_info_ptr->serial_number, string_to_wchar(serial_number).c_str(), string_to_wchar(serial_number).size() * sizeof(char)); }

    unsigned short get_release_number() { return hid_device_info_ptr->release_number; }
    void set_release_number(unsigned int release_number) { hid_device_info_ptr->release_number = release_number; }

    std::string get_manufacturer_string() { return wchar_to_string(hid_device_info_ptr->manufacturer_string); }
    void set_manufacturer_string(std::string &manufacturer_string) { std::memcpy(hid_device_info_ptr->manufacturer_string, string_to_wchar(manufacturer_string).c_str(), string_to_wchar(manufacturer_string).size() * sizeof(char)); }

    std::string get_product_string() { return wchar_to_string(hid_device_info_ptr->product_string); }
    void set_product_string(std::string &product_string) { std::memcpy(hid_device_info_ptr->product_string, string_to_wchar(product_string).c_str(), string_to_wchar(product_string).size() * sizeof(char)); }

    unsigned short get_usage_page() { return hid_device_info_ptr->usage_page; }
    void set_usage_page(unsigned short usage_page) { hid_device_info_ptr->usage_page = usage_page; }

    unsigned short get_usage() { return hid_device_info_ptr->usage; }
    void set_usage(unsigned short usage) { hid_device_info_ptr->usage = usage; }

    int get_interface_number() { return hid_device_info_ptr->interface_number; }
    void set_interface_number(int interface_number) { hid_device_info_ptr->interface_number = interface_number; }

    HidDeviceInfo get_next() { 
        HidDeviceInfo next_device_info;
        next_device_info.hid_device_info_ptr = hid_device_info_ptr->next;
        return next_device_info;
    }
    void set_next(HidDeviceInfo &hid_device_info) {
        hid_device_info_ptr->next = hid_device_info.hid_device_info_ptr;
    }

    hid_bus_type get_bus_type() { return hid_device_info_ptr->bus_type; }
    void set_bus_type(hid_bus_type bus_type){ hid_device_info_ptr->bus_type = bus_type; }

private:
    hid_device_info* hid_device_info_ptr;
};

class HidDevice {
public:
    HidDevice(unsigned short vendor_id, unsigned short product_id, const wchar_t *serial_number) {
        hid_device_ptr = hid_open(vendor_id, product_id, serial_number);
        if (!hid_device_ptr) {
            throw std::runtime_error("Failed to open HID device");
        }
    }
    HidDevice(const char *path) {
        hid_device_ptr = hid_open_path(path);
        if (!hid_device_ptr) {
            throw std::runtime_error("Failed to open HID device");
        }
    }

    ~HidDevice() { hid_close(hid_device_ptr); }

    int write(const unsigned char *data, size_t length) { return hid_write(hid_device_ptr, data, length); }
    int read_timeout(unsigned char *data, size_t length, int milliseconds) { return hid_read_timeout(hid_device_ptr, data, length, milliseconds); }
    int read(unsigned char *data, size_t length) { return hid_read(hid_device_ptr, data, length); }
    int set_nonblocking(int nonblock) { return hid_set_nonblocking(hid_device_ptr, nonblock); }
    int send_feature_report(const unsigned char *data, size_t length) { return hid_send_feature_report(hid_device_ptr, data, length); }
    int get_feature_report(unsigned char *data, size_t length) { return hid_get_feature_report(hid_device_ptr, data, length); }
    int get_manufacturer_string(wchar_t *string, size_t maxlen) { return hid_get_manufacturer_string(hid_device_ptr, string, maxlen); }
    int get_product_string(wchar_t *string, size_t maxlen) { return hid_get_product_string(hid_device_ptr, string, maxlen); }
    int get_serial_number_string(wchar_t *string, size_t maxlen) { return hid_get_serial_number_string(hid_device_ptr, string, maxlen); }
    int get_indexed_string(int string_index, wchar_t *string, size_t maxlen) { return hid_get_indexed_string(hid_device_ptr, string_index, string, maxlen); }
    const wchar_t * get_error() { return hid_error(hid_device_ptr); }

private:
    hid_device* hid_device_ptr;
};

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
        .def_property("bus_type", &HidDeviceInfo::get_bus_type, &HidDeviceInfo::set_bus_type, "Underly bus type");

    py::class_<HidDevice>(m, "HidDevice")
        .def(py::init<unsigned short, unsigned short, const wchar_t *>())
        .def(py::init<const char *>())
        .def("write", &HidDevice::write)
        .def("read_timeout", &HidDevice::read_timeout)
        .def("read", &HidDevice::read)
        .def("set_nonblocking", &HidDevice::set_nonblocking)
        .def("send_feature_report", &HidDevice::send_feature_report)
        .def("get_feature_report", &HidDevice::get_feature_report)
        .def("get_manufacturer_string", &HidDevice::get_manufacturer_string)
        .def("get_product_string", &HidDevice::get_product_string)
        .def("get_serial_number_string", &HidDevice::get_serial_number_string)
        .def("get_indexed_string", &HidDevice::get_indexed_string)
        .def("get_error", &HidDevice::get_error);

    m.def("hid_init", &hid_init, "Initialize the HIDAPI library");
    m.def("hid_exit", &hid_exit, "Finalize the HIDAPI library");
    m.def("hid_enumerate", &hid_enumerate, "Enumerate HID devices");
    m.def("hid_free_enumeration", &hid_free_enumeration, "Free enumeration results");

    m.def("hid_open", &hid_open, "Open a HID device by VID and PID");
    m.def("hid_open_path", &hid_open_path, "Open a HID device by path");
    m.def("hid_write", &hid_write, "Write data to a HID device");
    m.def("hid_read_timeout", &hid_read_timeout, "Read data from a HID device with timeout");
    m.def("hid_read", &hid_read, "Read data from a HID device");
    m.def("hid_set_nonblocking", &hid_set_nonblocking, "Set non-blocking mode for a HID device");
    m.def("hid_send_feature_report", &hid_send_feature_report, "Send a feature report to a HID device");
    m.def("hid_get_feature_report", &hid_get_feature_report, "Get a feature report from a HID device");
    m.def("hid_close", &hid_close, "Close a HID device");
    m.def("hid_get_manufacturer_string", &hid_get_manufacturer_string, "Get manufacturer string from a HID device");
    m.def("hid_get_product_string", &hid_get_product_string, "Get product string from a HID device");
    m.def("hid_get_serial_number_string", &hid_get_serial_number_string, "Get serial number string from a HID device");
    m.def("hid_get_indexed_string", &hid_get_indexed_string, "Get indexed string from a HID device");
    m.def("hid_error", &hid_error, "Get the last error message from a HID device");    
}