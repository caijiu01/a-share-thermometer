#!/bin/bash
# A股温度计 安装脚本

echo "🌡️ 安装 A股温度计..."

# 创建 rules 目录（如果不存在）
mkdir -p ~/.cursor/rules

# 复制规则文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp "$SCRIPT_DIR/RULE.md" ~/.cursor/rules/a-share-thermometer.md

echo "✅ 安装完成！"
echo ""
echo "使用方式："
echo "  /A股温度计"
echo "  /温度计"
echo "  /a股"
echo ""
echo "或直接问："
echo "  A股该买还是该卖"
echo "  现在是牛市还是熊市"
