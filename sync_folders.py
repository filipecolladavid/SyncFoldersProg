import sys
import os


def folder_exists(dir):
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Folder {dir} does not exist")


def sync_folders(source, replica):
    
    # Check if folders exist
    folder_exists(source)
    folder_exists(replica)
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("You need to provide two paths")
    sync_folders(sys.argv[1], sys.argv[2])
