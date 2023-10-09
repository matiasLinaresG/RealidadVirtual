import os


def rename_images(folder_path):
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    if not image_files:
        print("No image files found in the specified directory.")
        return

    for i, image_file in enumerate(image_files):
        new_filename = f"calibration_image_{i}.jpg"
        old_filepath = os.path.join(folder_path, image_file)
        new_filepath = os.path.join(folder_path, new_filename)
        os.rename(old_filepath, new_filepath)
        print(f"Renamed: {image_file} to {new_filename}")


if __name__ == "__main__":
    folder_path = "C:/Users/jpss8/Desktop/calibration"  # Replace with the actual folder path
    rename_images(folder_path)
