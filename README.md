# glassifier-api
 Flask API that returns a stylized version of an image.

## Usage:
The provided requesting tool in `request_glassifier.py` opens an image path provided by the user, formats it and communicates with the server API. The returned object is a Pillow.Image object, which can be saved and/or displayed to the user.

See [mock_code.py](the mock code) to see an example usage.
