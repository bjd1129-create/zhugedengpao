#!/bin/bash
# 共享技能库同步脚本

LOG_FILE=/Users/bjd/logs/skills-sync.log
DATE=$(date '+%Y-%m-%d %H:%M:%S')
SHARED_SKILLS_DIR=/Users/bjd/intelligence/skills/shared

echo "[$DATE] 开始同步共享技能库..." >> $LOG_FILE

# 同步节点列表
NODES=(
  "100.88.114.49:arda:MBP"
  "100.87.46.33:bettysunday:i3"
  "100.64.158.68:JINDA:AZW"
)

for node in "${NODES[@]}"; do
  IFS=':' read -r ip user name <<< "$node"
  echo "同步到 $name ($ip)..." >> $LOG_FILE
  
  rsync -avz -e "ssh -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no" \
    $SHARED_SKILLS_DIR/ \
    $user@$ip:~/intelligence/skills/shared/ \
    >> $LOG_FILE 2>&1
  
  if [ $? -eq 0 ]; then
    echo "[$DATE] ✅ $name 同步成功" >> $LOG_FILE
  else
    echo "[$DATE] ❌ $name 同步失败" >> $LOG_FILE
  fi
done

echo "" >> $LOG_FILE
