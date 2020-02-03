from request_glassifier import request_img_glassifier


api_url = 'https://glassifier-api.herokuapp.com/api/glassifier'
my_img_path = 'img/milu.jpg'
filtered_image = request_img_glassifier(my_img_path, api_url)
if filtered_image:
    filtered_image.save('output/filtered_milu.jpg')
    filtered_image.show()
