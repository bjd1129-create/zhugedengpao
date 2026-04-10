#!/bin/bash
# dispatch.sh - 大花团队 CrewAI 任务一键下发脚本
# 用法: ./dispatch.sh <crew_type> [params...]
#
# 示例:
#   ./dispatch.sh content "AI如何帮普通人提升效率" "官网"
#   ./dispatch.sh trading "BTC" 5000
#   ./dispatch.sh daily_ops
#   ./dispatch.sh research "DeFi市场分析"

set -e

BRIDGE_URL="http://127.0.0.1:8001"
USER_ID="laozhuang"

# 检查 Bridge 服务
check_bridge() {
    if ! curl -s --max-time 3 "$BRIDGE_URL/api/health" | grep -q "healthy"; then
        echo "❌ Bridge 服务未运行，请先启动: cd crewai-automation && python main.py"
        exit 1
    fi
}

# 提交内容创作任务
create_content() {
    local topic="$1"
    local platform="${2:-官网}"
    
    if [ -z "$topic" ]; then
        echo "❌ 请提供文章主题"
        echo "用法: $0 content <主题> [平台]"
        exit 1
    fi
    
    echo "📝 提交内容创作任务..."
    echo "   主题: $topic"
    echo "   平台: $platform"
    
    RESPONSE=$(curl -s -X POST "$BRIDGE_URL/api/tasks/start" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_type\": \"content\",
            \"user_id\": \"$USER_ID\",
            \"params\": {\"topic\": \"$topic\", \"platform\": \"$platform\"},
            \"description\": \"内容创作: $topic\"
        }")
    
    TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
    echo "✅ 任务已提交，ID: $TASK_ID"
    echo "🔍 查看进度: curl $BRIDGE_URL/api/tasks/$TASK_ID"
}

# 提交交易分析任务
create_trading() {
    local symbol="$1"
    local amount="${2:-1000}"
    
    if [ -z "$symbol" ]; then
        echo "❌ 请提供交易品种"
        echo "用法: $0 trading <品种> [金额]"
        exit 1
    fi
    
    echo "📊 提交交易分析任务..."
    echo "   品种: $symbol"
    echo "   金额: \$$amount"
    
    RESPONSE=$(curl -s -X POST "$BRIDGE_URL/api/tasks/start" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_type\": \"trading\",
            \"user_id\": \"$USER_ID\",
            \"params\": {\"symbol\": \"$symbol\", \"amount\": $amount, \"trade_type\": \"analysis\"},
            \"description\": \"交易分析: $symbol \$$amount\"
        }")
    
    TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
    echo "✅ 任务已提交，ID: $TASK_ID"
}

# 提交每日运营任务
create_daily_ops() {
    local date=$(date +%Y-%m-%d)
    
    echo "📋 提交每日运营任务..."
    echo "   日期: $date"
    
    RESPONSE=$(curl -s -X POST "$BRIDGE_URL/api/tasks/start" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_type\": \"daily_ops\",
            \"user_id\": \"$USER_ID\",
            \"params\": {\"date\": \"$date\"},
            \"description\": \"每日运营: $date\"
        }")
    
    TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
    echo "✅ 任务已提交，ID: $TASK_ID"
}

# 提交深度调研任务
create_research() {
    local topic="$1"
    
    if [ -z "$topic" ]; then
        echo "❌ 请提供调研主题"
        echo "用法: $0 research <主题>"
        exit 1
    fi
    
    echo "🔬 提交深度调研任务..."
    echo "   主题: $topic"
    
    RESPONSE=$(curl -s -X POST "$BRIDGE_URL/api/tasks/start" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_type\": \"research\",
            \"user_id\": \"$USER_ID\",
            \"params\": {\"research_topic\": \"$topic\"},
            \"description\": \"深度调研: $topic\"
        }")
    
    TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
    echo "✅ 任务已提交，ID: $TASK_ID"
}

# 查看任务状态
check_task() {
    local task_id="$1"
    
    if [ -z "$task_id" ]; then
        echo "❌ 请提供任务 ID"
        echo "用法: $0 status <task_id>"
        exit 1
    fi
    
    echo "🔍 任务状态: $task_id"
    curl -s "$BRIDGE_URL/api/tasks/$task_id" | python3 -m json.tool
}

# 列出所有任务
list_tasks() {
    echo "📋 所有任务:"
    curl -s "$BRIDGE_URL/api/tasks" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for t in data.get('tasks', []):
    status = t['status']
    emoji = {'completed': '✅', 'running': '🔄', 'pending': '⏳', 'failed': '❌'}.get(status, '❓')
    print(f\"{emoji} {t['task_id']} | {t['task_type']:10} | {status:10} | {t.get('description','')}[:50]\")
"
}

# 帮助信息
show_help() {
    echo "🦐 大花团队 CrewAI 任务调度脚本"
    echo ""
    echo "用法: $0 <命令> [参数...]"
    echo ""
    echo "命令:"
    echo "  content  <主题> [平台]          内容创作（Scout调研→Quill写作→Observer审核→Captain发布）"
    echo "  trading  <品种> [金额]           交易分析（Strategist分析→Captain审批→Observer复盘）"
    echo "  daily_ops                       每日运营（情报收集→市场分析→决策→审核）"
    echo "  research <主题>                  深度调研（调研→战略分析→可行性评估→决策）"
    echo "  developer <描述> [文件] [栈]     代码开发（Scout调研→Engineer写代码→Observer审查→Captain批准）"
    echo "  status   <task_id>              查看任务状态"
    echo "  list                            列出所有任务"
    echo "  health                          检查服务状态"
    echo ""
    echo "示例:"
    echo "  $0 content \"AI龙虾的日常\" \"官网\""
    echo "  $0 trading BTC 5000"
    echo "  $0 daily_ops"
    echo "  $0 research \"2026年DeFi市场趋势\""
    echo "  $0 status 2d5c68bf"
}

# 提交代码开发任务
create_developer() {
    local desc="$1"
    local target="$2"
    local stack="$3"
    
    if [ -z "$desc" ]; then
        echo "❌ 请提供开发任务描述"
        echo "用法: $0 developer <描述> [目标文件] [技术栈]"
        exit 1
    fi
    
    echo "💻 提交代码开发任务..."
    echo "   描述：$desc"
    
    RESPONSE=$(curl -s -X POST "$BRIDGE_URL/api/tasks/start" \
        -H "Content-Type: application/json" \
        -d "{
            \"task_type\": \"developer\",
            \"user_id\": \"$USER_ID\",
            \"params\": {\"task_description\": \"$desc\", \"target_file\": \"$target\", \"tech_stack\": \"$stack\"},
            \"description\": \"开发任务：$desc\"
        }")
    
    TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
    echo "✅ 任务已提交，ID: $TASK_ID"
}

# 主逻辑
main() {
    local cmd="${1:-help}"
    shift 2>/dev/null || true
    
    case "$cmd" in
        content)   check_bridge; create_content "$@" ;;
        trading)   check_bridge; create_trading "$@" ;;
        daily_ops) check_bridge; create_daily_ops ;;
        research)  check_bridge; create_research "$@" ;;
        developer) check_bridge; create_developer "$@" ;;
        status)    check_bridge; check_task "$@" ;;
        list)      check_bridge; list_tasks ;;
        health)    curl -s "$BRIDGE_URL/api/health" | python3 -m json.tool ;;
        help|--help|-h|*) show_help ;;
    esac
}

main "$@"
