import os
import numpy as np
import cv2
import glob
import tensorflow as tf
from keras.callbacks import ModelCheckpoint, CSVLogger, ReduceLROnPlateau, EarlyStopping
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from model import build_model
from metrics import dice_loss, dice_coef
# Minimize TensorFlow logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
# Global parameters for image dimensions
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256

def create_directory(path):
    """Create a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def load_dataset(path, split=0.2):
    """Load and split the dataset into training, validation, and test sets."""
    images = sorted(glob.glob(os.path.join(path, "images", "*.png")))
    masks = sorted(glob.glob(os.path.join(path, "masks", "*.png")))

    # Determine the size of each dataset split
    split_size = int(len(images) * split)

    # Splitting datasets
    train_x, valid_x = train_test_split(images, test_size=split_size, random_state=42)
    train_y, valid_y = train_test_split(masks, test_size=split_size, random_state=42)
    train_x, test_x = train_test_split(train_x, test_size=split_size, random_state=42)
    train_y, test_y = train_test_split(train_y, test_size=split_size, random_state=42)

    return (train_x, train_y), (valid_x, valid_y), (test_x, test_y)

def read_image(path):
    """Read and process image."""
    path = path.decode()
    x = cv2.imread(path, cv2.IMREAD_COLOR)
    x = cv2.resize(x, (IMAGE_WIDTH, IMAGE_HEIGHT))
    x = x / 255.0
    return x.astype(np.float32)

def read_mask(path):
    """Read and process mask."""
    path = path.decode()
    x = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    x = cv2.resize(x, (IMAGE_WIDTH, IMAGE_HEIGHT)) / 255.0
    return np.expand_dims(x, axis=-1).astype(np.float32)

def tf_parse(x, y):
    """Parse and preprocess dataset elements."""
    def _parse(x, y):
        x = read_image(x)
        y = read_mask(y)
        return x, y

    x, y = tf.numpy_function(_parse, [x, y], [tf.float32, tf.float32])
    x.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, 3])
    y.set_shape([IMAGE_HEIGHT, IMAGE_WIDTH, 1])
    return x, y

def tf_dataset(X, Y, batch_size=10):
    """Create a TensorFlow dataset."""
    dataset = tf.data.Dataset.from_tensor_slices((X, Y))
    dataset = dataset.map(tf_parse)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(10)
    return dataset

if __name__ == "__main__":
    # Seed setting for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    # Directory for saving training artifacts
    create_directory("files")

    # Training hyperparameters
    batch_size = 2
    learning_rate = 1e-4
    num_epochs = 500
    model_path = "files/model.h5"
    log_path = "files/log.csv"

    # Load and prepare the dataset
    dataset_path = "D:\Documents\Projects\EPICS\Brain Tumor Segmentation\scans and masks"
    (train_x, train_y), (valid_x, valid_y), _ = load_dataset(dataset_path)

    print(f"Training set: {len(train_x)} images")
    print(f"Validation set: {len(valid_x)} images")

    # Prepare TensorFlow datasets
    train_dataset = tf_dataset(train_x, train_y, batch_size=batch_size)
    valid_dataset = tf_dataset(valid_x, valid_y, batch_size=batch_size)

    # Build and compile the U-Net model
    model = build_model((IMAGE_HEIGHT, IMAGE_WIDTH, 3))
    model.compile(loss=dice_loss, optimizer=Adam(learning_rate), metrics=[dice_coef])

    # Define model training callbacks
    callbacks = [
        ModelCheckpoint(model_path, verbose=1, save_best_only=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, min_lr=1e-7, verbose=1),
        CSVLogger(log_path),
        EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=False)
    ]

    # Start training
    model.fit(
        train_dataset,
        epochs=num_epochs,
        validation_data=valid_dataset,
        callbacks=callbacks,
    )
