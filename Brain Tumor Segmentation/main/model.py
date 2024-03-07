import tensorflow as tf
from keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Conv2DTranspose, Concatenate, Input
from keras.models import Model
tf.config.list_physical_devices("GPU")
def convolutional_block(input_tensor, num_filters):
    """
    Creates a convolutional block with two Conv2D layers, each followed by BatchNormalization and ReLU activation.
 
    Args:
    input_tensor (tensor): Input tensor to the convolutional block.
    num_filters (int): Number of filters for the convolution layers.

    Returns:
    tensor: Output tensor after applying the convolutional block.
    """
    x = Conv2D(num_filters, kernel_size=3, padding="same")(input_tensor)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Conv2D(num_filters, kernel_size=3, padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    return x

def encoder_block(input_tensor, num_filters):
    """
    Creates an encoder block with a convolutional block and a MaxPooling layer.

    Args:
    input_tensor (tensor): Input tensor to the encoder block.
    num_filters (int): Number of filters for the convolution layers.

    Returns:
    tensor: Output tensor of the convolutional block.
    tensor: Output tensor of the MaxPooling layer.
    """
    conv_block_output = convolutional_block(input_tensor, num_filters)
    pool_output = MaxPool2D(pool_size=(2, 2))(conv_block_output)
    return conv_block_output, pool_output

def decoder_block(input_tensor, skip_tensor, num_filters):
    """
    Creates a decoder block with a Conv2DTranspose layer and concatenates it with the skip tensor.

    Args:
    input_tensor (tensor): Input tensor to the decoder block.
    skip_tensor (tensor): Tensor for skip connections.
    num_filters (int): Number of filters for the Conv2DTranspose layer.

    Returns:
    tensor: Output tensor after applying the decoder block.
    """
    x = Conv2DTranspose(num_filters, kernel_size=2, strides=2, padding="same")(input_tensor)
    x = Concatenate()([x, skip_tensor])
    x = convolutional_block(x, num_filters)
    return x

def build_model(input_shape):
    """
    Builds a U-Net model.

    Args:
    input_shape (tuple): Shape of the input tensor.

    Returns:
    Model: U-Net model.
    """
    inputs = Input(input_shape)

    skip1, pool1 = encoder_block(inputs, 64)
    skip2, pool2 = encoder_block(pool1, 128)
    skip3, pool3 = encoder_block(pool2, 256)
    skip4, pool4 = encoder_block(pool3, 512)

    bridge = convolutional_block(pool4, 1024)

    decoder1 = decoder_block(bridge, skip4, 512)
    decoder2 = decoder_block(decoder1, skip3, 256)
    decoder3 = decoder_block(decoder2, skip2, 128)
    decoder4 = decoder_block(decoder3, skip1, 64)

    outputs = Conv2D(1, kernel_size=1, padding="same", activation="sigmoid")(decoder4)

    model = Model(inputs, outputs, name="UNET")
    return model

if __name__ == "__main__":
    input_shape = (256, 256, 3)
    unet_model = build_model(input_shape)
    unet_model.summary()