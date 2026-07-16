# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等主流第三方模型，并提供兼容 OpenAI 的 API。本页面帮助开发者快速完成从选择模型、获取 API Key、配置 Base URL 到发起首次调用的全流程，并梳理地域、接入域名与限流等关键约束。

## 支持的模型与能力

百炼提供开箱即用的模型服务，无需自行部署或运维即可调用。文本生成方面，千问旗舰模型按能力与成本分层选择（参见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

- **千问 Max**（如 `qwen3.7-max`）：Qwen 系列效果最好的模型，适合复杂、多步骤任务。
- **千问 Plus**（如 `qwen3.7-plus`）：效果、速度和成本均衡，多数场景的**推荐选择**。
- **千问 Flash**（如 `qwen3.6-flash`）：高性价比、低延迟，适合需要快速响应的简单任务。

此外还覆盖视觉理解、图像生成、视频生成、语音识别与合成、嵌入向量等多模态能力，以及长文本、翻译、法律等细分领域模型。平台同时支持模型调优（SFT / CPT / DPO）、模型部署与模型评测，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 关键概念与参数

调用前需要先确定四个维度（详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）：

- **地域（Region）**：决定接入点和数据存储位置。目前提供华北2（北京，`cn-beijing`）、新加坡（`ap-southeast-1`）、日本（东京，`ap-northeast-1`）、德国（法兰克福，`eu-central-1`）、美国（弗吉尼亚，`us-east-1`）。就近选择可降低延迟。
- **服务部署范围**：决定推理执行位置。有数据合规需求时选择特定地理边界（如中国内地、欧盟、美国），无合规需求可选全球部署（推理资源池更大）。德国、日本地域通过[业务空间（Workspace）](../concepts/workspace.md)区分部署范围；美国地域可用带 `-us` 后缀的模型名（如 `qwen-plus-us`）限定境内推理。
- **接入域名**：影响并发上限、超时等服务保障，推荐使用**业务空间专属域名**（`{WorkspaceId}.{region}.maas.aliyuncs.com`，SLA 99.9%、请求超时 3600 秒、支持 HTTP/SSE/WebSocket/WebRTC），另有 Dashscope 域名（现有，超时 600 秒）和试用域名（限流小，不建议生产）。
- **API Key**：各地域相互独立、不能跨地域混用；Base URL 也必须与同一计费方案的 API Key 配套使用，否则报 401。

> **注意**：各地域接入点（Base URL）、API Key 和模型列表均不能跨地域混用；使用北京、新加坡、日本、德国地域时，业务空间专属域名中的 `{WorkspaceId}` 需替换为真实业务空间 ID（可在业务空间管理页查看）。

## 使用方式

**1. 账号与凭证准备**（参见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）：注册并开通百炼 → 在 API Key 页面创建 Key → 获取业务空间 ID。建议将 Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。

**2. 选择 Base URL**（详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）：百炼提供 OpenAI 兼容（`/compatible-mode/v1`）、Anthropic 兼容（`/apps/anthropic`）、DashScope（`/api/v1`）三类接口。以北京地域业务空间专属域名的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)为例：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。

**3. 发起调用**：兼容 OpenAI 接口规范，迁移现有代码只需调整 API Key、base_url 和模型名称。Python 示例：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
)
print(completion.choices[0].message.content)
```

也可通过 DashScope SDK（`pip install -U dashscope`）、curl，或 Chatbox、Claude Code 等客户端/开发工具调用。OpenAI Python SDK 要求 Python ≥ 3.8。

## 限制与注意事项

- **限流按主账号维度合并计算**：账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并统计，不同模型限流额度相互独立。超限请求被拒绝，通常一分钟内自动恢复。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **RPM 与 TPM 双重约束**：`Requests rate limit exceeded` 表示触发每分钟请求数（RPM）限流；`Allocated quota exceeded` 表示触发每分钟 Token 数（TPM）限流；`Request rate increased too quickly` 表示请求瞬时激增触发稳定性保护。限流可能按秒级 RPS（RPM/60）、TPS（TPM/60）执行。
- **规避限流**：优先选用高限流额度模型（稳定版比日期快照版更宽松）、平滑请求速率（匀速/指数退避/队列）、配置备选模型自动切换、拆分任务、无需实时响应时改用 Batch API（不受实时限流约束）。北京与新加坡地域支持在控制台申请临时 TPM 提额（生效 30 天）。
- **计费独立**：模型推理按 Token 用量计费，知识库（RAG）按规格时长与调用独立计费，两者互不相通。限流只约束速率、不限制累计用量；如需控费可设置费用告警、开启"免费额度用完即停"或订阅 Coding Plan（固定月费）。
- **各地域功能差异**：批量推理、模型调优、应用开发等能力目前主要在华北2（北京）支持，海外地域功能覆盖较少，选型前请核对目标地域的功能与模型列表。

> **注意**：Token Plan 与 Coding Plan 的 Base URL 及专属 API Key 仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务；使用非专属 Base URL 调用将按量付费。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


