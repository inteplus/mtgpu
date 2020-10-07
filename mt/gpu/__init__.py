from __future__ import absolute_import, division, print_function

from .arch import detect_machine


__all__ = ['detect_machine', 'get_mem_info']


def get_mem_info():
    '''Returns a dictionary containing information about detected CPU/GPU devices and their memory usage, or None if the architecture is unknown.'''
    arch = detect_machine()

    if arch == 'amd64-cpu':
        from .arch_amd64_cpu import get_mem_info_impl
        return get_mem_info_impl()

    if arch == 'amd64-nvidia':
        from .arch_amd64_nvidia import get_mem_info_impl
        return get_mem_info_impl()
    
    if arch == 'amd64-amd':
        from .arch_amd64_amd import get_mem_info_impl
        return get_mem_info_impl()
    
    if arch in ['arm64-tx1', 'arm64-tx2', 'arm64-j43']:
        from .arch_tegra import get_mem_info_impl
        return get_mem_info_impl()
    
    if arch == 'unknown':
        return None

    return None
