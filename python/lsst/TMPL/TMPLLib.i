// -*- lsst-c++ -*-
%define daf_base_DOCSTRING
"
Access to the classes from the daf_base library
"
%enddef

%feature("autodoc", "1");
%module(package="lsst.daf.base", docstring=daf_base_DOCSTRING) baseLib

%{
#include "lsst/daf/base/Citizen.h"
#include "lsst/daf/base/DateTime.h"
#include "lsst/daf/base/Persistable.h"
#include "lsst/daf/base/PropertySet.h"
%}

%include "lsst/p_lsstSwig.i"

%lsst_exceptions()
%import "lsst/pex/exceptions/exceptionsLib.i"

SWIG_SHARED_PTR(Persistable, lsst::daf::base::Persistable)
SWIG_SHARED_PTR_DERIVED(PropertySet, lsst::daf::base::Persistable, lsst::daf::base::PropertySet)

%include "persistenceMacros.i"
%lsst_persistable(lsst::daf::base::PropertySet);

class lsst::daf::base::Citizen;

%template(vectorCitizen) std::vector<lsst::daf::base::Citizen *>;

// Swig versions 1.3.33 - 1.3.36 have problems with std::vector<lsst::daf::base::Citizen const *>,
// so replace Citizen::census() with a function that casts to something swig understands.
%extend lsst::daf::base::Citizen {
    static std::vector<lsst::daf::base::Citizen *> const * census() {
        return reinterpret_cast<std::vector<lsst::daf::base::Citizen *> const *>(
                lsst::daf::base::Citizen::census());
    }
    %ignore census();
}

// This has to come before PropertySet.h
%define VectorAddType(type, typeName)
    %template(Vector ## typeName) std::vector<type>;
%enddef

VectorAddType(bool, Bool)
VectorAddType(short, Short)
VectorAddType(int, Int)
VectorAddType(long long, Int64)
VectorAddType(float, Float)
VectorAddType(double, Double)
VectorAddType(std::string, String)
VectorAddType(lsst::daf::base::DateTime, DateTime)

%include "lsst/daf/base/Citizen.h"
%include "lsst/daf/base/DateTime.h"
%include "lsst/daf/base/Persistable.h"
%include "lsst/daf/base/PropertySet.h"

// This has to come after PropertySet.h
%define PropertySetAddType(type, typeName)
    %template(set ## typeName) lsst::daf::base::PropertySet::set<type>;
    %template(add ## typeName) lsst::daf::base::PropertySet::add<type>;
    %template(get ## typeName) lsst::daf::base::PropertySet::get<type>;
    %template(getArray ## typeName) lsst::daf::base::PropertySet::getArray<type>;
%enddef

PropertySetAddType(bool, Bool)
PropertySetAddType(short, Short)
PropertySetAddType(int, Int)
PropertySetAddType(long long, Int64)
PropertySetAddType(float, Float)
PropertySetAddType(double, Double)
PropertySetAddType(std::string, String)
PropertySetAddType(lsst::daf::base::DateTime, DateTime)
