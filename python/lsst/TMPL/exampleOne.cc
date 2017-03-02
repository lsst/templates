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
#include "pybind11/stl.h"

#include "numpy/arrayobject.h"
#include "numpy/arrayobject.h"
#include "ndarray/pybind11.h"

#include "lsst/pex/exceptions/python/Exception.h"

#include "lsst/TMPL/ExampleOne.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace lsst {
namespace tmpl {

PYBIND11_PLUGIN(exampleOne) {
    py::module mod("exampleOne");

    if (_import_array() < 0) {
            PyErr_SetString(PyExc_ImportError, "numpy.core.multiarray failed to import");
            return nullptr;
    };

    pex::exceptions::python::declareException<ExampleError, pex::exceptions::RuntimeError>(
            mod, "ExampleError", "RuntimeError");

    py::class_<ExampleOne, std::shared_ptr<ExampleOne>> clsExampleOne(mod, "ExampleOne");

    py::enum_<ExampleOne::State>(clsExampleOne, "State")
        .value("RED", ExampleOne::State::RED)
        .value("ORANGE", ExampleOne::State::ORANGE)
        .value("GREEN", ExampleOne::State::GREEN)
        .export_values();

    clsExampleOne.def(py::init<>());
    clsExampleOne.def(py::init<std::string const&, ExampleOne::State>(), "fileName"_a, "state"_a=ExampleOne::State::RED);
    clsExampleOne.def(py::init<ExampleOne const&, bool>(), "other"_a, "deep"_a=true); // Copy constructor
    
    clsExampleOne.def("getState", &ExampleOne::getState);
    clsExampleOne.def("setState", &ExampleOne::setState);
    clsExampleOne.def_property("state", &ExampleOne::getState, &ExampleOne::setState);
    clsExampleOne.def("computeSomething", &ExampleOne::computeSomething);
    clsExampleOne.def("computeSomethingElse",
                      (double (ExampleOne::*)(int, double) const) & ExampleOne::computeSomethingElse,
                      "myFirstParam"_a, "mySecondParam"_a);
    clsExampleOne.def("computeSomethingElse", (double (ExampleOne::*)(int, std::string) const) &ExampleOne::computeSomethingElse, "myFirstParam"_a, "anotherParam"_a="foo");
    clsExampleOne.def("computeSomeVector", &ExampleOne::computeSomeVector);
    clsExampleOne.def("doSomethingWithArray", &ExampleOne::doSomethingWithArray);
    clsExampleOne.def_static("initializeSomething", &ExampleOne::initializeSomething);

    clsExampleOne.def("__eq__", &ExampleOne::operator==, py::is_operator());
    clsExampleOne.def("__ne__", &ExampleOne::operator!=, py::is_operator());
    clsExampleOne.def("__iadd__", &ExampleOne::operator+=);
    clsExampleOne.def("__add__", [](ExampleOne const & self, ExampleOne const & other) { return self + other; }, py::is_operator());

    return mod.ptr();
}

}  // tmpl
}  // lsst
