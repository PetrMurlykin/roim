import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from keras.callbacks import ProgbarLogger

# Load the CSV file with labels
labels_df = pd.read_csv('./labels.csv')

labels_df['Label'] = labels_df['Label'].astype(str)

# Define the image generator
image_generator = ImageDataGenerator(rescale=1.0/255.0)

# Split the data into training and testing sets
train_df, test_df = train_test_split(labels_df, test_size=0.2, random_state=42)

# Define the generator for training data
train_generator = image_generator.flow_from_dataframe(
    train_df,
    directory='./dataset/',  # Modify the directory path to match your dataset folder
    x_col='Filename',
    y_col='Label',
    color_mode='grayscale',
    target_size=(28, 56),
    batch_size=128,
    class_mode='categorical'
)

# Define the generator for testing data
test_generator = image_generator.flow_from_dataframe(
    test_df,
    directory='./dataset/',  # Modify the directory path to match your dataset folder
    x_col='Filename',
    y_col='Label',
    color_mode='grayscale',
    target_size=(28, 56),
    batch_size=128,
    class_mode='categorical',
    shuffle=False
)

# Build the neural network
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 56, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(100, activation='softmax'))


# Compile the model
model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

logger = ProgbarLogger(count_mode='steps')

# Train the model using the generator
model.fit(train_generator, epochs=10, validation_data=test_generator, callbacks=[logger])

# Evaluate the model using the generator
loss, accuracy = model.evaluate(test_generator)
print('Test loss:', loss)
print('Test accuracy:', accuracy)

# Save the trained model
model.save('trained_model.h5')

# Print a message to confirm the model has been saved
print("Trained model has been saved as 'trained_model.h5'")
