#!/bin/bash
# TODO Tracker Script
# Usage: todo.sh <command> [args]
#   add <priority> <item>  - Add item (priority: high|medium|low)
#   done <pattern>         - Mark matching item as done
#   remove <pattern>       - Remove matching item
#   list [priority]        - List items, optionally by priority
#   summary                - Quick summary for heartbeat

set -e

TODO_FILE="${TODO_FILE:-TODO.md}"
DATE=$(date +%Y-%m-%d)

# Ensure TODO.md exists with proper structure
init_todo() {
    if [[ ! -f "$TODO_FILE" ]]; then
        cat > "$TODO_FILE" << 'EOF'
# TODO - Nuri Scratch Pad

*Last updated: DATE_PLACEHOLDER*

## 🔴 High Priority

## 🟡 Medium Priority

## 🟢 Nice to Have

## ✅ Done

---

## Notes

EOF
        sed -i '' "s/DATE_PLACEHOLDER/$DATE/" "$TODO_FILE" 2>/dev/null || \
        sed -i "s/DATE_PLACEHOLDER/$DATE/" "$TODO_FILE"
    fi
}

# Update the "Last updated" date
update_date() {
    sed -i '' "s/\*Last updated:.*\*/*Last updated: $DATE*/" "$TODO_FILE" 2>/dev/null || \
    sed -i "s/\*Last updated:.*\*/*Last updated: $DATE*/" "$TODO_FILE"
}

# Add an item
add_item() {
    local priority="$1"
    local item="$2"
    
    init_todo
    
    local section=""
    case "$priority" in
        high)   section="## 🔴 High Priority" ;;
        medium) section="## 🟡 Medium Priority" ;;
        low)    section="## 🟢 Nice to Have" ;;
        *)      section="## 🟡 Medium Priority"; item="$priority $item" ;;
    esac
    
    # Find the section and add item after it
    local entry="- [ ] $item (added: $DATE)"
    
    # Use awk to insert after the section header
    awk -v section="$section" -v entry="$entry" '
        $0 == section { print; print entry; next }
        { print }
    ' "$TODO_FILE" > "$TODO_FILE.tmp" && mv "$TODO_FILE.tmp" "$TODO_FILE"
    
    update_date
    echo "✅ Added to $priority priority: $item"
}

# Mark item as done
mark_done() {
    local pattern="$1"
    
    # Find and move the item
    if grep -q "\- \[ \].*$pattern" "$TODO_FILE"; then
        # Extract the item text
        local item=$(grep -m1 "\- \[ \].*$pattern" "$TODO_FILE" | sed 's/- \[ \] //' | sed 's/ (added:.*//')
        
        # Remove from current location
        sed -i '' "/\- \[ \].*$pattern/d" "$TODO_FILE" 2>/dev/null || \
        sed -i "/\- \[ \].*$pattern/d" "$TODO_FILE"
        
        # Add to Done section
        local done_entry="- [x] $item (done: $DATE)"
        awk -v section="## ✅ Done" -v entry="$done_entry" '
            $0 == section { print; print entry; next }
            { print }
        ' "$TODO_FILE" > "$TODO_FILE.tmp" && mv "$TODO_FILE.tmp" "$TODO_FILE"
        
        update_date
        echo "✅ Marked done: $item"
    else
        echo "❌ No matching item found for: $pattern"
        exit 1
    fi
}

# Remove item completely
remove_item() {
    local pattern="$1"
    
    if grep -q "\- \[.\].*$pattern" "$TODO_FILE"; then
        sed -i '' "/\- \[.\].*$pattern/d" "$TODO_FILE" 2>/dev/null || \
        sed -i "/\- \[.\].*$pattern/d" "$TODO_FILE"
        update_date
        echo "🗑️ Removed item matching: $pattern"
    else
        echo "❌ No matching item found for: $pattern"
        exit 1
    fi
}

# List items
list_items() {
    local priority="$1"
    
    init_todo
    
    if [[ -z "$priority" ]]; then
        cat "$TODO_FILE"
    else
        local section=""
        case "$priority" in
            high)   section="High Priority" ;;
            medium) section="Medium Priority" ;;
            low)    section="Nice to Have" ;;
            done)   section="Done" ;;
        esac
        
        awk -v section="$section" '
            $0 ~ section { found=1 }
            found && /^## / && $0 !~ section { found=0 }
            found { print }
        ' "$TODO_FILE"
    fi
}

