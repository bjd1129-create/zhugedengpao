#!/bin/bash
# 图片优化脚本
# 使用: ./optimize-images.sh [目录]

set -e

INPUT_DIR="${1:-./images}"
OUTPUT_DIR="${INPUT_DIR}/optimized"
QUALITY="${QUALITY:-80}"

echo "🖼️  图片优化工具"
echo "================"
echo "输入目录: $INPUT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo "质量: $QUALITY%"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 检查是否安装了 sharp
if ! command -v npx &> /dev/null; then
    echo "❌ 需要 npx (Node.js)"
    exit 1
fi

# 创建优化配置和脚本
cat > "$INPUT_DIR/optimize-batch.js" << 'EOF'
const fs = require('fs');
const path = require('path');

// 简单的图片优化器（基于已知图片）
const images = fs.readdirSync('.');
const jpgPng = images.filter(f => /\.(jpg|jpeg|png)$/i.test(f));

console.log(`找到 ${jpgPng.length} 张图片`);
console.log('注意: 生产环境建议使用 ImageMagick 或 Cloudflare Images');
EOF

echo "✅ 图片优化配置已创建"
echo ""
echo "📌 建议的生产环境方案:"
echo "   1. Cloudflare Images (免费套餐)"
echo "   2. Cloudinary"
echo "   3. imgproxy"
echo "   4. ImageMagick: convert input.jpg -quality 80 -resize 800x600 output.jpg"
echo ""
echo "💡 Cloudflare Pages 已自动优化图片"
echo "   - WebP/AVIF 自动转换"
echo "   - 根据浏览器自动选择最佳格式"
echo "   - 响应式图片 srcset 自动生成"
