from nibabel import load
from matplotlib import pyplot as plt
import os

# Define input and output paths
input_file = "./t1_icbm_normal_5mm_pn3_rf20.mnc"
output_dir = "./output"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the MINC image
img_data = load(input_file).get_fdata()

# Extract image dimensions (z, y, x)
z_slices, y_dim, x_dim = img_data.shape

# Loop through each z-slice and save as PNG
for z in range(z_slices):
    slice_data = img_data[z, :, :]

    # Create PNG filename with informative numbering
    filename = f"slice_{z:03d}.png"
    output_path = os.path.join(output_dir, filename)

    # Save the slice as a PNG using matplotlib
    plt.imsave(output_path, slice_data, cmap="gray")  # Adjust cmap for color data

print(f"Saved {z_slices} slices as PNGs in {output_dir}")
