"""
Print some useful information about the platform and environment we are running under.
"""
import math
import multiprocessing
import os
import platform
import subprocess
import sys


def print_compute_info():
    print('==================================')
    print('Compute info')
    print('==================================')
    print('CPU cores available: {}'.format(multiprocessing.cpu_count()))


def print_memory_info():
    print('==================================')
    print('Memory info')
    print('==================================')
    try:
        import psutil
    except ImportError as e:
        print('Module psutil is not available. Skipping memory info.')
        return
    vm = psutil.virtual_memory()
    for k, v in vm._asdict().items():
        if k == 'percent':
            value = '{}%'.format(round(v, 2))
        else:
            value = convert_bytes_to_pretty_string(v)
        print('\t{key: <20}: {value}'.format(key=k, value=value))


def convert_bytes_to_pretty_string(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def print_environment_variables():
    print('==================================')
    print('Modules available')
    print('==================================')
    for name, value in sorted(os.environ.items()):
        print('{name: <36}{value}'.format(name=name, value=value))


def print_modules_available():
    print('==================================')
    print('Modules available')
    print('==================================')
    print(help('modules'))


def print_module_version_info():
    print('==================================')
    print('Module version info')
    print('==================================')
    package_info_list = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').split()
    for package_info in package_info_list:
        package_name, package_version = package_info.split('==')
        print('{package_name: <40}{package_version}'.format(package_name=package_name, package_version=package_version))


def print_platform_info():
    print('==================================')
    print('Platform info')
    print('==================================')
    print('Python {}'.format(platform.python_version()))
    for k, v in platform.uname()._asdict().items():
        print('{key: <16}{value}'.format(key=k, value=v))

def print_working_dir():
    print('==================================')
    print('Work directory contents')
    print('==================================')
    print(os.listdir(os.getcwd()))

def main():
    print_platform_info()
    print_module_version_info()
    print_modules_available()
    print_environment_variables()
    print_compute_info()
    print_memory_info()
    print_working_dir()


if __name__ == '__main__':
    main()
