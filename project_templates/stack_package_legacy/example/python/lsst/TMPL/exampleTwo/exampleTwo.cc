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

#include "lsst/TMPL/ExampleTwo.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace lsst {
namespace tmpl {

PYBIND11_PLUGIN(exampleTwo) {
    py::module mod("exampleTwo");

    py::class_<ExampleBase, std::shared_ptr<ExampleBase>> clsExampleBase(mod, "ExampleBase");
    clsExampleBase.def("someMethod", &ExampleBase::someMethod);

    py::class_<ExampleTwo, std::shared_ptr<ExampleTwo>, ExampleBase> clsExampleTwo(mod, "ExampleTwo");
    clsExampleTwo.def(py::init<>());
    clsExampleTwo.def("someOtherMethod", &ExampleTwo::someOtherMethod);

    return mod.ptr();
}
}  // tmpl
}  // lsst
