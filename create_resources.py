#!/usr/bin/env python3
"""
创建应用图标和界面资源的脚本
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=512, filename="icon.png"):
    """创建应用图标"""
    # 创建空白图像
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制蓝色圆形背景
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(33, 150, 243, 255), outline=(25, 118, 210, 255), width=4)
    
    # 绘制白色检查标记
    check_margin = size // 4
    check_points = [
        (check_margin, size // 2),
        (size // 2 - check_margin // 2, size - check_margin),
        (size - check_margin, check_margin)
    ]
    
    # 绘制线条
    draw.line(check_points[:2], fill=(255, 255, 255, 255), width=size//16, joint="curve")
    draw.line(check_points[1:], fill=(255, 255, 255, 255), width=size//16, joint="curve")
    
    # 保存图标
    img.save(filename, 'PNG', optimize=True)
    print(f"✓ 创建图标: {filename}")

def create_presplash(size=(1024, 1024), filename="presplash.png"):
    """创建启动画面"""
    img = Image.new('RGB', size, (33, 150, 243))
    draw = ImageDraw.Draw(img)
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font_size = size[0] // 20
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # 使用默认字体
        font = ImageFont.load_default()
    
    text = "SYSTEM"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    draw.text((text_x, text_y), text, fill=(255, 255, 255), font=font)
    
    # 保存启动画面
    img.save(filename, 'PNG', optimize=True)
    print(f"✓ 创建启动画面: {filename}")

def create_background(size=(1024, 1024), filename="background.png"):
    """创建背景图片"""
    img = Image.new('RGB', size, (248, 249, 250))
    draw = ImageDraw.Draw(img)
    
    # 添加渐变效果
    for y in range(size[1]):
        alpha = y / size[1]
        color = (
            int(248 + (33 - 248) * alpha),
            int(249 + (150 - 249) * alpha),
            int(250 + (243 - 250) * alpha)
        )
        draw.line([(0, y), (size[0], y)], fill=color)
    
    # 保存背景
    img.save(filename, 'PNG', optimize=True)
    print(f"✓ 创建背景图片: {filename}")

def main():
    """主函数"""
    print("创建应用资源文件...")
    print("=" * 40)
    
    # 创建资源目录
    os.makedirs("resources", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    
    # 创建各种尺寸的应用图标
    icon_sizes = [
        (512, "resources/icon-512.png"),
        (192, "resources/icon-192.png"),
        (144, "resources/icon-144.png"),
        (96, "resources/icon-96.png"),
        (72, "resources/icon-72.png"),
        (48, "resources/icon-48.png"),
        (36, "resources/icon-36.png")
    ]
    
    for size, filename in icon_sizes:
        create_icon(size, filename)
    
    # 复制主图标到项目根目录
    if os.path.exists("resources/icon-512.png"):
        import shutil
        shutil.copy("resources/icon-512.png", "icon.png")
        print("✓ 创建主图标: icon.png")
    
    # 创建启动画面和背景
    create_presplash((1024, 1024), "presplash.png")
    create_background((1024, 1024), "background.png")
    
    print("\n" + "=" * 40)
    print("✓ 所有资源文件创建完成！")
    print("\n生成的文件:")
    print("  - icon.png (主图标)")
    print("  - presplash.png (启动画面)")
    print("  - background.png (背景图片)")
    print("  - resources/ (各种尺寸的图标)")
    
    print("\n下一步:")
    print("1. 修改buildozer.spec中的图标和启动画面路径")
    print("2. 运行 build.sh 脚本构建APK")

if __name__ == "__main__":
    main()