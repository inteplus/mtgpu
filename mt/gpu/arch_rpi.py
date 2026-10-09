"""Module specific to arm64-rpi arch."""

import psutil as _pu
import subprocess as _sp


def get_mem_info_impl(arch):
    """Gets CPU memory information of a Raspberry Pi. See :func:`mt.gpu.get_mem_info`.

    Parameters
    ----------
    arch : str
        the architecture name, not used

    Returns
    -------
    dict
        a dictionary with keys 'gpus' (always an empty list), 'cpu_mem_free', 'cpu_mem_used',
        'cpu_mem_total' (bytes) and 'model' (the board model read from the device tree)
    """
    mem_info = _pu.virtual_memory()

    res = {
        "gpus": [],
        "cpu_mem_free": mem_info.free,
        "cpu_mem_used": mem_info.used,
        "cpu_mem_total": mem_info.total,
    }

    rpi_model_filepath = "/sys/firmware/devicetree/base/model"
    rpi_model = _sp.check_output(["cat", rpi_model_filepath]).decode().strip()
    res["model"] = rpi_model

    return res
