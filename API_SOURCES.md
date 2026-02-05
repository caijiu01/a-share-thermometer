# A股数据API接口文档

## ✅ 已验证可用的API接口

### 1. 上证指数（实时）

**腾讯财经API**（推荐）
```
URL: http://qt.gtimg.cn/q=sh000001
格式: GBK编码文本
返回: v_sh000001="1~上证指数~000001~价格~昨收~今开~..."
```

**东方财富API**（备用）
```
URL: https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&invt=2&fields=f2,f3,f4,f12,f14&secids=1.000001
格式: JSON
返回: {"data":{"diff":[{"f2":价格,"f3":涨跌幅,"f4":涨跌额,...}]}}
```

---

### 2. 10年期国债收益率

**Trading Economics**（可用）
```
URL: https://zh.tradingeconomics.com/china/government-bond-yield
格式: HTML页面（需解析）
方法: 正则匹配 \b(1\.8[0-9])\b
注意: 响应较慢（10-15秒），需要设置超时
```

---

### 3. 两融余额（沪深合计）

**上交所页面**（需解析HTML）
```
URL: https://www.sse.com.cn/market/othersdata/margin/sum/
格式: HTML
方法: 正则匹配 [0-9]{11,} 查找大数字
注意: 需要从HTML中提取，可能包含多个数字
```

**深交所API**（有数据结构，但需指定日期）
```
URL: https://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=json&CATALOGID=1837_xxpl&txtDate=YYYY-MM-DD
格式: JSON
返回: [{"metadata":{...}, "data":[...]}]
注意: 需要指定交易日，data可能为空（当天数据未更新）
```

**东方财富两融个股数据**（可汇总）
```
URL: https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=10&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6
格式: JSON
返回: 个股两融数据列表
注意: 需要汇总所有个股才能得到总余额
```

---

## ❌ 不可用或受限的接口

1. **新浪财经两融API**: `http://vip.stock.finance.sina.com.cn/mkt/api/json.php/MoneyFlow.getRzrqYe` - File not found
2. **同花顺两融API**: 需要JavaScript渲染，无法直接获取
3. **中债数据API**: HTML页面，需要复杂解析

---

## 推荐方案

| 数据类型 | 首选API | 备用方案 |
|---------|---------|---------|
| 上证指数 | 腾讯财经 | 东方财富 |
| 国债收益率 | Trading Economics | 网络搜索 |
| 两融余额 | 上交所HTML解析 | 深交所API + 网络搜索 |

---

## 使用示例

见 `fetch_all_data.py` 脚本
