#ifndef _HIDAPI_PY_HID_DEVICE_INFO_H_
#define _HIDAPI_PY_HID_DEVICE_INFO_H_

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

class HidDeviceInfo {
public:
    HidDeviceInfo() : hid_device_info_ptr(0) {}
    HidDeviceInfo(hid_device_info *ptr) : hid_device_info_ptr(ptr) {}
    ~HidDeviceInfo() { }
    
    std::string get_path() {return hid_device_info_ptr->path;}
    void set_path(std::string &path) { std::memcpy(hid_device_info_ptr->path, path.c_str(), path.size() * sizeof(wchar_t)); }

    unsigned short get_vendor_id() { return hid_device_info_ptr->vendor_id; }
    void set_vendor_id(unsigned short vencor_id) { hid_device_info_ptr->vendor_id = vencor_id; }

    unsigned short get_product_id() { return hid_device_info_ptr->product_id; }
    void set_product_id(unsigned short product_id) { hid_device_info_ptr->product_id = product_id; }

    std::wstring get_serial_number() { return hid_device_info_ptr->serial_number; }
    void set_serial_number(std::wstring &serial_number) { std::memcpy(hid_device_info_ptr->serial_number, serial_number.c_str(), serial_number.size() * sizeof(wchar_t)); }

    unsigned short get_release_number() { return hid_device_info_ptr->release_number; }
    void set_release_number(unsigned int release_number) { hid_device_info_ptr->release_number = release_number; }

    std::wstring get_manufacturer_string() { return std::wstring(hid_device_info_ptr->manufacturer_string); }
    void set_manufacturer_string(std::wstring &manufacturer_string) { std::memcpy(hid_device_info_ptr->manufacturer_string, manufacturer_string.c_str(), manufacturer_string.size() * sizeof(wchar_t)); }

    std::wstring get_product_string() { return std::wstring(hid_device_info_ptr->product_string); }
    void set_product_string(std::wstring &product_string) { std::memcpy(hid_device_info_ptr->product_string, product_string.c_str(), product_string.size() * sizeof(wchar_t)); }

    unsigned short get_usage_page() { return hid_device_info_ptr->usage_page; }
    void set_usage_page(unsigned short usage_page) { hid_device_info_ptr->usage_page = usage_page; }

    unsigned short get_usage() { return hid_device_info_ptr->usage; }
    void set_usage(unsigned short usage) { hid_device_info_ptr->usage = usage; }

    int get_interface_number() { return hid_device_info_ptr->interface_number; }
    void set_interface_number(int interface_number) { hid_device_info_ptr->interface_number = interface_number; }

    HidDeviceInfo get_next() {
        if (hid_device_info_ptr == nullptr || hid_device_info_ptr->next == nullptr)
        {
            return HidDeviceInfo(nullptr); // just return a null wrapper
        }
        return HidDeviceInfo(hid_device_info_ptr->next);
    }
    void set_next(HidDeviceInfo &hid_device_info) {
        hid_device_info_ptr->next = hid_device_info.hid_device_info_ptr;
    }

    hid_bus_type get_bus_type() { return hid_device_info_ptr->bus_type; }
    void set_bus_type(hid_bus_type bus_type){ hid_device_info_ptr->bus_type = bus_type; }

    bool has() { return hid_device_info_ptr != nullptr; }
    bool has_next() { return hid_device_info_ptr->next != nullptr; }

    hid_device_info *get_device_info() { return hid_device_info_ptr; }

private:
    hid_device_info *hid_device_info_ptr;
};

    /*py::class_<HidDeviceInfo>(m, "HidDeviceInfo")
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
        .def_property("bus_type", &HidDeviceInfo::get_bus_type, &HidDeviceInfo::set_bus_type, "Underly bus type");*/
    
#endif // _HIDAPI_PY_HID_DEVICE_INFO_H_