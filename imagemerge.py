from PIL import Image
from PIL import ImageDraw, ImageFont
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
def imagemergemat(usernames,directory, filelist):
    images, imagesizes = [], []
    for k in range(len(usernames)):
        image = Image.open(f'{directory}/{filelist[k]}.jpg')
        I1 = ImageDraw.Draw(image)
        myFont = ImageFont.truetype("../../Documents/ISSI/ImageJ/jre/lib/fonts/LucidaBrightDemiBold.ttf",35)
        I1.text((200,550),f"{usernames[k]}", font = myFont, fill = "#000")
        images.append(image)
        imagesizes.append(image.size[0])
    row = ceil(len(images)/3)
    new_image = Image.new('RGB',(min(3,len(images))*imagesizes[0], images[0].size[1]*row), (250,250,250))
    for k in range(len(images)):
        new_image.paste(images[k],(sum(imagesizes[3*floor(k/3):k]),images[0].size[1]*floor(k/3)))
    new_image.save(f"{directory}/mats-merged.jpg","JPEG")
#imagemergef("rasta","skull",["rastaflower", "rastaflower", "rastaflower", "rastaskull"])
directory = "skull"
image1 = Image.open(f'{directory}/rastaback.png')
image2 = Image.open(f'{directory}/rastamat1.jpg')
# Calculate width to be at the center
width = (image2.width - image1.width) // 2
# Calculate height to be at the center
height = (image2.height - image1.height) // 2
# Paste the frontImage at (width, height)
image2.paste(image1, (width, height), image1)
# Save this image
image2.save(f"{directory}/new.png", format="png")
