# 金融数据分析

> [English →](README.md)

基于阿里云百炼 CLI `bl mcp` 与金融 MCP `market-cmapi00073529`，查询 A 股、港股、基金、基金经理、财务估值、全球宏观与行业数据、券商研报、公告、财经新闻和企业风险信息。仅提供数据与中立分析，不下单、不荐股、不预测涨跌。

## 支持范围

- A 股筛选，以及 A 股、港股、基金、债券、指数等结构化查询
- 基金与基金经理筛选
- 中国及全球主要经济体 GDP、CPI、核心 PCE，以及行业产量、销量和价格时序
- 券商研报
- A 股、港股公司及公募基金公告
- 财经新闻、企业工商、合规与司法风险

实际范围以实时工具 schema 为准：

```bash
bl mcp tools --server market-cmapi00073529 --output json
```

## 鉴权说明

- `bl mcp list` 使用 Console 登录态，仅用于发现 Server Code。
- `bl mcp tools` 和 `bl mcp call` 使用 API Key；已知 `market-cmapi00073529` 时不必先调用 list。

```bash
bl auth status --output json

# 只有需要 mcp list 时才登录 Console；国内站是默认值，也可显式指定
bl auth login --console --console-site domestic
```

## 可用工具

| 工具 | 用途 |
|---|---|
| `SmartStockSelection` | A 股多维筛选 |
| `SmartFundSelection` | 基金筛选 |
| `SmartFundManagerSelection` | 基金经理筛选 |
| `FinQuery` | 财务、行情、估值和证券资料 |
| `MacroIndustryData` | 中国及全球主要经济体宏观与行业时序 |
| `FinancialResearchReport` | 券商研报 |
| `AnnouncementData` | A 股、港股公司及公募基金公告 |
| `NewsDataQuery` | 财经新闻与公开动态 |
| `IcEnterpriseDataQuery` | 企业工商、合规与司法风险 |

## 快速示例

```bash
bl mcp call \
  --target market-cmapi00073529.FinQuery \
  --query "查询贵州茅台（600519.SH）最近一个完整财年的营业收入、归母净利润和 ROE" \
  --output json
```

用户说“最新”或“最近一个完整财年”时，不要自行写死年份。先获取实际查询时间，再检查工具返回的报告期：

```bash
TZ=Asia/Shanghai date '+%F %T %Z'
```

完整调用、错误处理与输出规则见 [SKILL.md](SKILL.md)。

## 前置要求

安装 [阿里云百炼 CLI](https://bailian.aliyun.com/cli/install.md)，并配置 DashScope API Key：

```bash
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
bl auth status --output json
```

## License

Apache-2.0
