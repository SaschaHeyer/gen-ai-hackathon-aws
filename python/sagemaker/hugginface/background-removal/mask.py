from PIL import Image

# Open the original image and the mask
original_image = Image.open("124079.png").convert("RGBA")  # Convert to RGBA to add transparency
mask = Image.open("output.png").convert("L")  # Ensure mask is in grayscale (L mode)

# Resize the mask to match the dimensions of the original image
mask = mask.resize(original_image.size, Image.LANCZOS)

# Apply the mask as an alpha channel
original_image.putalpha(mask)

# Save the image with the background removed
original_image.save("output_with_transparent_background.png")
