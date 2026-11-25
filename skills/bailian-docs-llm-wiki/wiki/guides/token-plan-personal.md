# token plan personal

[Token](../concepts/token.md) Plan 个人版是面向独立开发者的按月订阅服务，提供模型调用 Credits 额度、内置工具权益及 Harness 专属工具额度。所有套餐均限定在华北2（北京）地域使用，API 调用需通过 `sk-sp-xxx` 格式的 [Token](../concepts/token.md) Plan 专属 API Key 进行鉴权。该计划不支持退订，降配需等待当前订阅到期后重新购买。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 个人版支持调用千问（Qwen）、万相（WanXiang）、DeepSeek、智谱 AI（GLM）、HappyHorse 及决策模型等多系列模型，覆盖文本生成、视觉理解、图片/视频生成、语音合成与识别等能力。其中 `auto` 模型支持自动选型，但**不支持** `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。

模型内置工具（如 `web_search`、`image_search`、`code_interpreter` 等）通过 Responses API 自动触发，按 Credits 抵扣，无需单独接入 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。此外，Standard 与 Pro 套餐额外附赠 Harness 权益，覆盖联网搜索增强版、垂类搜索、网页解析、图像生成、语音合成、语音识别、代码解释器等工具，其调用**不消耗任何 Credits**，且享有每月免费额度 + 超额部分 88 折后付费 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。

> **注意**：文档 1 中“领域模型”表格列出 `decision-model-preview` 为限时免费，但未说明其是否计入 Harness 权益；而文档 2 明确 Harness 权益仅限 Standard/Pro 套餐且不含决策模型。实际调用时，`decision-model-preview` 属于模型层调用（使用 `sk-sp-xxx` Key），免费策略以 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md) 中的限时说明为准，与 Harness 权益无关。

## 关键参数

- **API Key 类型**：必须使用 `sk-sp-xxx` 格式的 Token Plan 专属 Key 调用模型（如 `/v1/chat/completions`）；Harness 工具（如 MCP 服务）则必须使用 `sk-xxx` 格式的百炼通用 API Key [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。
- **模型路由**：`qwen4-max-preview` 已下线，请求自动路由至 `qwen4-max`，计费与用量统计均按后者执行，预览期折扣失效 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。
- **夜间折扣**：`qwen3.8-max`/`qwen3.8-flash` 每晚 22:00–次日 08:00 享 4 折；指定 DeepSeek 模型（如 `deepseek-v4-pro-0813`）同期享 5 折。
- **Harness 配置关键字段**：MCP 接入需设置 `Authorization: Bearer ${DASHSCOPE_API_KEY}`，且 URL 因工具而异（如联网搜索增强版为 `https://dashscope.aliyuncs.com/api/v1/mcps/EnhancedSearch/mcp`）。

## 使用方式

1. **模型调用**：使用 `sk-sp-xxx` Key，按标准 OpenAI/Anthropic 兼容接口发起请求（如 `POST /v1/chat/completions`），模型 ID 从[支持的模型](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md#tppo-h-models) 表格中选取。
2. **Harness 工具接入**：
   - 登录控制台 → **我的订阅** → 切换至 **Harness 权益** 页签；
   - 选择目标工具（如“联网搜索增强版”），点击 **AI Native 接入** 获取配置指令，或复制 MCP URL 与 Key 手动注入本地 Agent 配置（如 Qwen Code 的 `settings.json`、Claude Code 的 CLI 命令等）；
   - 确保环境变量 `DASHSCOPE_API_KEY` 已正确设置（值为 `sk-xxx`）。
3. **额度管理**：剩余额度、重置时间及消耗明细统一在 [控制台我的订阅](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan) 查看。

## 限制和注意事项

- **地域限制**：Token Plan 个人版**仅支持华北2（北京）地域**，跨地域调用将失败 [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)。
- **退订与降配**：个人版不支持自助退订；不支持降配，需等待当前订阅到期后重新购买低档位套餐。
- **额度规则**：
  - 月度 Credits 额度按自然月重置，不结转；用量包有效期为 1 个月，到期未用额度自动作废；
  - Harness 免费额度按订阅周期发放，未用完不结转，升配后剩余额度按公式折算（见 [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md#tphb-h-upgrade)）。
- **Key 隔离**：`sk-sp-xxx`（模型调用/Credits 抵扣）与 `sk-xxx`（Harness 工具/MCP 调用）**不可混用**；误用会导致 401 错误或额度误抵扣。
- **工具覆盖差异**：Harness 权益中“视频生成”“知识库 RAG”“记忆库 Memory”“托管智能体”“云沙箱”等工具无免费额度（标“—”），仅享 88 折后付费；而模型层的 `wan3.0-video`、`happyhorse-1.1-t2v` 等仍可按 Credits 正常调用。

## 来源文档

- [个人版订阅与权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)
- [Harness 权益](../../raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)


