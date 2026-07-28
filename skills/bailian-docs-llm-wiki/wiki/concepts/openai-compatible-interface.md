# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼提供的一组与 OpenAI API 规范对齐的调用协议（含 Chat Completions、Responses、Vision、Embedding、Completions、Files、Batch、Conversations 等），开发者只需替换 `base_url`、`api_key` 和 `model` 三个参数，即可将基于 OpenAI SDK 或 LangChain 等框架的现有应用平滑迁移到百炼，无需改写业务代码。

## 接口形态

| 接口 | 定位 |
| --- | --- |
| Chat Completions | 与 OpenAI 客户端库直接兼容，迁移成本最低的标准对话接口 |
| Responses API | Chat 的演进版本：内置联网搜索、代码解释器、网页提取等工具，通过 `previous_response_id` 自动管理对话历史（响应 id 有效期 7 天） |
| Vision | 视觉理解（Qwen-VL、QVQ、Qwen-OCR），通过 `image_url` 传图片 URL 或 Base64 |
| Embedding | 文本向量（text-embedding-v1~v4），v3/v4 支持 `dimensions` 指定维度 |

与之并列的还有 DashScope 原生接口（功能与参数最全）和 Anthropic 兼容 Messages 接口；OpenAI 兼容接口的优势在于生态兼容与最低迁移成本。

## 在百炼平台的使用场景

- **模型调用**：Qwen 商业版/开源版、Qwen-VL、Qwen-Coder、Qwen-Omni、Qwen-Math 及 DeepSeek、Kimi、GLM 等第三方模型均可通过该接口调用；支持[流式输出](streaming.md)（`stream=True`，配合 `stream_options={"include_usage": True}` 返回 token 用量）与 function call（`tools` 参数）。
- **专用模型**：意图理解（tongyi-intent-detect-v3）、翻译（qwen-mt-plus，通过 `extra_body` 传 `translation_options`）、OCR（qwen3.5-ocr）、GUI 交互（gui-plus）等大多支持 OpenAI 兼容调用。
- **应用调用**：智能体/工作流应用可通过 OpenAI 兼容的 Responses API 调用（`.../apps/agent/{APP_ID}/compatible-mode/v1/responses`），支持多轮对话、[多模态](multimodal.md)输入与 `background=true` 异步执行。
- **第三方工具接入**：Codex、Cursor、Cline、Qwen Code、Cherry Studio、Dify 等工具选择 "OpenAI Compatible" 提供方并填入百炼端点即可接入。

## 关键参数与配置

- **base_url**：统一格式为 `https://<host>/compatible-mode/v1`，按地域区分，例如：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - 日本（东京）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`
  - 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
  - Token Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`；Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`
- **api_key**：建议写入环境变量 `DASHSCOPE_API_KEY`。各地域、各计费方案（按量付费 / Token Plan / Coding Plan）的 API Key 互不通用，必须与 base_url 配套，否则返回 401。
- **model**：目标模型名，如 `qwen3.7-plus`；美国地域使用带 `-us` 后缀的模型名。
- **扩展参数**：百炼专属参数（如 `translation_options`、`vl_high_resolution_images`、`enable_thinking`）通过 OpenAI SDK 的 `extra_body` 传入。

## 调用示例

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}],
)
```

## 注意事项

- **并非全量兼容**：Qwen-Audio 仅支持 DashScope 协议；qwen-deep-research 仅支持 Python DashScope SDK；[多模态](multimodal.md) Embedding 模型（如 qwen3-vl-embedding）不支持 OpenAI 兼容接口。跨接口迁移时需核对参数映射，DashScope 原生接口参数最全。
- **域名迁移**：北京/新加坡地域推荐使用[业务空间](workspace.md)专属域名，旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 仍可用但建议迁移；Responses API 旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 即将停止维护，应迁移到 `/compatible-mode/v1/...` 新路径。
- **地域差异**：各地域可用模型、价格与 API Key 均不同；DeepSeek 等第三方直供模型仅限中国站中国内地且需先在控制台开通。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [get started with models](../guides/get-started-with-models.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


