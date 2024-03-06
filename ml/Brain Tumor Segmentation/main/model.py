from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Conv2DTranspose, Concatenate, Input
from tensorflow.keras.models import Model

def convolutional_block(input_tensor, num_filters):

    x = Conv2D(num_filters, kernel_size=3, padding="same")(input_tensor)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    x = Conv2D(num_filters, kernel_size=3, padding="same")(x)
    x = BatchNormalization()(x)
    x = Activation("relu")(x)

    return x

def encoder_block(input_tensor, num_filters):

    conv_block_output = convolutional_block(input_tensor, num_filters)
    pool_output = MaxPool2D(pool_size=(2, 2))(conv_block_output)
    return conv_block_output, pool_output

def decoder_block(input_tensor, skip_tensor, num_filters):

    x = Conv2DTranspose(num_filters, kernel_size=2, strides=2, padding="same")(input_tensor)
    x = Concatenate()([x, skip_tensor])
    x = convolutional_block(x, num_filters)
    return x

def build_model(input_shape):

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

    outputs = Conv2D(1, kernel_size=1, padding="same", activation="sigmod")(decoder4)

    model = Model(inputs, outputs, name="UNET")
    return model

if __name__ == "__main__":
    input_shape = (256, 256, 3)
    unet_model = build_model(input_shape)
    unet_model.summary()