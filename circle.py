from PIL import Image, ImageDraw
def circle():
    # Load the base image
    image_path = 'combined_image.jpg'
    image = Image.open(image_path)

    # Create a black background with the desired size
    black_background = Image.new('RGB', image.size, 'black')

    # Create a mask with the same size as the image
    mask = Image.new('L', image.size, 0)  # 'L' mode for grayscale
    draw = ImageDraw.Draw(mask)
    center = (image.size[0] // 2, image.size[1] // 2)
    radius = min(image.size) // 2.15 # Adjust the radius as needed
    draw.ellipse([(center[0] - radius, center[1] - radius), (center[0] + radius, center[1] + radius)], fill=255)

    # Apply the circular mask to the image
    circular_cutout = image.copy()
    circular_cutout.putalpha(mask)

    # Convert black background to RGBA to handle alpha channel in the cutout
    black_background = black_background.convert('RGB')

    # Paste the circular cutout onto the black background
    black_background.paste(circular_cutout, (0, 0), circular_cutout)

    # Save the final image
    black_background.save('output_image.jpg')

    # Display the result
    #black_background.show()
