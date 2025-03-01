# Detailed Documentation for AI Risk Assessment

## ALTrustworthyAI Application Overview

**ALTrustworthyAI Application** is engineered to deliver robust AI risk assessment by providing interpretable model predictions and global explanations using the Census Adult dataset. By quantifying feature importance and identifying key drivers of model behavior, the application enables stakeholders to:
- Translate complex model decisions into transparent, actionable insights.
- Flag anomalies and potential bias via detailed fairness metrics.
- Support continuous model monitoring and auditability.

The application is fully aligned with the approved design document, which defines ALT-AI as a toolbox that offers both global (overall model behavior) and local (individual prediction) explanations. These explanations empower data scientists, auditors, and compliance officers to assess potential biases—especially those linked to protected attributes (e.g., age, gender, race)—and ensure compliance with regulations such as GDPR and the evolving EU AI Act.

---

# Stage 2: Unit Testing and Component-Level Testing

## Prerequisites

- **Internal Unit Testing:**  
  Unit tests are defined in `test_app.py` and cover the core functions such as prediction and explanation.
- **Test Environment Setup:**  
  Use the native Python virtual environment (venv) as described in Stage 1.
- **Supporting Files:**  
  - `Makefile` and `run_tests.sh` for local testing  
  - Dockerfile/docker-compose.yml for containerized testing in a Linux VM (if necessary)

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

Below is the detailed functional testing report template for the ALTrustworthyAI Application.

[Functional Testing / 3: Test Execution for Component - AffectLog](https://docs.google.com/document/d/1SOZA9vsB7mkRtE6MP53y43FE6DLxPCnfkRuR-eHF6rc/edit?tab=t.0#heading=h.yu252ceyiwp) 
