import pytest, sys
from fs import mount
from zipfile import ZipFile
from commands import ls, cd, uniq, touch
from io import StringIO
from datetime import datetime, timedelta

class OutputIntercepter(list):
    def __enter__(self):
        self._stdout = sys.stdout
        self._stringio = StringIO()
        sys.stdout = self._stringio
        return self
    
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines(keepends=True))
        sys.stdout = self._stdout

@pytest.fixture
def test_zip_dt(tmp_path):
    zip_path = tmp_path / "test.zip"
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("dir1/", "")
        zf.writestr("dir1/file1.txt", "Hello, World!")
        zf.writestr("file2.txt", "Python testing")

    return zip_path

@pytest.fixture
def mounted_fs(test_zip_dt):
    fs = mount(str(test_zip_dt))
    return fs

def test_ls(mounted_fs):
    with mounted_fs.open_file("/ls_test.txt", "w") as file:
        file.write(b"Hello Word!")
        
    with OutputIntercepter() as output:
        ls.run("ls")
    assert output == [f"dir1/  file2.txt  ls_test.txt  \n"]

    with OutputIntercepter() as output:
        ls.run("ls /dir1/")
    assert output == [f"file1.txt  \n"]

    with OutputIntercepter() as output:
        ls.run("ls /dir2/")
    assert output == ["/dir2/ is not a directory\n"]

def test_uniq(mounted_fs):
    with mounted_fs.open_file("/uniq_test.txt", "w") as file:
        file.writelines([b"aaaaaaa\n",
                         b"aaaaaaa\n",
                         b"bbbbbbb\n",
                         b"ccccccc\n",
                         b"cccCccc\n",
                         b"ccccccc\n",
                         b"bbbbbbb\n",
                         b"bbbbbbb\n",
                         b"ggggggg\n",
                         b"fffffff\n",
                         b"ttttttt\n",
                         b"uuuuuuu\n",
                         b"uuuuuuu\n"])
        
    with OutputIntercepter() as output:
        uniq.run("uniq /uniq_test.txt")

    assert output == ["aaaaaaa\n",
                      "bbbbbbb\n",
                      "ccccccc\n",
                      "cccCccc\n",
                      "ccccccc\n",
                      "bbbbbbb\n",
                      "ggggggg\n",
                      "fffffff\n",
                      "ttttttt\n",
                      "uuuuuuu\n"]
    
    with OutputIntercepter() as output:
        uniq.run("uniq /uniq_test.txt -i")

    assert output == ["aaaaaaa\n",
                      "bbbbbbb\n",
                      "ccccccc\n",
                      "bbbbbbb\n",
                      "ggggggg\n",
                      "fffffff\n",
                      "ttttttt\n",
                      "uuuuuuu\n"]

    with OutputIntercepter() as output:
        uniq.run("uniq /uniq_test.txt -d")

    assert output == ["aaaaaaa\n",
                      "bbbbbbb\n",
                      "uuuuuuu\n"]
    
    
def test_cd(mounted_fs):
    cd.run("cd /")
    assert mounted_fs.cwd == "/"

    cd.run("cd /dir1")
    assert mounted_fs.cwd == "/dir1/"

    cd.run("cd /dir2")
    assert mounted_fs.cwd == "/dir1/"

def test_touch(mounted_fs):
    touch.run("touch /file3.txt")
    assert mounted_fs.is_file("/file3.txt")

    dt = datetime.now() 
    touch.run("touch /file2.txt")

    assert datetime(*mounted_fs.get_info("/file3.txt").date_time) - dt < timedelta(seconds=1)

    with OutputIntercepter() as output:
        touch.run("touch -c /no_exists.txt")
    assert output == ["/no_exists.txt is not a file.\n"]