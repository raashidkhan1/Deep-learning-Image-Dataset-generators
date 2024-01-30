import OpenEXR
import Imath
import numpy as np
from PIL import Image

# Load OpenEXR file
exr_file_path = "C:\\Users\\Raashid\\Thesis\\Data\\data2\\cube\\cube_r_000_depth0001.exr"
exr_file = OpenEXR.InputFile(exr_file_path)

# Get image header and channel information
header = exr_file.header()
dw = header['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

# Read the depth channel
depth_channel = exr_file.channel('R', Imath.PixelType(Imath.PixelType.FLOAT))

# Convert depth channel data to NumPy array
depth_data = np.frombuffer(depth_channel, dtype=np.float32)
depth_data = np.reshape(depth_data, (size[1], size[0]))

# Normalize the depth data if needed
normalized_depth = (depth_data - np.min(depth_data)) / (np.max(depth_data) - np.min(depth_data))

# Convert the depth data to a grayscale image
depth_image = (normalized_depth * 255).astype(np.uint8)
pil_image = Image.fromarray(depth_image)

# Save the result as a grayscale PNG
pil_image.save("output_depth.png")
