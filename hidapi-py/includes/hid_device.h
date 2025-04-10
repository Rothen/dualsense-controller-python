#ifndef _HIDAPI_PY_HID_DEVICE_H_
#define _HIDAPI_PY_HID_DEVICE_H_

#include <hidapi/hidapi.h>

#include <string>
#include <locale>
#include <codecvt>

#include <pybind11/pybind11.h>

namespace py = pybind11;

class HidDevice {
public:
    HidDevice(unsigned short vendor_id, unsigned short product_id, const wchar_t *serial_number, bool blocking = true)
    {
        hid_device_ptr = hid_open(vendor_id, product_id, serial_number);
        if (!hid_device_ptr) {
            throw std::runtime_error("Failed to open HID device");
        }
        if (!blocking)
        {
            hid_set_nonblocking(hid_device_ptr, 1);
        }
    }
    HidDevice(const char *path, bool blocking = true)
    {
        hid_device_ptr = hid_open_path(path);
        if (!hid_device_ptr) {
            throw std::runtime_error("Failed to open HID device");
        }
        if (!blocking)
        {
            hid_set_nonblocking(hid_device_ptr, 1);
        }
    }
    HidDevice(hid_device_info *device_info, bool blocking = true) : HidDevice(device_info->path, blocking) { }

    ~HidDevice()
    {
        close();
    }

    void close()
    {
        hid_close(hid_device_ptr);
    }

    int write(std::string data)
    {
        const unsigned char *data_ptr = reinterpret_cast<const unsigned char *>(data.c_str());
        return hid_write(hid_device_ptr, data_ptr, data.size());
    }

    py::bytes read(size_t length, int timeout_ms = 0, bool blocking = false)
    {
        unsigned char *data = new unsigned char[length];

        if (timeout_ms == 0 && blocking)
        {
            timeout_ms = -1;
        }
        if (timeout_ms)
        {
            hid_read_timeout(hid_device_ptr, data, length, timeout_ms);
        }
        else
        {
            hid_read(hid_device_ptr, data, length);
        }

        auto result = py::bytes(reinterpret_cast<const char *>(data));
        delete[] data;
        return result;
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
    /*
    int get_manufacturer_string(wchar_t *string, size_t maxlen) { return hid_get_manufacturer_string(hid_device_ptr, string, maxlen); }
    int get_product_string(wchar_t *string, size_t maxlen) { return hid_get_product_string(hid_device_ptr, string, maxlen); }
    int get_serial_number_string(wchar_t *string, size_t maxlen) { return hid_get_serial_number_string(hid_device_ptr, string, maxlen); }
    int get_indexed_string(int string_index, wchar_t *string, size_t maxlen) { return hid_get_indexed_string(hid_device_ptr, string_index, string, maxlen); }
    const wchar_t * get_error() { return hid_error(hid_device_ptr); }
    */

private:
    hid_device* hid_device_ptr;
};

#endif // _HIDAPI_PY_HID_DEVICE_H_