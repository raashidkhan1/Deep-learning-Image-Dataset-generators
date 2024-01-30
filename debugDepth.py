import cv2
import numpy as np

# Assuming you've read the depth image correctly
img_depth = cv2.imread("C:\\Users\\Raashid\\Thesis\\Data\\KinectData\\depth_image_1.png", -1)
# Verify that the image was loaded
if img_depth is None:
    print("Error: Depth image not loaded.")
else:
    # Find the maximum depth value in the image
    min_val, max_val, _, _ = cv2.minMaxLoc(img_depth)
    print(f"Min Depth Value: {min_val}, Max Depth Value: {max_val}")

    # Normalize the depth image based on the actual depth range
    depth_normalized = np.zeros_like(img_depth, dtype=np.uint8)
    cv2.normalize(img_depth, depth_normalized, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Display for debugging
    cv2.imshow('Normalized Depth Image', depth_normalized)
    cv2.waitKey(0)

    # Save the normalized depth image
    cv2.imwrite('capture_depth.png', depth_normalized)

cv2.destroyAllWindows()