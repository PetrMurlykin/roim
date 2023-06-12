import numpy as np
import os
from tensorflow.keras.datasets import mnist
import csv
import random
from PIL import Image

def generate_concatenated_dataset(save_dir, mnist_path):
    mnist_data = np.load(mnist_path)

    # Access the dataset arrays
    train_images = mnist_data['x_train']
    train_labels = mnist_data['y_train']
    test_images = mnist_data['x_test']
    test_labels = mnist_data['y_test']

    # Reshape and normalize the images
    train_images = train_images.reshape(-1, 28, 28, 1) / 255.0
    test_images = test_images.reshape(-1, 28, 28, 1) / 255.0

    # Generate concatenated images and labels
    labels = []
    count = 0

    os.makedirs(save_dir, exist_ok=True)

    for i in range(len(train_images)):
        for j in range(len(train_images)):
            ind_first = random.randint(0, len(train_images) - 1)
            ind_sec = random.randint(0, len(train_images) - 1)
            if train_labels[ind_first] == 0:
                continue
            concatenated_image = np.concatenate((train_images[ind_first], train_images[ind_sec]), axis=1)
            concatenated_image *= 255
            concatenated_image = concatenated_image.squeeze().astype(np.uint8)
            image = Image.fromarray(concatenated_image)
            image.save(os.path.join(save_dir, f'image_{count}.png'))
            labels.append(train_labels[ind_first] * 10 + train_labels[ind_sec])
            count += 1
            if count > 90_000:
                break
        if count > 90_000:
                break

    labels = np.array(labels)

    # Create save directory if it doesn't exist

    # Save the labels as a CSV file
    with open('./labels.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Index', 'Label'])
        for i in range(len(labels)):
            writer.writerow([i, labels[i]])

    print('Concatenated images saved as PNG files in', save_dir)
    print('Labels saved as CSV file in', save_dir)

# Example usage
save_directory = './dataset'
mnist_path = './mnist.npz'
generate_concatenated_dataset(save_directory, mnist_path)
