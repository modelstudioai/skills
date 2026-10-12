# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需自行部署或运维，只需配置 API Key、Base URL 和模型名称，即可在几分钟内完成首次调用。平台同时覆盖文本、图像、音频、视频、3D、向量等[多模态](../concepts/multi-modal.md)能力，并支持微调、部署、评测等全链路模型工程能力。

## 支持的模型与功能

百炼提供开箱即用的模型服务，涵盖自研千问（Qwen）全系列及 DeepSeek、Kimi、GLM、MiniMax 等主流第三方模型。模型按模态和场景分类，包括：

- **文本生成**：`qwen3.8-max`（旗舰，复杂任务首选）、`qwen3.7-plus`（效果/速度/成本均衡，[推荐选择](raw/model-user-guide/get-started-with-models/models.md)）、`qwen3.8-flash`（高性价比、低延迟）；第三方如 `deepseek-v4-pro-0813`、`kimi-k3`、`glm-5.3`。
- **[多模态](../concepts/multi-modal.md)**：`qwen3.8-omni-flash`（离线全模态理解与生成）、`qwen3.8-omni-flash-realtime`（实时音视频对话）；视觉理解与生成模型如 `qwen-image-3.0-pro`、`wan3.0-video`。
- **专业能力**：向量模型（`qwen3.7-text-embedding-flash`）、重排序（`qwen3.7-text-rerank`）、决策模型（`decision-model-preview`）、语音识别（`qwen-audio-3.1-asr-flash-streaming`）等。

所有模型均可通过 [模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market) 在线体验，具体支持情况因地域而异，详见 [选择模型](raw/model-user-guide/get-started-with-models/models.md) 文档。

## 关键参数

调用模型需明确以下核心参数：

- **`model`**：模型标识符，如 `"qwen3.8-max"`。必须与所选地域支持的模型列表一致，不同地域模型可用性不同（例如 DeepSeek 仅支持北京地域）。
- **`base_url`**：API 接入域名，**必须与 API Key 所属地域严格匹配**，且需替换 `{WorkspaceId}` 占位符为真实业务空间 ID（华北2、新加坡、日本、德国、中国香港、美国均需）。示例：
  - 北京地域业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
  - 新加坡地域 DashScope 域名：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
  > **注意**：文档 1 中列出的 `curl` 示例 Base URL 路径为 `/compatible-mode/v1/chat/completions`，但实际应使用 `/compatible-mode/v1`（即不带 `/chat/completions` 后缀），该路径由 SDK 或客户端自动拼接。此为文档表述不一致，以 [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md) 为准。
- **`api_key`**：通过 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，**不可跨地域复用**。建议配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码。
- **地域与服务部署范围**：地域决定数据存储位置和接入点；服务部署范围（如“全球”或“欧盟”）决定推理节点物理位置，影响合规性与性能。详情见 [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

### 1. 准备工作
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，创建业务空间（除北京、新加坡外，其他地域需手动创建并指定部署范围）；
- 在对应地域的 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建 Key，并记录 `WorkspaceId`（业务空间管理页可查）。

### 2. 配置与调用
推荐使用 OpenAI Python SDK（兼容性最佳）或 DashScope SDK。关键步骤如下：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId 和地域
)

completion = client.chat.completions.create(
    model="qwen3.7-plus",  # 推荐初学者选用
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

> **注意**：文档 2 中 DashScope SDK 示例使用了 `dashscope.base_http_api_url` 和 `MultiModalConversation.call`，但该接口实际用于[多模态](../concepts/multi-modal.md)（图文输入），而纯文本生成应优先使用 `Generation.call` 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。此差异表明 [首次调用千问API](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 文档中 DashScope 示例存在场景错配，开发者应依据任务类型选择正确 SDK 方法。

### 3. 多语言支持
除 Python 外，Node.js、curl 均有完整示例（见文档 1）。Node.js SDK 配置方式与 Python 类似，需确保 `baseURL` 格式正确。

## 限制和注意事项

- **限流机制**：百炼按主账号维度对 RPM（每分钟请求数）和 TPM（每分钟 [Token](../concepts/token.md) 消耗）进行限流，不同模型额度独立。`qwen3.8-max`、`qwen3.8-flash` 等模型采用 [动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随月消费金额分档提升（如北京地域消费 ¥10万~¥100万时，`qwen3.8-max` TPM 为 1000 万）。
- **地域隔离**：各地域的 API Key、Base URL、模型列表、计费规则完全独立，**严禁混用**。例如，北京地域的 Key 无法调用新加坡地域的模型。
- **域名选择**：生产环境**必须使用业务空间专属域名**（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其具备更高并发、3600 秒超时及 SLA 保障；DashScope 域名（`dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日起停止支持新特性，应尽快迁移。
- **费用控制**：免费额度仅限北京地域新人，用完后自动转为按量付费（已认证用户）或停止服务（未认证用户）。如需避免意外扣费，务必开启 [免费额度用完即停](https://help.aliyun.com/zh/model-studio/new-free-quota#d1cb80ac11i92) 开关，并设置费用告警。
- **[Token](../concepts/token.md) Plan / Coding Plan 注意事项**：二者均为交互式工具专用套餐，**不可用于后端服务调用**，且需使用专属 Base URL 和 API Key（如 `token-plan.cn-beijing.maas.aliyuncs.com`），与按量付费体系完全隔离。使用 Coding Plan 时，数据可能用于服务优化，详见 [常见问题](raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


