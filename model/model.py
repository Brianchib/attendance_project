import os

from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, losses, callbacks, utils

# sequential model allows us to specify a neural network, precisely, `sequence`:
# from input to output, passing through a series of neural layers
model = models.Sequential()

# Convolution is responsible for extracting appropriate features from image
# RELU - Sets all negative pixel values to zero for easier classification
# This is the first convolutional layer which accepts the input_shape of the incoming data.
# (224, 224, 3) means the dimension of 224x224 in rgb format or channel of 3: channel of one represents grayscale
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

# second convolutional layer with batch normalization that applies a transformation (on pixel values) that
# maintains the mean output close to 0 and the output standard deviation close to 1.
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())

# Average Pooling: Calculate the average value for each patch on the feature map (output after convulution).
# Dropout randomly sets some of the input units to 0 at each update during training time, which helps prevent overfitting
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.AveragePooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

# subsequent convulutional layer or kernel for further filtering
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())

# subsequent convulutional layer or kernel for further filtering
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.AveragePooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.5))

# subsequent convulutional layer or kernel for further filtering
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.BatchNormalization())

# subsequent convulutional layer or kernel for further filtering
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.AveragePooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

# subsequent convulutional layer or kernel for further filtering
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.BatchNormalization())

# Average Pooling: Calculate the maximum value for each patch on the feature map (output after convulution).
# flatten transforms the input data into a 1-D;
# the final dense layer units defines the number of outputs (classes) expected to be predicated during training
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))

# Flatten the output from convolutional layers and add dense layers with ReLU and sigmoid activations
model.add(layers.Flatten())
model.add(layers.Dense(units=128, activation='relu'))
model.add(layers.Dense(units=10000, activation='softmax'))

# output the summary of the model providing total number of parameters within the model
# model.summary()

# set directory for training data and validation data if availabe
train_data_dir = "../dataset/training"
vali_data_dir = "../dataset/validation"

# generate or convert real images into tensors
# rescale multiplies each input value
# rotation_range specifies the random angle for rotations
# shift_range species a fraction of the image that should be shifted
# horizontal_flip randomly flips the image horizontally
# fill_mode nearest means for input values that requires fill-in values,
# the nearest value should be used e.g: xxx|xyz|zzz where |xyz| is the input value
train_data_gen = ImageDataGenerator(
    rescale=1.0 / 255.0,
    rotation_range=45,
    width_shift_range=0.3,
    height_shift_range=0.3,
    horizontal_flip=True,
    fill_mode="nearest"
)
vali_data_gen = ImageDataGenerator(
    rescale=1.0 / 255.0
)

# Pass train images from directories to image generator variable created above
train_gen = train_data_gen.flow_from_directory(
    train_data_dir, target_size=(224, 224), batch_size=32, class_mode="categorical", color_mode="rgb"
)
# Pass train images from directories to image generator variable created above
vali_gen = vali_data_gen.flow_from_directory(
    vali_data_dir, target_size=(224, 224), batch_size=32, class_mode="categorical", color_mode="rgb"
)

# Initialize and setup callbacks to save the model weights during training
checkpoint_path = "checkpoints/model-cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = [callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)]

# compile model to check for errors and model correctness
# Also specify loss funtion and optimizer
model.compile(optimizer='adam', loss=losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

# Training starts with model.fit
history = model.fit(
    train_gen,
    validation_data=vali_gen,
    batch_size=256,
    epochs=5,
    callbacks=cp_callback,
)


