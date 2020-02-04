import requests
from PIL import Image
import numpy as np
from PIL.Image import ANTIALIAS


def resize(img, base_width=640):
    """
    Since the computational load grows exponentially
    with image size, large images should be avoided.
    """
    wpercent = (base_width / float(img.size[0]))
    if wpercent >= 1:
        return img
    hsize = int((float(img.size[1]) * float(wpercent)))

    resized_img = img.resize((base_width, hsize), ANTIALIAS)
    return resized_img

def request_img_glassifier(imgpath, apiurl):
    """
    Send a local image to the apiurl as a numpy array
    and returns a PIL.Image object with the response.
    """
    img = Image.open(imgpath)
    img = resize(img)
    imgarray = np.array(img)
    print("Requesting...")
    r = requests.post(apiurl,
                      json={"ndarray": imgarray.tolist()})
    print(f'Received with status code {r.status_code}.')
    if r.status_code != 200:
        return None
    data = r.json()
    array = np.array(data)
    returned_image = Image.fromarray(array.astype('uint8'))
    return returned_image
