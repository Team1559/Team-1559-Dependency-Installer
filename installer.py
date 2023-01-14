import os
import subprocess
import sys
import multiprocessing as mp
import time
from zipfile import ZipFile
import platform
from typing import *
import shutil


def photonlib_installer(year: str, operating_system: str):
    if operating_system == "windows":
        rm(f"C:\\Users\\Public\\wpilib\\{year}\\vendordeps\\PhotonLib-json-1.0.json")
        cp(f"{home_dir}\\tmp\\photon\\PhotonLib-json-1.0.json", f"C:\\Users\\Public\\wpilib"
                                                                f"\\{year}\\vendordeps\\PhotonLib-json-1.0.json")
    elif operating_system == "macos":
        user = home_dir.split("/")[2]
        rm(f"/Users/{user}/wpilib/{year}/vendordeps/PhotonLib-json-1.0.json")
        cp(f"{home_dir}/tmp/photon/PhotonLib-json-1.0.json", f"/Users/{user}/wpilib/{year}/vendordeps"
                                                             f"/PhotonLib-json-1.0.json")


def ctre_macos_installer(year: str):
    user = home_dir.split("/")[2]
    rmdir(f"/Users/{user}/wpilib/{year}/maven/com/ctre/Phoenix")
    mkdir(f"/Users/{user}/wpilib/{year}/maven/com/ctre/")
    cpdir(f"{home_dir}/tmp/ctre/maven/com/ctre/Phoenix", f"/Users/{user}/wpilib/"
                                                         f"{year}/maven/com/ctre/Phoenix")
    rm(f"/Users/{user}/wpilib/{year}/vendordeps/Phoenix.json")
    cp(f"{home_dir}/tmp/ctre/vendordeps/Phoenix.json", f"/Users/{user}/wpilib/{year}/vendordeps/Phoenix.json")


def cp(source: str, destination: str):
    shutil.copy(source, destination)


def cpdir(source: str, destination: str):
    shutil.copytree(source, destination)


def rev_windows_installer(year):
    rmdir(f"C:\\Users\\Public\\wpilib\\{year}\\maven\\com\\revrobotics\\frc")
    mkdir(f"C:\\Users\\Public\\wpilib\\{year}\\maven\\com\\revrobotics\\frc")
    cpdir(f"{home_dir}\\tmp\\rev\\maven\\com\\revrobotics\\frc", f"C:\\Users\\Public\\wpilib\\"
                                                                 f"{year}\\maven\\com\\revrobotics\\frc")
    rm(f"C:\\Users\\Public\\wpilib\\2021\\vendordeps\\REVLib.json")
    cp(f"{home_dir}\\tmp\\rev\\vendordeps\\REVLib.json", f"C:\\Users\\Public\\wpilib\\{year}\\vendordeps\\REVLib.json")


def wpi_macos_installer(operating_system):
    # os.system(f"{home_dir}/ltd/dmg_manager.sh {pwd()}/wpi.dmg")
    os.system(f"hdiutil attach {pwd()}/wpi.dmg")

    os.system("open -W \"/Volumes/WPILibInstaller/WPILibInstaller.app/\"")

    os.system("hdiutil detach \"/Volumes/WPILibInstaller\"")


def navx_installer(year: str):
    user = home_dir.split("/")[2]
    path = f"/Users/{user}/wpilib/{year}"

    # unzip("navx-mxp-libs.zip")

    # Get the vendor file
    cd(f"{path}/vendordeps")
    rm("navx_frc.json")

    def get_version(years):
        versions = None
        download(f"https://www.kauailabs.com/dist/frc/{years}/navx_frc.json")
        with open("navx_frc.json", "r") as file:
            for i in file.readlines():
                if "version" in i:
                    try:
                        versions = i.split(":")[1].strip().replace('"', '').replace(",", "")
                    except RecursionError:
                        pass
                    except IndexError:
                        pass
                    file.close()
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
    cd(f"{path}")
    mkdir(f"maven/com")
    cd(f"{path}/maven/com")

    # # Install the Java libraries
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


def rev_macos_installer(year):
    user = home_dir.split("/")[2]
    rmdir(f"/Users/{user}/wpilib/{year}/maven/com/revrobotics/frc")
    mkdir(f"/Users/{user}/wpilib/{year}/maven/com/revrobotics/")
    cpdir(f"{home_dir}/tmp/rev/maven/com/revrobotics/frc", f"/Users/{user}/wpilib/"
                                                           f"{year}/maven/com/revrobotics/frc")
    rm(f"/Users/{user}/wpilib/{year}/vendordeps/REVLib.json")
    cp(f"{home_dir}/tmp/rev/vendordeps/REVLib.json", f"/Users/{user}/wpilib/{year}/vendordeps/REVLib.json")


def check_wpi(operating_system: str, year: str):
    if operating_system == "windows":
        return os.path.exists(f"C:\\Users\\Public\\wpilib\\{year}")
    elif operating_system == "macos":
        user = home_dir.split("/")[2]
        return os.path.exists(f"/Users/{user}/wpilib/{year}")


def verify_wpi(operating_system: str, year: str):
    if not check_wpi(operating_system, year):
        print("WPILib is not installed. Please install WPILib before proceeding.")
        clean_exit(1)


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
            if i == "navx" and operating_system != "windows":
                continue
            elif operating_system != "macos" or i != "wpi":
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
    p.terminate()


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
        clean_exit(2)


