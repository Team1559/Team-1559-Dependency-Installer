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


def install(package: list[str], operating_system: str, year: str):
    for i in package:
        mkdir(i)
        cd(i)
        unzip(f"{i}.zip")
        if i == "wpi":

            if operating_system == "windows":
                run("WPILibInstaller.exe", operating_system)

            elif operating_system == "macos":
                run("WPILibInstaller.dmg", operating_system)

        elif i == "navx":
            if operating_system == "windows":
                cd("navx")
                run("NavXInstaller.exe", operating_system)
                cd("..")
            else:
                navx_installer(year)
        elif i == "rev":
            if operating_system == "windows":
                rev_windows_installer(year)
            else:
                rev_other_installer(year)
        elif i == "revhc":
            run("rev.exe", operating_system)

        cd("..")

def cp(source: str, destination: str):
    shutil.copy(source, destination)


def cpdir(source: str, destination: str):
    shutil.copytree(source, destination)


def rev_windows_installer(year):
    rm(f"C:\\Users\\Public\\wpilib\\{year}\\maven\\com\\revrobotics")
    mkdir(f"C:\\Users\\Public\\wpilib\\{year}\\maven\\com\\revrobotics")
    mkdir(f"C:\\Users\\Public\\wpilib\\{year}\\maven\\com\\revrobotics\\frc\\")
    cpdir("rev\\maven\\com\\revrobotics\\frc", f"C:\\Users\\Public\\wpilib\\"
                                                         f"{year}\\maven\\com\\revrobotics\\frc\\")
    rm(f"C:\\Users\\Public\\wpilib\\2021\\vendordeps\\REVLib.json")
    cp("rev\\vendordeps\\REVLib.json", f"C:\\Users\\Public\\wpilib\\{year}\\vendordeps\\REVLib.json")


def rev_other_installer(year):
    print("still in progress")


def unzip(file: str):
    zf = ZipFile(file, 'r')
    zf.extractall()
    zf.close()


def download(url: str, file_name: str = None):
    if file_name is None:
        file_name = url.split('/')[-1]
    response = requests.get(url)
    open(file_name, "wb").write(response.content)


def mp_download(data: tuple[str, str]):
    import requests
    url, file_name = data
    response = requests.get(url)
    open(file_name, "wb").write(response.content)


def mp_downloader(downloads: Union[list, tuple], main_url: str = None, year: str = None, operating_system: str = None):
    download_list = []
    cpu_arch = get_cpu_arch()

    for i in downloads:
        if main_url is None or year is None or operating_system is None:
            d = i
            n = i.split('/')[-1]
        else:
            if operating_system != "macos" or i != "wpi":
                d = f"{main_url}/{year}/{operating_system}/{i}.zip"
            else:
                d = f"{main_url}/{year}/{operating_system}/{cpu_arch}/{i}.zip"
            n = f"{i}.zip"
        download_list.append((d, n))
    if len(downloads) < 1:
        return
    p = mp.Pool(len(downloads))
    p.map(mp_download, download_list)
    p.close()
    p.join()


def cd(directory: str):
    operating_system = get_os()
    if operating_system == "windows":
        directory = directory.replace("/", "\\")
    else:
        directory = directory.replace("\\", "/")

    try:
        os.chdir(directory)
    except FileNotFoundError as e:
        print(e)
        exiter(2)


def mkdir(directory: str):
    directory = directory.replace("\\", "/")
    directory = directory.split("/")

    for i in directory:
        try:
            os.mkdir(i)
        except FileExistsError:
            pass
        if len(directory) > 1:
            cd(i)
    for i in range(len(directory)):
        if len(directory) > 1:
            cd("..")


def rmdir(directory: str):
    try:
        shutil.rmtree(directory)
    except FileNotFoundError:
        pass


def rm(file: str):
    try:
        os.remove(file)
    except FileNotFoundError:
        pass


def pwd():
    return os.getcwd()


def run(package: str, operating_system: str):
    if operating_system == "windows":
        os.system(f".\\{package}")
    else:
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
    download(f"{address}/year.txt")
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


