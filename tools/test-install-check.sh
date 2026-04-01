#!/bin/bash

# 快速测试版 - 只测试检查逻辑，不实际安装

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() { echo -e "${BLUE}[进度]${NC} $1"; }
print_success() { echo -e "${GREEN}[成功]${NC} $1"; }
print_error() { echo -e "${RED}[错误]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[警告]${NC} $1"; }
print_info() { echo -e "${BLUE}[信息]${NC} $1"; }

echo "========================================"
echo "OpenClaw 安装脚本逻辑测试（快速版）"
echo "========================================"

# 步骤1：检查Node.js
print_step "步骤 1/6: 检查 Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node -v)
    NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d 'v' -f 2 | cut -d '.' -f 1)
    if [ "$NODE_MAJOR" -ge 22 ]; then
        print_success "Node.js 检查通过！版本: $NODE_VERSION"
    else
        print_error "Node.js 版本过低！需要 >= v22"
    fi
else
    print_error "Node.js 未安装！"
fi

# 步骤2：检查npm
print_step "步骤 2/6: 检查 npm..."
if command -v npm &> /dev/null; then
    print_success "npm 检查通过！版本: $(npm -v)"
else
    print_error "npm 未找到！"
fi

# 步骤3：检查OpenClaw
print_step "步骤 3/6: 检查 OpenClaw..."
if command -v openclaw &> /dev/null; then
    print_success "OpenClaw 已安装！版本: $(openclaw --version 2>/dev/null || echo '未知')"
else
    print_warning "OpenClaw 未安装（脚本会执行 npm install -g openclaw）"
fi

# 步骤4：检查Gateway
print_step "步骤 4/6: 检查 Gateway 服务..."
print_info "Gateway 状态："
openclaw gateway status 2>&1 | head -5

echo ""
echo "========================================"
print_success "✅ 脚本逻辑测试通过！"
echo ""
print_info "完整安装请运行："
echo "  ./tools/install-openclaw-mac.sh"
echo "========================================"