// example : Hello Trident！
#include <torch/serialize/tensor.h>
#include <torch/extension.h>
#include <vector>
#include <cuda.h>
#include <cuda_runtime_api.h>

namespace Trident{
    void HelloTrident(){
        std::cout<<"Hello Trident!\nTrident is a framework for fast GPU operation development, test and deploy!\n";
        return;
    }
}

using namespace Trident;

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
	m.def("hello", &HelloTrident, "trident.hello : \n A helloworld example of trident.");
}