def mkdir(directory: str):
    directory = directory.replace("\\", "/")
    directory = directory.split("/")
    for i in range(len(directory)):
        if directory[i] == "":
            directory.pop(i)
            directory.insert(i, "/")

    for i in directory:

        try:
            os.mkdir(i)
        except FileExistsError:
            pass
        except FileNotFoundError:
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


def mv(source: str, destination: str):
    try:
        shutil.move(source, destination)
    except FileNotFoundError:
        pass


def run(package: str, operating_system: str):
    if operating_system == "windows":
        os.system(f".\\{package}")

    elif operating_system == "macos":
        os.system(f"open {package}")

    else:
        os.system(f"./{package}")


def get_normalized_input(message: str) -> str:
    return input(f"{message} (y/n): ").lower()


def get_os():

    if "windows" in str(platform.system()).lower():
        operating_system = "windows"
    elif "linux" in str(platform.system()).lower():
        operating_system = "linux"
    elif "darwin" in str(platform.system()).lower():
        operating_system = "macos"
    else:
        operating_system = None
        clean_exit(3)
    return operating_system


def get_cpu_arch():
    if get_os() == "macos" and "arm64" in platform.uname():
        return "arm"
    else:
        return "x86"


def clean_exit(code: int = 0):
    cd(home_dir)
    time.sleep(1)
    if get_normalized_input("\nDo you want to remove temporary data?: ") != "n":
        try:
            rmdir("tmp")
        except:
            os.system("rm -r tmp")
    exit(code)


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
        clean_exit(3)
    return year


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
        cd(f"{home_dir}/tmp")
        if operating_system != "windows" and i == "navx":
            pass

        else:
            mkdir(i)
            cp(f"{i}.zip", i)
            cd(i)
            unzip(f"{i}.zip")
        if i != "wpi":
            verify_wpi(operating_system, year)
        if i == "wpi":
            if operating_system == "windows":
                run("WPILibInstaller.exe", operating_system)

            elif operating_system == "macos":
                wpi_macos_installer(operating_system)

        elif i == "navx":
            if operating_system == "windows":
                run("setup.exe", operating_system)
            elif operating_system == "macos":
                navx_installer(year)

        elif i == "ctre":
            if operating_system == "windows":
                run("cf.exe", operating_system)
            elif operating_system == "macos":
                ctre_macos_installer(year)

        elif i == "rev":
            if operating_system == "windows":
                rev_windows_installer(year)
            elif operating_system == "macos":
                rev_macos_installer(year)

        elif i == "photon":
            photonlib_installer(year, operating_system)

        elif i == "revhc":
            run("rev.exe", operating_system)
        elif i == "ds":
            run("driverstation.exe", operating_system)


def init(operating_system: str):
    available_packages = ["wpi", "navx", "ctre", "rev", "photon"]
    output = []
    if get_normalized_input("Do you want to install all available packages?") != "n":
        output = available_packages
        if operating_system == 'windows':
            output.append("ds")
            output.append("revhc")
    else:
        if get_normalized_input("Do you want to install Wpilib?") != "n":
            output.append("wpi")
        if get_normalized_input("Do you want to install Navx libs?") != "n":
            output.append("navx")
        if get_normalized_input("Do you want to install Revlib?") != "n":
            output.append("rev")
        if get_normalized_input("Do you want to install Ctre libs?") != "n":
            output.append("ctre")
        if get_normalized_input("Do you want to install Photonlib?") != "n":
            output.append("photon")
        if operating_system == 'windows':
            if get_normalized_input("Do you want to install the rev hardware client?") != "n":
                output.append("revhc")
                if get_normalized_input("Do you want to install the driver station?") != "n":
                    output.append("ds")

    return output


def main():
    importer('requests')
    rm(f"{home_dir}/ltd/log.txt")
    main_address = "https://files.rylanswebsite.com/publicdocuments/files/frc"
    operating_system = get_os()
    mkdir("ltd")
    try:
        rmdir("tmp")
    except:
        os.system("rm -r tmp")
    mkdir('tmp')
    cd('tmp')

    if operating_system == "linux":
        print("Linux is not supported yet")
        exit(2)

    year = get_year(main_address)
    print(f"Welcome to the Team 1559 dependency installer for the {year} season! use this tool to easily install all "
          f"necessary dependencies")

    packages = init(operating_system)
    download_queue = list(packages)
    if len(download_queue) > 0:
        if "wpi" not in download_queue:
            if not check_wpi(operating_system, year):
                if input("WPI is not installed, would you like to install it?: ").lower() != "n":
                    download_queue.append("wpi")

        print("Downloading Packages")
        mp_downloader(download_queue, main_address, year, operating_system)
        print("Download Finished")

        install(download_queue, operating_system, year)
        print("Installation Finished, all you need to do now is install (or reinstall by removing and then "
              "reinstalling) the libraries from within vscode")
    else:
        print("No packages selected")

    try:
        file = open(f"{home_dir}/ltd/log.txt", "r")
        data = file.readlines()
        file.close()
        print("The following packages were not installed:")
        for i in data:
            print(i)
    except FileNotFoundError:
        pass

    clean_exit(0)


if __name__ == '__main__':
    mkdir("Team1559-Dependencies-Installer")
    cd("Team1559-Dependencies-Installer")
    home_dir = f"{pwd()}"
    try:
        main()
    except KeyboardInterrupt:
        clean_exit(1)
