import os
import cv2
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

# ==========================
# SETTINGS
# ==========================

DATASET_PATH = "dataset"

IMG_WIDTH = 160
IMG_HEIGHT = 75
CAPTCHA_LEN = 6

# ==========================
# LOAD DATASET
# ==========================

images = []
labels = []

for file in os.listdir(DATASET_PATH):

    if not file.endswith(".png"):
        continue

    # label = first part of filename
    label = file.split("_")[0][:6]

    if len(label) != CAPTCHA_LEN:
        print("Skipping bad label:", file)
        continue

    img_path = os.path.join(DATASET_PATH, file)

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))

    img = img / 255.0

    images.append(img)
    labels.append(label)

images = np.array(images).reshape(-1, IMG_HEIGHT, IMG_WIDTH, 1)

print("Images loaded:", len(images))

# ==========================
# CHARACTER SET
# ==========================

characters = sorted(list(set("".join(labels))))

print("Character set:", characters)

char_to_num = {c:i for i,c in enumerate(characters)}
num_to_char = {i:c for i,c in enumerate(characters)}

def encode_label(label):
    return [char_to_num[c] for c in label]

encoded_labels = np.array([encode_label(l) for l in labels])

# ==========================
# TRAIN TEST SPLIT
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    images,
    encoded_labels,
    test_size=0.2,
    random_state=42
)

# ==========================
# MODEL
# ==========================

model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1)),

    tf.keras.layers.Conv2D(32,(3,3),activation="relu"),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Conv2D(64,(3,3),activation="relu"),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Conv2D(128,(3,3),activation="relu"),
    tf.keras.layers.MaxPooling2D((2,2)),

    tf.keras.layers.Flatten(),

    tf.keras.layers.Dense(512,activation="relu"),

    tf.keras.layers.Dense(CAPTCHA_LEN * len(characters),activation="softmax"),

    tf.keras.layers.Reshape((CAPTCHA_LEN,len(characters)))

])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==========================
# TRAIN
# ==========================

history = model.fit(

    X_train,
    y_train,

    validation_data=(X_test,y_test),

    epochs=20,
    batch_size=16

)

# ==========================
# SAVE MODEL
# ==========================

model.save("captcha_test_model.h5")

print("\nModel saved.")