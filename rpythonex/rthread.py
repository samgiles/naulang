from rpython.translator.tool.cbuild import ExternalCompilationInfo
from rpython.rtyper.lltypesystem import rffi, lltype
from rpython.rtyper.tool import rffi_platform

eci = ExternalCompilationInfo(
    includes=["errno.h"],
    post_include_bits=['''
#include <pthread.h>
#define rpy_thread_join(thread_id, result) pthread_join((pthread_t)thread_id, (void*)&result)
'''],
    libraries=["pthread"]
)


def llexternal(name, args, result, **kwargs):
    return rffi.llexternal(name, args, result, compilation_info=eci, **kwargs)

c_thread_join = llexternal("rpy_thread_join", [rffi.LONG, rffi.SIGNEDP], rffi.SIGNED, macro=True)


class CConfig:
    _compilation_info_ = eci
    EDEADLK = rffi_platform.ConstantInteger("EDEADLK")
    EINVAL = rffi_platform.ConstantInteger("EINVAL")
    ESRCH = rffi_platform.ConstantInteger("ESRCH")

for k, v in rffi_platform.configure(CConfig).items():
    globals()[k] = v


def thread_join(thread_id):
    result = lltype.malloc(rffi.SIGNEDP.TO, 1, flavor="raw")
    error_code = c_thread_join(thread_id, result)
    if error_code is not 0:
        if error_code is EDEADLK:
            raise Exception("error thread join: deadlock (%d)" % error_code)
        elif error_code is EINVAL:
            raise Exception("error thread join: invalid thread (%d)" % error_code)
        elif error_code is ESRCH:
            print "join failed"
        else:
            raise Exception(
                "Error thread join: unknown. Expected one of (EINVAL: %d; EDEADLK: %d; ESRCH: %d) was %d" %
                (EINVAL, EDEADLK, ESRCH, error_code))

    return result[0]
