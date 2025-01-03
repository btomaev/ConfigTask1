from typing import Literal, List
from zipfile import ZipFile, ZipInfo, Path
from io import BytesIO

def mount(path: str):
    global _FS
    _FS = FS(path)
    return _FS

def get_fs():
    return _FS

class FS:
    def __init__(self, path):
        self._fs_image_path: str = path
        self._cwd = "/"

    @property
    def cwd(self):
        return self._cwd
    
    def _normalize_path(path: str):
        return path.removeprefix("/").strip()
    
    def _full_path(path: str):
        path = path.strip()
        return path if path.startswith("/") else f"/{path}"

    def exists(self, path: str):
        with ZipFile(self._fs_image_path, mode="r") as fs:
            path = FS._normalize_path(path)
            return Path(fs, path).exists()

    def is_dir(self, path: str):
        with ZipFile(self._fs_image_path, mode="r") as fs:
            if path == "/":
                return True
            path_obj = Path(fs, FS._normalize_path(path))
            return path_obj.exists() and path_obj.is_dir()
    
    def is_file(self, path: str):
       with ZipFile(self._fs_image_path, mode="r") as fs:
            if path == "/":
                return False
            path_obj = Path(fs, FS._normalize_path(path))
            return path_obj.exists() and path_obj.is_file()
        
    def cd(self, path: str):
        if path != "/":
            if not path.endswith("/"):
                path += "/"
            if not self.is_dir(FS._normalize_path(path)):
                return False
        self._cwd = FS._full_path(path)
        return True
    
    def repair(self):
        with ZipFile(self._fs_image_path, mode="a") as fs:
            files = fs.namelist()
            files.sort(reverse=True)
            leafs = []
            k = 0
            for n, a in enumerate(files):
                if k:
                    k -= 1
                    continue
                for m, b in enumerate(files[n+1:]):
                    if not a.startswith(b) or n+m+2 == len(files):
                        leafs.append(a)
                        k = m
                        break

            for file in leafs:
                path = file.removesuffix("/")
                while path.count("/"):
                    path = path[:path.rfind("/")]
                    self.mkdir(path, repair=False)

    def list_dir(self, path: str):
        with ZipFile(self._fs_image_path, mode="r") as fs:
            if not path.endswith("/"):
                path += "/"
            path = FS._normalize_path(path)
            return [(path, fs.getinfo(path.at)) for path in Path(fs, path).iterdir()]
        
    def get_path(self, path):
        with ZipFile(self._fs_image_path, mode="r") as fs:
            if not path.endswith("/"):
                path += "/"
            path = FS._normalize_path(path)
            return Path(fs, path)
        
    def get_info(self, path):
        with ZipFile(self._fs_image_path, mode="r") as fs:
            path = FS._normalize_path(path)
            return fs.getinfo(path)
             
    def mkdir(self, path: str, mode: int=511, repair: bool=True):
        with ZipFile(self._fs_image_path, mode="a") as fs:
            path = FS._normalize_path(path)
            if not path.endswith("/"):
                path += "/"
            if not self.is_dir(path):
                mode = int(f"40{mode}", base=8)
                fs.mkdir(path, mode=mode)
        if repair:
            self.repair()

    def open_file(self, path: str | ZipInfo, mode: Literal["r", "w"]="r"):
        class FileDescriptor(object):
            def __init__(self, zip_path, file_path):
                self.zip_path = zip_path
                self.file_path = file_path
            def __enter__(self):
                self.fs = ZipFile(self.zip_path, mode="a")
                if not isinstance(self.file_path, ZipInfo):
                    self.file_path = FS._normalize_path(self.file_path)
                self.file = self.fs.open(self.file_path, mode=mode, force_zip64=True)
                return self.file
            def __exit__(self, type, value, traceback):
                self.file.close()
                self.fs.close()

        return FileDescriptor(self._fs_image_path, path)
    
    def delete(self, paths: List[str]):
        paths = [FS._normalize_path(path) for path in paths]
        tmp = BytesIO()
        with ZipFile(self._fs_image_path, mode="r") as fs:
            with ZipFile(tmp, mode="w") as new_fs:
                for fileinfo in fs.filelist:
                    if fileinfo.filename not in paths:
                        new_fs.writestr(fileinfo, fs.read(fileinfo))
        with open(self._fs_image_path, mode="wb") as file:
            file.write(tmp.getvalue())