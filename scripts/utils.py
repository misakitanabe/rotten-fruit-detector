import matplotlib.pyplot as plt
import os
import shutil
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_training_history(history, output_path=None, base_model='xception'):
    # Create directories if not exist
    if output_path:
        os.makedirs(output_path, exist_ok=True)

    """Plots validation accuracy/loss over epochs."""
    acc = history.history['val_accuracy']
    loss = history.history['val_loss']
    epochs = range(len(acc))

    # Plot accuracy
    plt.figure()
    plt.plot(epochs, acc, label='Cross Validation Accuracy')
    if base_model == 'xception':
        plt.title('Cross Validation Accuracy (Xception)')
    else:
        plt.title('Cross Validation Accuracy (MobileNet)')
    plt.ylabel('Accuracy')
    plt.xlabel('Number of Epochs')
    plt.legend()
    if output_path:
        plt.savefig(f"{output_path}_accuracy.jpg")

    # Plot loss
    plt.figure()
    plt.plot(epochs, loss, label='Cross Validation Loss')
    plt.title('Cross Validation Loss')
    plt.ylabel('Loss')
    plt.xlabel('Number of Epochs')
    plt.legend()
    if output_path:
        plt.savefig(f"{output_path}_loss.jpg")


# Plotting the combined distribution
def plot_combined_class_distribution(train_counts, test_counts, title, save_path=None):
    """Plots the combined distribution of images per class for train and test sets."""
    classes = list(train_counts.keys())
    train_values = list(train_counts.values())
    test_values = [test_counts.get(cls, 0) for cls in classes]

    x = range(len(classes))  # Indices for the classes
    width = 0.35  # Width of the bars

    plt.figure(figsize=(10, 6))
    plt.bar(x, train_values, width, label='Train', color='blue', alpha=0.7)
    plt.bar([i + width for i in x], test_values, width, label='Test', color='orange', alpha=0.7)

    plt.xlabel("Class")
    plt.ylabel("Number of Images")
    plt.title(title)
    plt.xticks([i + width / 2 for i in x], classes)  # Center labels
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    if save_path:
        plt.savefig(save_path)
    # plt.show()


# Function to clear directory contents
def clear_directory(directory):
    """Deletes all contents of a directory."""
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))

# Function to count images in each class
def count_images(directory):
    """Counts the number of images in each class within a directory."""
    class_counts = {}
    if os.path.exists(directory):
        for class_name in os.listdir(directory):
            class_path = os.path.join(directory, class_name)
            if os.path.isdir(class_path):
                class_counts[class_name] = len(os.listdir(class_path))
    return class_counts

def extract_data_and_labels(generator):
    """Extracts all data and labels from a data generator."""
    data = []
    labels = []

    for _ in range(len(generator)):  # Iterate through all batches
        batch_data, batch_labels = next(generator)
        data.extend(batch_data)  # Add batch images to data
        labels.extend(batch_labels)  # Add batch labels to labels

    print(f"Successfully extracted data and labels.")

    return np.array(data), np.array(labels)

def plot_confusion_matrix(y_true, y_pred, class_names, output_path=None):
    """
    Plots a confusion matrix as a heatmap.
    
    Args:
        y_true (list or np.array): Ground truth labels.
        y_pred (list or np.array): Predicted labels.
        class_names (list): List of class names.
    """
    # Generate confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Plot the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix on Generalization Set')
    plt.ylabel('True Labels')
    plt.xlabel('Predicted Labels')
    plt.tight_layout()
    if output_path:
        plt.savefig(output_path)