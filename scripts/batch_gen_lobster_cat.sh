#!/bin/bash
# 批量生成120张穿龙虾衣服的加菲猫配图
# 场景x10 × 风格x12 = 120张

SCRIPT_DIR="/Users/bjd/Desktop/ZhugeDengpao-Team/skills/minimax-image-gen/scripts"
OUTPUT_DIR="/Users/bjd/Desktop/ZhugeDengpao-Team/images/ai-generated"
LOG_FILE="$OUTPUT_DIR/batch_gen.log"

# 场景列表
declare -a SCENES=(
  "办公室工作"
  "写作创作"
  "学习研究"
  "团队协作"
  "用户见证"
  "休闲放松"
  "出差旅行"
  "运动健身"
  "美食烹饪"
  "家庭生活"
)

# 风格列表
declare -a STYLES=(
  "写实摄影"
  "卡通插画"
  "水彩画"
  "油画"
  "极简主义"
  "赛博朋克"
  "复古漫画"
  "矢量扁平"
  "水墨国风"
  "像素艺术"
  "梦幻光影"
  "黑白素描"
)

# Base prompt
BASE_PROMPT="一只穿着红色龙虾衣服的橙色加菲猫 Garfield，"
COUNTER=0
TOTAL=120

echo "========================================" | tee "$LOG_FILE"
echo "开始生成120张龙虾加菲猫配图" | tee -a "$LOG_FILE"
echo "时间: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

for scene_idx in {0..9}; do
  for style_idx in {0..11}; do
    SCENE="${SCENES[$scene_idx]}"
    STYLE="${STYLES[$style_idx]}"
    COUNTER=$((COUNTER + 1))
    
    PROMPT="${BASE_PROMPT}场景：${SCENE}，风格：${STYLE}"
    FILENAME="lobster_cat_$(printf '%02d' $((scene_idx+1)))_$(printf '%02d' $((style_idx+1))).png"
    OUTPUT_PATH="$OUTPUT_DIR/$FILENAME"
    
    echo "[$COUNTER/$TOTAL] 生成中: $FILENAME" | tee -a "$LOG_FILE"
    echo "  Prompt: $PROMPT" | tee -a "$LOG_FILE"
    
    # 调用MiniMax API生成并下载
    python3 "$SCRIPT_DIR/generate_image.py" \
      --prompt "$PROMPT" \
      --aspect-ratio "1:1" \
      --output "$OUTPUT_PATH" 2>&1 | tee -a "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
      echo "  ✅ 成功: $FILENAME" | tee -a "$LOG_FILE"
    else
      echo "  ❌ 失败: $FILENAME" | tee -a "$LOG_FILE"
    fi
    
    echo "---" | tee -a "$LOG_FILE"
  done
done

echo "========================================" | tee -a "$LOG_FILE"
echo "全部完成！共生成 $COUNTER 张图片" | tee -a "$LOG_FILE"
echo "时间: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
