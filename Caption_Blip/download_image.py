import requests

# Image URL and filename

url = 'https://southeastasiaglobe.com/wp-content/uploads/2021/02/9dc1a336.jpg'
filename = 'image.jpg'

# Download and save the image
response = requests.get(url)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Image saved as {filename}')
else:
    print('Failed to download image')