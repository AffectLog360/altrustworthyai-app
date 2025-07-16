# **Note:** The development repository at https://github.com/AffectLog360/altrustworthyai-app has been moved and is no longer the primary source. All development and collaboration should now occur through the Prometheus-X repository.

# ALTrustworthyAI Application Documentation

## Overview

**ALTrustworthyAI Application** is engineered to deliver robust AI risk assessment by providing interpretable model predictions and global explanations using the Census Adult dataset. By quantifying feature importance and identifying key drivers of model behavior, the application enables stakeholders to:

- Translate complex model decisions into transparent, actionable insights.
- Flag anomalies and potential bias via detailed fairness metrics.
- Support continuous model monitoring and auditability.

The application is fully aligned with the approved design document, which defines ALT-AI as a toolbox that offers both global (overall model behavior) and local (individual prediction) explanations. These outputs empower data scientists, auditors, and compliance officers to assess potential biases—especially those linked to protected attributes (e.g., age, gender, race)—and ensure compliance with regulations such as GDPR and the evolving EU AI Act.

---

# Stage 1: Building and Deployment

## Prerequisites

- **Design Document:**  
  *AffectLog's Trustworthy AI (ALT-AI) - Design Document*  
  [View Design Document](https://github.com/Prometheus-X-association/t-ai-affectlog/blob/main/docs/design-document.md)  
  This document outlines the ALT-AI architecture and functionalities emphasizing transparency, interpretability, and fairness. It details how global and local explanations empower AI risk assessment by quantifying feature importance and highlighting potential biases.

- **Test Definitions:**  
  [ALT-AI Test Definitions](https://github.com/Prometheus-X-association/t-ai-affectlog/blob/main/docs/design-document.md#test-specification)  
  These definitions cover detailed scenarios for model explanation, fairness evaluation, and compliance testing.

- **Containerization Files:**  
  - Dockerfile  
  - docker-compose.yml  
  Note: Due to container instability on the Mac M4, local development is recommended using a Python virtual environment (venv). For production deployments, use a Linux VM (e.g., via UTM) to support high-performance AI risk assessment.

- **Disclaimer:**  
  The provided code and container files are for demonstration and validation purposes. Testers should ensure proper system configuration and follow security best practices when deploying in production environments.

## Cloning the Repository

```bash
git clone https://github.com/AffectLog360/altrustworthyai-app.git
```

## Build Commands

### Local Setup (Using Virtual Environment)

1. Create and activate the virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies:

```bash
cd altrustworthyai-app
pip install --upgrade pip && pip install -r requirements.txt
```

3. Build/Train the application:

```bash
python app.py
```

Or use the Makefile:

```bash
make install
```

---

## Run Commands

### Local Run (venv)

Start the application:

```bash
python app.py
```

Or via the Makefile:

```bash
make run
```

The application runs on port 5002 and can be accessed via:

- http://127.0.0.1:5002
- http://[your-local-IP]:5002

---

## Demonstration of Working Endpoints

### 1. POST /predict

Generates a binary income prediction from an input feature vector. The model expects 14 features. If the payload includes a 15th value (target), it is automatically discarded.

**Example Input:**

```bash
curl -X POST http://localhost:5002/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]}'
```

**Expected Output:**

```json
{"prediction":[">50K"]}
```

The model drops the 15th value and makes a prediction using the first 14 features.

---

### 2. GET /explain

Returns a global explanation of the model including feature names and importance scores.

**Example Input:**

```bash
curl -X GET http://localhost:5002/explain
```

**Expected Output:**

```json
{
  "explanation": {
    "names": ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "age & fnlwgt", "age & education", "age & education-num", "age & occupation", "age & relationship", "fnlwgt & education", "fnlwgt & education-num", "fnlwgt & occupation", "fnlwgt & capital-gain", "education & occupation", "education-num & occupation", "education-num & relationship", "education-num & hours-per-week"],
    "scores": [0.10030026144908563, 0.03664318379769542, 0.24975116765419172, 0.1488645646615102, 0.20944761139323734, 0.42322504057033855, 0.12574066502535564, 0.5710896729423394, 0.011000480682267213, 0.33181536652471005, 0.2593678397039449, 0.07728615199109472, 0.16042266115260645, 0.028367282938769764, 0.07067067727366978, 0.040491572478995506, 0.08526054194318065, 0.057883992020588505, 0.1645009854216891, 0.09860817273793579, 0.047694463840421995, 0.10801773717623105, 0.11770528313943834, 0.03328933954001463, 0.021476448749105464, 0.20432854299840708, 0.06396007310885912],
    "type": "univariate"
  }
}
```

This allows stakeholders to understand feature importance and interaction terms.

---

### 3. GET /compare

Returns a model comparison between the ExplainableBoostingClassifier and a baseline LogisticRegression model, using 5-fold cross-validation.

**Example Input:**

```bash
curl http://localhost:5002/compare
```

**Sample Output:**

```json
{
  "comparison": {
    "Baseline_LogisticRegression_cv_scores": [0.9, 0.95, 0.75, 0.75, 0.85],
    "Baseline_LogisticRegression_mean_accuracy": 0.8400000000000001,
    "EBM_cv_scores": [0.85, 0.8, 0.85, 0.75, 0.85],
    "EBM_mean_accuracy": 0.82
  }
}
```

This comparison helps validate whether interpretable models offer competitive performance compared to standard baselines.

---

# Stage 2: Unit Testing and Component-Level Testing

## Prerequisites

- Internal unit testing is implemented in `test_app.py`.
- Test environment setup uses virtualenv as in Stage 1.
- Supporting files:
  - `Makefile`
  - `run_tests.sh`
  - `Dockerfile`, `docker-compose.yml` for container-based testing (optional)

## Running the Tests

Using Makefile:

```bash
make test
```

Or directly:

```bash
python -m unittest discover -s . -p "test_app.py"
```

## Test Execution Report

Refer to the report for validation details:

[Functional Testing – Test Execution](https://docs.google.com/document/d/1SOZA9vsB7mkRtE6MP53y43FE6DLxPCnfkRuR-eHF6rc/edit?usp=sharing)

---
