from flask import Flask
from flask import request, send_file
from glassifier import Glassifier
import numpy as np
from PIL import Image
from io import BytesIO
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


def img_filter(img_array):
    print("Filtering...")
    filtered = Glassifier(n_clusters=13).load_image_array(
            img_array).glassify(as_array=True)

    return filtered


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')


class ImageFilter(Resource):
    # @app.route('/api/glassifier', methods=['POST'])
    def post(self):
        """
        Receives an image in numpy array format wrapped in a json
        object as {'ndarray': numpy.array}, process it through
        a filter and returns the image also as numpy array.
        """
        data = request.get_json(silent=True)
        try:
            img_array = np.array(data['ndarray'])
        except Exception:
            return "Invalid format. See documentation.", 400
        filtered = img_filter(img_array)
        return filtered.tolist()


@app.route('/')
def serve_img():
    img = Image.open('output/api.jpg')
    return serve_pil_image(img)


api.add_resource(ImageFilter, '/api/glassifier')


if __name__ == "__main__":
    app.run(port=5000)
