# toolkits and [frameworks](frameworks.md)

阿里云百炼提供 OpenAI 和 Anthropic 兼容的 API 接口，开发者可以通过多种主流 AI 编程工具、客户端和框架接入百炼模型服务。百炼支持三种计费方案：Token Plan 团队版（按坐席订阅）、Coding Plan（固定月费订阅）和按量计费，各方案的 API Key、Base URL 和支持的模型均不相同，配置时需注意区分。

## 接入协议与 Base URL

百炼同时支持 OpenAI 兼容协议和 Anthropic 兼容协议，不同计费方案对应不同的 Base URL：

**Token Plan 团队版**：

| 协议 | Base URL |
|------|----------|
| OpenAI | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` |

**Coding Plan**：

| 协议 | Base URL |
|------|----------|
| OpenAI | `https://coding.dashscope.aliyuncs.com/v1` |
| Anthropic | `https://coding.dashscope.aliyuncs.com/apps/anthropic` |

**按量计费**（按地域区分）：

| 协议 | 华北2（北京） | 新加坡 | 弗吉尼亚 |
|------|------------|--------|---------|
| OpenAI | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| Anthropic | `https://dashscope.aliyuncs.com/apps/anthropic` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/apps/anthropic` | — |

> **注意**：三种计费方案的 API Key 互不通用，配置时必须确保 API Key 与 Base URL 来自同一方案。按量计费的 API Key 还需与所选地域对应。详见[更多工具](../../raw/model-user-guide/use-chat-client-or-development-tool/more-tools.md)。

## 支持的开发工具

### AI 编程助手（终端/CLI）

| 工具 | 接入协议 | 计费方案 | 配置方式 |
|------|---------|---------|---------|
| [Claude Code](../../raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md) | Anthropic | 按量/Coding Plan/Token Plan | `~/.claude/settings.json` 配置环境变量 |
| [Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) | OpenAI | 按量/Coding Plan/Token Plan | `~/.codex/config.toml` + 环境变量 |
| [Qwen Code](../../raw/model-user-guide/use-chat-client-or-development-tool/qwen-code.md) | OpenAI | 按量/Coding Plan/Token Plan | `/auth` 命令或 `settings.json` |
| [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) | Anthropic | 按量/Coding Plan/Token Plan | `hermes config set` 命令 |
| [Kilo CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/kilo-cli.md) | OpenAI | 按量/Coding Plan/Token Plan | `~/.config/kilo/config.json` |
| [Qoder CLI](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) | OpenAI | 按量/Coding Plan/Token Plan | `/model` 命令交互配置 |

### AI 编程 IDE/插件

| 工具 | 接入协议 | 支持 IDE | 配置方式 |
|------|---------|---------|---------|
| Cursor | OpenAI | 独立 IDE | Settings > Models 填入 API Key 和 Base URL |
| Cline | OpenAI Compatible | VS Code | 选择 OpenAI Compatible Provider |
| OpenCode | OpenAI/Anthropic | 独立 CLI IDE | `opencode.json` 配置文件 |
| Qoder CN（原 Lingma） | OpenAI | 独立 IDE | 设置 > 模型 > 添加 |
| Qoder IDE | OpenAI | 独立 IDE | 设置 > 模型 > 添加 |
| Qoder JetBrains 插件 | OpenAI | JetBrains 系列 | 插件设置 > 添加模型 |

> **注意**：Cursor 免费版仅支持 Auto 模式，需升级至 Pro 及以上套餐才能调用自定义模型。部分模型在 Cursor 中需使用别名（如 `kimi-k2.6` 写为 `kimi-k2-6`）。详见 [Cursor](../../raw/model-user-guide/use-chat-client-or-development-tool/cursor.md) 文档。

### 通用 AI 客户端

| 工具 | 类型 | 接入协议 |
|------|------|---------|
| Cherry Studio | 桌面客户端 | OpenAI |
| Chatbox | 跨平台客户端 | OpenAI API 兼容 |
| QwenPaw | Web 客户端 | OpenAI |
| OpenClaw | Web/桌面客户端 | OpenAI |
| Dify | 开源应用开发平台 | 通义千问插件 / OpenAI 兼容 |

### 开发框架

| 框架 | 协议 | 说明 |
|------|------|------|
| OpenAI SDK | OpenAI Chat | 调整 `api_key`、`base_url` 和模型名称即可迁移 |
| Postman / cURL | HTTP | 适用于图像/视频生成等异步 API 的快速测试 |

## 典型接入方式

### 通过 OpenAI SDK 调用

只需将 `api_key` 替换为百炼 API Key，`base_url` 指向百炼端点，即可复用已有 OpenAI 代码：

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",  # 百炼 API Key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
)
```

