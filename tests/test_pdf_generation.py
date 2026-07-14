from PIL import Image

# 1. Provide the list of image file paths in the exact order you want them
image_files = ["frame1.png", "frame2.png", "frame3.png"]

# 2. Open all images and convert them to RGB mode
opened_images = []
for file in image_files:
    img = Image.open(file)
    opened_images.append(img.convert("RGB"))

# 3. Take the first image and append the remaining images to it
first_image = opened_images[0]
remaining_images = opened_images[1:]

# 4. Save everything together as a single PDF
output_pdf_path = "combined_photos.pdf"
first_image.save(output_pdf_path, "PDF", save_all=True, append_images=remaining_images)

print(f"Successfully joined {len(image_files)} photos into {output_pdf_path}!")
