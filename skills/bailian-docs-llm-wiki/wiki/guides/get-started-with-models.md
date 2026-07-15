# get started with models

阿里云百炼是一站式大模型开发与应用平台，集成千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型，并提供兼容 OpenAI 的 API。本页面面向开发者，梳理从选模型、拿 API Key 到发起首次调用所需的关键信息：可用模型、接入地域与域名、Base URL、以及限流规则与规避策略。

## 支持的模型与能力

百炼提供开箱即用的模型服务，无需自行部署或运维即可直接调用。文本生成方面，千问旗舰系列按能力与成本分层，可按需选择（详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)）：

- **千问 Max**（如 `qwen3.7-max`）：效果最好，适合复杂、多步骤任务。
- **千问 Plus**（如 `qwen3.7-plus`）：效果、速度与成本均衡，多数场景的推荐选择。
- **千问 Flash**（如 `qwen3.6-flash`）：高性价比、低延迟，适合简单、需快速响应的任务。

除文本生成外，还覆盖视觉理解、图像生成、视频生成、语音识别与合成、嵌入向量等[多模态能力](../concepts/multimodal.md)，以及长文本、翻译、法律等细分领域模型。平台同时支持模型调优（SFT/CPT/DPO）、模型部署和模型评测，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 首次调用：获取 API Key 与发起请求

调用流程分为账号准备与代码调用两步，完整步骤见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)：

1. **开通与拿 Key**：用阿里云主账号开通百炼（需实名认证），在控制台 API Key 页面创建 API Key。
2. **获取业务空间 ID**：使用华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域时，需在 Base URL 中填入业务空间 ID（`WorkspaceId`）。
3. **配置环境变量**：建议将 Key 写入环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。
4. **安装 SDK 并调用**：可用 OpenAI Python/Node SDK（`pip install -U openai`）或 DashScope SDK（`pip install -U dashscope`）。

OpenAI 兼容方式的最小示例（北京地域）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 各地域 base_url 不通用，{WorkspaceId} 替换为业务空间 ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

> **注意**：不同文档中示例模型名不一致（概述文档用 `qwen3.7-plus`，首次调用文档用 `qwen-plus`）。`qwen-plus` 为稳定版别名，`qwen3.7-plus` 为具体版本，二者均可用，请以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 页面当前列出的模型 ID 为准。

## 地域、服务部署范围与接入域名

百炼目前提供华北2（北京 `cn-beijing`）、新加坡（`ap-southeast-1`）、美国弗吉尼亚（`us-east-1`）、德国法兰克福（`eu-central-1`）、日本东京（`ap-northeast-1`）五个地域。调用前需选定三项，详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)：

- **地域**：决定接入点与数据存储位置，就近选择可降低延迟。
- **服务部署范围**：决定推理执行位置；有数据合规需求选特定地理边界（如"中国内地""欧盟""美国"），无合规需求选"全球"（推理资源池更大）。北京与新加坡各仅支持一种范围，无需选择。
- **接入域名**：影响并发上限、超时等服务保障。

> **注意**：各地域的接入域名、API Key 和模型列表相互独立，**不能跨地域混用**；跨地域使用 API Key 会报错。美国（弗吉尼亚）地域可用带 `-us` 后缀的模型名（如 `qwen-plus-us`）限定美国境内推理。

## Base URL 选择

Base URL 是模型 API 的调用地址，必须与同一计费方案的 API Key 配套使用，否则会报错 401。按量付费下有三类域名（详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）：

- **业务空间专属域名（推荐）**：格式 `{WorkspaceId}.{region}.maas.aliyuncs.com`，用于生产环境，具备更高并发、更低时延与流量隔离，请求超时 3600 秒，支持 HTTP/SSE/WebSocket/WebRTC。
- **Dashscope 域名**：如 `dashscope.aliyuncs.com`（北京）、`dashscope-intl.aliyuncs.com`（新加坡）、`dashscope-us.aliyuncs.com`（美国），存量兼容用，建议迁移到专属域名，请求超时 600 秒。
- **试用域名**：`trial.{region}.maas.aliyuncs.com`，仅用于快速验证，RPM 固定 1000，不提供 SLA，不建议生产使用。

三种接口路径后缀：OpenAI 兼容 `/compatible-mode/v1`、DashScope `/api/v1`、Anthropic 兼容 `/apps/anthropic`。此外，Token Plan 与 Coding Plan 有各自专属域名和 API Key，仅限 Claude Code、Codex 等交互式 AI 工具使用，不能用于后端服务。

## 限流规则与规避

百炼按**主账号维度**限流，账号下所有 RAM 子账号、业务空间和 API Key 的调用量合并计算；不同模型的限流额度相互独立。限流同时约束 RPM（每分钟请求数）和 TPM（每分钟 Token 数，含输入与输出），并可能按秒级 RPS/TPS 执行。超限请求会被拒绝，通常一分钟内自动恢复。详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

常见错误信息与对策：

- `Requests rate limit exceeded`：触发 RPM 限流，降低调用频率。
- `Allocated quota exceeded`：触发 TPM 限流，缩短输入或限制输出。
- `Request rate increased too quickly`：请求瞬时激增触发稳定性保护，采用匀速调度、指数退避或请求队列平滑请求。

规避建议：优先选用限流额度更高的模型（稳定版比带日期的快照版更宽松）；配置备选模型做失败重试；拆分大任务；无需实时响应时改用批量推理（Batch API，不受实时限流约束）；额度不足时在控制台"限流提额"页面提升临时 TPM 额度（提交即生效，有效期 30 天，目前支持北京和新加坡地域）。

> **注意**：限流仅约束单位时间内的调用速率，**不限制累计用量与费用**。控制费用需另行设置消费限额、费用告警，或开启"免费额度用完即停"（仅新用户、仅北京地域、且在免费额度有效期内有效）。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


