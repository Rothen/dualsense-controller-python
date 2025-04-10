#ifndef _HIDAPI_PY_HID_DEVICE_H_
#define _HIDAPI_PY_HID_DEVICE_H_

#include "hid_device_info.h"

#ifdef _WIN32
    #include <hidapi.h>
#else
    #include <hidapi/hidapi.h>
#endif

#include <string>
#include <locale>
#include <codecvt>

#include <pybind11/pybind11.h>

#include <iostream>
#include <iomanip> // for std::setw, std::setfill

namespace py = pybind11;

class HidDevice {
public:
    HidDevice(unsigned short vendor_id, unsigned short product_id, const wchar_t *serial_number, bool blocking = true) : HidDevice(hid_open(vendor_id, product_id, serial_number), blocking) { }

    HidDevice(const char *path, bool blocking = true) : HidDevice(hid_open_path(path), blocking) {}

    HidDevice(HidDeviceInfo &device_info, bool blocking = true) : HidDevice(device_info.get_device_info()->path, blocking) { }

    ~HidDevice()
    {
        close();
    }

    void close()
    {
        if (hid_device_ptr != nullptr)
        {
            hid_close(hid_device_ptr);
            hid_device_ptr = nullptr; // Ensure the pointer is null after closing
        }

        opened = false;
    }

    int write(std::string &data)
    {
        const unsigned char *data_ptr = reinterpret_cast<const unsigned char *>(data.c_str());
        return hid_write(hid_device_ptr, data_ptr, data.size());
    }

    int write(py::bytes &data)
    {
        py::buffer_info info(py::buffer(data).request(true));
        return hid_write(hid_device_ptr, reinterpret_cast<unsigned char *>(info.ptr), info.size);
    }

    py::bytes read(size_t length, int timeout_ms = 0, bool blocking = false)
    {
        unsigned char *buffer = new unsigned char[length];
        int rv = read(buffer, length, timeout_ms, blocking);
        auto result = py::bytes(reinterpret_cast<const char *>(buffer), rv);
        delete[] buffer;
        return result;
    }

    py::bytes read(int timeout_ms = 0, bool blocking = false)
    {
        int rv = read(temp_read_data, 100, timeout_ms, blocking);
        return py::bytes(reinterpret_cast<const char *>(temp_read_data), rv);
    }

    int read(py::bytearray &buffer, int timeout_ms = 0, bool blocking = false)
    {
        py::buffer_info info(py::buffer(buffer).request(true));
        return read(reinterpret_cast<unsigned char *>(info.ptr), info.size, timeout_ms, blocking);
    }

    int read(unsigned char *buffer, size_t length, int timeout_ms = 0, bool blocking = false)
    {
        if (timeout_ms == 0 && blocking)
        {
            timeout_ms = -1;
        }
        int rv;
        if (timeout_ms)
        {
            rv = hid_read_timeout(hid_device_ptr, buffer, length, timeout_ms);
        }
        else
        {
            rv = hid_read(hid_device_ptr, buffer, length);
        }
        return rv;
    }

    int set_nonblocking(int nonblock)
    {
        return hid_set_nonblocking(hid_device_ptr, nonblock);
    }
    
    int send_feature_report(std::string data, uint8_t report_id=0x0)
    {
        unsigned char *data_ptr = new unsigned char[data.size() + 1];
        data_ptr[0] = report_id;
        std::memcpy(data_ptr + 1, data.c_str(), data.size());
        int result = hid_send_feature_report(hid_device_ptr, data_ptr, data.size() + 1);
        delete[] data_ptr;
        return result;
    }

    int get_feature_report(uint8_t report_id, size_t length) {
        unsigned char *data_ptr = new unsigned char[length + 1];
        data_ptr[0] = report_id;
        return hid_get_feature_report(hid_device_ptr, data_ptr, length);
    }

    std::string get_error() {
        std::wstring ws(hid_error(hid_device_ptr));
        return std::string(ws.begin(), ws.end());
    }

    bool is_opened() const { return opened; }
    /*
    int get_manufacturer_string(wchar_t *string, size_t maxlen) { return hid_get_manufacturer_string(hid_device_ptr, string, maxlen); }
    int get_product_string(wchar_t *string, size_t maxlen) { return hid_get_product_string(hid_device_ptr, string, maxlen); }
    int get_serial_number_string(wchar_t *string, size_t maxlen) { return hid_get_serial_number_string(hid_device_ptr, string, maxlen); }
    int get_indexed_string(int string_index, wchar_t *string, size_t maxlen) { return hid_get_indexed_string(hid_device_ptr, string_index, string, maxlen); }
    const wchar_t * get_error() { return hid_error(hid_device_ptr); }
    */

private:
    HidDevice(hid_device *device_ptr, bool blocking = true) : hid_device_ptr(device_ptr)
    {
        if (!hid_device_ptr)
        {
            opened = false;
            throw std::runtime_error("Failed to open HID device");
        }
        if (!blocking)
        {
            hid_set_nonblocking(hid_device_ptr, 1);
        }
        opened = true;
    }

    hid_device *hid_device_ptr;
    unsigned char temp_read_data[100];
    bool opened = true;
};

#endif // _HIDAPI_PY_HID_DEVICE_H_