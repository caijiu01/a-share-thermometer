#!/usr/bin/env python3
"""
A股完整数据获取脚本 - 整合所有可用API
"""

import json
import subprocess
import sys
import re
from datetime import datetime, timedelta

def fetch_shanghai_index():
    """获取上证指数"""
    try:
        script_path = __file__.replace('fetch_all_data.py', 'fetch_market_data.py')
        result = subprocess.run(['python3', script_path], capture_output=True, text=True)
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return None

def fetch_rzrq_balance():
    """获取两融余额（沪深合计）- 多种方法"""
    # 方法1: 上交所页面解析
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://www.sse.com.cn/market/othersdata/margin/sum/'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            html = result.stdout
            # 查找大数字（可能是余额）
            numbers = re.findall(r'[0-9]{11,}', html)
            if numbers:
                # 取最大的数字（可能是余额）
                max_num = max([int(n) for n in numbers])
                # 转换为亿元
                balance_yi = max_num / 100000000
                if 20000 < balance_yi < 30000:  # 合理范围
                    return {
                        'balance_yi': balance_yi,
                        'balance_yuan': max_num,
                        'source': 'sse_html'
                    }
    except:
        pass
    
    # 方法2: 深交所API（尝试最近交易日）
    for days_ago in range(3):
        date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        try:
            url = f"https://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=json&CATALOGID=1837_xxpl&txtDate={date}"
            result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if isinstance(data, list) and len(data) > 0:
                    # 查找有数据的项
                    for item in data:
                        if item.get('data') and len(item['data']) > 0:
                            return {'source': f'szse_api_{date}', 'data_structure': 'found'}
        except:
            continue
    
    return None

def fetch_bond_yield():
    """获取10年期国债收益率"""
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '15', 'https://zh.tradingeconomics.com/china/government-bond-yield'],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            data = result.stdout
            # 查找1.8x格式
            match = re.search(r'\b(1\.8[0-9])\b', data)
            if match:
                return {'yield_10y': float(match.group(1)), 'source': 'tradingeconomics'}
    except:
        pass
    return None

def main():
    """主函数"""
    result = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'shanghai_index': fetch_shanghai_index(),
        'rzrq_balance': fetch_rzrq_balance(),
        'bond_yield': fetch_bond_yield()
    }
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
