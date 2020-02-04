from request_glassifier import request_img_glassifier


#api_url = 'http://localhost:5000/api/glassifier'
api_url = 'https://glassifier-api.herokuapp.com/api/glassifier'

# The value above is set as the default for request_img_glassifier('img/path', api_url='http...')

#images = ["demogorgon.jpg", "flowers.jpg", "lion.jpg", "mirai.jpg", "rose.jpg"]
images = ["milu.jpg",]
for image in images:
    filtered_image = request_img_glassifier('img/'+image, api_url, n_clusters=20)
    if filtered_image:
        filtered_image.save('output/filtered_'+image)
