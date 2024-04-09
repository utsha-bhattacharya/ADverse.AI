from openai import OpenAI
from authtoken import OPENAI_API_KEY

#Function to generate AI based images 
def generate_images_using_openai(text, num_images=3, resolution=(256, 256)):
    # Map resolution to width and height
    resolution_mapping = {
        (256, 256): (256, 256),
        (512, 512): (512, 512),
        (1024, 1024): (1024, 1024)
    }

    # Ensure resolution is one of the available options, default to 256x256 otherwise
    width, height = resolution_mapping.get(resolution, (256, 256))

    client = OpenAI()
    response = client.images.generate(prompt=text, n=num_images, size=f"{width}x{height}")
    image_urls = [image_data.url for image_data in response.data]
    return image_urls
