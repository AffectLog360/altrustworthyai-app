## Test Definitions

| **Test Case** | **Test Description**                                                                                                              | **Prerequisites**                                                                                                                     | **Inputs**                                                                                                                                                                                                                                        | **Expected Outcome**                                                                                                                                                                                                           |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **#1**        | **Predict Endpoint (14 Features):** Verifies that submitting a valid 14-feature vector to `/predict` returns a single-item prediction array. | 1. The application is running (e.g., `python app.py` or via Docker).<br>2. A trained ExplainableBoostingClassifier (EBM) model is loaded.<br>3. No authentication is required. | **JSON Payload:**<br>`{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India"]}` | 1. Returns **HTTP 200**.<br>2. Response JSON includes `"prediction": ["<class>"]`.<br>3. Prediction list must contain exactly one element.<br>4. Output should reflect model behavior on 14 features. |
| **#2**        | **Predict Endpoint (15 Features):** Verifies that submitting 15 values (14 features + target) still returns a valid prediction by discarding the 15th. | 1. Same as Test #1.                                                                                                                   | **JSON Payload:**<br>`{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]}` | 1. Returns **HTTP 200**.<br>2. Response JSON includes `"prediction": ["<class>"]`.<br>3. Logs contain a warning: “Received 15 features; removing extra.”<br>4. Model processes only the first 14 features. |
| **#3**        | **Explain Endpoint:** Verifies that `/explain` returns global model explanation with names and importance scores.                     | 1. The application is running.<br>2. A trained EBM model is in memory.                                                                | **No input required** (GET request).                                                                                                                                                                                                               | 1. Returns **HTTP 200**.<br>2. Response JSON includes `{"explanation": {"names": [...], "scores": [...], "type": "univariate"}}`.<br>3. Arrays must be non-empty and match model structure. |
| **#4**        | **Model Comparison Endpoint (`/compare`):** Verifies that the endpoint compares EBM and LogisticRegression models using cross-validation. | 1. The application is running.<br>2. Both models (EBM and LogisticRegression) have been trained.<br>3. Required dependencies are installed. | **No input required** (GET request).                                                                                                                                                                                                               | 1. Returns **HTTP 200**.<br>2. Response includes `{"comparison": {<model metrics>}}`.<br>3. Keys include `Baseline_LogisticRegression_cv_scores`, `EBM_cv_scores`, and their mean accuracies.<br>4. Output must reflect 5-fold CV results. |
| **#5**        | **Missing Value Warning (During Training):** Verifies that the system logs a warning if missing values are detected during model training. | 1. Dataset includes missing values.<br>2. Model training is triggered by running the application.                                      | No specific input beyond standard data usage.                                                                                                                                                                                                      | 1. **HTTP 200** for training.<br>2. Logs include: “Missing values detected…” warning.<br>3. Verifies visibility of missing value handling and model interpretability risks. |

---

## Manual Reproducibility

### 1. Set Up the Component

- Ensure **Python 3.9+** or Docker is installed.
- Install dependencies:

```bash
pip install -r requirements.txt
```

or build with Docker:

```bash
docker compose build
```

---

### 2. Run the Application

- **Local (venv):**

```bash
python app.py
```

- **Docker:**

```bash
docker compose up app
```

---

### 3. Execute the Test Cases

#### Test #1 – 14 Feature Prediction

```bash
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [30,"State-gov",141297,"Bachelors",13,"Married-civ-spouse","Prof-specialty","Husband","Asian-Pac-Islander","Male",0,0,40,"India"]}'
```

- Expect response:

```json
{"prediction":[">50K"]}
```

---

#### Test #2 – 15 Feature Prediction (Extra Target)

```bash
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [30,"State-gov",141297,"Bachelors",13,"Married-civ-spouse","Prof-specialty","Husband","Asian-Pac-Islander","Male",0,0,40,"India",">50K"]}'
```

- Expect valid response and a log warning:

```text
Received 15 features; removing extra.
```

---

#### Test #3 – Global Explanation

```bash
curl -X GET http://localhost:5002/explain
```

- Expect JSON response including:

```json
{
  "explanation": {
    "names": [...],
    "scores": [...],
    "type": "univariate"
  }
}
```

---

#### Test #4 – Model Comparison

```bash
curl -X GET http://localhost:5002/compare
```

- Expect:

```json
{
  "comparison": {
    "Baseline_LogisticRegression_cv_scores": [...],
    "Baseline_LogisticRegression_mean_accuracy": ...,
    "EBM_cv_scores": [...],
    "EBM_mean_accuracy": ...
  }
}
```

---

### 4. Validate Results

- Check HTTP status (must be 200).
- Compare the JSON structure and contents with expected output.
- Verify any expected logs (e.g., missing value or dimension warnings).

If results match expectations, the test **passes**. Any structural or output deviations indicate **failure**.
