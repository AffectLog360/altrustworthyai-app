import pandas as pd

def load_and_preprocess_data():
    """
    Loads and preprocesses the UCI Census Adult dataset for binary income prediction.
    The dataset includes 15 columns; the first 14 columns are features and the last column ('income')
    is the binary target indicating whether income is '>50K' or '<=50K'. This preprocessing:
      - Reads the dataset from the UCI repository.
      - Drops rows with missing target values.
      - Splits the dataset into training and test sets.
    This process ensures that the model is trained on clean, reliable data—essential for generating
    transparent predictions and fairness metrics for AI risk assessment.
    
    Returns:
        X_train, X_test, y_train, y_test: Preprocessed features (14 columns) and income targets.
    """
    URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num",
        "marital-status", "occupation", "relationship", "race", "sex",
        "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"
    ]
    
    # Read the dataset using a raw string for the separator to avoid invalid escape sequence warnings.
    df = pd.read_csv(URL, names=column_names, sep=r",\s", na_values="?", engine="python")
    
    # Drop rows where the target ("income") is missing.
    df = df.dropna(subset=["income"])
    
    # Split into training and test sets.
    train = df.sample(frac=0.8, random_state=42)
    test = df.drop(train.index)
    
    # Use the first 14 columns as features; "income" is the target.
    X_train = train.drop("income", axis=1)
    y_train = train["income"]
    X_test = test.drop("income", axis=1)
    y_test = test["income"]
    
    return X_train, X_test, y_train, y_test
