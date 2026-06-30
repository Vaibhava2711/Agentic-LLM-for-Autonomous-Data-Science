# DeepAnalyze Healthcare Case Study: Heart Failure Outcome Prediction

Clinical outcome prediction is a core modeling task in biomedical data science. Given clinical endpoints, researchers need interpretable, verifiable pipelines for feature selection, model training, and performance benchmarking, yielding publication-ready summaries and figures.

In this case study, DeepAnalyze automates the end-to-end clinical modeling pipeline: **Data Understanding → Variable Selection → Model Training → Comparative Evaluation → Interpretation**.

---

## 1. Dataset Overview

- **Dataset**: `heart_failure_clinical_records_dataset.csv`
- **Samples**: 299 patient records × 13 clinical features
- **Target Variable**: `DEATH_EVENT` (0 = survived, 1 = deceased)
- **Positive Class Prevalence**: ~32.1% (96 / 299)
- **Missing Values**: 0 (complete cohort)

### Clinical Feature Dictionary

| Feature | Type | Description |
|---|---|---|
| `age` | Continuous | Patient age (years) |
| `creatinine_phosphokinase` | Continuous | Level of the CPK enzyme in blood (mcg/L) |
| `ejection_fraction` | Continuous | Percentage of blood leaving the heart at each contraction (%) |
| `platelets` | Continuous | Platelets in blood (kiloplatelets/mL) |
| `serum_creatinine` | Continuous | Level of serum creatinine in blood (mg/dL) |
| `serum_sodium` | Continuous | Level of serum sodium in blood (mEq/L) |
| `time` | Continuous | Follow-up period (days) |
| `anaemia` | Binary | Decrease of red blood cells or hemoglobin (0/1) |
| `diabetes` | Binary | Patient has diabetes (0/1) |
| `high_blood_pressure` | Binary | Patient has hypertension (0/1) |
| `sex` | Binary | Gender (0 = female, 1 = male) |
| `smoking` | Binary | Patient smokes (0/1) |

---

## 2. Experimental Setup

- **Train / Test Split**: 70% training, 30% holdout test (`random_state = 42`)
- **Preprocessing**: `StandardScaler` for linear models
- **Feature Selection**: L1 / Lasso regularization (`alpha = 0.01`)
- **Evaluated Models**:
  - **Logistic Regression**: `max_iter = 1000`
  - **Random Forest**: `n_estimators = 100`, `random_state = 42`
- **Evaluation Metrics**:
  - **Accuracy**: Overall classification accuracy
  - **ROC-AUC**: Area under the ROC Curve (robust to moderate class imbalance)

---

## 3. Results Summary

### 3.1 Feature Selection (Lasso L1)
Lasso penalized regression selected 9 informative clinical indicators out of 12 baseline candidates:
1. `age`
2. `anaemia`
3. `ejection_fraction`
4. `high_blood_pressure`
5. `serum_creatinine`
6. `serum_sodium`
7. `sex`
8. `smoking`
9. `time`

These features align strongly with established cardiological risk factors: cardiac ejection performance (`ejection_fraction`), renal function markers (`serum_creatinine`, `serum_sodium`), and patient baseline demographics.

### 3.2 Model Comparison

| Model | Accuracy | ROC-AUC |
|---|---|---|
| **Logistic Regression** | **0.8000** | 0.8332 |
| **Random Forest** | 0.7556 | **0.8610** |

- **ROC-AUC Champion**: Random Forest achieved **0.8610**, demonstrating superior cohort separation and discrimination.
- **Accuracy Champion**: Logistic Regression achieved **0.8000** on default thresholding.
- For clinical outcome forecasting where ranking calibration is paramount, Random Forest is the preferred architecture.

---

## 4. End-to-End Workflow & Self-Correction

In a traditional manual workflow, variable selection, model tuning, metric calculations, and chart exporting typically require 2–4 hours of iterative scripting across multiple notebooks.

With DeepAnalyze:
- Complete execution completed autonomously in ~20 minutes.
- When an initial column name mismatch occurred during data exploration, the agent captured the runtime exception in its `<Execute>` loop, self-corrected the pandas indexing logic in the next turn, and proceeded to completion without human intervention.
- Produced artifacts: feature importance rankings, confusion matrices, ROC/PR curves, and an empirical summary report.

---

## 5. Reproduction

```bash
cd example/analysis_on_medicine
curl -s -X POST http://localhost:8200/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "DeepAnalyze-8B",
    "messages": [
      {
        "role": "user",
        "content": "Perform Lasso feature selection on heart failure data and benchmark Logistic Regression vs Random Forest."
      }
    ]
  }'
```
