import cv2
import numpy as np

# Calibration pattern parameters (e.g., checkerboard)
pattern_size = (9, 6)  # Number of inner corners in the calibration pattern
square_size = 1.0  # Size of each square in the calibration pattern (in your chosen units, e.g., cm)

# Prepare object points, assuming the calibration pattern is at the origin (0,0,0) and extends in the X and Y directions
object_points = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
object_points[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from all the images
obj_points = []  # 3D points in real-world space
img_points = []  # 2D points in image plane

# Load images and find calibration pattern corners
# Add the paths to your calibration images
image_paths = ["calibration_image1.jpg", "calibration_image2.jpg"]


for image_path in image_paths:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        obj_points.append(object_points)
        img_points.append(corners)

# Perform camera calibration
ret, camera_matrix, distortion_coefficients, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Print the intrinsic parameters
print("Camera Matrix (Intrinsic Parameters):\n", camera_matrix)
print("\nDistortion Coefficients:\n", distortion_coefficients)