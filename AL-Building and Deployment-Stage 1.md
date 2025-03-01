# Detailed Documentation for AI Risk Assessment

## ALTrustworthyAI Application Overview

**ALTrustworthyAI Application** is engineered to deliver robust AI risk assessment by providing interpretable model predictions and global explanations using the Census Adult dataset. By quantifying feature importance and identifying key drivers of model behavior, the application enables stakeholders to:
- Translate complex model decisions into transparent, actionable insights.
- Flag anomalies and potential bias via detailed fairness metrics.
- Support continuous model monitoring and auditability.

The application is fully aligned with the design document, which defines ALT-AI as a toolbox that offers both global (overall model behavior) and local (individual prediction) explanations. These explanations empower data scientists, auditors, and compliance officers to assess potential biases—especially those linked to protected attributes (e.g., age, gender, race)—and ensure compliance with regulations such as GDPR and the evolving EU AI Act.

---

# Stage 1: Building and Deployment

## Prerequisites

- **Test Definitions within Design Document:**  
  *AffectLog's Trustworthy AI (ALT-AI) - Design Document*  
  [View Design Document](https://github.com/Prometheus-X-association/t-ai-affectlog/blob/main/docs/design-document.md#test-specification)  
  *This document details the ALT-AI architecture, transparency and fairness features, and explains how global and local explanations support AI risk assessment by quantifying feature importance and highlighting potential biases.*

- **Containerization Files:**  
  - Dockerfile  
  - docker-compose.yml

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

   Running the app initiates model training on a reduced dataset extracted from the Census Adult data. The model is trained using 13 features (with the target income column removed), and it produces both predictions and transparent global explanations that are critical for risk assessment and fairness analysis.

   ```bash
   python app.py
   ```

   Or, via the provided Makefile:

   ```bash
   make install
   ```

### Container Build (For Linux VM Deployment)

1. **Build the Container Image:**

   ```bash
   docker-compose build
   ```

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

  The application runs on port **5002** and is accessible via:
  - http://127.0.0.1:5002  
  - http://[your-local-IP]:5002

### Container Run (Inside a Linux VM via UTM)

- **Run the Application Container:**

  ```bash
  docker-compose up app
  ```

## Demonstration of Working Endpoints

The ALTrustworthyAI Application powers AI risk assessment by:

- **Explaining Model Behavior:**  
  The global explanation output quantifies the influence of each feature on the prediction. By examining feature importance, stakeholders can determine whether protected attributes (such as age, gender, or race) disproportionately affect predictions.

- **Ensuring Compliance:**  
  Transparent explanations help ensure that model decisions are interpretable and that any potential biases are flagged—supporting regulatory compliance (e.g., GDPR, EU AI Act).

- **Supporting Fairness Analysis:**  
  Detailed importance scores serve as fairness metrics. They enable continuous monitoring and auditability by revealing the extent to which individual features impact model outcomes.

### 1. POST /predict Endpoint

- **Function:**  
  Generates a binary income prediction based on an input feature vector.  
  *Important:* The model expects 14 features (i.e. all columns except the target income). If a payload includes the target column (15 values), the system automatically removes the last element to ensure consistent input.

- **Input Interpretation:**  
  For example, if a payload is sent as:
  
  ```
  [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]
  ```
  
  the application will remove the last value (">50K") and use the first 14 values to make the prediction.

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
  The prediction “>50K” indicates that the model, after adjusting the input to the expected 14 features, classifies the individual’s income as above 50K. This outcome is crucial for risk assessment, as it feeds into fairness evaluation by showing how demographic and socioeconomic factors contribute to the prediction.

### 2. GET /explain Endpoint

- **Function:**  
  Provides a global explanation of the model by returning a list of feature names and corresponding importance scores.  
  *This output is used for fairness assessment by revealing how each attribute—including protected features—impacts the model’s decision-making process.*

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
  The explanation details the relative importance of each feature (and certain interaction terms) in the model's decision process. Auditors can inspect the scores for protected attributes like age, race, and sex to determine if these features exert undue influence on income prediction, which is critical for fairness assessment.
