import os
from PIL import Image
def cut_image(image):
    # 读取图片大小
    width, height = image.size
    item_width = int(width / 3)
    box_list = []
    # 两重循环，生成9张图片基于原图的位置
    for i in range(0, 3):
        for j in range(0, 3):
            box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
            box_list.append(box)

    image_list = [image.crop(box) for box in box_list]
    # 利用save_images保存切割好的图
    save_images(image_list)


def save_images(image_list):
    path = './problem'
    if not os.path.exists(path):
        os.mkdir('problem')
    index = 1
    for image in image_list:
        image.save('./problem/'+str(index) + '.png')
        index += 1
img = Image.open('photo.jpg')
cut_image(img)
