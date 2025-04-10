#include <hidapi/hidapi.h>

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(hidapi_py, m) {
    m.doc() = "HIDAPI C++ bindings";

    m.def("hid_init", &hid_init, "Initialize the HIDAPI library");
    m.def("hid_exit", &hid_exit, "Finalize the HIDAPI library");
}