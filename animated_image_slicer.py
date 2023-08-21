from PIL import Image

def slice_image(image_path, slice_height):
    # Open the input image
    original_image = Image.open(image_path)

    # Get the dimensions of the original image
    original_width, original_height = original_image.size

    # Calculate the number of slices needed
    num_slices = original_height // slice_height

    # Iterate through each slice and save it as a separate PNG
    for i in range(num_slices):
        # Calculate the coordinates for the current slice
        left = 0
        top = i * slice_height
        right = original_width
        bottom = (i + 1) * slice_height

        # Crop the slice from the original image
        slice_image = original_image.crop((left, top, right, bottom))

        # Save the slice as a separate PNG
        slice_image.save(f"output/slice_{i}.png")

        # Uncomment the following line to display each slice
        # slice_image.show()

    print(f"{num_slices} slices created.")

# Example usage:
image_path = input("Paste the path for the original image.\n")
image_path = image_path[1:-1]
slice_height = 128

slice_image(image_path, slice_height)