from rpython.translator.tool.cbuild import ExternalCompilationInfo
from rpython.rtyper.lltypesystem import lltype, llmemory, rffi

import py
import os

cdir = os.path.dirname(os.path.realpath(__file__))
translator_c_dir = py.path.local(cdir)

eci = ExternalCompilationInfo(
    include_dirs = [translator_c_dir / "atomicprimitives" ],
    post_include_bits=['''
#include "atomic.h"
#define cas(ptr, old, _new) compare_and_swap((volatile unsigned long*)(ptr), (unsigned long)(old), (unsigned long)(_new))
#define faa(ptr, value) fetch_and_add((volatile unsigned long*)(ptr), (unsigned long)(value))
''']
)

def llexternal(name, args, result, **kwds):
    return  rffi.llexternal(name, args, result, compilation_info=eci, **kwds)


compare_and_swap = llexternal('cas', [rffi.SIGNEDP, lltype.Signed, lltype.Signed], lltype.Signed, macro=True)
fetch_and_add = llexternal('faa', [llmemory.Address, lltype.Signed], lltype.Signed, macro=True)
