import os
import joblib
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(MODEL_DIR, "intent_bilstm.keras")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")


# Load trained components
model = load_model(MODEL_PATH)
tokenizer = joblib.load(TOKENIZER_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

MAX_LENGTH = 20


def predict_intent(text):
    # Convert text to sequence
    sequence = tokenizer.texts_to_sequences([text])

    # Pad sequence exactly like training
    padded = pad_sequences(
        sequence,
        maxlen=MAX_LENGTH,
        padding="post",
        truncating="post"
    )

    # Predict
    probabilities = model.predict(padded, verbose=0)[0]

    predicted_index = np.argmax(probabilities)
    confidence = probabilities[predicted_index]

    predicted_intent = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    return predicted_intent, confidence


if __name__ == "__main__":

    test_sentences = [
        "How much does this phone cost?",
        "Is this product available?",
        "Do you have this item in stock?",
        "Can you suggest a good phone for me?",
        "Are there any discounts available?",
        "What features does this product have?",
        "Hello",
        "Thank you, goodbye"
    ]

    print("=" * 60)
    print("VOICE SALES AGENT - INTENT PREDICTION TEST")
    print("=" * 60)

    for sentence in test_sentences:

        intent, confidence = predict_intent(sentence)

        print("\nUser:", sentence)
        print("Predicted Intent:", intent)
        print(f"Confidence: {confidence * 100:.2f}%")

    print("\nPrediction testing completed successfully.")