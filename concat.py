import os
import csv
import numpy as np
from PIL import Image

def resize_mnist_image(image):
    # Create a new array with the desired size
    resized_image = np.zeros((28, 56), dtype=np.uint8)
    
    # Calculate the number of empty columns to add on each side
    empty_columns = (56 - 28) // 2
    
    # Copy the original image to the resized image with empty columns
    resized_image[:, empty_columns:empty_columns+28] = image
    
    return resized_image


def extract_mnist_subset(filename, percent):
    # Load the MNIST dataset
    with np.load(filename) as data:
        images = data['x_train']
        labels = data['y_train']
    
    # Calculate the number of samples to extract
    num_samples = int(len(images) * (percent / 100))
    
    # Shuffle the dataset
    indices = np.arange(len(images))
    np.random.shuffle(indices)
    
    # Select the subset based on the specified percentage
    subset_indices = indices[:num_samples]
    subset_images = images[subset_indices]
    subset_labels = labels[subset_indices]
    
    return subset_images, subset_labels


def merge_mnist_with_existing(mnist_images, mnist_labels, image_folder, csv_file):
    # Read the existing CSV file
    existing_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        existing_data = list(reader)
    
    # Determine the starting index for the new data
    starting_index = len(existing_data)
    
    # Save the MNIST images and labels
    for i, image in enumerate(mnist_images):
        # Generate the new image filename
        image_number = starting_index + i
        image_filename = f"image_{image_number}.png"
        
        # Save the image as PNG
        image_path = os.path.join(image_folder, image_filename)
        resized_image = resize_mnist_image(image)
        image = Image.fromarray(resized_image)
        image.save(image_path)
        
        # Append the label to the existing data
        label = mnist_labels[i]
        existing_data.append([image_number, label])
    
    # Write the updated CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(existing_data)

# Example usage
subset_images, subset_labels = extract_mnist_subset('./mnist.npz', 26)
merge_mnist_with_existing(subset_images, subset_labels, './dataset', './labels.csv')
