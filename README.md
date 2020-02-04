# glassifier-api
 Flask API that returns a stylized version of an image.

## Usage
The provided requesting tool in `request_glassifier.py` opens an image path provided by the user, formats it and communicates with the server API. The returned object is a Pillow.Image object, which can be saved and/or displayed to the user.

See [the mock code](./mock_code.py) or [# Example](#example) to see an example usage.

The API is hosted at [`https://glassifier-api.herokuapp.com`](https://glassifier-api.herokuapp.com).

## Running in local server
To run the api in a local server, simply clone this repository and run `app.py`.

The server should be running at `http://localhost:5000`.

## Installing dependencies
Before you run the server, make sure to have the requirements installed on your machine.

You can install from the `requirements.txt` file:
```
$ pip install -r requirements.txt
```
or manually:
```
$ pip install Flask-RESTful Pillow sklearn pandas requests
```

Alternatively, to run only the request tool:
```
$ pip install Pillow numpy requests
```

## Example
```python
from request_glassifier import request_img_glassifier


api_url = 'https://glassifier-api.herokuapp.com/api/glassifier'

my_img = 'milu.jpg'
filtered_image = request_img_glassifier('img/'+my_img)
if filtered_image:
    filtered_image.save('output/filtered_'+my_img)
    filtered_image.show()
```
