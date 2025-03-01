# ALTrustworthyAI Application

The **ALTrustworthyAI Application** is a production‑ready application that provides interpretable predictions and global explanations using the UCI Census Adult dataset. This tool is designed to power robust AI risk assessment by delivering fairness metrics and transparency in income predictions. Its outputs help auditors, data scientists, and compliance officers evaluate whether model decisions are influenced disproportionately by protected attributes (such as age, gender, and race) and ensure that the model complies with regulations (e.g., GDPR, EU AI Act).

## Features

- **Transparent Predictions:**  
  Generates binary income predictions (">50K" vs. "<=50K") using 14 features extracted from the Census Adult dataset.
  
- **Global Explanations:**  
  Provides a detailed breakdown of feature importance—including interaction effects—to explain model decisions and support fairness assessments.

- **Fairness Analysis:**  
  Enables evaluation of potential biases by highlighting the impact of protected attributes on model predictions.

## Technical Overview

The application leverages a native boosting library (dynamically located at runtime) for high-performance computations. It uses an ExplainableBoostingClassifier to train a model on a reduced subset of the dataset for development purposes, then generates predictions and global explanations.

## Prerequisites

- **Design Document:**  
  [AffectLog's Trustworthy AI (ALT-AI) - Design Document](https://github.com/Prometheus-X-association/t-ai-affectlog/blob/main/docs/design-document.md)

- **Test Definitions:**  
  [ALT-AI Test Definitions](https://example.com/alt-ai-test-definitions)

- **Technical Documentation:**  
  [ALT-AI Technical Documentation](https://example.com/alt-ai-technical-docs)

## Installation and Build

### Local Setup (Using Virtual Environment)

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-repo/altrustworthyai-adult-app.git
   cd altrustworthyai-adult-app
   ```

2. **Create and Activate the Virtual Environment:**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```

4. **Build/Train the Application:**

   Running the app trains the model on a reduced subset of the Census Adult dataset using 13 features (the target is removed). This training is crucial to power AI risk assessment by generating transparent predictions and fairness metrics.

   ```bash
   python app.py
   ```

   Or, via the Makefile:

   ```bash
   make install
   ```

### Container Deployment

For containerized deployments (recommended on a Linux VM, e.g., via UTM):

1. **Build the Container Image:**

   ```bash
   docker-compose build
   ```

2. **Run the Application Container:**

   ```bash
   docker-compose up app
   ```

3. **Run Tests in Container:**

   ```bash
   docker-compose up tests
   ```

## Running the Application

### Local Execution

Start the application using the virtual environment:

```bash
python app.py
```

Or, using the Makefile:

```bash
make run
```

The app will be available on port **5002**:
- [http://127.0.0.1:5002](http://127.0.0.1:5002)
- [http://[your-local-IP]:5002](http://[your-local-IP]:5002)

## Testing Fairness

Fairness is evaluated by comparing model predictions and global explanations:

1. **Test Prediction Endpoint:**

   Send a complete data row (15 values) where the target is included. The app will automatically remove the last value (target) and predict based on 14 features:

   ```bash
   curl -X POST http://localhost:5002/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse", "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]}'
   ```

   *Expected Output:*

   ```json
   {"prediction":[">50K"]}
   ```

2. **Test Explanation Endpoint:**

   Retrieve the global explanation to assess how features (including protected attributes) impact predictions:

   ```bash
   curl -X GET http://localhost:5002/explain
   ```

   *Expected Output:*  
   An explanation JSON that includes feature names and their importance scores. Review the scores for attributes like age, race, and sex to assess fairness.

3. **Run the Complete Test Suite:**

   ```bash
   make test
   ```

   This command runs all unit tests and verifies that the endpoints return the correct outputs.
