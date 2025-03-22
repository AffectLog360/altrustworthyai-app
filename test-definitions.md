## Test Definitions

| **Test Case** | **Test Description**                                                                                                              | **Prerequisites**                                                                                                                     | **Inputs**                                                                                                                                                                                                                                        | **Expected Outcome**                                                                                                                                                                                                           |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **#1**       | **Predict Endpoint**: Verifies that submitting a valid feature vector (14 features) to `/predict` returns a single‐item prediction array. | 1. The application is running (started via `python app.py` or in Docker).<br>2. A trained EBM model is loaded within the Flask app.<br>3. No credentials are required for `/predict`. | **Feature Payload** (JSON):<br>`{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India"]}` <br>(14 features, no target)                                | 1. **HTTP 200** response code.<br>2. JSON body with a `"prediction"` key, e.g. `{"prediction": [">50K"]}` or `[0]` or `[1]`. <br>3. The `"prediction"` value must be a list with exactly one element. <br>4. Easy to verify: compare the single predicted class with expected structure (a one‐element list). |
| **#2**       | **Predict Endpoint (Extra Feature)**: Verifies that submitting 15 values (i.e., including the target) still returns a valid prediction, discarding the 15th. | 1. Same as above (app running, model loaded).                                                                                          | **Feature Payload** (JSON):<br>`{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]}` <br>(15 features, last is target).              | 1. **HTTP 200** response code.<br>2. JSON body with a `"prediction"` key containing a single‐item list.<br>3. The logs or console show a warning: “Received 15 features; ... removing it.”<br>4. Verifiable by checking if the model predicts using 14 features (the last one is discarded). |
| **#3**       | **Explain Endpoint**: Verifies that the `/explain` endpoint returns a global explanation including feature names and importance scores.   | 1. The application is running.<br>2. A trained EBM model is in memory.                                                                 | **No input** (GET request).                                                                                                                                                                                                                       | 1. **HTTP 200** response code.<br>2. JSON body with an `"explanation"` object containing a `"names"` list and a `"scores"` list.<br>3. Verifiable by checking these arrays are present and non‐empty (e.g. `explanation["names"]`, `explanation["scores"]`).                          |
| **#4**       | **Validation of Missing Values** (optional) — If the dataset has missing values, the model warns.                                   | 1. The application is running with a dataset containing missing fields.<br>2. The model has been trained (which might log warnings). | **Feature Payload** or normal usage that triggers the model training phase.                                                                                                                                                                        | 1. **HTTP 200** if model training or predictions succeed.<br>2. A **UserWarning** in logs: “Missing values detected...”<br>3. The test can confirm whether the system prints/logs a warning, ensuring that the user is aware of missing data.                         |

---

## Manual Reproducibility

### 1. Set up the Component
- Ensure Python 3.9+ or Docker is installed.
- Run `pip install -r requirements.txt` or `docker-compose build`.

### 2. Run the App
- **Local**: `python app.py` (listening on port 5002).
- **Docker**: `docker-compose up app`.

### 3. Execute the Test Cases
- **Test #1**:  
  ```bash
  curl -X POST http://localhost:5002/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [30,"State-gov",141297,"Bachelors",13,"Married-civ-spouse","Prof-specialty","Husband","Asian-Pac-Islander","Male",0,0,40,"India"]}'
  ```
  - Check for `{"prediction": ["..."]}` with a single item.

- **Test #2**:  
  ```bash
  curl -X POST http://localhost:5002/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [30,"State-gov",141297,"Bachelors",13,"Married-civ-spouse","Prof-specialty","Husband","Asian-Pac-Islander","Male",0,0,40,"India",">50K"]}'
  ```
  - Check logs for warning about 15 features.  
  - Confirm the `{"prediction": [... ]}` single item response is valid.

- **Test #3**:  
  ```bash
  curl -X GET http://localhost:5002/explain
  ```
  - Expect a JSON with `{"explanation": {"names": [...], "scores": [...]}}`.

### 4. Compare Expected vs. Actual
- If the HTTP responses and JSON structures match the “Expected Outcome” columns above, the test **passes**.
- If there’s any mismatch (wrong status, missing fields), the test **fails**.
