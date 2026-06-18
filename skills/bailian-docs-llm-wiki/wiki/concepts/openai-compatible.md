# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套与 OpenAI API 协议对齐的调用方式，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数，即可将基于 OpenAI SDK 的现有应用无缝迁移至百炼平台。

## 核心价值

百炼的 OpenAI 兼容接口大幅降低了迁移成本。已使用 OpenAI Python/Node.js SDK 的开发者无需更换 SDK 或重构代码逻辑，仅需调整服务端点和认证信息即可接入百炼的千问（Qwen）系列及 DeepSeek、Kimi、GLM 等第三方模型。

## 支持的接口类型

百炼提供的 OpenAI 兼容接口覆盖完整的模型调用链路：

| 接口 | 用途 | 典型场景 |
|------|------|----------|
| Chat Completions | 对话式文本生成 | 聊天、问答、Function Call |
| Responses | Chat Completions 的演进版本 | 内置工具调用（联网搜索、代码解释器等）、自动上下文管理 |
| Completions | 文本/代码补全 | 代码补全（FIM）、内容续写 |
| Vision | 视觉理解 | 图像描述、视频分析、OCR |
| Embedding | 文本向量化 | RAG、语义检索、文本分类 |
| Files | 文件管理 | 文档问答、Batch 输入、模型调优数据集 |
| Batch | 异步批量推理 | 数据标注、模型评测（费用为实时调用的 50%） |
| Batch Chat | 同步批量推理 | 保持同步调用方式的批量任务 |
| Conversations | 会话管理 | 跨设备/跨场景对话延续 |

其中 Chat Completions 和 Responses 是最常用的两个接口。Chat Completions 适合标准对话场景和从 OpenAI 迁移；Responses 在此基础上内置了联网搜索、代码解释器、网页内容提取等工具能力，适合需要工具调用的复杂场景。

## 服务地址配置

各地域的 `base_url` 如下：

| 地域 | base_url |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` 或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（推荐） |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为[业务空间](workspace.md) ID，可在百炼控制台查看。北京和新加坡地域推荐使用含 WorkspaceId 的新版专属域名，性能和稳定性更优。

不同计费方案使用不同的 Base URL：

| 计费方案 | Base URL |
|---------|----------|
| 按量计费 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |

> 各地域和计费方案的 API Key 不同，不可混用。

## 关键参数

使用 OpenAI SDK 接入百炼时，需要设置以下参数：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-dashscope-api-key>",       # 百炼 API Key（建议配置到环境变量 DASHSCOPE_API_KEY）
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",                     # 百炼模型 ID
    messages=[{"role": "user", "content": "你好"}]
)
```

常用模型参数：

| 参数 | 说明 |
|------|------|
| `model` | 模型 ID，如 `qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-flash` 等 |
| `messages` | 对话消息列表，格式与 OpenAI 一致 |
| `stream` | 是否[流式输出](streaming.md) |
| `temperature` | 生成随机性控制 |
| `tools` | Function Calling 工具定义 |
| `enable_thinking` | 启用思考模式（Qwen3 及以上模型支持） |

## 支持的模型

通过 OpenAI 兼容接口可调用的模型包括：

- **千问系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash、Qwen-VL 系列、Qwen-Coder 系列等
- **第三方模型**：deepseek-v4-pro、deepseek-v4-flash、kimi-k2.7-code、glm-5.2、MiniMax-M2.7 等
- **向量模型**：text-embedding-v4 等

> 注意：Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。三方直供模型仅在中国站的中国内地地域可用。

## 第三方工具接入

百炼的 OpenAI 兼容接口支持多种第三方开发工具直接接入，包括：

- **终端编程工具**：Claude Code、Codex、Qwen Code、OpenCode 等
- **IDE 插件**：Cursor、Cline 等
- **桌面客户端**：Cherry Studio、Chatbox 等
- **开发框架**：LlamaIndex（Python）、Spring AI Alibaba（Java）等

任何兼容 OpenAI API 协议且支持自定义服务端点的工具均可接入百炼。

## 与 DashScope 原生接口的对比

| 维度 | OpenAI 兼容接口 | DashScope 原生接口 |
|------|----------------|-------------------|
| 迁移成本 | 极低，复用现有 OpenAI SDK 代码 | 需使用 [DashScope SDK](dashscope-sdk.md) 或接口规范 |
| 功能覆盖 | 覆盖主流场景 | 最完整，包含平台特有的高级参数 |
| 生态兼容 | 与 OpenAI 工具链和框架无缝配合 | 百炼专属 |
| 适用场景 | 从 OpenAI 迁移、使用第三方工具 | 需要平台全部能力和最大灵活性 |

如需使用百炼平台的全部能力（包括平台特有的高级参数和功能），推荐使用 DashScope 原生接口。

## 来源文档

- 文本生成模型API参考
- OpenAI接口兼容
- 首次调用千问API
- 通过第三方工具使用百炼
- 模型推理概览
- 第三方开发框架集成

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model inference](../guides/model-inference.md)
- [frameworks](../api/frameworks.md)


