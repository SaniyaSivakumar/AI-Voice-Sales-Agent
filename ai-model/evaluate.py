import os
import joblib
import numpy as np

from tensorflow.keras.models import load_model
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

TEST_DATA_PATH = os.path.join(
    MODEL_DIR,
    "test_data.pkl"
)

LABEL_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "intent_bilstm.keras"
)


# --------------------------------------------------
# 2. Load test data
# --------------------------------------------------

test_data = joblib.load(TEST_DATA_PATH)

X_test = test_data["X_test"]
y_test = test_data["y_test"]


# --------------------------------------------------
# 3. Load label encoder
# --------------------------------------------------

label_encoder = joblib.load(
    LABEL_ENCODER_PATH
)


# --------------------------------------------------
# 4. Load trained BiLSTM model
# --------------------------------------------------

model = load_model(
    MODEL_PATH
)


print("Model loaded successfully.")

print("X_test shape:", X_test.shape)
print("y_test shape:", y_test.shape)

print("Number of classes:", len(label_encoder.classes_))


# --------------------------------------------------
# 5. Make predictions
# --------------------------------------------------

probabilities = model.predict(
    X_test,
    verbose=0
)

y_pred = np.argmax(
    probabilities,
    axis=1
)


# --------------------------------------------------
# 6. Calculate accuracy
# --------------------------------------------------

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\n" + "=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(
    f"\nTest Accuracy: {accuracy * 100:.2f}%"
)


# --------------------------------------------------
# 7. Classification report
# --------------------------------------------------

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# --------------------------------------------------
# 8. Confusion matrix
# --------------------------------------------------

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")

print(cm)


# --------------------------------------------------
# 9. Class names
# --------------------------------------------------

print("\nIntent class order:")

for index, intent in enumerate(
    label_encoder.classes_
):
    print(
        f"{index}: {intent}"
    )


print("\nEvaluation completed successfully.")