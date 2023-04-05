import filecmp
import hashlib
import shutil
import sys
import os
# TODO - use os.path.join() to join file paths
# TODO - To be checked with program performance
MIN_SYNC_INT = 500


# Check if folder_exists
def folder_exists(dir):
    if not os.path.isdir(dir):
        raise FileNotFoundError(f"Folder {dir} does not exist")


# Check if file exists
def file_exists(dir):
    if not os.path.isfile(dir):
        raise FileNotFoundError(f"File {dir} does not exist")


# Prints in log_file
def print_log(action, log_path, file_dest, file_source=None):

    with open(log_path, 'a') as f:
        if file_source:
            # Write COPY file_source file_dest
            f.write("COPY:   "+file_source+"  ->  "+file_dest+"\n")
            return

        if action == "create":
            # Write CREATE file_dest
            f.write("CREATE: "+file_dest+"\n")
            return

        if action == "remove":
            # Write REMOVE file_dest
            f.write("REMOVE: "+file_dest+"\n")
            return


# Copy file from source to replica
def copy_file(source, replica, replace=False):
    with open(source, 'rb') as f:
        data = f.read()
    file_name = os.path.basename(source)
    if replace:
        new_file = replica
    else:
        new_file = os.path.join(replica, file_name)

    with open(new_file, 'wb') as f:
        f.write(data)


def sync_files(source, replica, log_path):
    """
    Recursively syncs the files.

    Args:
        source (str): The path to the source directory.
        replica (str): The path to the replica directory
    """
    try:
        dcmp = filecmp.dircmp(source, replica)
    except OSError as e:
        print(f"Error: {e}")
        return False

    # To be replaced in replica
    for file in dcmp.diff_files:
        pathL = os.path.join(dcmp.left, file)
        pathR = os.path.join(dcmp.right, file)
        try:
            copy_file(pathL, pathR, replace=True)
        except (OSError, IOError) as e:
            print(f"Error: {e}")
            return False
        print_log("COPY", log_path, pathR, pathL)

    # To be removed from replica
    for dir in dcmp.right_only:
        pathR = os.path.join(dcmp.right, dir)
        # Delete extra directories from replica
        if os.path.isdir(pathR):
            try:
                shutil.rmtree(pathR)
            except OSError as e:
                print(f"Error: {e}")
                return False
        # Delete extra files from replica
        else:
            try:
                os.remove(pathR)
            except OSError as e:
                print(f"Error: {e}")
                return False
        print_log("remove", log_path, pathR)

    # To be coppied to replica
    for dir in dcmp.left_only:
        pathL = os.path.join(dcmp.left, dir)
        pathR = os.path.join(dcmp.right, dir)
        # Non-existing directories in Replica
        if os.path.isdir(pathL):
            try:
                os.mkdir(pathR)
            except OSError as e:
                print(f"Error: {e}")
                return False
            print_log("create", log_path, pathR)
            sync_files(pathL, pathR, log_path)

        # Non existing files in Replica
        else:
            try:
                copy_file(pathL, dcmp.right)
            except (OSError, IOError) as e:
                print(f"Error: {e}")
                return False
            print_log("copy", log_path, pathR, pathL)

    return True


def main(args):

    if len(args) != 4:
        raise ValueError("You need to provide 4 arguments")

    source_path, replica_path, sync, log_path = args[0], args[1], args[2], args[3]

    # Check if folders exist
    folder_exists(source_path)
    folder_exists(replica_path)

    # Assuming log_file must exist
    file_exists(log_path)

    # Validate int value for sync
    try:
        sync_int = int(sync)
    except ValueError:
        raise ValueError("The sync string is not a valid integer")
    if sync_int < MIN_SYNC_INT:
        raise ValueError("The synchronization interval is too low")

    sync_files(source_path, replica_path, log_path)


if __name__ == "__main__":
    main(sys.argv[1:])
