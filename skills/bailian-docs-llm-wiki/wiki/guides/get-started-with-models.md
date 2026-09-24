# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，仅需配置 API Key 和 Base URL 即可发起首次请求。平台同时覆盖文本、图像、音频、视频、3D、向量等多模态能力，并支持可视化应用构建与模型微调。

## 支持的模型/功能

百炼提供自研千问（Qwen）全系列模型（如 `qwen3.8-max`、`qwen3.8-plus`、`qwen3.8-flash`）、DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，按模态划分为：

- **文本生成**：旗舰模型 `qwen3.8-max`（推荐用于复杂任务）、均衡型 `qwen3.8-plus`（多数场景首选）、高性价比 `qwen3.8-flash`（低延迟简单任务）；
- **多模态**：`qwen3.8-omni-flash`（离线音视频理解与文本生成）、`qwen3.8-omni-flash-realtime`（实时音视频对话）；
- **专业能力**：向量模型（`qwen3.7-text-embedding-flash`）、重排序（`qwen3.7-text-rerank`）、决策模型（`decision-model-preview`）、世界模型（`happyoyster-1.0-adventure`）等；
- **其他模态**：图像生成（`qwen-image-3.0-pro`）、语音合成（`qwen-audio-3.0-tts-plus`）、ASR（`qwen-audio-3.1-asr-flash-streaming`）、音乐生成（`fun-music-v1`）、3D 生成（`Tripo/Tripo-H3.1`）。

完整模型列表请参见[选择模型](raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 1 中称 “qwen3.8-max 推理能力全面超越前代”，但文档 3 的模型列表中未列出 `qwen3.8-max` 的上下文长度或具体性能指标；而文档 5 的限流表中明确列出其适用[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)，且 RPM/TPM 值为“动态”而非固定数值——这与 `qwen3.7-max` 等固定限流模型形成关键差异，使用时应以动态限流机制为准。

## 关键参数

调用模型必需的核心参数包括：

- `model`：模型标识符，如 `"qwen3.8-plus"`，必须与所选地域支持的模型一致（例如 `deepseek-v4-pro-0813` 仅支持北京地域）；
- `base_url`：必须匹配地域与计费方案（按量付费、[Token](../concepts/token.md) Plan 或 Coding Plan），且与 API Key 所属地域严格一致；
- `api_key`：通过[获取API Key](raw/model-api-reference/preparations/get-api-key.md)创建，不同地域的 API Key 不通用；
- `WorkspaceId`：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、中国香港、美国（弗吉尼亚）地域均需在 `base_url` 中填入业务空间 ID（可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面查看）。

请求体大小受严格限制：不含 Base64 的请求最大 16 MiB；含 Base64 的请求整体最大 64 MiB，但解码后仍不得超过 16 MiB，否则返回 HTTP 413 错误 [限流](raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 使用方式

### 1. 配置环境
- 获取 API Key：前往[API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)创建；
- 设置环境变量：推荐将 `DASHSCOPE_API_KEY` 写入 `~/.bashrc`（Linux/macOS）或系统属性（Windows），避免硬编码；
- 选择 Base URL：生产环境**强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与流量隔离能力；DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）将于 2026 年 9 月 30 日起停止支持新特性 [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md)。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.8-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 1 与文档 2 均给出 Python/Node.js/curl 示例，但文档 2 的代码中 `MultiModalConversation.call` 使用 DashScope SDK 且 endpoint 路径为 `/api/v1`，而文档 1 的 OpenAI 兼容示例统一使用 `/compatible-mode/v1` —— 二者协议栈不同，不可混用。生产环境应统一选用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)以保障生态一致性。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国弗吉尼亚等）的 Base URL、API Key、模型列表、功能支持完全独立，**严禁跨地域混用**。例如美国地域不支持批量推理，德国/日本地域暂不支持模型调优与应用开发 [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。
- **限流机制**：
  - `qwen3.8-max`、`qwen3.8-flash` 等主力模型采用[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值按账号月消费金额分档（如北京地域消费 ¥10–100 万对应 1000 万 TPM），每月 15 日生效；
  - 非动态限流模型（如 `qwen3.7-plus-2026-05-26`）有固定 RPM/TPM 上限（如 600 RPM / 1,000,000 TPM），详见[限流](raw/model-user-guide/get-started-with-models/rate-limit.md)；
  - 试用域名 RPM 仅为 1000（主账号维度），**禁止用于生产**。
- **费用控制**：
  - 免费额度仅限华北2（北京）地域新用户，用完后可自动转按量付费，或开启“免费额度用完即停”避免扣费；
  - Coding Plan 与 [Token](../concepts/token.md) Plan 使用**专属 Base URL 和 API Key**，若错误使用按量付费域名，将导致按量计费；
  - 模型推理与知识库（RAG）**计费完全独立**：前者按 [Token](../concepts/token.md) 用量计费，后者按规格时长+模型调用计费，且知识库不支持节省计划 [什么是阿里云百炼](raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。
- **安全与合规**：按量付费与 Token Plan 团队版**不使用客户数据训练模型**；但 Token Plan 个人版与 Coding Plan 明确允许使用输入/输出内容优化服务，请务必审阅对应条款。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


