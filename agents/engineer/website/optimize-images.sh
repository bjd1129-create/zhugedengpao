#!/bin/bash
# 图片优化脚本 - 压缩 pages 目录下的所有 JPG/PNG 图片
# 使用 ImageMagick 或 sips (macOS 自带)

cd "$(dirname "$0")"

echo "🔍 开始优化图片..."
echo "📂 工作目录：$(pwd)"

# 检查是否有 sips (macOS)
if command -v sips &> /dev/null; then
    echo "📱 使用 sips (macOS 自带)"
    
    count=0
    total_saved=0
    
    for img in pages/*.jpg pages/*.jpeg pages/*.png; do
        if [ -f "$img" ]; then
            original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
            
            # 压缩到 85% 质量，最大宽度 1920px
            sips -s formatOptions 85 --resampleWidth 1920 "$img" 2>/dev/null
            
            if [ -f "$img" ]; then
                new_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
                saved=$((original_size - new_size))
                if [ $saved -gt 0 ]; then
                    saved_kb=$((saved / 1024))
                    total_saved=$((total_saved + saved_kb))
                    count=$((count + 1))
                    echo "✅ $img: 节省 ${saved_kb}KB"
                fi
            fi
        fi
    done
    
    echo ""
    echo "✨ 优化完成！"
    echo "📊 共优化 $count 张图片，总计节省 ${total_saved}KB"
    
elif command -v magick &> /dev/null; then
    echo "🖼️ 使用 ImageMagick"
    
    for img in pages/*.jpg pages/*.jpeg pages/*.png; do
        if [ -f "$img" ]; then
            original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
            
            # 压缩到 85% 质量，最大宽度 1920px
            magick "$img" -quality 85 -resize 1920x1920\> "$img"
            
            if [ -f "$img" ]; then
                new_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
                saved=$((original_size - new_size))
                if [ $saved -gt 0 ]; then
                    saved_kb=$((saved / 1024))
                    echo "✅ $img: 节省 ${saved_kb}KB"
                fi
            fi
        fi
    done
    
else
    echo "❌ 未找到图片处理工具"
    echo "请安装 ImageMagick: brew install imagemagick"
    exit 1
fi

echo "✨ 图片优化完成!"
