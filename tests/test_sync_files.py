import filecmp
import os
import shutil
import tempfile
import pytest
from ..sync_folders import sync_files

# Define test data
TEST_DATA = {
    "src": {
        "file1.txt": "This is file 1.",
        "file2.txt": "This is file 2.",
        "dir3": {
            "file1.txt": "This is a different file inside"
        },
        "dir1": {
            "file3.txt": "This is file 3.",
            "file4.txt": "This is file 4."
        }
    },
    "replica": {
        "file2.txt": "This file will be overwritten.",
        "dir3": {
            "file1.txt": "This will be overwritten"
        },
        "dir2": {
            "file5.txt": "This file will be deleted."
        }
    }
}


@pytest.fixture(scope="module")
def temp_dir():
    """Create a temporary directory for testing."""
    dir_path = tempfile.mkdtemp()
    yield dir_path
    shutil.rmtree(dir_path)


def create_test_files(data, path):
    """Helper function to create test files and directories."""
    for name, content in data.items():
        file_path = os.path.join(path, name)
        if isinstance(content, dict):
            os.mkdir(file_path)
            create_test_files(content, file_path)
        else:
            with open(file_path, "w") as f:
                f.write(content)


def test_sync_files(temp_dir, tmp_path):
    """Test the sync_files function."""
    # Create source and replica directories
    src_dir = os.path.join(temp_dir, "src")
    replica_dir = os.path.join(temp_dir, "replica")
    os.mkdir(src_dir)
    os.mkdir(replica_dir)

    # Create test files in source and replica directories
    create_test_files(TEST_DATA["src"], src_dir)
    create_test_files(TEST_DATA["replica"], replica_dir)

    # Create temporary log file
    log_file = tmp_path / "sync_log.txt"

    # Sync the files
    sync_files(src_dir, replica_dir, log_path=log_file)

    # Check that the replica directory matches the source directory
    assert filecmp.dircmp(src_dir, replica_dir).diff_files == []
    assert filecmp.dircmp(src_dir, replica_dir).left_only == []
    assert filecmp.dircmp(src_dir, replica_dir).right_only == []

    # Check that the log file was created and contains the expected entries
    with open(log_file) as f:
        log_entries = f.readlines()

    print(log_entries)
    assert len(log_entries) == 6

    assert log_entries[0].strip(
    ) == f"COPY:   {os.path.join(src_dir, 'file2.txt')}  ->  {os.path.join(replica_dir, 'file2.txt')}"
    assert log_entries[1].strip(
    ) == f"REMOVE: {os.path.join(replica_dir, 'dir2')}"
    assert log_entries[2].strip(
    ) == f"CREATE: {os.path.join(replica_dir, 'dir1')}"
    assert log_entries[3].strip(
    ) == f"COPY:   {os.path.join(src_dir, 'dir1', 'file3.txt')}  ->  {os.path.join(replica_dir, 'dir1', 'file3.txt')}"
    assert log_entries[4].strip(
    ) == f"COPY:   {os.path.join(src_dir, 'dir1', 'file4.txt')}  ->  {os.path.join(replica_dir, 'dir1', 'file4.txt')}"
    assert log_entries[5].strip(
    ) == f"COPY:   {os.path.join(src_dir, 'file1.txt')}  ->  {os.path.join(replica_dir, 'file1.txt')}"
