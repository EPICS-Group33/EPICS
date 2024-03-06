import os
import numpy as np
import cv2
import pandas as pd
from tqdm import tqdm
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope
from sklearn.metrics import f1_score, jaccard_score, precision_score, recall_score
from metrics import dice_loss, dice_coef
from train import load_dataset

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

IMAGE_HEIGHT = 256
IMAGE_WIDTH = 256

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_results(image, mask, prediction, save_path):
    
    mask = np.expand_dims(mask, axis=-1)
    mask_overlay = np.concatenate([mask, mask, mask], axis=-1)
    prediction_overlay = np.expand_dims(prediction, axis=-1) * 255
    prediction_overlay = np.concatenate([prediction_overlay, prediction_overlay, prediction_overlay], axis=-1)

    separator = np.ones((IMAGE_HEIGHT, 10, 3)) * 255
    concatenated_images = np.concatenate([image, separator, mask_overlay, separator, prediction_overlay], axis=1)
    cv2.imwrite(save_path, concatenated_images)

if __name__ == "__main__":
    np.random.seed(42)
    tf.random.set_seed(42)

    create_directory("results")

    with CustomObjectScope({"dice_coef": dice_coef, "dice_loss": dice_loss}):
        model = tf.keras.models.load_model("files/model.h5")

    dataset_path = "/path/to/dataset"
    _, _, (test_images, test_masks) = load_dataset(dataset_path)

    evaluation_scores = []

    for img_path, mask_path in tqdm(zip(test_images, test_masks), total=len(test_masks)):
        image = cv2.imread(img_path, cv2.IMREAD_COLOR)
        image_resized = cv2.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT))
        image_normalized = image_resized / 255.0
        image_array = np.expand_dims(image_normalized, axis=0)

        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask_resized = cv2.resize(mask, (IMAGE_WIDTH, IMAGE_HEIGHT)) / 255.0

        prediction = model.predict(image_array)[0].squeeze()
        prediction_binary = (prediction >= 0.5).astype(np.int32)

        result_file_name = os.path.basename(img_path)
        save_results(image_resized, mask_resized, prediction_binary, os.path.join("results", result_file_name))

        mask_flat = (mask_resized > 0.5).astype(np.int32).flatten()
        prediction_flat = prediction_binary.flatten()

        f1_val = f1_score(mask_flat, prediction_flat, average="binary")
        jaccard_val = jaccard_score(mask_flat, prediction_flat, average="binary")
        recall_val = recall_score(mask_flat, prediction_flat, average="binary", zero_division=0)
        precision_val = precision_score(mask_flat, prediction_flat, average="binary", zero_division=0)

        evaluation_scores.append([result_file_name, f1_val, jaccard_val, recall_val, precision_val])

    average_scores = np.mean([scores[1:] for scores in evaluation_scores], axis=0)
    print(f"F1 Score: {average_scores[0]:0.5f}")
    print(f"Jaccard Index: {average_scores[1]:0.5f}")
    print(f"Recall: {average_scores[2]:0.5f}")
    print(f"Precision: {average_scores[3]:0.5f}")

    scores_df = pd.DataFrame(evaluation_scores, columns=["Image", "F1", "Jaccard", "Recall", "Precision"])
    scores_df.to_csv("files/score.csv")