# Summary for heartbeat
summary() {
    init_todo
    
    # Count by section
    local high_count=$(awk '/🔴 High/,/^## 🟡/' "$TODO_FILE" | grep -c "^- \[ \]" 2>/dev/null || echo 0)
    local med_count=$(awk '/🟡 Medium/,/^## 🟢/' "$TODO_FILE" | grep -c "^- \[ \]" 2>/dev/null || echo 0)
    local low_count=$(awk '/🟢 Nice/,/^## ✅/' "$TODO_FILE" | grep -c "^- \[ \]" 2>/dev/null || echo 0)
    local total=$((high_count + med_count + low_count))
    
    # Check for stale items (>7 days old)
    local stale=0
    local week_ago=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)
    while IFS= read -r line; do
        if [[ "$line" =~ added:\ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
            local added="${BASH_REMATCH[1]}"
            if [[ "$added" < "$week_ago" ]]; then
                ((stale++))
            fi
        fi
    done < <(grep "^- \[ \]" "$TODO_FILE")
    
    echo "📋 TODO: $total items ($high_count high, $med_count medium, $low_count low)"
    if [[ $stale -gt 0 ]]; then
        echo "⚠️ $stale stale items (>7 days old)"
    fi
    if [[ $high_count -gt 0 ]]; then
        echo "🔴 High priority items:"
        awk '/🔴 High/,/^## 🟡/' "$TODO_FILE" | grep "^- \[ \]" | head -3 | sed 's/- \[ \] /  • /' | sed 's/ (added:.*//' | sed 's/\*\*//g'
    fi
}

# Stale check - detailed overdue detection
stale_check() {
    init_todo
    
    local today=$(date +%Y-%m-%d)
    local high_overdue=0
    local med_overdue=0
    local low_overdue=0
    local total_overdue=0
    local health_score=100
    
    # Get date thresholds
    local high_threshold=$(date -v-3d +%Y-%m-%d 2>/dev/null || date -d "3 days ago" +%Y-%m-%d)
    local med_threshold=$(date -v-7d +%Y-%m-%d 2>/dev/null || date -d "7 days ago" +%Y-%m-%d)
    local low_threshold=$(date -v-14d +%Y-%m-%d 2>/dev/null || date -d "14 days ago" +%Y-%m-%d)
    
    # Check high priority items
    while IFS= read -r line; do
        if [[ "$line" =~ added:\ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
            local added="${BASH_REMATCH[1]}"
            if [[ "$added" < "$high_threshold" ]]; then
                ((high_overdue++))
                ((total_overdue++))
                echo "🔴 High overdue: ${line#- \[ \]} (added: $added)"
            fi
        fi
    done < <(awk '/🔴 High/,/^## 🟡/' "$TODO_FILE" | grep "^- \[ \]")
    
    # Check medium priority items
    while IFS= read -r line; do
        if [[ "$line" =~ added:\ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
            local added="${BASH_REMATCH[1]}"
            if [[ "$added" < "$med_threshold" ]]; then
                ((med_overdue++))
                ((total_overdue++))
                echo "🟡 Medium overdue: ${line#- \[ \]} (added: $added)"
            fi
        fi
    done < <(awk '/🟡 Medium/,/^## 🟢/' "$TODO_FILE" | grep "^- \[ \]")
    
    # Check low priority items
    while IFS= read -r line; do
        if [[ "$line" =~ added:\ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
            local added="${BASH_REMATCH[1]}"
            if [[ "$added" < "$low_threshold" ]]; then
                ((low_overdue++))
                ((total_overdue++))
                echo "🟢 Low overdue: ${line#- \[ \]} (added: $added)"
            fi
        fi
    done < <(awk '/🟢 Nice/,/^## ✅/' "$TODO_FILE" | grep "^- \[ \]")
    
    # Calculate health score
    if [[ $total_overdue -gt 0 ]]; then
        health_score=$((100 - total_overdue * 10))
        [[ $health_score -lt 0 ]] && health_score=0
    fi
    
    # Output summary
    echo ""
    echo "═══════════════════════════════════════"
    echo "📊 逾期检测报告"
    echo "═══════════════════════════════════════"
    echo "🔴 高优先级逾期 (>3天): $high_overdue"
    echo "🟡 中优先级逾期 (>7天): $med_overdue"
    echo "🟢 低优先级逾期 (>14天): $low_overdue"
    echo "───────────────────────────────────────"
    echo "📈 健康度评分: $health_score/100"
    
    if [[ $health_score -ge 90 ]]; then
        echo "🟢 状态: 优秀"
    elif [[ $health_score -ge 70 ]]; then
        echo "🟡 状态: 良好"
    elif [[ $health_score -ge 50 ]]; then
        echo "🟠 状态: 警告"
    else
        echo "🔴 状态: 危险"
    fi
    echo "═══════════════════════════════════════"
    
    if [[ $total_overdue -gt 0 ]]; then
        echo ""
        echo "建议: 使用 'todo.sh done <pattern>' 标记完成"
        echo "      或 'todo.sh remove <pattern>' 删除不需要的任务"
    fi
}

# Main
case "$1" in
    add)
        add_item "$2" "$3"
        ;;
    done)
        mark_done "$2"
        ;;
    remove)
        remove_item "$2"
        ;;
    list)
        list_items "$2"
        ;;
    summary)
        summary
        ;;
    stale-check)
        stale_check
        ;;
    *)
        echo "Usage: todo.sh <command> [args]"
        echo "  add <priority> <item>  - Add item (priority: high|medium|low)"
        echo "  done <pattern>         - Mark matching item as done"
        echo "  remove <pattern>       - Remove matching item"
        echo "  list [priority]        - List items (high|medium|low|done)"
        echo "  summary                - Quick summary for heartbeat"
        echo "  stale-check            - Detailed overdue detection"
        exit 1
        ;;
esac
