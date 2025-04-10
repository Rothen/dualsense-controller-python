
/*
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
};*/

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