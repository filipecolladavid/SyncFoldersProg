# Veeam Test Task - Folder Synchronization

## Task:
Program that synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

## Requirements:
- Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder;
- Synchronization should be performed periodically.
- File creation/copying/removal operations should be logged to a file and to the
console output;
- Folder paths, synchronization interval and log file path should be provided
using the command line arguments;
- It is undesirable to use third-party libraries that implement folder
synchronization;
- It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library.

## Usage:
1. Create a virtual envoirment with:
  ```bash
    python3 -m venv venv
  ```
2. Activate the virtual envoirment with:
  ```bash
    source venv/bin/activate
  ```
3. Install the required deppedencies
  ```bash
    pip install -r requirements.txt
  ```
4. Run the tests with:
  ```bash
    pytest
  ```
   
5. Try the program
  ```bash
    python3 sync_folders.py source_folder replica_folder sync_interval log_file
  ```
  
  Where:
  - ``source_folder``: is the path to the source folder.
  - ``replica_folder``: is the path to the replica folder.
  - ``sync_interval``: is an integer value for the synchronization interval.
  - ``log_file``: is the path to the log_file

## Notes:
  ``MIN_SYNC_INT = 500`` tries to treshold the minimum value allowed for the synchronization interval, however it's arbitrary and may not work deppending on the number of subdirectories needed to scan.
