import requests

# Image URL and filename

url = 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/19/86/ec/a5/spectrum-lounge-bar-at.jpg?w=600&h=-1&s=1'
filename = 'image.jpg'

# Download and save the image
response = requests.get(url)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Image saved as {filename}')
else:
    print('Failed to download image')