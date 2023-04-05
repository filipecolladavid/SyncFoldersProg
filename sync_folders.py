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


def main(args):

    if len(args) != 4:
        raise ValueError("You need to provide 4 arguments")

    # source_path - Path of the source file
    # replica_path - Path of the replica
    # sync - Synchronization interval in ms
    # log_path - Path of log file

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

    pass


if __name__ == "__main__":
    main(sys.argv[1:])
