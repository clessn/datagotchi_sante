# Datagotchi Health

Datagotchi Health is an algorithm designed to predict mental health outcomes based on lifestyle behaviors and provide recommendations for improving mental health.

## Table of Contents
1. [Prerequisites / Installation](#prerequisites--installation)
2. [Getting Started](#getting-started)
3. [Repository Structure](#repository-structure)
4. [Launching an Experiment](#when-launching-an-experiment)
5. [Analysing results of explainability study](#analysing-results-of-explainability-study)

## Prerequisites / Installation

Before you begin, ensure you have met the following requirements:
- Python 3.9
- R
- Poetry (for Python virtual environment)
- Make (to run the Makefile)

To install the required dependencies, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/datagotchi-health.git
    ```
2. Navigate to the project directory:
    ```sh
    cd datagotchi-health
    ```
3. Install the dependencies using Poetry:
    ```sh
    poetry install
    ```

## Getting Started

To get started with the project, follow these steps:

1. Request access to the data by contacting the repository owner.
2. Create a `.env` file in the project root directory with the `DATA_PATH` environment variable set to the location of your data:
    ```env
    DATA_PATH='path/to/data'
    ```
3. Edit the `config.py` file to suit your specific needs.
4. Run the ML pipeline : 
- Step 1 : create features : 
    ```sh
    make create-features
    ```
- Step 2 : select features : 
    ```sh
    make select-features
    ```
- Step 3 : Run the cross-validation:
    ```sh
    make run-crossval
    ```

## Repository Structure

The repository is organized as follows:
code

```markdown
code/
├── cleaning/
│   └── (various cleaning functions)
├── eda/
│   └── (exploratory data analysis scripts)
app/
├── ml/
    └── (machine learning workflow from raw data to evaluated predictions)
``````
- **cleaning**: Contains scripts for data cleaning.
- **eda**: Contains scripts for exploratory data analysis to explore and understand the data.
- **ml**: Contains scripts for the machine learning workflow, including data processing, model training, and evaluation.

## When launching an experiment
### How to track the incoming data
- on the remote machine, run 'make regular-track'
- on the local machine, run 'make regular-download vm=trainmachine DATA_EXPERIMENT_PATH='/Users/cvandekerckh/Code/datagotchi_sante/deploy/data'

## Analysing results of explainability study

To work on the analysis of the explainability study results (using `explain_study.R`), follow these steps:

### Prerequisites

- **R** installed on your machine.
- You need a `.env` file at the root of the project directory.  
  This file is used to store environment variables for the analysis scripts.  
  To create it:
    1. In the main project folder, create a new file named `.env` (no filename, just `.env`).
    2. Open the file and add the following line (replace the path with the actual location of your results folder):
        ```
        DATA_RESULT_PATH=/path/to/results
        ```
    3. Save the file.  
  This variable should point to the folder containing your results data (for example, where `clean_results.csv` is located).
- The results file `clean_results.csv` must be present in the folder:  
  `${DATA_RESULT_PATH}/clean/clean_results.csv`

### How to run the analysis

1. Open `explain_study.R` in your R environment or in VS Code (with the R extension).
2. Make sure your `.env` file is loaded and the environment variable `DATA_RESULT_PATH` is correctly set.
3. Run the script. It will:
    - Load the results data.
    - Convert columns to appropriate types (e.g., factors, durations).
    - Prepare the data for manipulation checks and modeling.

You can now complete or extend the analysis in `explain_study.R` as needed.

