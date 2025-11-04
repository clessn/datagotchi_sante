# Machine Learning and Explainable AI for Well-Being Prediction

**Datagotchi Health** is a research platform combining **machine learning** and **behavioral experimentation** to investigate how lifestyle and socio-demographic factors relate to **mental well-being**, and how different explanation formats affect users’ understanding, trust, and behavior.  
The repository includes all code supporting two empirical studies:

1. **Study 1 – Predictive Modeling:** Development and validation of machine learning models predicting well-being from lifestyle data.  
2. **Study 2 – Explainability Experiment:** Online evaluation of five explanation modalities for model outputs through an interactive web application.

---

## ⚙️ Reproducibility and Data Access

All analyses were conducted in **Python 3.9** and **R 4.3**, with dependencies managed via **Poetry** for environment reproducibility.  

Data used for Study 1 were collected through the **Léger Panel**, while Study 2 used data from **Prolific**.  
Because the datasets contain human-subject information, raw data are **not publicly available**.  
Processed or synthetic examples may be shared upon request in compliance with ethics protocols.

---

## 🧭 Getting Started

To reproduce or extend the analyses and experiments, please follow these steps:

1. **Install required software**

   Ensure you have the following installed on your system:
   - **Python 3.9**
   - **R 4.3**
   - **Make**
   - **Poetry** (for Python dependency management)

2. **Create a `.env` file**

   In the project root directory, create a file named `.env` containing the following paths and configuration variables:

   ```bash
   # Paths for Study 1 (Machine Learning)
   DATA_PATH='path/to/ml/data'

   # Paths for Study 2 (Web Application Experiment)
   DATA_WEBAPP_PATH='/path/to/webapp/data'
   SECRET_KEY='your_secret_key_here'                   # Protects the web app database
   PROLIFIC_STUDY_ID='your_prolific_study_id_here'     # Used when running the experiment on Prolific
   PROLIFIC_COMPLETION_CODE='your_completion_code_here' # Used for study completion validation

---

## 🚀 Study 1 — Running the Machine Learning Pipeline

The **Makefile** automates the entire workflow, from feature generation to model evaluation. All model configurations and parameter grids are stored in the directory `app/ml/configs`, allowing full reproducibility and easy modification of model settings. 
Below is an overview of key commands:

| Command | Description |
|----------|-------------|
| `make create-features` | Generates model input features from the raw questionnaire data. |
| `make select-features` | Selects the most informative predictors using XGBoost feature importance. |
| `make run-crossval` | Runs nested cross-validation for model comparison and hyperparameter tuning. |
| `make regular-track` | Monitors new experimental data on the remote server. |
| `make regular-download` | Downloads updated results from the remote server for local analysis. |

To reproduce Study 1 model training:

```bash
make create-features
make select-features
make run-crossval
```

## 🧪 Study 2 — Online Explainability Experiment

Study 2 builds upon the predictive model developed in Study 1 and investigates how different **explanation formats** influence users’ interpretation of their predicted well-being scores.  
An interactive **Flask web application** serves as the experimental platform, where participants are randomly assigned to one of five explanation conditions—**contextual**, **quantitative**, **textual**, **visual**, or **interactive**—or to a control condition without explanation.

Each condition presents a distinct communication strategy for model reasoning, implemented dynamically using HTML templates and Flask rendering logic.  
Participant interactions, response times, and navigation behaviors are automatically logged for later analysis.

To launch the web interface locally:

```bash
python app/microapp.py
```

### 🌐 Running the Application on a Remote Server

The web application can also be deployed on a remote server for conducting online experiments.  
Once the experiment is running, data can be continuously monitored and synchronized between the server and your local machine.

#### Tracking and Synchronizing Experimental Data

- **On the remote server:**  
  Start automatic tracking of new incoming participant data  
  ```bash
  make regular-track
  ```

- **On the remote server:**  
  Download the latest experimental data from the remote server
  ```bash
  make regular-download vm=trainmachine DATA_EXPERIMENT_PATH='/root/deploy/data'
  ```
  
### Behavioral and Statistical Analysis

The file `analysis/study_2.R` reproduces the statistical analysis of Study 2, including manipulation checks, between-condition comparisons, and hypothesis testing on user comprehension and trust.  
Analyses were conducted using **R 4.3**, and results focus on identifying how explanation modality influences perceived understanding, satisfaction, and behavioral intention.

---

## 🧰 Environment Setup

Clone the repository and install dependencies using Poetry:

```bash
poetry install
```

Then activate the environment:

```bash
poetry shell
```

## 🪪 Contact

For questions or collaboration requests, please contact:  
**flore.vromman@gmail.com**

---

## 📜 License

This project is distributed under an open academic license.  
Please contact the authors for reuse or redistribution inquiries.
