# managed agents

managed agents 是百炼平台提供的托管式智能体运行时服务，允许开发者无需自行部署和运维 Agent 服务，即可通过 API 或 CLI 快速创建、配置并调用具备多步推理与工具调用能力的智能体。其核心设计目标是降低 Agent 工程复杂度，统一生命周期管理与上下文隔离。所有 Agent 实例均在平台受控环境中执行，支持自动扩缩容与资源隔离。

## 支持的模型与功能

- **模型支持**：当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款通义千问系列模型（详见 [Managed Agents](../../raw/application-user-guide/managed-agents.md)）；其他模型（如 `qwen2.5-*` 系列）暂未开放接入，尝试传入将返回 `400 Bad Request`。
- **核心功能**：
  - 多轮对话状态自动维护（基于 session ID）
  - 内置工具调用（HTTP、数据库、知识库检索等）与自定义工具注册
  - 上下文窗口自动截断与[长期记忆](../concepts/memory.md)（通过 `context_id` 关联外部向量库）
  - 异步任务委派与结果回调（需显式启用 `enable_async`）

> **注意**：[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md) 中提及“支持任意百炼已上线模型”，该描述已过时；实际可用模型以 [Managed Agents](../../raw/application-user-guide/managed-agents.md) 主文档列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 仅限 `qwen-max` / `qwen-plus` / `qwen-turbo`，不区分大小写 |
| `tools` | array | 否 | 工具定义数组，每个元素含 `name`、`description`、`parameters`（JSON Schema 格式）；空数组表示禁用工具调用 |
| `session_id` | string | 否 | 用于关联多轮对话；若未提供，平台自动生成唯一 ID |
| `context_id` | string | 否 | 指向预存的上下文快照 ID（需提前通过 `/v1/contexts` 创建）；与 `session_id` 独立生效 |
| `timeout` | integer | 否 | 单次请求超时（秒），范围 10–300，默认 60 |

## 使用方式

1. **API 调用**（推荐）：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/agents \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-plus",
           "input": {"query": "查一下北京今天天气"},
           "tools": [{"name": "weather_api", "description": "..."}]
         }'
   ```
   完整请求结构与响应格式见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。

2. **CLI 快速验证**：  
   ```bash
   baiLian agent run --model qwen-turbo --query "总结这篇文档" --file doc.pdf
   ```
   CLI 支持文件上传、会话复用及环境变量注入，详细选项参见 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **并发与配额**：免费版默认最大并发数为 2；企业版按 license 授权，上限 50；超出将触发 `429 Too Many Requests`。
- **上下文长度**：单次请求输入 + 工具返回内容总 token 不得超过模型原生上下文的 80%（例如 `qwen-plus` 为 8192 × 0.8 ≈ 6553 tokens）。
- **工具安全性**：所有 HTTP 工具默认仅允许访问白名单域名（`*.aliyuncs.com`, `*.alibabacloud.com`, `*.baidu.com`），自定义域名需提交工单申请；该策略在 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) 中明确说明。
- **计费粒度**：按实际消耗 token 计费（含 [prompt](prompt.md) + completion + 工具调用输入/输出），非按请求次数；详情见 [计费](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [Managed Agents](../../raw/application-user-guide/managed-agents.md)


