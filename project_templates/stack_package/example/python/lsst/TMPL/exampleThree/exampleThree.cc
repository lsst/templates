/*
 * LSST Data Management System
 * Copyright 2008-2017  AURA/LSST.
 *
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the LSST License Statement and
 * the GNU General Public License along with this program.  If not,
 * see <https://www.lsstcorp.org/LegalNotices/>.
 */

#include "pybind11/pybind11.h"

#include "lsst/TMPL/ExampleThree.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace lsst {
namespace tmpl {
namespace {

template <typename T>
static void declareExampleThree(py::module & mod, std::string const & suffix) {
    using Class = ExampleThree<T>;
    using PyClass = py::class_<Class, std::shared_ptr<Class>, ExampleBase>;

    PyClass cls(mod, ("ExampleThree" + suffix).c_str());

    cls.def(py::init<T>());
    cls.def("someOtherMethod", &Class::someOtherMethod);
}

}  // <anonymous>

PYBIND11_PLUGIN(exampleThree) {
    py::module::import("lsst.TMPL.exampleTwo");

    py::module mod("exampleThree");

    declareExampleThree<float>(mod, "F");
    declareExampleThree<double>(mod, "D");

    return mod.ptr();
}
}  // tmpl
}  // lsst
