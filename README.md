# IPL Promo Hit Predictor 🎯🏏

This project uses Machine Learning to **predict the probability of a six being hit in the first 2 overs of an IPL match**, which is commonly used in betting app promotions or fantasy predictions.

## 📌 Problem Statement

Many platforms offer a promotion:  
> *"If there's a six in the first 2 overs, you win a bonus!"*

We wanted to build a model that predicts whether such a "promo hit" (a six in the first 12 balls) is likely based on:
- The teams playing
- The venue
- Historical data patterns

## 📂 Project Structure
. ├── ipl_dataset_final_enhanced_v2.csv # Final cleaned and enhanced dataset ├── IPL.ipynb # Main notebook with data prep, model training & prediction ├── model.joblib # Trained Random Forest model ├── preprocessor.joblib # Fitted preprocessing pipeline ├── ipl_yamls/ # Contains YAML files scraped from IPL match pages ├── web_scrapping.ipynb # Script to extract data from YAML files ├── matplotlib.ipynb # (Optional) Notebook for EDA & plots


## 🧠 ML Pipeline

- **Data Collection**: Extracted YAMLs from Cricsheet
- **Feature Engineering**:
  - Counted sixes in the first 2 overs
  - Added context like venue and team matchups
- **Modeling**:
  - Used `RandomForestClassifier`
  - Handled class imbalance using SMOTE
  - Optimized hyperparameters using GridSearchCV
- **Evaluation**:
  - Accuracy, F1-score, and ROC-AUC on test data

## 🚀 How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/ipl-promo-hit-predictor.git
   cd ipl-promo-hit-predictor
