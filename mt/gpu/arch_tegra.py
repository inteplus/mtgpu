"""Module specific to Nvidia Tegra/Jetson arch.

Besides memory information, it knows how to map the Linux kernel version to the L4T (Linux for
Tegra) release and the corresponding JetPack version. The dictionaries are `arch2gpu`, mapping
an architecture name to the GPU name, and `version_l4t_to_jetpack`, mapping an L4T version to a
JetPack version.
"""


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
    "36.3.0": "6.0",
}


def detect_l4t_version_range():
    """Detects the range of L4T versions from the Linux kernel version.

    Returns
    -------
    list or str
        a list of one or two L4T version strings `[first, last]` (a range of versions sharing the
        same kernel), or the string 'unknown' if the kernel version is not recognised. The strings
        are keys of `version_l4t_to_jetpack`.
    """
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
    if kernel_version.startswith("5.15.136-tegra"):
        return ["36.3.0"]
    return "unknown"


def get_mem_info_impl(arch):
    """Gets memory information of a Jetson device. See :func:`mt.gpu.get_mem_info`.

    The GPU shares the system memory with the CPU, so the GPU memory figures are the same as the CPU
    ones.

    Parameters
    ----------
    arch : str
        the architecture name, one of 'arm64-tk1', 'arm64-tx1', 'arm64-tx2', 'arm64-xnx' and
        'arm64-orin'. For 'arm64-orin', the GPU name is read from the device tree.

    Returns
    -------
    dict
        a dictionary with keys 'cpu_mem_free', 'cpu_mem_used', 'cpu_mem_total' (bytes),
        'cpu_mem_shared_with_gpu' (always True), 'gpus' (a list of one GPU dictionary with keys
        'name', 'mem_free', 'mem_used' and 'mem_total'), 'l4t' (see
        :func:`detect_l4t_version_range`)
        and, if the L4T version is recognised, 'jetpack' (list of the corresponding JetPack
        versions)
    """
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
