import pytest
from fs import mount, get_fs
from zipfile import ZipFile


@pytest.fixture
def test_zip(tmp_path):
    zip_path = tmp_path / "test.zip"
    with ZipFile(zip_path, "w") as zf:
        zf.writestr("dir1/", "")
        zf.writestr("dir1/file1.txt", "Hello, World!")
        zf.writestr("file2.txt", "Python testing")
    return zip_path

@pytest.fixture
def mounted_fs(test_zip):
    fs = mount(str(test_zip))
    return fs

def test_mount_and_get_fs(test_zip):
    fs = mount(str(test_zip))
    assert get_fs() is fs
    assert fs._fs_image_path == str(test_zip)

def test_exists(mounted_fs):
    assert mounted_fs.exists("/dir1/")
    assert mounted_fs.exists("/dir1/file1.txt")
    assert mounted_fs.exists("/file2.txt")
    assert not mounted_fs.exists("/nonexistent")

def test_is_dir(mounted_fs):
    assert mounted_fs.is_dir("/")
    assert mounted_fs.is_dir("/dir1/")
    assert not mounted_fs.is_dir("/dir1/file1.txt")
    assert not mounted_fs.is_dir("/file2.txt")

def test_is_file(mounted_fs):
    assert not mounted_fs.is_file("/")
    assert not mounted_fs.is_file("/dir1/")
    assert mounted_fs.is_file("/dir1/file1.txt")
    assert mounted_fs.is_file("/file2.txt")

def test_cd(mounted_fs):
    assert mounted_fs.cd("/")
    assert mounted_fs.cwd == "/"
    assert mounted_fs.cd("/dir1/")
    assert mounted_fs.cwd == "/dir1/"
    assert not mounted_fs.cd("/nonexistent")

def test_repair(mounted_fs, test_zip):
    mounted_fs.repair()
    with ZipFile(test_zip, "r") as zf:
        files = zf.namelist()
        assert "dir1/" in files
        assert "dir1/file1.txt" in files
        assert "file2.txt" in files

def test_list_dir(mounted_fs):
    contents = mounted_fs.list_dir("/")
    assert len(contents) > 0

def test_mkdir(mounted_fs):
    mounted_fs.mkdir("/newdir")
    assert mounted_fs.is_dir("/newdir/")
    mounted_fs.mkdir("/newdir/subdir")
    assert mounted_fs.is_dir("/newdir/subdir/")

def test_open_file(mounted_fs):
    with mounted_fs.open_file("/dir1/file1.txt", "r") as f:
        assert f.read() == b"Hello, World!"
    with mounted_fs.open_file("/newfile.txt", "w") as f:
        f.write(b"New Content")
    assert mounted_fs.is_file("/newfile.txt")

def test_delete(mounted_fs):
    mounted_fs.delete(["/dir1/file1.txt"])
    assert not mounted_fs.exists("/dir1/file1.txt")
    assert mounted_fs.exists("/dir1/")