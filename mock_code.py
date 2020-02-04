from request_glassifier import request_img_glassifier


# api_url = 'https://glassifier-api.herokuapp.com/api/glassifier'
# The value above is set as the default for request_img_glassifier('img/path', api_url='http...')
my_img = 'milu.jpg'
filtered_image = request_img_glassifier('img/'+my_img)
if filtered_image:
    filtered_image.save('output/filtered_'+my_img)
    filtered_image.show()
