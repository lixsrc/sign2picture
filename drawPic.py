from PIL import Image
import numpy as np
import os
import math
import random

def create_sketch_portrait_with_randomness(portrait_path, signature_path, output_path, block_size=10, signature_size=(30, 30), max_signatures=10):
    """
    将人像图片转换为由签名叠加而成的素描效果图片，包含随机偏移和旋转。

    :param portrait_path: 人像图片的路径。
    :param signature_path: 签名图片的路径。
    :param output_path: 输出图片的路径。
    :param block_size: 每个签名块对应的人像图片区域的大小（像素）。
    :param signature_size: 签名图片在最终图像中的大小。
    :param max_signatures: 每个区域最多叠加的签名数量。
    """
    # 加载人像图片并转换为灰度
    portrait = Image.open(portrait_path).convert('L')
    portrait_width, portrait_height = portrait.size
    print(f"Original portrait size: {portrait_width}x{portrait_height}")

    # 计算缩小后的尺寸
    resized_width = math.ceil(portrait_width / block_size)
    resized_height = math.ceil(portrait_height / block_size)
    portrait_small = portrait.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    print(f"Resized portrait size: {resized_width}x{resized_height}")

    # 将灰度图转换为 NumPy 数组
    portrait_array = np.array(portrait_small)

    # 加载签名图片并确保是RGBA模式
    signature = Image.open(signature_path).convert('RGBA')
    signature = signature.resize(signature_size, Image.Resampling.LANCZOS)
    print(f"Signature size: {signature.size}")

    # 创建输出图片，背景为白色
    output_image = Image.new('RGBA', (resized_width * signature_size[0], resized_height * signature_size[1]), (255, 255, 255, 255))

    # 预计算签名的亮度（假设签名为黑色）
    signature_brightness = 0  # 黑色签名

    # 遍历每个像素块
    for y in range(resized_height):
        for x in range(resized_width):
            # 获取当前块的灰度值
            brightness = portrait_array[y, x]  # 0（黑）到 255（白）

            # 计算需要叠加的签名数量
            # 映射：brightness=0 -> max_signatures, brightness=255 -> 0
            num_signatures = int((255 - brightness) / 255 * max_signatures)
            if num_signatures < 0:
                num_signatures = 0
            elif num_signatures > max_signatures:
                num_signatures = max_signatures

            # 计算每个签名的透明度
            if num_signatures > 0:
                opacity = (255 - brightness) / (num_signatures * 255)
                opacity = min(max(opacity, 0), 1)  # 确保在0到1之间
            else:
                opacity = 0

            # 计算粘贴位置的基准坐标
            base_pos_x = x * signature_size[0]
            base_pos_y = y * signature_size[1]

            for _ in range(num_signatures):
                # 随机旋转角度
                angle = random.uniform(-30, 30)  # 旋转-30到+30度
                signature_rotated = signature.rotate(angle, expand=True)

                # 随机偏移
                max_offset = int(signature_size[0] * 0.5)  # 偏移不超过签名尺寸的20%
                offset_x = random.randint(-max_offset, max_offset)
                offset_y = random.randint(-max_offset, max_offset)
                paste_x = base_pos_x + offset_x
                paste_y = base_pos_y + offset_y

                # 调整签名的透明度
                signature_adjusted = signature_rotated.copy()
                # alpha = signature_adjusted.split()[3]
                # new_alpha = alpha.point(lambda p: int(p * opacity))
                # signature_adjusted.putalpha(new_alpha)

                # 粘贴签名到输出图片
                output_image.paste(signature_adjusted, (paste_x, paste_y), signature_adjusted)

        # 可选：显示进度
        if (y+1) % 50 == 0 or (y+1) == resized_height:
            print(f"Processing row {y+1} of {resized_height}")

    # 保存输出图片
    output_image.convert('RGB').save(output_path, 'PNG')
    print(f"Signature sketch portrait saved to {output_path}")

if __name__ == "__main__":
    # 示例用法
    portrait_image_path = "./out-pics/portrait.jpg"         # 替换为你的人像图片路径
    signature_image_path = "./out-pics/signature.png"       # 替换为你的签名图片路径
    output_image_path = "./out-pics/outPic.png"  # 输出图片路径

    # 检查文件是否存在
    if not os.path.exists(portrait_image_path):
        print(f"人像图片未找到: {portrait_image_path}")
    elif not os.path.exists(signature_image_path):
        print(f"签名图片未找到: {signature_image_path}")
    else:
        create_sketch_portrait_with_randomness(
            portrait_path=portrait_image_path,
            signature_path=signature_image_path,
            output_path=output_image_path,
            block_size=5,                # 每个签名块对应的人像图片区域大小，可根据需要调整
            signature_size=(100, 100),      # 签名图片在最终图像中的大小，可根据需要调整
            max_signatures=15            # 每个区域最多叠加的签名数量，可根据需要调整
        )