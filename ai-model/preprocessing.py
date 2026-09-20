import json
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "intents.json"
)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)


texts = []
labels = []

for intent_data in data["intents"]:
    intent = intent_data["intent"]

    for example in intent_data["examples"]:
        texts.append(example)
        labels.append(intent)


print("Dataset loaded successfully.")
print("Total examples:", len(texts))
print("Total intents:", len(set(labels)))


# --------------------------------------------------
# 3. Train / test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=42,
    stratify=labels
)


print("\nData split:")
print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))


# --------------------------------------------------
# 4. Text tokenization
# --------------------------------------------------

MAX_WORDS = 2000
MAX_SEQUENCE_LENGTH = 20

tokenizer = Tokenizer(
    num_words=MAX_WORDS,
    oov_token="<OOV>"
)

# IMPORTANT:
# Fit tokenizer only on training data
tokenizer.fit_on_texts(X_train)


X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_test_sequences = tokenizer.texts_to_sequences(X_test)


# --------------------------------------------------
# 5. Padding
# --------------------------------------------------

X_train_padded = pad_sequences(
    X_train_sequences,
    maxlen=MAX_SEQUENCE_LENGTH,
    padding="post",
    truncating="post"
)

X_test_padded = pad_sequences(
    X_test_sequences,
    maxlen=MAX_SEQUENCE_LENGTH,
    padding="post",
    truncating="post"
)


# --------------------------------------------------
# 6. Encode intent labels
# --------------------------------------------------

label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)


print("\nIntent classes:")

for index, intent in enumerate(label_encoder.classes_):
    print(index, "->", intent)


# --------------------------------------------------
# 7. Save preprocessing artifacts
# --------------------------------------------------

tokenizer_path = os.path.join(
    OUTPUT_DIR,
    "tokenizer.pkl"
)

label_encoder_path = os.path.join(
    OUTPUT_DIR,
    "label_encoder.pkl"
)

train_data_path = os.path.join(
    OUTPUT_DIR,
    "train_data.pkl"
)

test_data_path = os.path.join(
    OUTPUT_DIR,
    "test_data.pkl"
)


joblib.dump(tokenizer, tokenizer_path)

joblib.dump(
    label_encoder,
    label_encoder_path
)

joblib.dump(
    {
        "X_train": X_train_padded,
        "y_train": y_train_encoded
    },
    train_data_path
)

joblib.dump(
    {
        "X_test": X_test_padded,
        "y_test": y_test_encoded
    },
    test_data_path
)


# --------------------------------------------------
# 8. Final information
# --------------------------------------------------

print("\nPreprocessing completed successfully.")

print("\nShapes:")
print("X_train:", X_train_padded.shape)
print("y_train:", y_train_encoded.shape)

print("X_test:", X_test_padded.shape)
print("y_test:", y_test_encoded.shape)

print("\nSaved files:")
print("tokenizer.pkl")
print("label_encoder.pkl")
print("train_data.pkl")
print("test_data.pkl")