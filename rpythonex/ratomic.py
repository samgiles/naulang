from rpython.translator.tool.cbuild import ExternalCompilationInfo
from rpython.rtyper.lltypesystem import lltype, llmemory, rffi

import py
import os

cdir = os.path.dirname(os.path.realpath(__file__))
translator_c_dir = py.path.local(cdir)

eci = ExternalCompilationInfo(
    include_dirs = [translator_c_dir],
    post_include_bits = ['''
#include "atomic.h"
#define pypy_cas(ptr, old, _new) compare_and_swap((volatile unsigned long*)(ptr), (unsigned long)(old), (unsigned long)(_new))
#define pypy_faa(ptr, value) fetch_and_add((volatile unsigned long*)(ptr), (unsigned long)(value))
    '''],
    export_symbols = ["pypy_cas", "pypy_faa"]
)

def llexternal(name, args, result, **kwds):
    kwds.setdefault('sandboxsafe', True)
    return  rffi.llexternal(name, args, result, compilation_info=eci, **kwds)


compare_and_swap = llexternal('pypy_cas', [llmemory.Address] * 3, lltype.Bool, macro=True, _nowrapper=True)
fetch_and_add = llexternal('pypy_faa', [llmemory.Address, lltype.Signed], lltype.Signed, macro=True, _nowrapper=True)
