# Financial Data Analysis

> [中文说明 →](README.zh.md)

This skill uses Aliyun Model Studio CLI `bl mcp` and the financial MCP server `market-cmapi00073529` to query China and Hong Kong securities, funds, fund managers, company financials and valuation, global macro and industry data, broker research, disclosures, financial news, and enterprise risk data. It provides sourced facts and neutral analysis only; it does not trade, recommend securities, or predict prices.

## Coverage

- A-share screening, plus structured data for supported A-share, Hong Kong, fund, bond, and index instruments
- Fund and fund-manager screening
- GDP, CPI, core PCE, and industry production, sales, and price series across China and other major economies
- Broker research reports
- A-share, Hong Kong company, and public-fund announcements
- Financial news and enterprise registration, compliance, and judicial-risk data

Treat the live tool schema as authoritative:

```bash
bl mcp tools --server market-cmapi00073529 --output json
```

## Authentication

- `bl mcp list` uses a Console session and is only needed to discover a Server Code.
- `bl mcp tools` and `bl mcp call` use a DashScope API Key. When `market-cmapi00073529` is already known, skip `mcp list`.

```bash
bl auth status --output json

# Only for mcp list; domestic is the default and may be selected explicitly
bl auth login --console --console-site domestic
```

## Tools

| Tool | Purpose |
|---|---|
| `SmartStockSelection` | Multi-factor A-share screening |
| `SmartFundSelection` | Fund screening |
| `SmartFundManagerSelection` | Fund-manager screening |
| `FinQuery` | Financials, market data, valuation, and instrument facts |
| `MacroIndustryData` | Macro and industry time series across major economies |
| `FinancialResearchReport` | Broker research |
| `AnnouncementData` | A-share, Hong Kong company, and public-fund announcements |
| `NewsDataQuery` | Financial news and public updates |
| `IcEnterpriseDataQuery` | Enterprise registration, compliance, and judicial risk |

## Quick example

```bash
bl mcp call \
  --target market-cmapi00073529.FinQuery \
  --query "Query Kweichow Moutai (600519.SH) revenue, parent net profit, and ROE for its latest complete fiscal year" \
  --output json
```

For “latest” or “latest complete fiscal year,” do not hard-code a year. Capture the actual query time and verify the reporting period returned by the tool:

```bash
TZ=Asia/Shanghai date '+%F %T %Z'
```

See [SKILL.md](SKILL.md) for routing, error handling, and output requirements.

## Prerequisites

Install [Aliyun Model Studio CLI](https://bailian.aliyun.com/cli/install.md) and configure a DashScope API Key:

```bash
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
bl auth status --output json
```

## License

Apache-2.0
