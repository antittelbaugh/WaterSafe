from PIL import Image
def combine():
    # Define the grid layout (rows, columns)
    rows = 3
    columns = 2

    # List of image file paths (change these to your images)
    image_paths = [
        '1.jpg',
        '6.jpg',
        '2.jpg',
        '5.jpg',
        '3.jpg',
        '4.jpg',
    ]

    # Load the images
    images = [Image.open(path) for path in image_paths]

    # Determine the size of the images (assuming all images are the same size)
    image_width, image_height = images[0].size

    # Calculate the size of the final combined image
    final_width = image_width * columns
    final_height = image_height * rows

    # Create a blank image with the size of the final combined image
    final_image = Image.new('RGB', (final_width, final_height))

    # Combine the images into the final image according to the grid layout
    for index, img in enumerate(images):
        # Calculate the row and column position of the current image
        row = index // columns
        col = index % columns
    
        # Calculate the top-left corner position of the current image in the final image
        x = col * image_width
        y = row * image_height
    
        # Paste the image into the final image at the calculated position
        final_image.paste(img, (x, y))

    # Save the final combined image
    final_image.save('combined_image.jpg')

    
