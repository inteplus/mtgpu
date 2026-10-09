'''Module specific to amd64-amd arch.

It requires the module `rocm_smi`, which comes with ROCm, to be importable (or to be found
in `/opt/rocm/bin/`), otherwise importing this module raises :class:`RuntimeError`.
'''


import subprocess as _sp
import psutil as _pu

try:
    import rocm_smi as rs
except ImportError:
    import sys
    sys.path.append('/opt/rocm/bin/')
    try:
        import rocm_smi as rs
    except ImportError:
        raise RuntimeError(
            "Module 'rocm_smi.py' is required on a machine with an AMDGPU card. "
            "It should come with the rocm docker image by default. "
            "Please consult rocm to install it."
        )

if hasattr(rs, 'initializeRsmi'):
    rs.initializeRsmi()

def get_mem_info_impl():
    '''Gets CPU and AMD GPU memory information. See :func:`mt.gpu.get_mem_info`.

    Returns
    -------
    dict
        a dictionary with keys 'cpu_mem_free', 'cpu_mem_used', 'cpu_mem_total' (bytes),
        'cpu_mem_shared_with_gpu' (always False) and 'gpus'. Each GPU dictionary has keys 'bus',
        'name', 'fan_speed', 'mem_free', 'mem_used' and 'mem_total' (bytes), and 'driver_version'
        if known.
    '''
    res = {}

    mem_info = _pu.virtual_memory()
    res['cpu_mem_free'] = mem_info.free
    res['cpu_mem_used'] = mem_info.used
    res['cpu_mem_total'] = mem_info.total
    res['cpu_mem_shared_with_gpu'] = False

    try:
        device_names = rs.listDevices(False)
    except TypeError:
        device_names = rs.listDevices() # 1.4.1 or later
    device_names = [x for x in device_names if rs.checkAmdGpus([x])]

    if device_names:
        gpus = []

        for device_name in device_names:
            gpu = {}
            
            gpu['bus'] = rs.getBus(device_name)
            z = rs.getVersion([device_name], 'driver')
            if z is not None:
                gpu['driver_version'] = z

            bus = gpu['bus']
            if bus.startswith("0000:"):
                bus = bus[5:]
            lspci = _sp.check_output(['lspci', '-s', bus]).decode().strip()
            gpu['name'] = lspci[lspci.find(' ')+1:]

            gpu['fan_speed'] = rs.getFanSpeed(device_name)

            mem_info = rs.getMemInfo(device_name, 'vram')
            
            gpu['mem_used'] = int(mem_info[0])
            gpu['mem_total'] = int(mem_info[1])
            gpu['mem_free'] = gpu['mem_total'] - gpu['mem_used']

            gpus.append(gpu)

        res['gpus'] = gpus
    else:
        res['gpus'] = []
        
    
    return res
