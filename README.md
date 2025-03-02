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
  *This document outlines the ALT-AI architecture and functionalities emphasizing transparency, interpretability, and fairness. It details how global and local explanations empower AI risk assessment by quantifying feature importance and highlighting potential biases.*

- **Test Definitions:**  
  [ALT-AI Test Definitions](https://github.com/Prometheus-X-association/t-ai-affectlog/blob/main/docs/design-document.md#test-specification)  
  *These definitions cover detailed scenarios for model explanation, fairness evaluation, and compliance testing.*

- **Containerization Files:**  
  - Dockerfile  
  - docker-compose.yml  
  *Note: Due to container instability on the Mac M4, local development is recommended using a Python virtual environment (venv). For production deployments, use a Linux VM (e.g., via UTM) to support high-performance AI risk assessment.*

- **Disclaimer:**  
  The provided code and container files are for demonstration and validation purposes. Testers should ensure proper system configuration and follow security best practices when deploying in production environments.

## Cloning the Repository

For validation, clone the ALTrustworthyAI Application repository:

```bash
git clone https://github.com/AffectLog360/altrustworthyai-app.git
cd altrustworthyai-app
```

## Build Commands

### Local Setup (Using Virtual Environment)

1. **Create and Activate the Virtual Environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

2. **Install Dependencies:**

   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```

3. **Build/Train the Application:**

   Running the app triggers model training on a reduced dataset extracted from the Census Adult dataset. The ExplainableBoostingClassifier is trained on 13 features (target removed), enabling generation of transparent predictions and global explanations essential for AI risk assessment.

   ```bash
   python app.py
   ```

   Alternatively, use the Makefile:

   ```bash
   make install
   ```

### Container Build (For Linux VM Deployment)

1. **Build the Container Image:**

   ```bash
   docker-compose build
   ```

---

## Run Commands

### Local Run (venv)

- **Start the Application:**

  ```bash
  python app.py
  ```
  
  Or via the Makefile:

  ```bash
  make run
  ```

  The application runs on port **5002** and can be accessed via:
  - [http://127.0.0.1:5002](http://127.0.0.1:5002)
  - [http://[your-local-IP]:5002](http://[your-local-IP]:5002)

### Container Run (Inside a Linux VM via UTM)

- **Run the Application Container:**

  ```bash
  docker-compose up app
  ```

---

## Demonstration of Working Endpoints

The **ALTrustworthyAI Application** powers AI risk assessment by:

- **Explaining Model Behavior:**  
  Global explanations quantify the influence of each feature on the prediction, helping auditors pinpoint potential biases.

- **Ensuring Compliance:**  
  Transparent explanations support compliance with regulations (e.g., GDPR, EU AI Act) by providing insight into the decision process.

- **Assessing Fairness:**  
  Detailed feature importance scores and interaction metrics enable fairness analysis by revealing how protected attributes impact predictions.

### 1. POST /predict Endpoint

- **Function:**  
  Generates a binary income prediction from an input feature vector. The model expects 14 features (all columns except the target). If the payload includes the target column (15 values), the application automatically removes the last value.

- **Input Interpretation:**  
  For example, if a payload is submitted as:  
  ```bash
  [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]
  ```
  The app removes the last element (">50K") and uses the first 14 values to generate a prediction.

- **Example Input (via curl):**

  ```bash
  curl -X POST http://localhost:5002/predict \
    -H "Content-Type: application/json" \
    -d '{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]}'
  ```

- **Expected Output:**

  ```json
  {"prediction":[">50K"]}
  ```

  *Interpretation:*  
  The prediction “>50K” indicates that the model classifies the individual’s income as above 50K based on the processed 14-feature vector. This outcome is critical for AI risk assessment, allowing auditors to evaluate whether the model is fair and unbiased.

### 2. GET /explain Endpoint

- **Function:**  
  Returns a global explanation of the model’s behavior, including a list of feature names and their corresponding importance scores.

- **Example Command:**

  ```bash
  curl -X GET http://localhost:5002/explain
  ```

- **Expected Output:**

  ```json
  {
    "explanation": {
      "names": ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "age & fnlwgt", "age & education", "age & education-num", "age & occupation", "age & relationship", "fnlwgt & education", "fnlwgt & education-num", "fnlwgt & occupation", "fnlwgt & capital-gain", "education & occupation", "education-num & occupation", "education-num & relationship", "education-num & hours-per-week"],
      "scores": [0.10030026144908563, 0.03664318379769542, 0.24975116765419172, 0.1488645646615102, 0.20944761139323734, 0.42322504057033855, 0.12574066502535564, 0.5710896729423394, 0.011000480682267213, 0.33181536652471005, 0.2593678397039449, 0.07728615199109472, 0.16042266115260645, 0.028367282938769764, 0.07067067727366978, 0.040491572478995506, 0.08526054194318065, 0.057883992020588505, 0.1645009854216891, 0.09860817273793579, 0.047694463840421995, 0.10801773717623105, 0.11770528313943834, 0.03328933954001463, 0.021476448749105464, 0.20432854299840708, 0.06396007310885912],
      "type": "univariate"
    }
  }
  ```

  *Interpretation:*  
  The explanation output details the influence of each feature (and key interaction terms) on the prediction. Auditors can use these scores to assess if protected attributes (such as age, race, or sex) are exerting disproportionate influence, which would indicate potential fairness issues.

---

# Stage 2: Unit Testing and Component-Level Testing

## Prerequisites

- **Internal Unit Testing:**  
  Unit tests are defined in `test_app.py` to validate core functionalities (e.g., prediction and explanation).
- **Test Environment Setup:**  
  Use the native Python virtual environment (venv) as described in Stage 1.
- **Supporting Files:**  
  - Makefile and run_tests.sh for local test execution.
  - Dockerfile/docker-compose.yml for containerized testing (if needed).

## Commands to Run Tests

- **Using Makefile:**

  ```bash
  make test
  ```

- **Direct Command:**

  ```bash
  python -m unittest discover -s . -p "test_app.py"
  ```

## Test Execution Report / Summary

[Functional testing / 3: Test execution - AffectLog](https://docs.google.com/document/d/1SOZA9vsB7mkRtE6MP53y43FE6DLxPCnfkRuR-eHF6rc/edit?usp=sharing) is the detailed report for the functional testing of the ALTrustworthyAI Application.

---
