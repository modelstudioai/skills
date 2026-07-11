# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼提供的一套遵循 OpenAI API 协议规范的调用方式，让开发者只需替换 `base_url`、`api_key` 和 `model` 三个参数，即可将现有 OpenAI 应用无缝迁移到百炼平台，复用原有的 SDK 与示例代码。它是百炼上迁移成本最低、生态兼容性最好的接入路径。

## 在百炼平台的使用场景

OpenAI 兼容接口贯穿百炼的模型调用、应用调用、工具接入等多个场景：

- **模型直接调用**：通过 OpenAI 官方 SDK 调用 Qwen 系列（`qwen-max`/`qwen-plus`/`qwen-flash` 等）以及 DeepSeek、Kimi、GLM、MiniMax 等第三方直供模型，API 格式与千问一致。
- **专用模型调用**：`tongyi-intent-detect-v3`（意图理解）、`qwen-mt-plus`（翻译）、`qwen3.5-ocr`（OCR）、`gui-plus`（界面交互）等专用模型多数支持 OpenAI 兼容协议；但 `qwen-deep-research`、Qwen-Audio、[多模态](multimodal.md) Embedding 模型仅支持 DashScope 协议。
- **应用调用**：智能体和工作流应用可通过 OpenAI 兼容的 Responses API 调用，支持同步/异步、多轮对话、[流式输出](streaming.md)。
- **第三方工具接入**：Cursor、Cline、Cherry Studio、Chatbox、Qwen Code、OpenCode 等工具选择 "OpenAI Compatible" 提供商，填入 Base URL、API Key 和 Model ID 即可接入。
- **订阅套餐**：Token Plan 团队版与 Coding Plan 均提供 OpenAI 兼容端点，供 AI 编程工具交互式使用。

## 接口类型

百炼在 OpenAI 兼容协议下提供多套接口，覆盖从对话到文件管理的完整场景：

| 接口类型 | 说明 | 典型用途 |
| --- | --- | --- |
| Chat Completions | 标准对话接口，支持流式/非流式、function call | 通用对话、工具调用 |
| Responses | Chat Completions 的演进版，内置联网搜索、代码解释器、网页内容提取，自动管理对话历史 | 智能体、简化上下文管理 |
| Completions | 文本补全接口，支持 FIM（fill-in-middle） | 代码补全、内容续写 |
| Embedding | 文本向量化接口 | 文本检索、语义相似度 |
| Files | 文件上传/查询/删除 | 文档问答、Batch 输入、模型调优 |
| Conversations | 会话管理，配合 Responses API 使用 | 跨设备对话延续 |
| Batch（文件输入）/ Batch Chat | 异步或同步批量处理，费用为实时调用的 50% | 数据标注、模型评测、批量对话 |

## 关键参数与配置

- **`model`（必选）**：指定具体模型名，按精确字符串匹配，版本号差异视为不同模型。
- **`messages`（必选）**：对话消息列表，含 `role`（user/assistant/system）和 `content`；Responses 接口改用 `input`，且由平台自动维护历史。
- **`stream`（可选）**：是否[流式输出](streaming.md)，默认 `false`。
- **`api_key`**：推荐写入环境变量 `DASHSCOPE_API_KEY`，避免硬编码。Base URL 必须与同计费方案的 API Key 配套，否则报 401/403。

### Base URL

OpenAI 兼容接口的路径统一为 `/compatible-mode/v1`（部分套餐为 `/v1`），各地域与计费方案的域名不同、不可混用：

| 计费方案 / 地域 | OpenAI 兼容 Base URL（示例） |
| --- | --- |
| 业务空间专属域名（北京，推荐） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 按量计费（存量域名） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

其中 `{WorkspaceId}` 为业务空间 ID，可在控制台业务空间详情页查看。北京、新加坡、东京、法兰克福地域调用时 Base URL 必须包含 WorkspaceId。

### 最简调用示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

## 限制与注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；需要最全采样参数、插件或业务字段时，建议改用 DashScope 原生接口。
- **工具能力差异**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，Chat Completions 不内置，需自行实现或按工具调用协议接入。
- **对话历史管理**：仅 Responses 接口自动维护历史，其他接口需调用方自行管理上下文，避免超出模型上下文窗口。
- **协议不支持的模型**：Qwen-Audio、[多模态](multimodal.md) Embedding（如 qwen3-vl-embedding）、`qwen-deep-research` 等仅支持 DashScope 协议，无法用 OpenAI 兼容接口调用。
- **凭证与域名隔离**：按量计费、Token Plan、Coding Plan 三者的 API Key 与 Base URL 完全隔离，混用会导致意外扣费或鉴权失败；各地域的 API Key 与模型列表也不能跨地域混用。
- **模型名冲突**：在 Cursor 等工具中部分模型名会与内置模型冲突，需改写别名（如 `kimi-k2.6` → `kimi-k2-6`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [get started with models](../guides/get-started-with-models.md)
- [more models](../api/more-models.md)
- [application call](../api/application-call.md)
- [token plan guide](../guides/token-plan-guide.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


