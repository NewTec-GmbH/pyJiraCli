
# Jira Sprint Progress Analyzer

## Overview

This Python script analyzes Jira sprint progress using the `pyJiraCli` tool. It retrieves sprint and issue data from a Jira board and processes it into an Excel file for easy tracking and analysis.

The script performs the following operations:

1. **Retrieves Sprint Data**: Fetches all sprints from the specified Jira board using `get_sprints` command
2. **Collects Issue Metrics**: For each sprint, retrieves all issues and extracts time-related data:
   - Time estimates (including idle estimates)
   - Time remaining on open issues
   - Time actually spent on completed issues
3. **Calculates Derived Metrics**: Computes additional metrics using Excel formulas:
   - **Time Buffer**: The difference between original estimate and spent/remaining time
   - **Processed Time Units**: Spent time plus time buffer (actual work done + buffer)
   - **Efficiency**: How efficiently the sprint used allocated time
   - **Progress**: Overall completion percentage of the sprint
4. **Identifies Data Gaps**: Logs issues with missing data (no time estimates or no spent time on closed issues)
5. **Generates Excel Report**: Creates or updates an Excel file with one row per sprint, complete with all metrics and summary calculations

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

## Excel Output Structure

### Columns (Metrics)

The Excel file contains the following columns for each sprint:

| Column                    | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **Sprint Name**           | Name of the Jira sprint                                                          |
| **Start Date**            | Sprint start date                                                                |
| **End Date**              | Sprint end date                                                                  |
| **Delta Days**            | Duration of the sprint in days                                                   |
| **Time Est. (Idle)**      | Time estimates for issues that weren't worked on                                 |
| **Time Remaining (Open)** | Time remaining on active/open issues                                             |
| **Time Spent (Done)**     | Total time spent on completed issues                                             |
| **Original Estimate**     | Total original time estimation for the sprint                                    |
| **Time Buffer**           | Formula: Original Estimate - (Spent + Remaining + Idle)                          |
| **Processed Time Units**  | Formula: Spent time + Time Buffer (actual work performed)                        |
| **Efficiency**            | Formula: Original Estimate / Spent Time (how well estimates match actual effort) |
| **Progress**              | Formula: (Done + Remaining/2) / (Done + Remaining + Idle) (% completion)         |

### Summary Row

At the bottom of the data, the script calculates summary totals for each metric column using SUM formulas, allowing you to view aggregate sprint statistics.

### Date Stamp

The current date when the report was generated is recorded in the Excel file for tracking purposes.

## Data Quality Reports

### Missing Data File

The script generates two types of reports for data quality issues:

1. **Tickets with No Time Estimation** (`{BOARD}_MissingTicketData.txt`)
   - Lists all tickets that lack time estimates
   - Includes ticket key and URL for easy access
   - Helpful for identifying incomplete ticket configurations

2. **Closed Tickets with No Spent Time**
   - Lists completed issues where no time was tracked
   - Helps identify tracking gaps in completed work
   - Useful for process improvement and compliance

## Notes

Ensure that the paths and configurations are correctly set according to your environment. The script utilizes `pyJiraCli` for Jira data retrieval, so make sure it's properly installed and configured.

### Tips for Best Results

- Ensure all team members log time in Jira for completed issues
- Verify that all issues have time estimates before sprint planning
- Run the script regularly (e.g., daily) to track sprint progress over time
- Use the Excel file's conditional formatting to visualize efficiency and progress metrics
- Monitor the missing data file to improve data quality in future sprints
