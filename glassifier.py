from pandas import DataFrame
from PIL import Image
from numpy import array as nparray
from numpy import hstack as nphstack, indices as npindices
from numpy import concatenate
from numpy import uint8
from numpy import newaxis
from PIL.Image import ANTIALIAS
# from PIL.ImageFilter import GaussianBlur
from sklearn.cluster import KMeans


class Glassifier:
    """
    Image filter based on pixel clustering using sklearn k-means.


    Example usage:
    >>>glassifier = Glassifier()
    >>>glassifier.load_image('/path/to/img.jpg')
    >>>transformed_img = glassifier.glassify()
    >>>display(transformed_img)
    >>>transformed_img.save('/path/to/output.jpg')
    """

    def __init__(self, n_clusters=15, base_width=640, edge_size=0):
        try:
            self.n_clusters = int(abs(n_clusters))
            self.base_width = int(abs(base_width))
            self.edge_size = int(abs(edge_size))
        except ValueError:
            raise Exception("""Numeric arguments couldn't
         be converted to positive integers.""")

    def load_image(self, filename):
        """
        Load PIL.Image objects from file path and transform
        it to numpy.array to pass to the clustering algorithm.
        """
        self.img = Image.open(filename)
        self.img = self.resize(self.img)
        self.array = nparray(self.img)
        return self

    def load_image_array(self, imarray):
        """
        Load images in numpy.array form and resizes it to
        pass to the clustering algorithm.
        """
        self.img = Image.fromarray(imarray.astype('uint8'))
        self.img = self.resize(self.img)
        self.array = nparray(self.img)
        return self

    def resize(self, img):
        """
        Since the computational load grows exponentially
        with image size, large images should be avoided.
        """
        wpercent = (self.base_width / float(img.size[0]))
        if wpercent >= 1:
            return img
        hsize = int((float(img.size[1]) * float(wpercent)))

        resized_img = img.resize((self.base_width, hsize), ANTIALIAS)
        return resized_img

    def edge_detect(self, arr, edge_size=0):
        """
        Identifies the indexes of pixels at the borders
        of clusters and changes the values of the bordering pixels to 0.
        """

        if not edge_size:
            return arr

        shape = arr.shape
        arr = arr.reshape(-1,)
        edge_idx = [i for i in range(1, len(arr)) if not arr[i] == arr[i-1]]
        for idx in edge_idx:
            for i in range(edge_size):
                try:
                    arr[idx+i] = 0
                except Exception:
                    pass
                try:
                    arr[idx-i] = 0
                except Exception:
                    pass
        return arr.reshape(shape)

    def imarray2df(self, arr):
        """
        From a 2D image array, make a dataframe with
        the X and Y indexes and the pixel values columns.
        """
        return DataFrame(nphstack((
                        npindices(arr.shape).reshape(2, arr.size).T,
                        arr.reshape(-1, 1))), columns=['x', 'y', 'value'])

    def unpackRGB(self, arr):
        img_R, img_G, img_B = arr[..., 0], arr[..., 1], arr[..., 2]
        return img_R, img_G, img_B

    def glassify(self, as_array=False):
        """
        Applies the k-means algorithm to the image converted
        to numpy array to each color channel.

        The image should be pre-loaded with
        self.load_image('/path/to/img.jpg')
        before calling glassify().
        Returns a PIL Image Object.
        """
        arrays = []
        img_R, img_G, img_B = self.unpackRGB(self.array)

        for img_arr in (img_R, img_G, img_B):
            X = self.imarray2df(img_arr)

            kmeans = KMeans(n_clusters=self.n_clusters,
                            init='k-means++', max_iter=1, n_init=1)
            y_kmeans = kmeans.fit_predict(X)

            clusters_avg = kmeans.cluster_centers_[..., 2][y_kmeans]
            array = clusters_avg.reshape(img_arr.shape)
            array = array.astype(uint8)
            array = self.edge_detect(array, self.edge_size)
            # array = nparray(Image.fromarray(array).\
            #               filter(GaussianBlur(radius=0.7)))
            arrays.append(array)
        glassified_array = concatenate([arrays[i][..., newaxis]
                                        for i in range(3)], axis=2)

        if as_array:
            self.glassified = glassified_array
        else:
            self.glassified = Image.fromarray(glassified_array)
        return self.glassified
