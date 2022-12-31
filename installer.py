import os
import subprocess
import sys
import multiprocessing as mp
from zipfile import ZipFile

def importer(package: str):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", f'{package}'])
    finally:
        globals()[package] = importlib.import_module(package)


def unzip(file: str):
    zf = ZipFile(file, 'r')
    zf.extractall()
    zf.close()


def download(url: str, file_name: str):

    # 2. download the data behind the URL
    response = requests.get(url)
    # 3. Open the response into a new file called instagram.ico
    open(file_name, "wb").write(response.content)


def cd(directory: str):
    os.chdir(directory)


def mkdir(directory: str):
    os.mkdir(directory)


def pwd():
    return os.getcwd()

def main():
    importer('requests')
    mkdir('tmp')
    cd('tmp')
    download('https://www.rylanswebdav.cf/publicdocuments/files/frc/navx.zip', 'e.zip')


if __name__ == '__main__':
    main()
