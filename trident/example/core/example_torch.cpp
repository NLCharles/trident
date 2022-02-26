// example : Hello Trident！
#include <torch/serialize/tensor.h>
#include <torch/extension.h>
#include <vector>
#include <cuda.h>
#include <cuda_runtime_api.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
namespace Trident{
    void HelloTrident(){
        std::cout<<"Hello Trident!\nTrident is a framework for fast GPU operation development, test and deploy!\n";
        return;
    }
    py::array_t<double> add_arrays(py::array_t<double> input1, py::array_t<double> input2);
}

using namespace Trident;

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
	m.def("hello", &HelloTrident, "trident.hello : \n A helloworld example of trident.");
    m.def("add_arrays", &add_arrays, "Add two NumPy arrays");
}
