"""Detects the machine architecture and reports CPU/GPU memory usage.

The functions of this package are hardware-dependent: their results depend on the machine
they run on, and some of them need extra packages (`psutil` everywhere, `pynvml` on machines with
Nvidia GPUs, `rocm_smi` on machines with AMD GPUs, and `tqdm` to print bars).

 - :func:`detect_machine` returns a short name identifying the architecture, e.g. 'amd64-cpu'.
 - :func:`get_mem_info` returns the memory usage of the CPU and of each GPU.
 - :func:`sort_gpu_devices` makes the CUDA GPUs with most free memory come first.
"""

from __future__ import absolute_import, division, print_function

from .version import version as __version__
from .arch import detect_machine


__all__ = ["detect_machine", "get_mem_info", "sort_gpu_devices"]


def get_mem_info(print_bars=False):
    """Returns a dictionary containing information about detected CPU/GPU devices and their memory
    usage, or None if the architecture is unknown.

    The architecture is detected with :func:`detect_machine`. The returned dictionary has the
    following keys. All memory sizes are in bytes.

    - 'cpu_mem_free', 'cpu_mem_used', 'cpu_mem_total' : system memory, as reported by
      :func:`psutil.virtual_memory`
    - 'cpu_mem_shared_with_gpu' : bool, True if the GPU uses the system memory (Jetson devices). It
      is absent on machines without a GPU and on Raspberry Pi and Rock boards.
    - 'gpus' : list of dictionaries, one per GPU (empty if there is none). Each has keys 'name',
      'mem_free', 'mem_used' and 'mem_total', and, depending on the architecture, 'driver_version',
      'bus' and 'fan_speed'.
    - 'model' : str, the board model. Only on Raspberry Pi and Rock boards.
    - 'l4t', 'jetpack' : lists of version strings. Only on Jetson devices whose Linux kernel is
      recognised. See :func:`mt.gpu.arch_tegra.detect_l4t_version_range`.

    Parameters
    ----------
    print_bars : bool, optional
        whether or not to print some :mod:`tqdm` bars showing the memory usage in MB of the CPU and,
        unless the memory is shared, of each GPU. Default is False.

    Returns
    -------
    dict or None
        the dictionary described above, or None if the architecture is 'unknown'

    Raises
    ------
    RuntimeError
        on an Nvidia (resp. AMD) machine, if `pynvml` (resp. `rocm_smi`) is not installed
    UnboundLocalError
        if the detected architecture is 'arm64-tk1', which is not handled

    See Also
    --------
    detect_machine : detects the architecture
    sort_gpu_devices : orders the GPU devices by free memory
    """
    arch = detect_machine()

    if arch == "amd64-cpu":
        from .arch_amd64_cpu import get_mem_info_impl

        res = get_mem_info_impl()
    elif arch == "amd64-nvidia":
        from .arch_amd64_nvidia import get_mem_info_impl

        res = get_mem_info_impl()
    elif arch == "amd64-amd":
        from .arch_amd64_amd import get_mem_info_impl

        res = get_mem_info_impl()
    elif arch in ["arm64-rp3", "arm64-rp4"]:
        from .arch_rpi import get_mem_info_impl

        res = get_mem_info_impl(arch)
    elif arch in ["arm64-r5b"]:
        from .arch_rock import get_mem_info_impl

        res = get_mem_info_impl(arch)
    elif arch in ["arm64-tx1", "arm64-tx2", "arm64-xnx", "arm64-orin"]:
        from .arch_tegra import get_mem_info_impl

        res = get_mem_info_impl(arch)
    elif arch == "unknown":
        res = None

    if print_bars and res:
        from tqdm.auto import tqdm

        MB = 1024 * 1024

        is_cgpu = res.get("cpu_mem_shared_with_gpu", False)

        cpu_desc = "cpu_gpu" if is_cgpu else "cpu"
        cpu_bar = tqdm(
            desc=cpu_desc,
            total=res["cpu_mem_total"] // MB,
            initial=res["cpu_mem_used"] // MB,
            unit="MB",
            bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt} {unit}",
        )
        cpu_bar.display()
        cpu_bar.close()

        if not is_cgpu:
            for i, gpu in enumerate(res["gpus"]):
                gpu_desc = f"gpu {i} ({gpu['name']})"
                gpu_bar = tqdm(
                    desc=gpu_desc,
                    total=gpu["mem_total"] // MB,
                    initial=gpu["mem_used"] // MB,
                    unit="MB",
                    bar_format="{l_bar}{bar}|{n_fmt}/{total_fmt} {unit}",
                )
                gpu_bar.display()
                gpu_bar.close()

    return res


def sort_gpu_devices():
    """Sorts the GPU devices in decreasing order of free memory. Only effective with CUDA
    hardware.

    On a machine with Nvidia GPUs, the function sets the environment variable `CUDA_VISIBLE_DEVICES`
    of the current process to the comma-separated list of GPU indices, from the one with the most
    free
    memory to the one with the least. It should be invoked before the CUDA runtime is initialised,
    so
    that the first visible device (device 0) is the freest one. It does nothing on other
    architectures or if there is no GPU.

    Returns
    -------
    None
        the function returns nothing
    """

    arch = detect_machine()
    if arch == "amd64-nvidia":
        from .arch_amd64_nvidia import sort_cuda_devices

        return sort_cuda_devices()
