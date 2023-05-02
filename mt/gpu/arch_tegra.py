"""Module specific to Nvidia Tegra/Jetson arch."""


from platform import uname
import psutil as _pu


arch2gpu = {
    "arm64-tk1": "NVIDIA Jetson TK1",
    "arm64-tx1": "NVIDIA Jetson TX1",
    "arm64-tx2": "NVIDIA Jetson TX2",
    "arm64-xnx": "NVIDIA Jetson Xavier-NX",
}


version_l4t_to_jetpack = {
    "28.2.1": "3.3",
    "28.3": "3.3",
    "28.3.1": "3.3.1",
    "28.3.2": "3.3.2",
    "28.4": "3.3.3",
    "31.0.1": "4.0",
    "31.1": "4.1.1",
    "32.1": "4.2",
    "32.2": "4.2.1",
    "32.2.1": "4.2.2",
    "32.2.3": "4.2.3",
    "32.3.1": "4.3",
    "32.4.2": "4.4",
    "32.4.3": "4.4",
    "32.4.4": "4.4.1",
    "32.5": "4.5",
    "32.5.1": "4.5.1",
    "32.6.1": "4.6",
    "34.0.1": "5.0",
    "35.1": "5.0.2",
    "35.3.1": "5.1.1",
}


def detect_l4t_version_range():
    kernel_version = uname().release
    if kernel_version.startswith("4.4.38"):
        return ["28.2.1", "28.2.1"]
    if kernel_version.startswith("4.4.159"):
        return ["28.3", "28.3.2"]
    if kernel_version.startswith("4.4.197"):
        return ["28.4", "28.4"]
    if kernel_version.startswith("4.9.108"):
        return ["31.0.1", "31.1"]
    if kernel_version.startswith("4.9.140"):
        return ["32.1", "32.4.4"]
    if kernel_version.startswith("4.9.201"):
        return ["32.5", "32.5.1"]
    if kernel_version.startswith("4.9.253-tegra"):
        return ["32.6.1"]
    if kernel_version.startswith("5.10.65-tegra"):
        return ["34.0.1"]
    if kernel_version.startswith("5.10.104-tegra"):
        return ["35.1", "35.3.1"]
    return "unknown"


def get_mem_info_impl(arch):
    res = {}

    mem_info = _pu.virtual_memory()
    res["cpu_mem_free"] = mem_info.free
    res["cpu_mem_used"] = mem_info.used
    res["cpu_mem_total"] = mem_info.total
    res["cpu_mem_shared_with_gpu"] = True

    gpu = {}
    gpu["mem_free"] = res["cpu_mem_free"]
    gpu["mem_used"] = res["cpu_mem_used"]
    gpu["mem_total"] = res["cpu_mem_total"]
    if arch == "arm64-orin":
        name = open("/sys/firmware/devicetree/base/model", "rt").read()
        name = name.strip(chr(0))
    else:
        name = arch2gpu.get(arch, "Unknown")
    gpu["name"] = name
    res["gpus"] = [gpu]

    l4t_version = detect_l4t_version_range()
    res["l4t"] = l4t_version
    if l4t_version != "unknown":
        jetpack_version = [version_l4t_to_jetpack[x] for x in l4t_version]
        res["jetpack"] = jetpack_version

    return res
