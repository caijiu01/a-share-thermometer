#!/usr/bin/env python3
"""
A股市场数据获取脚本
使用腾讯财经和东方财富API获取实时数据
"""

import json
import re
import subprocess
import sys
from datetime import datetime

def fetch_tencent_data(code="sh000001"):
    """从腾讯财经API获取数据"""
    try:
        result = subprocess.run(
            ['curl', '-s', f'http://qt.gtimg.cn/q={code}'],
            capture_output=True,
            text=False
        )
        data = result.stdout.decode('gbk')
        
        match = re.search(r'v_[^=]+="([^"]+)"', data)
        if match:
            parts = match.group(1).split('~')
            return {
                'name': parts[1],
                'code': parts[2],
                'current_price': float(parts[3]),
                'prev_close': float(parts[4]),
                'open': float(parts[5]),
                'high': float(parts[33]),
                'low': float(parts[34]),
                'change': float(parts[31]),
                'change_percent': float(parts[32]),
                'volume': parts[6],
                'amount': parts[37]
            }
    except Exception as e:
        print(f"腾讯API获取失败: {e}", file=sys.stderr)
    return None

def fetch_eastmoney_data(code="1.000001"):
    """从东方财富API获取数据"""
    try:
        url = f"https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f5,f6,f12,f14&secids={code}"
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True
        )
        data = json.loads(result.stdout)
        
        if 'data' in data and 'diff' in data['data'] and len(data['data']['diff']) > 0:
            item = data['data']['diff'][0]
            return {
                'name': item.get('f14', ''),
                'code': item.get('f12', ''),
                'current_price': item.get('f2', 0),
                'change_percent': item.get('f3', 0),
                'change': item.get('f4', 0),
                'open': item.get('f5', 0),
                'high': item.get('f6', 0)
            }
    except Exception as e:
        print(f"东方财富API获取失败: {e}", file=sys.stderr)
    return None

def get_shanghai_index():
    """获取上证指数数据（优先腾讯，失败用东方财富）"""
    data = fetch_tencent_data("sh000001")
    if not data:
        data = fetch_eastmoney_data("1.000001")
    
    if data:
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'index_name': data.get('name', '上证指数'),
            'current_price': data.get('current_price', 0),
            'prev_close': data.get('prev_close', 0),
            'change': data.get('change', 0),
            'change_percent': data.get('change_percent', 0),
            'high': data.get('high', 0),
            'low': data.get('low', 0),
            'open': data.get('open', 0)
        }
    return None

if __name__ == "__main__":
    data = get_shanghai_index()
    if data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "无法获取数据"}, ensure_ascii=False))
        sys.exit(1)
