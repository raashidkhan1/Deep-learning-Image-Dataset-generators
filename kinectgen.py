import cv2
import numpy as np
from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import os

folder = "C:\\Users\\Raashid\\Thesis\\Data\\KinectData"
# Initialize Kinect sensor
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth)
size  = 1
i= 1
# Define depth range (in millimeters)
min_depth = 0   # Minimum depth in mm
max_depth = 3000  # Maximum depth in mm

while i <= size:
    # Check if a new frame is available
    if kinect.has_new_color_frame() and kinect.has_new_depth_frame():
        color_frame = kinect.get_last_color_frame()
        depth_frame = kinect.get_last_depth_frame()

        # Reshape frames to correct dimensions
        color_image = color_frame.reshape((1080, 1920, 4)).astype(np.uint8)
        depth_image = depth_frame.reshape((424, 512)).astype(np.uint16)
        
        # Apply depth thresholding
        depth_image = np.where((depth_image > min_depth) & (depth_image < max_depth), depth_image, 0)

        # # Normalize depth image for visualization
        # depth_image_visual = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

        # Resize images to 160x120
        # resized_color_image = cv2.resize(color_image, (160, 120))
        # resized_depth_image = cv2.resize(depth_image, (160, 120), interpolation=cv2.INTER_NEAREST)

        # Display images using OpenCV
        cv2.imshow('Color Image', color_image)
        cv2.imshow('Depth Image', depth_image)

        cv2.imwrite(os.path.join(folder, f'color_image_{i}.jpg'), color_image)
        cv2.imwrite(os.path.join(folder, f'depth_image_{i}.png'), depth_image)

        i = i+1
        # Break loop on 'q' keypress
        if cv2.waitKey(1) == ord('q'):
            break
        
# Release resources
kinect.close()
cv2.destroyAllWindows()
