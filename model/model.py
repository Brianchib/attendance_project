import os

from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, losses, callbacks, utils

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(layers.BatchNormalization())
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))

model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.AveragePooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.AveragePooling2D(pool_size=(2, 2)))
model.add(layers.Dropout(0.5))
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(layers.AveragePooling2D(pool_size=(2,2)))
model.add(layers.Dropout(0.5))
model.add(layers.Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(layers.MaxPooling2D(pool_size=(2,2)))
model.add(layers.Flatten())
model.add(layers.Dense(units=128, activation='relu'))
model.add(layers.Dense(units=2, activation='sigmoid'))
model.summary()

train_data_dir = "../dataset/training"
vali_data_dir = "../dataset/validation"
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
train_gen = train_data_gen.flow_from_directory(
    train_data_dir, target_size=(224, 224), batch_size=32, class_mode="categorical", color_mode="rgb"
)
vali_gen = vali_data_gen.flow_from_directory(
    vali_data_dir, target_size=(224, 224), batch_size=32, class_mode="categorical", color_mode="rgb"
)

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
cp_callback = [callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)]

model.compile(optimizer='adam', loss=losses.CategoricalCrossentropy(from_logits=True), metrics=['accuracy'])
history = model.fit(
    train_gen,
    batch_size=32,
    epochs=10,
    validation_data=vali_gen,
    callbacks=cp_callback,
)

# optional use the line below to save the weights instead of the callback
# Save classifier weights
# detector.save('classifier.h5')