'''Module specific to amd64-amd arch.'''


import psutil as _pu

try:
    import rocm_smi as rs
except ImportError:
    import sys
    sys.path.append('/opt/rocm/bin/')
    try:
        import rocm_smi as rs
    except ImportError:
        raise RuntimeError("Module 'rocm_smi.py' is required on a machine with an AMDGPU card. It should come with the rocm docker image by default. Please consult rocm to install it.")


def get_mem_info_impl():
    res = {}

    mem_info = _pu.virtual_memory()
    res['cpu_mem_free'] = mem_info.free
    res['cpu_mem_used'] = mem_info.used
    res['cpu_mem_total'] = mem_info.total
    res['cpu_mem_shared_with_gpu'] = False
    
    device_names = rs.listDevices(False)
    device_names = [x for x in device_names if rs.checkAmdGpus([x])]

    if device_names:
        gpus = []

        for device_name in device_names:
            gpu = {}
            
            gpu['name'] = device_name
            gpu['driver_version'] = rs.getVersion([device_name], 'driver')

            mem_info = rs.getMemInfo(device_name, 'vram')
            
            gpu['mem_used'] = int(mem_info[0])
            gpu['mem_total'] = int(mem_info[1])
            gpu['mem_free'] = gpu['mem_total'] - gpu['mem_used']

            gpus.append(gpu)

        res['gpus'] = gpus
    else:
        res['gpus'] = []
        
    
    return res
