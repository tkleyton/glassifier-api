import requests
from PIL import Image
import numpy as np


def request_img_glassifier(imgpath, apiurl):
    """
    Send a local image to the apiurl as a numpy array
    and returns a PIL.Image object with the response.
    """
    img = Image.open(imgpath)
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
