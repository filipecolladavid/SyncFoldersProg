import filecmp
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
            f.write("COPY:   "+file_source+" -> "+file_dest)
            return

        if action == "create":
            # Write CREATE file_dest
            f.write("CREATE: "+file_dest+"\n")
            return

        if action == "remove":
            # Write REMOVE file_dest
            f.write("REMOVE: "+file_dest+"\n")
            return


def copy_file(source, replica):
    with open(source, 'rb') as f:
        data = f.read()
    file_name = os.path.basename(source)
    new_file = os.path.join(replica, file_name)
    with open(new_file, 'wb') as f:
        f.write(data)


def sync_files(source, replica, log_path):
    """
    Recursively syncs the files.

    Args:
        source (str): The path to the source directory.
        replica (str): The path to the replica directory.

    Returns:
        list: A list of files that are different between the two directories, with their full path.
    """

    dcmp = filecmp.dircmp(source, replica)

    # To be coppied to replica
    for dir in dcmp.left_only:
        pathL = os.path.join(dcmp.left, dir)
        pathR = os.path.join(dcmp.right, dir)

        # Non-existing directories in Replica
        if os.path.isdir(pathL):
            os.mkdir(pathR)
            print_log("create", log_path, pathR)
            # sync_files(pathL, pathR, log_path)

        # Non existing files in Replica
        else:
            copy_file(pathL, dcmp.right)
            print_log("copy", log_path, pathR, pathL)


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

    # TODO - while in execution refresh files every sync time - do it once now
    # TODO - recursvely by each sub-dir
    # Sync
    print()
    print("-------------------------------")
    print("source_path:", source_path)
    print("replica_path:", replica_path)
    print("-------------------------------")
    print()
    sync_files(source_path, replica_path, log_path)

    # # Check if directories have the same content
    # cmp = filecmp.dircmp(source_path, replica_path)

    # # Replica to be replaced by source
    # diff_files = cmp.diff_files

    # # To be coppied to replica
    # source_only = cmp.left_only

    # # To be deleted
    # replica_only = cmp.right_only

    # if diff_files or source_only or replica_only:  # Different directories

    #     print("Different Files", diff_files)
    #     print("Source Only: ", source_only)
    #     print("Replica Only: ", replica_only)

    # else:  # Same directory
    #     print("They are the same")


if __name__ == "__main__":
    main(sys.argv[1:])
