# get started with models

阿里云百炼是一站式大模型开发与应用平台，提供千问（Qwen）全系列及 DeepSeek、Kimi、GLM 等第三方模型的开箱即用服务，并兼容 OpenAI / Anthropic / DashScope 三种接口规范。本页汇总从开通账号、选择模型、获取 API Key，到选择地域与 Base URL、理解[限流](../concepts/rate-limit.md)规则的完整入门路径，帮助开发者快速发起第一次模型调用。

## 前置准备：账号与 API Key

按照[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)的引导完成以下步骤：

1. **注册阿里云账号**并完成实名认证。
2. **开通百炼**：使用阿里云主账号访问百炼控制台，同意服务协议后自动开通（开通免费，调用按量计费）。
3. **创建 API Key**：在控制台 API Key 页面创建。各地域的 API Key 相互独立，**不能跨地域使用**。
4. **获取[业务空间](../concepts/workspace.md) ID（WorkspaceId）**：使用华北2（北京）、新加坡、日本（东京）或德国（法兰克福）地域时，Base URL 中需填入 WorkspaceId，可在[业务空间](../concepts/workspace.md)管理页面查看。
5. **配置环境变量**：建议将 API Key 写入 `DASHSCOPE_API_KEY` 环境变量（Linux/macOS 用 `export`，Windows 用系统属性或 `setx`），避免硬编码泄露。

## 选择模型

根据[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)与[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)，千问旗舰文本模型按"能力—成本"梯度分为三档：

| 系列 | 代表模型 ID | 定位 |
| --- | --- | --- |
| 千问 Max | `qwen3.7-max` | 效果最强，适合复杂多步骤任务 |
| 千问 Plus | `qwen3.7-plus` | 效果、速度、成本均衡，多数场景的推荐选择 |
| 千问 Flash | `qwen3.7-flash` | 高性价比、低延迟，适合简单快速任务 |

此外平台覆盖视觉理解、图像/视频生成、语音识别与合成、嵌入向量等[多模态](../concepts/multimodal.md)能力，以及长文本、翻译、法律等细分领域模型。

> **注意**：`qwen3.8-max-preview` 目前仅面向 Token Plan 订阅用户开放，按量付费用户不可直接调用。

> **注意**：DeepSeek 等部分第三方模型仅在华北2（北京）地域提供，选型前请核对目标地域的可用模型列表。

## 地域与 Base URL

地域决定接入点和数据存储位置，各地域的 Base URL、API Key、可用模型与价格均不同。详见[地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)与[Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)。

### 三种接入域名（按量付费）

| 域名类型 | 格式 | 适用场景 | 请求超时 |
| --- | --- | --- | --- |
| [业务空间](../concepts/workspace.md)专属域名（**推荐**） | `{WorkspaceId}.{region}.maas.aliyuncs.com` | 生产环境，高并发、流量隔离，SLA 99.9% | 3600 秒 |
| Dashscope 域名 | `dashscope.aliyuncs.com`（北京）等 | 存量业务兼容，建议迁移 | 600 秒 |
| 试用域名 | `trial.{region}.maas.aliyuncs.com` | 快速验证，RPM 固定 1000，无 SLA | 600 秒 |

### 各地域 OpenAI 兼容 Base URL

- 华北2（北京，`cn-beijing`）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- 新加坡（`ap-southeast-1`）：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- 日本（东京，`ap-northeast-1`）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`
- 德国（法兰克福，`eu-central-1`）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
- 美国（弗吉尼亚，`us-east-1`）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`（暂不支持业务空间专属域名）

DashScope 原生接口将路径 `/compatible-mode/v1` 换为 `/api/v1`，Anthropic 兼容接口换为 `/apps/anthropic`。

> **注意**：Base URL 必须与同一计费方案的 API Key 配套使用，否则返回 401。Token Plan / Coding Plan 有独立的专属域名和 API Key，仅限 Claude Code、Codex 等 AI 工具交互式使用，不能用于后端服务。

> **注意**：德国（法兰克福）和日本（东京）地域需先创建业务空间并选择服务部署范围（全球/欧盟、全球/日本）；美国（弗吉尼亚）地域用带 `-us` 后缀的模型名（如 `qwen-plus-us`）限定美国境内推理。

## 发起第一次调用

以 OpenAI Python SDK 为例（`pip install -U openai`，Python ≥ 3.8）：

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 北京地域示例，{WorkspaceId} 替换为真实业务空间 ID
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

DashScope SDK（`pip install -U dashscope`）则设置 `dashscope.base_http_api_url = 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1'` 后用 `Generation.call()` 调用。已有 OpenAI 代码只需替换 `api_key`、`base_url` 和模型名即可迁移。

## [限流](../concepts/rate-limit.md)规则

根据[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)：

- **账号级别[限流](../concepts/rate-limit.md)**：按主账号维度计算，所有 RAM 子账号、业务空间、API Key 的调用量合并统计；不同模型的额度相互独立。
- **双重限制**：RPM（每分钟请求数）与 TPM（每分钟 Token 数，含输入和输出）超出任一即触发；系统还可能按秒级 RPS（RPM/60）、TPS（TPM/60）执行，瞬时爆发也会被限。
- **典型额度（北京地域）**：`qwen3.7-max` / `qwen3.7-plus` / `qwen3.7-flash` 均为 30,000 RPM；带日期的快照版本额度显著更低（多为 60–600 RPM）。
- **常见错误**：`Requests rate limit exceeded`（RPM 超限）、`Allocated quota exceeded`（TPM 超限）、`Request rate increased too quickly`（请求激增触发保护）。限流通常一分钟内自动恢复。

规避建议：优先选稳定版高额度模型、匀速调度 + 指数退避、配置备选模型自动切换、大任务改用批量推理（Batch API 不受实时限流约束），或在控制台"限流提额"页面申请临时 TPM 提额（立即生效，有效期 30 天，仅支持北京和新加坡地域）。

## 限制与注意事项

- **地域间不通用**：API Key、Base URL、模型列表、价格均按地域隔离；批量推理仅北京和新加坡支持，模型调优与应用开发仅北京支持。
- **计费**：开通免费，调用按 Token 量计费，按分钟出账。新用户有北京地域专属免费额度，可开启"免费额度用完即停"避免意外扣费。
- **调用统计延迟**：模型监控数据在调用完成约一小时后可见，高峰期可能有小时级延迟。
- **数据安全**：阿里云不会将用户数据用于模型训练，传输全程加密。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [地域及接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


