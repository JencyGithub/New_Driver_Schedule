import os
import psutil
import speedtest
from screeninfo import get_monitors
import platform
import socket

def get_installed_software():
    try:
        import winreg as reg
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        software_list = []

        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
            for i in range(reg.QueryInfoKey(key)[0]):
                subkey_name = reg.EnumKey(key, i)
                with reg.OpenKey(key, subkey_name) as subkey:
                    try:
                        software_name = reg.QueryValueEx(subkey, "DisplayName")[0]
                        software_list.append(software_name)
                    except (FileNotFoundError, PermissionError):
                        pass

        return software_list
    except Exception as e:
        print(f"Error getting installed software: {e}")
        return []

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download()
    upload_speed = st.upload()
    return f"Download Speed: {download_speed / 1_000_000:.2f} Mbps, Upload Speed: {upload_speed / 1_000_000:.2f} Mbps"

def get_screen_resolution():
    monitors = get_monitors()
    resolutions = [(monitor.width, monitor.height) for monitor in monitors]
    return resolutions

def get_cpu_info():
    cpu_info = {}
    cpu_info["model"] = platform.processor()
    cpu_info["cores"] = psutil.cpu_count(logical=False)
    cpu_info["threads"] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    try:
        import wmi
        w = wmi.WMI()
        gpu_info = [gpu.Name for gpu in w.Win32_VideoController()]
        return gpu_info[0] if gpu_info else None
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None

def get_ram_size():
    ram = psutil.virtual_memory()
    ram_size_gb = ram.total / (1024 ** 3)
    return f"{ram_size_gb:.2f} GB"

def get_screen_size():
    # This example assumes a single monitor setup
    monitors = get_monitors()
    if monitors:
        monitor = monitors[0]
        diagonal_size = round((monitor.width ** 2 + monitor.height ** 2) ** 0.5 / 25.4, 2)
        return f"{diagonal_size} inch"
    else:
        return "Screen size information not available"

def get_mac_address(interface="Ethernet"):
    try:
        import uuid
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        return mac
    except Exception as e:
        print(f"Error getting MAC address: {e}")
        return None

def get_public_ip():
    try:
        public_ip = socket.gethostbyname(socket.gethostname())
        return public_ip
    except Exception as e:
        print(f"Error getting public IP address: {e}")
        return None

def get_windows_version():
    return platform.version()

if __name__ == "__main__":
    print("Installed Software:")
    for software in get_installed_software():
        print(f"  - {software}")

    print("\nInternet Speed:")
    try:
        print(get_internet_speed())
    except Exception as e:
        print(e)

    print("\nScreen Resolution:")
    for resolution in get_screen_resolution():
        print(f"  - {resolution[0]}x{resolution[1]} pixels")

    print("\nCPU Information:")
    cpu_info = get_cpu_info()
    print(f"  - Model: {cpu_info['model']}")
    print(f"  - Cores: {cpu_info['cores']}")
    print(f"  - Threads: {cpu_info['threads']}")

    print("\nGPU Information:")
    gpu_info = get_gpu_info()
    if gpu_info:
        print(f"  - Model: {gpu_info}")
    else:
        print("  - No GPU information available")

    print("\nRAM Size:")
    print(f"  - {get_ram_size()}")

    print("\nScreen Size:")
    print(f"  - {get_screen_size()}")

    print("\nMAC Address (Ethernet):")
    print(f"  - {get_mac_address()}")

    print("\nPublic IP Address:")
    print(f"  - {get_public_ip()}")

    print("\nWindows Version:")
    print(f"  - {get_windows_version()}")