def navx_installer(year: str):
    mkdir("navx-mxp")
    cd("navx-mxp")

    # unzip("navx-mxp-libs.zip")

    # Get the vendor file
    mkdir("frc2019/vendordeps")
    cd("frc2019/vendordeps")
    rm("navx_frc.json")

    def get_version(years):
        download(f"https://www.kauailabs.com/dist/frc/{years}/navx_frc.json")
        with open("navx_frc.json", "r") as f:
            for i in f.readlines():
                if "version" in i:
                    try:
                        versions = i.split(":")[1].strip().replace('"', '').replace(",", "")
                    except RecursionError:
                        pass
                    except IndexError:
                        pass
                    f.close()
                    break
                versions = None

        if versions is None:
            try:
                versions = get_version(str(int(years) - 1))
            except:
                return None
        return versions

    version = get_version(year)
    if version is None:
        print("There was a problem with the navx package, Skipping")
        cd(f"{home_dir}/ltd")
        with open("log.txt", "w") as f:
            f.write("navx")
            f.close()
            cd(f"{home_dir}/tmp")
        return

    # Install the C++ libraries
    directory = pwd()
    cd(f"{home_dir}/ltd")
    try:
        with open("navx-version-old.txt", "r") as f:
            old_version = f.readline()
            f.close()
    except FileNotFoundError:
        old_version = ""
    with open("navx-version-old.txt", "w") as f:
        f.write(version)
        f.close()
    cd(directory)
    cd(f"{home_dir}/tmp/")
    mkdir("frc2019/maven/com")
    cd(f"{home_dir}/tmp/frc2019/maven/com")
    mkdir("kauailabs/navx/frc/navx-cpp")
    cd("kauailabs/navx/frc/navx-cpp")
    rm("maven-metadata.xml")
    download(f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/maven-metadata.xml")
    rmdir(old_version)
    mkdir(version)
    cd(version)
    cds = [f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/navx-cpp-{version}-headers.zip",
           f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/"
           f"navx-cpp-{version}-linuxathena.zip",
           f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/"
           f"navx-cpp-{version}-linuxathenadebug.zip", f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx"
                                                       f"-cpp/{version}/"
                                                       f"navx-cpp-{version}-linuxathenastatic.zip",
           f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/"
           f"navx-cpp-{version}-linuxathenastaticdebug.zip",
           f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/navx-cpp-{version}-sources.zip",
           f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-cpp/{version}/navx-cpp-{version}.pom"]
    mp_downloader(cds)

    # # Install the Java libraries
    cd(f"{home_dir}/tmp/frc2019/maven/com")
    mkdir("kauailabs/navx/frc/navx-java")
    cd("kauailabs/navx/frc/navx-java")
    rm("maven-metadata.xml")
    download(f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-java/maven-metadata.xml")
    rmdir(old_version)
    mkdir(version)
    cd(version)
    dl = [f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-java/{version}/"
          f"navx-java-{version}-javadoc.jar",
          f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-java/{version}/"
          f"navx-java-{version}-sources.jar", f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-java/"
                                              f"{version}/navx-java-{version}.jar",
          f"https://repo1.maven.org/maven2/com/kauailabs/navx/frc/navx-java/{version}/navx-java-{version}.pom"]
    mp_downloader(dl)
    cd(f"{home_dir}/tmp")


def main():
    operating_system = get_os()
    if operating_system == "linux":
        exit(2)
    importer('requests')
    main_address = "https://www.rylanswebdav.cf/publicdocuments/files/frc"
    mkdir("ltd")
    mkdir('tmp')
    cd('tmp')

    year = get_year(main_address)

    packages = init(operating_system)

    download_queue = list(packages)
    if len(download_queue) > 0:
        print("Downloading Packages")
    mp_downloader(download_queue, main_address, year, operating_system)
    print("Download Finished")
    try:
        file = open(f"{home_dir}/ltd/log.txt", "r")
        data = file.readlines()
        file.close()
        print("The following packages were not installed:")
        for i in data:
            print(i)
    except FileNotFoundError:
        pass

    exiter(0)


if __name__ == '__main__':
    mkdir("Team1559-Dependencies-Installer")
    cd("Team1559-Dependencies-Installer")
    home_dir = f"{pwd()}"
    main()
