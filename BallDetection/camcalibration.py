import cv2
import numpy as np

# Calibration pattern parameters (e.g., checkerboard)
pattern_size = (7, 7)  # Number of inner corners in the calibration pattern
square_size = 2.0  # Size of each square in the calibration pattern (in your chosen units, e.g., cm)

# Prepare object points, assuming the calibration pattern is at the origin (0,0,0) and extends in the X and Y directions
object_points = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
object_points[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2) * square_size

# Arrays to store object points and image points from all the images
obj_points = []  # 3D points in real-world space
img_points = []  # 2D points in image plane

# Load images and find calibration pattern corners
# Add the paths to your calibration images
folder_path = "C:/Users/jpss8/Desktop/calibration/"
image_names = [f"calibration_image_{x}.jpg" for x in range(64)]


for image_name in image_names:
    full_path = folder_path + image_name
    image = cv2.imread(full_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

    if ret:
        obj_points.append(object_points)
        img_points.append(corners)

# Perform camera calibration
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

# Print the intrinsic parameters
print("Camera Matrix (Intrinsic Parameters):\n", mtx)
print("\nDistortion Coefficients:\n", dist)
