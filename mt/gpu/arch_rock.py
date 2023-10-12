"""Module specific to arm64-r5b arch."""

import psutil as _pu
import subprocess as _sp


def get_mem_info_impl(arch):
    mem_info = _pu.virtual_memory()

    res = {
        "gpus": [],
        "cpu_mem_free": mem_info.free,
        "cpu_mem_used": mem_info.used,
        "cpu_mem_total": mem_info.total,
    }

    r5b_model_filepath = "/sys/firmware/devicetree/base/model"
    r5b_model = (
        _sp.check_output(["cat", r5b_model_filepath]).decode().strip().strip("\0")
    )
    res["model"] = r5b_model

    return res
