import os
import subprocess
import sys
import multiprocessing as mp
from zipfile import ZipFile
import platform
from typing import *
import shutil


def importer(package: str):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", f'{package}'])
    finally:
        globals()[package] = importlib.import_module(package)


def install(package: list[str], operating_system: str):
    for i in package:
        pass


def unzip(file: str):
    zf = ZipFile(file, 'r')
    zf.extractall()
    zf.close()


def download(data: tuple[str, str]):
    url, file_name = data
    response = requests.get(url)
    open(file_name, "wb").write(response.content)


def mp_download(data: tuple[str, str]):
    import requests
    url, file_name = data
    response = requests.get(url)
    open(file_name, "wb").write(response.content)


def mp_downloader(main_url: str, year: str, operating_system: str, downloads: Union[list, tuple]):
    download_list = []
    cpu_arch = get_cpu_arch()

    for i in downloads:
        if operating_system != "macos" or i != "wpi":
            d = f"{main_url}/{year}/{operating_system}/{i}.zip"
        else:
            d = f"{main_url}/{year}/{operating_system}/{cpu_arch}/{i}.zip"
        n = f"{i}.zip"
        download_list.append((d, n))

    p = mp.Pool(len(downloads))
    p.map(mp_download, download_list)
    p.close()
    p.join()


def cd(directory: str):
    os.chdir(directory)


def mkdir(directory: str):
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass


def rmdir(directory: str):
    shutil.rmtree(directory)


def pwd():
    return os.getcwd()


def install(package: str):
    os.system(f"./{package}")


def get_normalized_input(message: str) -> str:
    return input(f"{message} (y/n): ").lower()


def init(operating_system: str):
    available_packages = ["wpi", "navx", "ctre", "rev"]
    output = []
    do_all = False
    if get_normalized_input("do you want to install all available packages?") != "n":
        do_all = True
        output = available_packages
    else:
        if get_normalized_input("do you want to install wpilib?") != "n":
            output.append("wpi")
        if get_normalized_input("do you want to install navx?") != "n":
            output.append("navx")
        if get_normalized_input("do you want to install rev?") != "n":
            output.append("rev")
        if get_normalized_input("do you want to install ctre?") != "n":
            output.append("wpi")
        if operating_system == 'windows':
            if do_all:
                output.append("ds")
                output.append("revhc")
            elif get_normalized_input("do you want to install the driver station?") != "n":
                output.append("ds")

    return output


def get_os():

    if "windows" in str(platform.system()).lower():
        operating_system = "windows"
    elif "linux" in str(platform.system()).lower():
        operating_system = "linux"
    elif "darwin" in str(platform.system()).lower():
        operating_system = "macos"
    else:
        operating_system = None
        exiter(3)
    return operating_system


def get_cpu_arch():
    if get_os() == "macos" and "arm" in platform.uname():
        return "arm"
    else:
        return "x86"


def get_year(address: str):
    download((f"{address}/year.txt", "year.txt"))
    try:
        year_file = open("year.txt", "r")
        year = year_file.readline()
        if "<!DOCTYPE html" in year:
            year = 0
        year_file.close()
    except FileNotFoundError:
        print("There was a problem, Please try again")
        year = 0
        exiter(3)
    return year


def exiter(code: int):
    cd(home_dir)
    if get_normalized_input("do you want to remove temporary data?") != "n":
        rmdir("tmp")
    exit(code)


def main():
    importer('requests')
    main_address = "https://www.rylanswebdav.cf/publicdocuments/files/frc"

    mkdir('tmp')
    cd('tmp')

    operating_system = get_os()
    year = get_year(main_address)
    packages = init(operating_system)

    download_queue = list(packages)

    print("Downloading Packages")
    mp_downloader(main_address, year, operating_system, download_queue)
    print("Download Finished")
    exiter(0)


if __name__ == '__main__':
    home_dir = pwd()
    main()
