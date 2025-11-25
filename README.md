# Fitts’ Law Pointing Experiment

This repository contains a complete setup for running a Fitts’ Law pointing experiment and analyzing the resulting dataset. It includes:

- `main.py` – the experiment program (run locally, e.g., in PyCharm)  
- `raw_data.csv` – recorded movement data from the experiment  
- A Google Colab notebook – for data analysis and statistical modeling  
- `requirements.txt` – dependencies for running the experiment script

The project supports both data collection and data analysis, making it suitable for coursework, replication studies, and HCI research.

---

## 1. Running the Experiment (`main.py`)

The experiment script implements a controlled Fitts’ Law pointing task. Participants click on circular targets at varying distances and sizes. For each trial, the script records:

- participant ID  
- block and trial numbers  
- amplitude (distance)  
- diameter (target size)  
- movement direction (left/right)  
- movement time  
- errors  
- trajectory distance  
- endpoint deviation  

### **How to run in PyCharm**

1. Create a virtual environment (recommended).  
2. Install dependencies:

   ```bash
   pip install -r requirements.txt

## 2. Fitts’ Law Experiment Analysis Notebook

The notebook **`Fitts_Law_Experiment_Analysis.ipynb`** contains the full analysis pipeline for the Fitts’ Law pointing experiment. It walks through:

- loading the raw experimental data  
- cleaning and preprocessing  
- computing the Index of Difficulty (ID)  
- summarizing movement time and error rates  
- fitting Fitts’ Law regression models  
- running additional statistical tests (e.g., ANOVA, regression on secondary factors)  
- generating figures and tables used in the report  

You can open this notebook directly in Google Colab and run all cells to reproduce the analysis.

[Open the analysis notebook in Google Colab](https://colab.research.google.com/github/atieh-ameri/fitts-law-experiment/blob/main/Fitts_Law_Experiment_Analysis.ipynb)
