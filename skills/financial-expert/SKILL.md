---
name: financial-expert
description: >-
  Use when users need China or Hong Kong securities, funds, fund managers, company financials,
  valuation, global macro or industry time series, broker research, announcements, financial news,
  or enterprise-risk data. Triggers include 选股、基金筛选、基金经理、净利润、营收、ROE、估值、
  GDP、CPI、核心 PCE、行业产销价、研报、公告、财经新闻、工商与司法风险。
---

# 金融数据分析

通过百炼 CLI `bl mcp` 调用金融 MCP `market-cmapi00073529`。只返回数据与中立分析，不下单、不荐股、不预测涨跌。

## 能力边界

- 适用：A 股筛选；A 股、港股、基金、债券、指数等结构化查询；基金和基金经理筛选；中国及全球主要经济体宏观/行业时序；券商研报；A 股、港股公司及公募基金公告；财经新闻；企业工商、合规与司法风险。
- 不适用：美股个股、加密货币等未被实时 schema 证实的证券或资产；交易下单；无数据依据的投资结论。全球宏观指标不受此限制。
- 工具能力可能更新。执行前以 `bl mcp tools --server market-cmapi00073529 --output json` 返回的实时 schema 为准。

## 前置检查与鉴权

```bash
bl --version
bl auth status --output json
```

未安装时按 [百炼 CLI 安装文档](https://bailian.aliyun.com/cli/install.md) 安装。API Key 可通过环境变量或 CLI 配置：

```bash
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
# 或
bl auth login --api-key "YOUR_DASHSCOPE_API_KEY"
```

鉴权边界：

- `bl mcp list` 查询账号控制面，使用 Console 登录态。只有需要发现 Server Code 时才调用；国内站登录使用 `bl auth login --console --console-site domestic`。
- `bl mcp tools` 与 `bl mcp call` 使用 API Key。已知 Server Code 时，即使 Console 会话过期，也应直接查询 tools 或调用工具。

```bash
# 可选：发现已激活的金融 MCP（Console）
bl mcp list --name 金融 --output json

# 权威：查看实时工具与入参 schema（API Key）
bl mcp tools --server market-cmapi00073529 --output json
```

## 工具路由

| 用户意图 | MCP 工具 | 说明 |
|---|---|---|
| 筛选股票 | `SmartStockSelection` | A 股候选清单 |
| 筛选基金 | `SmartFundSelection` | 基金业绩、风险、持仓、类型 |
| 筛选基金经理 | `SmartFundManagerSelection` | 规模、业绩、风格、风险控制 |
| 财务、行情、估值、证券资料 | `FinQuery` | A 股、港股、基金、债券、指数等结构化数据 |
| 全球 GDP、CPI、核心 PCE、行业产销价 | `MacroIndustryData` | 中国及全球主要经济体宏观和行业时序数据 |
| 公司或行业券商研报 | `FinancialResearchReport` | 研报原文与机构观点 |
| 公司或基金公告 | `AnnouncementData` | A 股、港股公司及公募基金公告 |
| 财经新闻与公开动态 | `NewsDataQuery` | 新闻、事件与舆情素材 |
| 企业深度信息 | `IcEnterpriseDataQuery` | 工商、经营、合规与司法风险 |

复杂问题应分别调用相关工具，再对齐实体、日期、单位和口径；不要让一个宽泛 query 替代多工具核验。涉及“前 N / Top N”时必须先确定排序指标；排序指标不明确时先追问，再通过 query 和 `topk` 固化口径。

## 调用格式

所有工具使用 `--target <server.tool>`：

```bash
bl mcp call \
  --target market-cmapi00073529.FinQuery \
  --query "查询贵州茅台（600519.SH）最近一个完整财年的营业收入、归母净利润和 ROE" \
  --output json
```

结构化参数必须先查看实时 schema：

```bash
bl mcp call \
  --target market-cmapi00073529.SmartStockSelection \
  --json '{"query":"筛选 ROE 大于 15% 且净利润增速超过 20% 的消费股"}' \
  --output json
```

## 时间与数据口径

- 用户说“最新”“最近一个完整财年”时，先运行 `TZ=Asia/Shanghai date '+%F %T %Z'` 获取实际查询时间；不要自行写死年份。
- 让工具按相对时间查询，并检查返回的报告期是否真是最新已披露期间。若只返回更早期间，明确说明，不得静默替代。
- 区分实际查询时间、行情交易时间、财报报告期和研报/公告发布时间。

## 输出规范

- 筛选与结构化数据：Markdown 表格，包含名称、代码、期间、数值、单位和来源。
- 宏观/行业时序：时序表格 + 一句话趋势，区分同比和环比。
- 研报：标题、日期、机构，每篇最多 3 条观点；机构评级只能作为来源事实转述。
- 公告：标题、日期、主体、披露事项；新闻和企业信息注明对应工具。
- 结尾注明：实际查询时间、调用的工具、`market-cmapi00073529`，以及“仅供数据参考，不构成投资建议”。
- 空结果、冲突数据或缺失指标必须如实说明；保留工具返回的单位和有效精度，不编造、不擅自换口径。

## 常见错误

| 现象 | 处理 |
|---|---|
| `Unexpected argument: market-...` | 使用 `tools --server` 或 `call --target`，不要再传位置参数 |
| `mcp list` 提示 Console token/session 缺失 | 如确需发现服务，按站点登录 Console；已知 Server Code 则跳过 list |
| `mcp tools` / `mcp call` 返回 401 或 API Key 缺失 | 检查 `DASHSCOPE_API_KEY` 或运行 `bl auth login --api-key ...` |
| 提示 MCP 未开通或不存在 | 打开错误中的市场链接，在当前账号/Workspace 激活服务后重试 |
| `isError: true` | 原样读取 `result.content[].text`，补全实体、代码、指标或时间范围后重试 |
| 无结果 | 核对全称、简称、证券代码和日期；征得用户同意后再放宽条件 |

## 端到端示例

用户问：“筛选 ROE > 15% 且近三年净利润复合增速 > 20% 的消费股，按 ROE 从高到低取前三家公司，再看它们近一个月研报。”

```bash
bl mcp call \
  --target market-cmapi00073529.SmartStockSelection \
  --query "ROE 大于 15%，近三年净利润复合增速大于 20% 的消费股，按 ROE 从高到低排序" \
  --arg topk=3 \
  --output json

# 从真实返回中取前三名，逐家公司调用；不要预设公司名单
bl mcp call \
  --target market-cmapi00073529.FinancialResearchReport \
  --query "<公司名称或代码>近一个月券商研报核心观点" \
  --output json
```

汇总候选指标和研报事实，注明来源与时间，不输出买卖建议。
