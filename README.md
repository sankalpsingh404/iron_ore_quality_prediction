# 🏭 Iron Ore Quality Predictor

> **Predicting % Silica Concentrate in a Mining Flotation Plant using Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2%2B-orange)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-1.7%2B-green)](https://xgboost.readthedocs.io)
[![Flask](https://img.shields.io/badge/Flask-2.2%2B-lightgrey)](https://flask.palletsprojects.com)

---

## 📌 Problem Statement

In mining flotation plants, reducing **% Silica Concentrate** in the final iron ore output is critical for quality control. High silica content lowers the grade of iron ore concentrate. This project builds ML models to **predict silica levels** from real-time process parameters, helping operators take corrective action earlier.

---

## 📊 Dataset

| Property | Value |
|----------|-------|
| Source | Mining Process Flotation Plant |
| Rows | ~737,453 |
| Features | 22 process variables |
| Target | `% Silica Concentrate` |
| Sampling rate | Every 20 seconds |

**Key Features:**
- Iron Feed & Silica Feed percentages
- Starch Flow, Amina Flow, Ore Pulp Flow
- Ore Pulp pH & Density
- Flotation Column Air Flows (7 columns)
- Flotation Column Levels (7 columns)

---

## 🤖 Models Used

| Model | Description |
|-------|-------------|
| **Random Forest** | Ensemble of decision trees, robust to outliers |
| **XGBoost** | Gradient boosting, high accuracy |

---

## 📁 Project Structure

```
iron-ore-quality-predictor/
│
├── data/
│   └── MiningProcess_Flotation_Plant_Database.csv
│
├── models/
│   ├── random_forest_model.pkl
│   ├── xgboost_model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
│
├── notebooks/
│   └── iron_ore_quality_prediction.ipynb   ← Main Colab Notebook
│
├── webapp/
│   └── app.py                              ← Flask Web App
│
├── train_model.py                          ← Training Script
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/iron-ore-quality-predictor.git
cd iron-ore-quality-predictor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the model
```bash
python train_model.py
```

### 4. Run the web app
```bash
python webapp/app.py
# Open http://localhost:5000
```

---

## 📓 Google Colab

Open the notebook directly in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/iron-ore-quality-predictor/blob/main/notebooks/iron_ore_quality_prediction.ipynb)

---

## 📈 Results

| Model | R² Score | MAE | RMSE |
|-------|----------|-----|------|
| Random Forest | ~0.78 | ~0.04 | ~0.06 |
| XGBoost | ~0.82 | ~0.03 | ~0.05 |

> *Actual metrics depend on sample size and hyperparameters used during training.*

---

## 🖼️ Visualizations

- Target distribution (Silica & Iron Concentrate)
- Feature correlation heatmap
- Actual vs Predicted scatter plots
- Feature importance ranking
- Residuals plot

---

## 👤 Author

**Your Name**  
[GitHub](https://github.com/YOUR_USERNAME) | [LinkedIn](https://linkedin.com/in/yourprofile)

---

## 📝 License

This project is open source under the [MIT License](LICENSE).
