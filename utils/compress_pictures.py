# __author: Lambert
# __date: 2018/6/8 11:21
from PIL import Image
import os


def compress_picture(image_path):
    image = Image.open(image_path)
    dir_name = os.path.dirname(image_path)
    base, ext = os.path.splitext(os.path.basename(image_path))
    width = image.width
    height = image.height
    rate = 1.0  # 压缩率

    # 根据图像大小设置压缩率
    if width >= 2000 or height >= 2000:
        rate = 0.3
    elif width >= 1000 or height >= 1000:
        rate = 0.5
    elif width >= 500 or height >= 500:
        rate = 0.9

    width = int(width * rate)  # 新的宽
    height = int(height * rate)  # 新的高

    image.thumbnail((width, height), Image.ANTIALIAS)  # 生成缩略图
    image.save(os.path.join(dir_name, base + ext), 'JPEG')  # 保存到原路径
