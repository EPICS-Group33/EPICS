import os
import numpy as np
import cv2
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from keras.utils import CustomObjectScope
from sklearn.metrics import f1_score, jaccard_score, precision_score, recall_score
from metrics import dice_loss, dice_coef
from train import load_dataset

tf.config.list_physical_devices("GPU")

# Setting TensorFlow log level to minimize verbose outputs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Global parameters for image dimensions
IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256

def create_directory(path):
    """Create a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_results(image, mask, prediction, save_path):
    """Save overlay of original image, mask, and prediction."""
    # Prepare mask and prediction for saving
    mask = np.expand_dims(mask, axis=-1)
    mask_overlay = np.concatenate([mask, mask, mask], axis=-1)
    prediction_overlay = np.expand_dims(prediction, axis=-1) * 255
    prediction_overlay = np.concatenate([prediction_overlay, prediction_overlay, prediction_overlay], axis=-1)

    separator = np.ones((IMAGE_HEIGHT, 10, 3)) * 255
    concatenated_images = np.concatenate([image, separator, mask_overlay, separator, prediction_overlay], axis=1)
    cv2.imwrite(save_path, concatenated_images)

if __name__ == "__main__":
    # Seed initialization for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    # Create results directory
    create_directory("results")

    # Load the pre-trained model
    with CustomObjectScope({"dice_coef": dice_coef, "dice_loss": dice_loss}):
        model = tf.keras.models.load_model(
            os.path.join(
                os.getcwd(),
                "files",
                "model.h5"
            )
        )

    # Load test dataset
    dataset_path = os.path.join(
        os.getcwd(),
        ".",
        "scans and masks",
        "images"
    )
    _, _, (test_images, test_masks) = load_dataset(dataset_path)

    # Evaluation metrics storage
    evaluation_scores = []

    for img_path, mask_path in tqdm(zip(test_images, test_masks), total=len(test_masks)):
        
        # Read and preprocess the image
        image = cv2.imread(img_path, cv2.IMREAD_COLOR)
        image_resized = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        image_normalized = image_resized / 255.0
        image_array = np.expand_dims(image_normalized, axis=0)

        # Read and preprocess the mask
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask_resized = cv2.resize(mask, (IMAGE_WIDTH, IMAGE_HEIGHT)) / 255.0

        # Make predictions
        prediction = model.predict(image_array)[0].squeeze()
        prediction_binary = (prediction >= 0.5).astype(np.int32)

        # Save the results
        result_file_name = os.path.basename(img_path)
        save_results(image_resized, mask_resized, prediction_binary, os.path.join("results", result_file_name))

        # Flatten the mask and prediction for metrics computation
        mask_flat = (mask_resized > 0.5).astype(np.int32).flatten()
        prediction_flat = prediction_binary.flatten()

        # Compute metrics
        f1_val = f1_score(mask_flat, prediction_flat, average="binary")
        jaccard_val = jaccard_score(mask_flat, prediction_flat, average="binary")
        recall_val = recall_score(mask_flat, prediction_flat, average="binary", zero_division=0)
        precision_val = precision_score(mask_flat, prediction_flat, average="binary", zero_division=0)

        evaluation_scores.append([result_file_name, f1_val, jaccard_val, recall_val, precision_val])

    # Average of evaluation metrics
    average_scores = np.mean([scores[1:] for scores in evaluation_scores], axis=0)
    print(f"F1 Score: {average_scores[0]:0.5f}")
    print(f"Jaccard Index: {average_scores[1]:0.5f}")
    print(f"Recall: {average_scores[2]:0.5f}")
    print(f"Precision: {average_scores[3]:0.5f}")

    # Save the scores to a CSV file
    scores_df = pd.DataFrame(evaluation_scores, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
    scores_df.to_csv("files/score.csv")
