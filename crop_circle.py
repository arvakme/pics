#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import sys
import os

def crop_to_circle(image_path, output_path=None, size=None):
    """
    将图片裁剪为圆形
    
    参数:
    image_path: 输入图片路径
    output_path: 输出图片路径（如果为None，则自动生成）
    size: 输出图片尺寸，如果为None则使用原图的最小边长
    """
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"错误：找不到文件 '{image_path}'")
        return False
    
    # 如果没有指定输出路径，自动生成
    if output_path is None:
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_circle.png"
    
    try:
        # 打开图片
        img = Image.open(image_path).convert("RGBA")
        
        # 获取图片尺寸
        width, height = img.size
        print(f"原始图片尺寸: {width}x{height}")
        
        # 确定圆形的尺寸（取宽高中的最小值）
        if size is None:
            size = min(width, height)
        
        # 将图片调整为正方形
        if width != height:
            # 计算裁剪区域，使图片居中
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            img = img.crop((left, top, right, bottom))
        
        # 调整图片大小
        if img.size[0] != size:
            img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # 创建一个透明背景
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        
        # 创建圆形蒙版
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # 应用蒙版
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        # 保存图片
        output.save(output_path, 'PNG')
        print(f"✅ 圆形图片已保存到: {output_path}")
        print(f"   输出尺寸: {size}x{size}")
        return True
        
    except Exception as e:
        print(f"❌ 处理图片时出错: {str(e)}")
        return False

def main():
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python3 crop_circle.py <图片路径> [输出路径] [尺寸]")
        print("\n示例:")
        print("  python3 crop_circle.py avatar.jpg")
        print("  python3 crop_circle.py avatar.jpg output.png")
        print("  python3 crop_circle.py avatar.jpg output.png 300")
        sys.exit(1)
    
    # 获取参数
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    size = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    # 执行裁剪
    success = crop_to_circle(image_path, output_path, size)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
