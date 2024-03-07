import os
import numpy as np
import cv2
import glob
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from model import build_model
from metrics import dice_loss, dice_coef
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def load_dataset(path, split=0.2):
    images = sorted(glob.glob(os.path.join(path, "x-rays", "*.png")))
    masks = sorted(glob.glob(os.path.join(path, "masks", "*.png")))

    split_size = int(len(images) * split)

    train_x, valid_x = train_test_split(images, test_size=split_size, random_state=42)
    train_y, valid_y = train_test_split(masks, test_size=split_size, random_state=42)
    train_x, test_x = train_test_split(train_x, test_size=split_size, random_state=42)
    train_y, test_y = train_test_split(train_y, test_size=split_size, random_state=42)

    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)

def read_image(path):
    path = path.decode()
    x = cv2.imread(path, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (IMAGE_WIDTH, IMAGE_HEIGHT))
    x = x / 255.0
    return x.astype(np.float32)

def read_mask(path):
    path = path.decode()
    x = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x = cv2.resize(x, (IMAGE_WIDTH, IMAGE_HEIGHT)) / 255.0
    return np.expand_dims(x, axis=-1).astype(np.float32)

def tf_parse(x, y):
    def _parse(x, y):
        x = read_image(x)
        y = read_mask(y)
        return x, y

    x, y = tf.numpy_function(_parse, [x, y], [tf.float32, tf.float32])
    x.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, 3])
    y.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    return x, y

def tf_dataset(X, Y, batch_size=10):
    dataset = tf.data.Dataset.from_tensor_slices((X, Y))
    dataset = dataset.map(tf_parse)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(10)
    return dataset

if __name__ == "__main__":
    np.random.seed(42)
    tf.random.set_seed(42)

    create_directory("files")

    batch_size = 16
    learning_rate = 1e-4
    num_epochs = 500
    model_path = "files/model.h5"
    log_path = "files/log.csv"

    dataset_path = os.path.join(
        os.getcwd(),
        "scans and masks"
    )
    print(dataset_path)
    (train_x, train_y), (valid_x, valid_y), _ = load_dataset(dataset_path)

    print(f"Training set: {len(train_x)} images")
    print(f"Validation set: {len(valid_x)} images")

    train_dataset = tf_dataset(train_x, train_y, batch_size=batch_size)
    valid_dataset = tf_dataset(valid_x, valid_y, batch_size=batch_size)

    model = build_model((IMAGE_HEIGHT, IMAGE_WIDTH, 3))
    model.compile(loss=dice_loss, optimizer=Adam(learning_rate), metrics=[dice_coef])

    callbacks = [
        ModelCheckpoint(model_path, verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, min_lr=1e-7, verbose=1),
        CSVLogger(log_path),
        EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=False)
    ]

    model.fit(
        train_dataset,
        epochs=num_epochs,
        validation_data=valid_dataset,
        callbacks=callbacks
    )
