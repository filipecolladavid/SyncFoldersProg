import os
import pytest
from unittest.mock import patch

from ..sync_folders import MIN_SYNC_INT
from ..sync_folders import main, folder_exists, file_exists

# Test that main function raises invalid number of arguments
def test_main_invalid_args():
    with pytest.raises(ValueError, match="You need to provide 4 arguments"):
        main([]) # Pass empty arguments

    with pytest.raises(ValueError, match="You need to provide 4 arguments"):
        main(["","",""]) # Pass 3 arguments

    with pytest.raises(ValueError, match="You need to provide 4 arguments"):
        main(["", ""]) # Pass 2 arguments

    with pytest.raises(ValueError, match="You need to provide 4 arguments"):
        main([""]) # Pass 1 argument


# Test that main function raises an error with non-existent folders
def test_main_non_existent_folders(tmpdir):
    source_path = os.path.join(tmpdir, "non_existent_source")
    replica_path = os.path.join(tmpdir, "non_existent_replica")
    sync = str(MIN_SYNC_INT)
    log_path = os.path.join(tmpdir, "log_file.txt")
    with pytest.raises(FileNotFoundError):
        main([source_path, replica_path, sync, log_path])


# Test that main function raises an error with non-existent log file
def test_main_non_existent_log_file(tmpdir):
    source_path = os.path.join(tmpdir, "source")
    replica_path = os.path.join(tmpdir, "replica")
    sync = "1000"
    log_path = os.path.join(tmpdir, "non_existent_log_file.txt")
    os.makedirs(source_path)
    os.makedirs(replica_path)
    with pytest.raises(FileNotFoundError):
        main([source_path, replica_path, sync, log_path])


# Test that main function raises an error with invalid sync interval
def test_main_invalid_sync_interval(tmpdir):
    source_path = os.path.join(tmpdir, "source")
    replica_path = os.path.join(tmpdir, "replica")
    sync = str(MIN_SYNC_INT - 1)
    log_path = os.path.join(tmpdir, "log_file.txt")
    os.makedirs(source_path)
    os.makedirs(replica_path)
    with open(log_path, 'w'):  # Create empty file at log_path
        pass
    with pytest.raises(ValueError):
        main([source_path, replica_path, sync, log_path])


# Test that main function works with valid arguments
def test_main_valid_args(tmpdir):
    source_path = os.path.join(tmpdir, "source")
    replica_path = os.path.join(tmpdir, "replica")
    sync = "1000"
    log_path = os.path.join(tmpdir, "log_file.txt")
    os.makedirs(source_path)
    os.makedirs(replica_path)
    file_path = os.path.join(source_path, "test_file.txt")
    with open(log_path, 'w'):  # Create empty file at log_path
        pass
    with open(file_path, "w") as f:
        f.write("test")
    with patch("builtins.input", return_value="y"):
        main([source_path, replica_path, sync, log_path])


# Test that folder_exists function raises an error with non-existent folder
def test_folder_exists_non_existent_folder(tmpdir):
    non_existent_folder = os.path.join(tmpdir, "non_existent_folder")
    with pytest.raises(FileNotFoundError):
        folder_exists(non_existent_folder)


# Test that folder_exists function works with valid folder
def test_folder_exists_valid_folder(tmpdir):
    valid_folder = os.path.join(tmpdir, "valid_folder")
    os.makedirs(valid_folder)
    folder_exists(valid_folder)


# Test that file_exists function raises an error with non-existent file
def test_file_exists_non_existent_file(tmpdir):
    non_existent_file = os.path.join(tmpdir, "non_existent_file.txt")
    with pytest.raises(FileNotFoundError):
        file_exists(non_existent_file)


