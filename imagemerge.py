from PIL import Image
from math import ceil, floor
def imagemergef(player,directory, filenamelist):
    images, imagesizes = [], []
    for name in filenamelist:
        image = Image.open(f'{directory}/{name}.jpg')
        images.append(image)
        imagesizes.append(image.size[0])
    row = ceil(len(images)/5)
    new_image = Image.new('RGB',(min(5,len(images))*imagesizes[0], images[0].size[1]*row), (250,250,250))
    for k in range(len(images)):
        new_image.paste(images[k],(sum(imagesizes[5*floor(k/5):k]),images[0].size[1]*floor(k/5)))
    new_image.save(f"{directory}/{player}-merged.jpg","JPEG")
#    new_image.show()

#imagemerge("sushigo",[1,1,1,1,1,1,1,1,1,1])
