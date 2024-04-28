import tensorflow as tf

# Small constant for numerical stability
SMOOTH = 1e-15

def dice_coef(y_true, y_pred):
    """
    Compute the Dice Coefficient.

    Args:
    y_true (tensor): Ground Truth or Actual Mask.
    y_pred (tensor): Predicted Mask.

    Returns:
    dice_coefficient (float): Computed Dice Coefficient.
    """
    # Flatten the tensors to convert them into vectors
    y_true_flat = tf.keras.layers.Flatten()(y_true)
    y_pred_flat = tf.keras.layers.Flatten()(y_pred)

    # Calculate intersection and union
    intersection = tf.reduce_sum(y_true_flat * y_pred_flat)
    union = tf.reduce_sum(y_true_flat) + tf.reduce_sum(y_pred_flat)

    # Compute Dice Coefficient
    dice_coefficient = (2. * intersection + SMOOTH) / (union + SMOOTH)
    return dice_coefficient

def dice_loss(y_true, y_pred):
    """
    Compute the Dice Loss.

    Args:
    y_true (tensor): Ground Truth or Actual Mask.
    y_pred (tensor): Predicted Mask.

    Returns:
    dice_loss (float): Computed Dice Loss.
    """
    # Dice loss is 1 minus dice coefficient
    return 1.0 - dice_coef(y_true, y_pred)