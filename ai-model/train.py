import os
import joblib
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))

TRAIN_DATA_PATH = os.path.join(
    MODEL_DIR,
    "train_data.pkl"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "intent_bilstm.keras"
)


# --------------------------------------------------
# 2. Load preprocessed data
# --------------------------------------------------

train_data = joblib.load(TRAIN_DATA_PATH)

X_train = train_data["X_train"]
y_train = train_data["y_train"]


print("Training data loaded successfully.")
print("X_train shape:", X_train.shape)
print("y_train shape:", y_train.shape)


# --------------------------------------------------
# 3. Load tokenizer
# --------------------------------------------------

tokenizer_path = os.path.join(
    MODEL_DIR,
    "tokenizer.pkl"
)

tokenizer = joblib.load(tokenizer_path)

vocab_size = min(
    2000,
    len(tokenizer.word_index) + 1
)

print("Vocabulary size:", vocab_size)


# --------------------------------------------------
# 4. Load label encoder
# --------------------------------------------------

label_encoder_path = os.path.join(
    MODEL_DIR,
    "label_encoder.pkl"
)

label_encoder = joblib.load(label_encoder_path)

num_classes = len(label_encoder.classes_)

print("Number of intent classes:", num_classes)


# --------------------------------------------------
# 5. Build BiLSTM model
# --------------------------------------------------

model = Sequential([
    
    Embedding(
        input_dim=vocab_size,
        output_dim=64,
        input_length=X_train.shape[1]
    ),

    Bidirectional(
        LSTM(64)
    ),

    Dropout(0.5),

    Dense(
        32,
        activation="relu"
    ),

    Dropout(0.3),

    Dense(
        num_classes,
        activation="softmax"
    )
])


# --------------------------------------------------
# 6. Compile model
# --------------------------------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# --------------------------------------------------
# 7. Display architecture
# --------------------------------------------------

print("\nModel architecture:\n")

model.summary()


# --------------------------------------------------
# 8. Early stopping
# --------------------------------------------------

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=8,
    restore_best_weights=True
)


# --------------------------------------------------
# 9. Train model
# --------------------------------------------------

print("\nStarting BiLSTM training...\n")

history = model.fit(
    X_train,
    y_train,
    validation_split=0.20,
    epochs=50,
    batch_size=16,
    callbacks=[early_stopping],
    verbose=1
)


# --------------------------------------------------
# 10. Save trained model
# --------------------------------------------------

model.save(MODEL_PATH)

print("\nTraining completed successfully.")

print("\nModel saved at:")
print(MODEL_PATH)

print("\nBest validation accuracy:")

best_val_accuracy = max(
    history.history["val_accuracy"]
)

print(
    f"{best_val_accuracy * 100:.2f}%"
)