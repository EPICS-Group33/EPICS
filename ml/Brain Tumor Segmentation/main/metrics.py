import tensorflow as tf

SMOOTH = 1e-15

def dice_coef(y_true, y_pred):

    y_true_flat = tf.keras.layers.Flatten()(y_true)
    y_pred_flat = tf.keras.layers.Flatten()(y_pred)

    intersection = tf.reduce_sum(y_true_flat * y_pred_flat)
    union = tf.reduce_sum(y_true_flat) + tf.reduce_sum(y_pred_flat)

    dice_coefficient = (2. * intersection + SMOOTH) / (union + SMOOTH)
    return dice_coefficient

def dice_loss(y_true, y_pred):
    return 1.0 - dice_coef(y_true, y_pred)