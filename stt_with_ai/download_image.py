import requests

# Image URL and filename

url = 'https://s.isanook.com/ca/0/ud/285/1426955/istock-2163657039.jpg?ip/resize/w728/q80/jpg'
filename = 'Images/image.jpg'

# Download and save the image
response = requests.get(url)
if response.status_code == 200:
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f'Image saved as {filename}')
else:
    print('Failed to download image')