#!/bin/bash

# ========================================
# OpenClaw 一键安装脚本（Mac版）
# ========================================

set -e  # 遇到错误立即退出（但我们会捕获关键步骤的错误）

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_step() {
    echo -e "${BLUE}[进度]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[成功]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[信息]${NC} $1"
}

# 分隔线
print_separator() {
    echo "========================================"
}

# ========================================
# 步骤1：检查Node.js
# ========================================
print_separator
print_step "步骤 1/6: 检查 Node.js 环境..."

if ! command -v node &> /dev/null; then
    print_error "Node.js 未安装！"
    echo ""
    print_info "解决方案："
    echo "  1. 访问 https://nodejs.org 下载并安装 Node.js（推荐 v22.x LTS）"
    echo "  2. 或使用 Homebrew 安装："
    echo "     brew install node@22"
    echo ""
    exit 1
fi

NODE_VERSION=$(node -v | cut -d 'v' -f 2)
NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d '.' -f 1)

if [ "$NODE_MAJOR" -lt 22 ]; then
    print_error "Node.js 版本过低！当前版本: v$NODE_VERSION，需要 >= v22"
    echo ""
    print_info "解决方案："
    echo "  1. 升级 Node.js 到 v22.x LTS："
    echo "     brew upgrade node@22"
    echo "  2. 或使用 n 管理器切换版本："
    echo "     n 22"
    echo ""
    exit 1
fi

print_success "Node.js 检查通过！当前版本: v$NODE_VERSION"

# ========================================
# 步骤2：检查npm
# ========================================
print_step "步骤 2/6: 检查 npm..."

if ! command -v npm &> /dev/null; then
    print_error "npm 未找到！"
    print_info "npm 应随 Node.js 自动安装，请检查 Node.js 安装是否完整"
    exit 1
fi

NPM_VERSION=$(npm -v)
print_success "npm 检查通过！当前版本: v$NPM_VERSION"

# ========================================
# 步骤3：全局安装 OpenClaw
# ========================================
print_separator
print_step "步骤 3/6: 全局安装 OpenClaw..."

# 检查是否已安装
if command -v openclaw &> /dev/null; then
    EXISTING_VERSION=$(openclaw --version 2>/dev/null || echo "未知版本")
    print_warning "OpenClaw 已安装（版本: $EXISTING_VERSION），将升级到最新版本..."
fi

print_info "正在安装 OpenClaw（可能需要几分钟）..."

if npm install -g openclaw 2>&1; then
    print_success "OpenClaw 安装完成！"
    OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "未知版本")
    print_info "安装版本: $OPENCLAW_VERSION"
else
    print_error "OpenClaw 安装失败！"
    echo ""
    print_info "解决方案："
    echo "  1. 检查网络连接是否正常"
    echo "  2. 尝试使用 sudo："
    echo "     sudo npm install -g openclaw"
    echo "  3. 清除 npm 缓存重试："
    echo "     npm cache clean --force"
    echo "     npm install -g openclaw"
    echo ""
    exit 1
fi

# ========================================
# 步骤4：初始化配置
# ========================================
print_separator
print_step "步骤 4/6: 运行 openclaw setup 初始化配置..."

print_info "正在初始化配置（会打开浏览器进行授权）..."

if openclaw setup 2>&1; then
    print_success "配置初始化完成！"
else
    print_error "配置初始化失败！"
    echo ""
    print_info "解决方案："
    echo "  1. 确保浏览器已打开并完成授权流程"
    echo "  2. 手动运行："
    echo "     openclaw setup"
    echo "  3. 检查是否有防火墙阻止浏览器打开"
    echo ""
    print_warning "配置初始化失败，但脚本将继续执行后续步骤..."
    # 不退出，继续执行
fi

# ========================================
# 步骤5：安装 Gateway 后台服务
# ========================================
print_separator
print_step "步骤 5/6: 安装 Gateway 后台服务..."

print_info "正在安装 Gateway（后台守护进程）..."

if openclaw gateway install 2>&1; then
    print_success "Gateway 服务安装完成！"
else
    print_error "Gateway 安装失败！"
    echo ""
    print_info "解决方案："
    echo "  1. 检查是否有权限问题："
    echo "     sudo openclaw gateway install"
    echo "  2. 查看详细错误日志："
    echo "     openclaw gateway status"
    echo ""
    exit 1
fi

# ========================================
# 步骤6：启动 Gateway
# ========================================
print_separator
print_step "步骤 6/6: 启动 Gateway 服务..."

print_info "正在启动 Gateway..."

if openclaw gateway start 2>&1; then
    print_success "Gateway 已启动！"
else
    print_error "Gateway 启动失败！"
    echo ""
    print_info "解决方案："
    echo "  1. 检查服务状态："
    echo "     openclaw gateway status"
    echo "  2. 查看日志："
    echo "     openclaw gateway logs"
    echo "  3. 尝试重启："
    echo "     openclaw gateway restart"
    echo ""
    print_warning "Gateway 启动失败，请手动检查"
    # 不退出，继续输出状态检查
fi

# ========================================
# 安装完成 - 状态检查
# ========================================
print_separator
echo ""
print_step "正在检查安装状态..."
echo ""

# 检查 openclaw 命令
if command -v openclaw &> /dev/null; then
    print_success "✓ OpenClaw 命令可用"
    print_info "  版本: $(openclaw --version 2>/dev/null || echo '未知')"
else
    print_error "✗ OpenClaw 命令不可用"
fi

# 检查 Gateway 状态
echo ""
print_info "Gateway 服务状态："
openclaw gateway status 2>&1 || print_warning "无法获取 Gateway 状态"

# ========================================
# 最终成功信息
# ========================================
print_separator
echo ""
print_success "🎉 OpenClaw 安装完成！"
echo ""
print_info "下一步操作："
echo "  1. 运行 openclaw help 查看所有命令"
echo "  2. 运行 openclaw status 查看系统状态"
echo "  3. 开始使用 OpenClaw："
echo "     openclaw chat          # 启动聊天"
echo "     openclaw plugins list  # 查看插件"
echo "     openclaw skills check  # 检查技能"
echo ""
print_info "常用 Gateway 命令："
echo "  openclaw gateway status   # 查看状态"
echo "  openclaw gateway stop     # 停止服务"
echo "  openclaw gateway restart  # 重启服务"
echo "  openclaw gateway logs     # 查看日志"
echo ""
print_separator
print_success "✅ 一键安装流程完成！"
print_separator