支持非流式、流式和 function call 调用。支持的模型包括 Qwen 系列（商业版、开源版）、DeepSeek、Kimi、GLM、MiniMax 等。详见 [OpenAI Chat接口兼容](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 文档中的模型列表。

> **注意**：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。三方直供模型（SiliconFlow DeepSeek 等）仅在中国站的中国内地地域可用，需先在百炼控制台开通。

### 通过 Anthropic 兼容协议调用

Claude Code、Hermes Agent 等工具通过 Anthropic Messages API 协议接入。以 Claude Code 为例，在 `~/.claude/settings.json` 中配置：

```json
{
    "env": {
        "ANTHROPIC_AUTH_TOKEN": "YOUR_API_KEY",
        "ANTHROPIC_BASE_URL": "https://dashscope.aliyuncs.com/apps/anthropic",
        "ANTHROPIC_MODEL": "qwen3.7-max"
    }
}
```

### Completions 接口（代码补全）

百炼提供 Completions 接口，专为文本补全场景设计，支持前缀补全和前后缀中间填充（Fill-in-the-Middle）。当前仅支持 qwen-coder-turbo 模型，且仅限北京地域。

```python
completion = client.completions.create(
    model="qwen-coder-turbo",
    prompt="<|fim_prefix|>def quick_sort(arr):<|fim_suffix|>",
)
```

### Responses API

部分模型（qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash）支持 OpenAI Responses API，可在 Codex 等工具中以 `wire_api = "responses"` 方式接入。其他模型需通过 Chat/Completions API（`wire_api = "chat"`）接入，部分工具（如 Codex）需安装旧版本。

## 百炼 CLI 集成

多款编程工具（Cursor、Cline、Qoder）支持通过百炼 CLI 扩展能力。安装百炼 CLI 后，工具会自动注册 Skill，可通过自然语言调用百炼的图像生成、视频生成等能力。前置要求 Node.js 18+。

```
npm install -g bailian-cli
```

## 使用限制

- Token Plan 团队版和 Coding Plan 仅限在 AI 编程工具和 OpenClaw 类型 Agent 中使用，不支持工作流/自动化平台（Dify、n8n、Coze 等）、API 测试工具（Postman、Insomnia 等）及自定义应用程序。违规使用可能导致订阅暂停或 API Key 封禁。
- Dify 中使用百炼需安装通义千问插件，使用 DeepSeek 模型也需通过该插件接入。
- 图像/视频生成 API 采用异步调用机制，需先创建任务获取 `task_id`，再轮询查询结果。

## 常见问题排查

- **401 Incorrect API key provided**：确认 API Key 与 Base URL 来自同一计费方案，且按量计费的 API Key 与 Base URL 地域一致。
- **400 InternalError.Algo.InvalidParameter**：使用 Qwen3（思考模式）或 QwQ 模型时需开启 R1 messages format 或思考模式。
- **The value of the enable_thinking parameter is restricted to True**：该模型仅支持思考模式，请在客户端中开启。
- **上下文超限**：在工具设置中调整 `max_tokens` 等生成参数。
- 各计费方案错误码排查：按量计费参见错误码文档，Coding Plan 和 Token Plan 团队版参见各自的常见问题文档。

## 来源文档

- [OpenAI Chat接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)
- [completions 接口](../../raw/model-api-reference/toolkits-and-frameworks/completions.md)
- [OpenAI Responses接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)
- [OpenAI Vision接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/qwen-vl-compatible-with-openai.md)
- [OpenAI文件接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)
- [OpenAI兼容-Batch（文件输入）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)
- [OpenAI兼容-Batch Chat](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-batch-chat.md)
- [OpenAI Embedding接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/embedding-interfaces-compatible-with-openai.md)
- [OpenAI Conversations接口兼容](../../raw/model-api-reference/toolkits-and-frameworks/openai-compatible-conversations.md)
- [在LangChain中使用阿里云百炼](../../raw/model-api-reference/toolkits-and-frameworks/use-bailian-in-langchain.md)



