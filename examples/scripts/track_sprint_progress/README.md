
# Jira Sprint Progress Analyzer

## Overview

This Python script analyzes Jira sprint progress using the `pyJiraCli` tool. It retrieves sprint and issue data from a Jira board and processes it into an Excel file for easy tracking and analysis.

## Configuration

Before running the script, ensure the following configurations are set:

- `BOARD`: The Jira board to be analyzed (e.g., "BSP_BOARD: COMPONENT_1").
- `SERVER_PROFILE`: The server profile used to connect to Jira via `pyJiraCli`.
- `EXCEL_TABLE`: The name of the Excel table where data will be stored.
- `EXCEL_FILE`: The path to the Excel file where data will be stored.
- `MISSING_DATA_FILE`: The path to the file where tickets with missing data will be logged.

## Dependencies

- Python 3.x
- `openpyxl`: To install, run `pip install openpyxl`
- `pyJiraCli`: A command-line tool to interact with Jira

## Usage

1. Ensure `pyJiraCli` is installed and configured with your Jira credentials.
2. Set the required configurations in the script.
3. Run the script:

```sh
python track_sprint_progress.py
```

## How the Script Utilizes `pyJiraCli`

### Overview

The script leverages the `pyJiraCli` tool to interact with the Jira API. `pyJiraCli` is a command-line interface that simplifies the process of fetching and managing Jira data. In this script, it is used to retrieve sprint and issue data from Jira.

### Using the `subprocess` library

The script uses the `subprocess` module to run `pyJiraCli` commands. This allows the script to execute shell commands from within Python, capturing the output and handling errors. Here are the key functions that utilize `subprocess`:

1. **Fetching Sprint Data:**

   The `get_sprint_data` function uses `pyJiraCli` to fetch sprint data for a specified board. The command constructed is:

   ```sh
   pyJiraCli --verbose --profile {profile} get_sprints "{board}" --file {TMP_FILE}
   ```

   - `--verbose`: Provides detailed output for debugging purposes.
   - `--profile {profile}`: Specifies the server profile configured in `pyJiraCli`.
   - `get_sprints "{board}"`: Retrieves the sprints for the given board.
   - `--file {TMP_FILE}`: Saves the output to a temporary JSON file.

   The `subprocess.run` function executes this command:

   ```python
   command = f'pyJiraCli --verbose --profile {profile} get_sprints "{board}" --file {TMP_FILE}'
   result = subprocess.run(command, shell=True, check=False)
   ```

   - `command`: The command string to be executed.
   - `shell=True`: Allows the command to be executed through the shell.
   - `check=False`: Prevents `subprocess` from raising an exception if the command fails.

   After execution, the function checks `result.returncode` to ensure the command was successful (a return code of 0 indicates success). If successful, it reads the JSON output from the temporary file:

   ```python
   if result.returncode == 0:
       with open(TMP_FILE, mode='r', encoding='utf-8') as file:
           sprint_dict = json.load(file)
       os.remove(TMP_FILE)
   ```

2. **Fetching Issue Data:**

   The `get_issue_data` function uses `pyJiraCli` to fetch issue data for a specific sprint. The command constructed is:

   ```sh
   pyJiraCli --verbose --profile {profile} search "sprint = '{sprint}'" --file {TMP_FILE}
   ```

   - `--verbose`: Provides detailed output for debugging purposes.
   - `--profile {profile}`: Specifies the server profile configured in `pyJiraCli`.
   - `search "sprint = '{sprint}'"`: Searches for issues in the specified sprint.
   - `--file {TMP_FILE}`: Saves the output to a temporary JSON file.

   The `subprocess.run` function executes this command:

   ```python
   command = f'pyJiraCli --verbose --profile {profile} search "sprint = '{sprint}'" --file {TMP_FILE}'
   result = subprocess.run(command, shell=True, check=False)
   ```

   Similar to `get_sprint_data`, the function checks the return code and reads the JSON output if the command was successful.

## Notes

Ensure that the paths and configurations are correctly set according to your environment. The script utilizes `pyJiraCli` for Jira data retrieval, so make sure it's properly installed and configured.
