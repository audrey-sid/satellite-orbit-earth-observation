import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Load and display the downloaded satellite image
def plot_satellite_image(image_path="data/raw/sentinel_kourou.jpg"):
    # Open image using Pillow
    img = Image.open(image_path)

    # Display image with matplotlib
    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    plt.title("Sentinel-2 Preview - Kourou (French Guiana)")
    plt.axis("off")

    # Save figure plot
    output_plot = "data/raw/sentinel_kourou_plot.png"
    plt.savefig(output_plot, bbox_inches="tight")
    print(f"Plot saved to: {output_plot}")
    plt.show()

# Calculate and plot RGB color distribution
def plot_color_histogram(image_path="data/raw/sentinel_kourou.jpg"):
    # Open image using Pillow
    img = Image.open(image_path)

    # Convert image to numpy array
    img_array = np.array(img)

    # Plot histogram
    colors = ("red", "green", "blue")
    plt.figure(figsize=(10, 5))

    for i, color in enumerate(colors):
        # Calculate pixel values from 0 to 255
        histogram, bin_edges = np.histogram(
            img_array[:, :, i], bins=256, range=(0, 256))
        plt.plot(
            bin_edges[:-1], 
            histogram, 
            color=color, 
            alpha=0.7, 
            label=f"{color.capitalize()} channel")

    plt.title("RGB Color Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Number of Pixels")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    # Save histogram plot
    output_hist = "data/raw/sentinel_kourou_histogram.png"
    plt.savefig(output_hist, bbox_inches="tight")
    print(f"Histogram saved to: {output_hist}")
    plt.show()

if __name__ == "__main__":
    plot_satellite_image()
    plot_color_histogram()