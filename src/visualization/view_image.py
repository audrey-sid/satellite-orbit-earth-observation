import matplotlib.pyplot as plt
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

if __name__ == "__main__":
    plot_satellite_image()