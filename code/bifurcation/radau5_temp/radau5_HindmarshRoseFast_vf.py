# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.8
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info
if version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_radau5_HindmarshRoseFast_vf', [dirname(__file__)])
        except ImportError:
            import _radau5_HindmarshRoseFast_vf
            return _radau5_HindmarshRoseFast_vf
        if fp is not None:
            try:
                _mod = imp.load_module('_radau5_HindmarshRoseFast_vf', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _radau5_HindmarshRoseFast_vf = swig_import_helper()
    del swig_import_helper
else:
    import _radau5_HindmarshRoseFast_vf
del version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.


def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr_nondynamic(self, class_type, name, static=1):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    if (not static):
        return object.__getattr__(self, name)
    else:
        raise AttributeError(name)

def _swig_getattr(self, class_type, name):
    return _swig_getattr_nondynamic(self, class_type, name, 0)


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object:
        pass
    _newclass = 0



def new_doubleArray(nelements):
    return _radau5_HindmarshRoseFast_vf.new_doubleArray(nelements)
new_doubleArray = _radau5_HindmarshRoseFast_vf.new_doubleArray

def delete_doubleArray(ary):
    return _radau5_HindmarshRoseFast_vf.delete_doubleArray(ary)
delete_doubleArray = _radau5_HindmarshRoseFast_vf.delete_doubleArray

def doubleArray_getitem(ary, index):
    return _radau5_HindmarshRoseFast_vf.doubleArray_getitem(ary, index)
doubleArray_getitem = _radau5_HindmarshRoseFast_vf.doubleArray_getitem

def doubleArray_setitem(ary, index, value):
    return _radau5_HindmarshRoseFast_vf.doubleArray_setitem(ary, index, value)
doubleArray_setitem = _radau5_HindmarshRoseFast_vf.doubleArray_setitem

def new_intArray(nelements):
    return _radau5_HindmarshRoseFast_vf.new_intArray(nelements)
new_intArray = _radau5_HindmarshRoseFast_vf.new_intArray

def delete_intArray(ary):
    return _radau5_HindmarshRoseFast_vf.delete_intArray(ary)
delete_intArray = _radau5_HindmarshRoseFast_vf.delete_intArray

def intArray_getitem(ary, index):
    return _radau5_HindmarshRoseFast_vf.intArray_getitem(ary, index)
intArray_getitem = _radau5_HindmarshRoseFast_vf.intArray_getitem

def intArray_setitem(ary, index, value):
    return _radau5_HindmarshRoseFast_vf.intArray_setitem(ary, index, value)
intArray_setitem = _radau5_HindmarshRoseFast_vf.intArray_setitem

def Integrate(ic, t, hinit, hmax, safety, jacRecompute, newtonStop, stepChangeLB, stepChangeUB, stepSizeLB, stepSizeUB, hessenberg, maxNewton, newtonStart, index1dim, index2dim, index3dim, stepSizeStrategy, DAEstructureM1, DAEstructureM2, useJac, useMass, verbose, calcAux, calcSpecTimes):
    return _radau5_HindmarshRoseFast_vf.Integrate(ic, t, hinit, hmax, safety, jacRecompute, newtonStop, stepChangeLB, stepChangeUB, stepSizeLB, stepSizeUB, hessenberg, maxNewton, newtonStart, index1dim, index2dim, index3dim, stepSizeStrategy, DAEstructureM1, DAEstructureM2, useJac, useMass, verbose, calcAux, calcSpecTimes)
Integrate = _radau5_HindmarshRoseFast_vf.Integrate

def InitBasic(PhaseDim, ParamDim, nAux, nEvents, nExtInputs, HasJac, HasJacP, HasMass, extraSize):
    return _radau5_HindmarshRoseFast_vf.InitBasic(PhaseDim, ParamDim, nAux, nEvents, nExtInputs, HasJac, HasJacP, HasMass, extraSize)
InitBasic = _radau5_HindmarshRoseFast_vf.InitBasic

def CleanUp():
    return _radau5_HindmarshRoseFast_vf.CleanUp()
CleanUp = _radau5_HindmarshRoseFast_vf.CleanUp

def InitInteg(Maxpts, atol, rtol):
    return _radau5_HindmarshRoseFast_vf.InitInteg(Maxpts, atol, rtol)
InitInteg = _radau5_HindmarshRoseFast_vf.InitInteg

def ClearInteg():
    return _radau5_HindmarshRoseFast_vf.ClearInteg()
ClearInteg = _radau5_HindmarshRoseFast_vf.ClearInteg

def InitEvents(Maxevtpts, EventActive, EventDir, EventTerm, EventInterval, EventDelay, EventTol, Maxbisect, EventNearCoef):
    return _radau5_HindmarshRoseFast_vf.InitEvents(Maxevtpts, EventActive, EventDir, EventTerm, EventInterval, EventDelay, EventTol, Maxbisect, EventNearCoef)
InitEvents = _radau5_HindmarshRoseFast_vf.InitEvents

def ClearEvents():
    return _radau5_HindmarshRoseFast_vf.ClearEvents()
ClearEvents = _radau5_HindmarshRoseFast_vf.ClearEvents

def InitExtInputs(nExtInputs, extInputLens, extInputVals, extInputTimes):
    return _radau5_HindmarshRoseFast_vf.InitExtInputs(nExtInputs, extInputLens, extInputVals, extInputTimes)
InitExtInputs = _radau5_HindmarshRoseFast_vf.InitExtInputs

def ClearExtInputs():
    return _radau5_HindmarshRoseFast_vf.ClearExtInputs()
ClearExtInputs = _radau5_HindmarshRoseFast_vf.ClearExtInputs

def SetRunParameters(ic, pars, gt0, t0, tend, refine, specTimeLen, specTimes, upperBounds, lowerBounds):
    return _radau5_HindmarshRoseFast_vf.SetRunParameters(ic, pars, gt0, t0, tend, refine, specTimeLen, specTimes, upperBounds, lowerBounds)
SetRunParameters = _radau5_HindmarshRoseFast_vf.SetRunParameters

def ClearParams():
    return _radau5_HindmarshRoseFast_vf.ClearParams()
ClearParams = _radau5_HindmarshRoseFast_vf.ClearParams

def Reset():
    return _radau5_HindmarshRoseFast_vf.Reset()
Reset = _radau5_HindmarshRoseFast_vf.Reset

def SetContParameters(tend, pars, upperBounds, lowerBounds):
    return _radau5_HindmarshRoseFast_vf.SetContParameters(tend, pars, upperBounds, lowerBounds)
SetContParameters = _radau5_HindmarshRoseFast_vf.SetContParameters

def Vfield(t, x, p):
    return _radau5_HindmarshRoseFast_vf.Vfield(t, x, p)
Vfield = _radau5_HindmarshRoseFast_vf.Vfield

def Jacobian(t, x, p):
    return _radau5_HindmarshRoseFast_vf.Jacobian(t, x, p)
Jacobian = _radau5_HindmarshRoseFast_vf.Jacobian

def JacobianP(t, x, p):
    return _radau5_HindmarshRoseFast_vf.JacobianP(t, x, p)
JacobianP = _radau5_HindmarshRoseFast_vf.JacobianP

def AuxFunc(t, x, p):
    return _radau5_HindmarshRoseFast_vf.AuxFunc(t, x, p)
AuxFunc = _radau5_HindmarshRoseFast_vf.AuxFunc

def MassMatrix(t, x, p):
    return _radau5_HindmarshRoseFast_vf.MassMatrix(t, x, p)
MassMatrix = _radau5_HindmarshRoseFast_vf.MassMatrix
# This file is compatible with both classic and new-style classes.


