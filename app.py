from flask import Flask
from flask import request, send_file, render_template
from glassifier import Glassifier
from numpy import array
from PIL import Image
from flask_restful import Api, Resource


app = Flask(__name__, static_folder="static", template_folder="templates")
api = Api(app)


def img_filter(img_array, n_clusters=25, **kwargs):
    print("Filtering...")
    filtered = Glassifier(n_clusters=n_clusters).load_image_array(
            img_array).glassify(as_array=True)

    return filtered


class ImageFilter(Resource):
    def post(self):
        """
        Receives an image in numpy array format wrapped in a json
        object as {'ndarray': numpy.array}, process it through
        a filter and returns the image also as numpy array.
        """
        data = request.get_json(silent=True)
        try:
            img_array = array(data['ndarray'])
            n_clusters = int(data['n_clusters'])
            filtered = img_filter(img_array, n_clusters=n_clusters)
        except Exception:
            return "Invalid format. Use the provided request tool.", 400

        return filtered.tolist()


@app.route('/')
def serve_img():
    return render_template('index.html', title='Home')


api.add_resource(ImageFilter, '/api/glassifier')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
