from hidapi_py import hid_enumerate, hid_free_enumeration, HidDeviceInfo

def enumerate(vendor_id: int = 0, product_id: int = 0):
    """Enumerate the HID Devices.

    Returns a generator that yields all of the HID devices attached to the
    system.

    :param vendor_id:   Only return devices which match this vendor id
    :type vendor_id:    int
    :param product_id:  Only return devices which match this product id
    :type product_id:   int
    :return:            Generator that yields informations about attached
                        HID devices
    :rval:              generator(DeviceInfo)

    """
    devices: list[HidDeviceInfo] = []
    info = hid_enumerate(vendor_id, product_id)
    devices.append(info)
    while info.has_next():
        info = info.next
        devices.append(info)
    # hid_free_enumeration(info)
    return devices
