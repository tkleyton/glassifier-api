from request_glassifier import request_img_glassifier


api_url = 'https://glassifier-api.herokuapp.com/api/glassifier'
my_img_path = 'img/cat.jpg'
filtered_image = request_img_glassifier(my_img_path, api_url)
filtered_image.save('output/filtered_cat.jpg')
filtered_image.show()