'''Module specific to amd64-cpu arch.'''

import psutil as _pu


def get_mem_info_impl():
    '''Gets CPU memory information of a machine without GPU. See :func:`mt.gpu.get_mem_info`.

    Returns
    -------
    dict
        a dictionary with keys 'gpus' (always an empty list) and 'cpu_mem_free', 'cpu_mem_used',
        'cpu_mem_total' (bytes)
    '''
    mem_info = _pu.virtual_memory()
    return {
        'gpus': [],
        'cpu_mem_free': mem_info.free,
        'cpu_mem_used': mem_info.used,
        'cpu_mem_total': mem_info.total,
    }
