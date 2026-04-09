#!/bin/bash
# 生成缩略图脚本 - 为漫画图片生成 400px 宽的缩略图
# 缩略图存储在 pages/thumbnails/

cd "$(dirname "$0")"

THUMB_DIR="pages/thumbnails"
mkdir -p "$THUMB_DIR"

echo "🔍 开始生成缩略图..."
echo "📂 输出目录：$THUMB_DIR"

count=0
total_saved=0

# 检查是否有 sips (macOS)
if command -v sips &> /dev/null; then
    echo "📱 使用 sips (macOS 自带)"
    
    for img in pages/images/comic*.jpg pages/images/comic*.png; do
        if [ -f "$img" ]; then
            # 获取文件名
            filename=$(basename "$img")
            thumb_path="$THUMB_DIR/$filename"
            
            # 如果缩略图不存在或原图已更新
            if [ ! -f "$thumb_path" ] || [ "$img" -nt "$thumb_path" ]; then
                original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
                
                # 生成 400px 宽的缩略图，质量 80%
                sips -s formatOptions 80 --resampleWidth 400 "$img" --out "$thumb_path" 2>/dev/null
                
                if [ -f "$thumb_path" ]; then
                    new_size=$(stat -f%z "$thumb_path" 2>/dev/null || stat -c%s "$thumb_path" 2>/dev/null)
                    saved=$((original_size - new_size))
                    if [ $saved -gt 0 ]; then
                        saved_kb=$((saved / 1024))
                        total_saved=$((total_saved + saved_kb))
                        count=$((count + 1))
                        echo "✅ $filename: ${saved_kb}KB → $((new_size/1024))KB"
                    fi
                fi
            fi
        fi
    done
    
elif command -v magick &> /dev/null; then
    echo "🖼️ 使用 ImageMagick"
    
    for img in pages/images/comic*.jpg pages/images/comic*.png; do
        if [ -f "$img" ]; then
            filename=$(basename "$img")
            thumb_path="$THUMB_DIR/$filename"
            
            if [ ! -f "$thumb_path" ] || [ "$img" -nt "$thumb_path" ]; then
                original_size=$(stat -f%z "$img" 2>/dev/null || stat -c%s "$img" 2>/dev/null)
                magick "$img" -quality 80 -resize 400x400 "$thumb_path"
                
                if [ -f "$thumb_path" ]; then
                    new_size=$(stat -f%z "$thumb_path" 2>/dev/null || stat -c%s "$thumb_path" 2>/dev/null)
                    saved=$((original_size - new_size))
                    if [ $saved -gt 0 ]; then
                        saved_kb=$((saved / 1024))
                        total_saved=$((total_saved + saved_kb))
                        count=$((count + 1))
                        echo "✅ $filename: ${saved_kb}KB → $((new_size/1024))KB"
                    fi
                fi
            fi
        fi
    done
else
    echo "❌ 未找到图片处理工具"
    echo "请安装 ImageMagick: brew install imagemagick"
    exit 1
fi

echo ""
echo "✨ 缩略图生成完成！"
echo "📊 共生成 $count 张缩略图，总计节省 ${total_saved}KB"
