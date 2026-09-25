# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署和运维模型基础设施，只需配置 API Key、Base URL 和模型名称，即可在数分钟内完成首次调用。平台同时覆盖文本、图像、音频、视频、3D、向量等多模态能力，并支持可视化应用构建与模型微调。

## 支持的模型与功能

百炼提供自研千问（Qwen）全系模型（如 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.8-flash`）、第三方模型（如 `deepseek-v4-pro-0813`、`kimi/kimi-k3`、`glm-5.2`）及领域专用模型（法律、长文本、意图理解等）。[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)文档完整列出了各模态下的可用模型及其适用场景，包括文本生成、多模态理解与生成、语音识别与合成、向量嵌入与重排序、世界模型、3D 生成等。

除基础推理外，平台还提供：
- **模型调优**：支持监督微调（SFT）、继续预训练（CPT）和直接偏好优化（DPO）；
- **专属部署**：将预置或微调后的模型部署为资源专享的推理服务；
- **模型评测**：支持人工、自动与基线评测，验证效果与风险；
- **应用构建**：支持智能体（Agent）、工作流（Workflow）、高代码应用及 RAG 知识库集成。

> **注意**：文档 1 中称“DeepSeek 仅支持北京地域”，但文档 3 的模型列表中 `deepseek-v4-pro-0813` 和 `deepseek-v4.1-flash` 均未标注地域限制；实际可用性请以[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)控制台实时展示为准。

## 关键参数

调用模型需明确以下核心参数：

- **`model`**：模型标识符，如 `"qwen3.8-max"`、`"deepseek-v4.1-flash"`。必须与所选地域支持的模型一致，详见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。
- **`base_url`**：接入域名，**必须与 API Key 所属地域和计费方案严格匹配**。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高并发、更低延迟与业务空间级隔离。DashScope 域名（如 `dashscope.aliyuncs.com`）已进入迁移期，将于 2026 年 9 月 30 日起停止支持新特性 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **`api_key`**：通过[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)创建，按地域独立管理，不可跨地域复用。
- **`WorkspaceId`**：业务空间 ID，用于构造业务空间专属域名，可在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面查看。华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、中国香港、美国（弗吉尼亚）均需此参数。

## 使用方式

### 1. 环境准备
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，在[API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)创建密钥；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量（推荐永久配置），避免硬编码；
- 安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope 原生）。

### 2. 发起调用（OpenAI 兼容示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换 {WorkspaceId}
)

completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

完整代码与 Node.js/curl 示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 3. 协议与路径
- [OpenAI 兼容接口](../concepts/openai-compatible-api.md)路径后缀为 `/compatible-mode/v1`；
- DashScope 原生接口路径后缀为 `/api/v1`；
- Anthropic 兼容接口路径后缀为 `/apps/anthropic`；
- 实时流式响应支持 SSE、WebSocket、WebRTC、AOQ（仅业务空间专属域名支持）。

## 限制和注意事项

### 限流机制
- **账号级聚合限流**：RPM（每分钟请求数）与 TPM（每分钟 [Token](../concepts/token.md) 消耗）按主账号维度合并计算，子账号、所有业务空间和 API Key 共享额度。
- **动态限流模型**：`qwen3.8-max`、`qwen3.8-flash` 等主力模型采用动态限流，TPM 阈值随百炼月消费金额分档调整（如北京地域消费 ¥10–100 万档对应 1000 万 TPM），且为软限流——实际可用值 ≥ 限流值 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。
- **静态限流模型**：如 `qwen-plus-2025-07-28` 固定 RPM=60、TPM=1,000,000，详见[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)表格。
- **触发判断**：`Requests rate limit exceeded` → RPM 超限；`Allocated quota exceeded` → TPM 超限；`Request rate increased too quickly` → 短时爆发触发保护。

### 其他关键限制
- **请求体大小**：不含 Base64 的请求 ≤ 16 MiB；含 Base64 的请求整体 ≤ 64 MiB，且解码后仍须 ≤ 16 MiB。
- **超时设置**：业务空间专属域名默认 3600 秒；DashScope/试用域名仅 600 秒。
- **地域隔离**：各地域的 Base URL、API Key、模型列表、监控数据完全独立，**严禁混用**。
- **费用控制**：免费额度耗尽后默认转为按量付费；如需自动停服，须在免费额度有效期内开启“免费额度用完即停”开关（仅北京地域支持）。

> **注意**：文档 5 的限流表格中，`qwen3.7-plus` 在北京地域标为 RPM=30,000，而文档 4 的动态限流表中 `qwen3.8-flash` 同档位为 1000 万 TPM —— 二者模型代际不同，限流策略也不同（前者为静态上限，后者为动态基线），不构成矛盾，但开发者需根据所选模型查阅对应文档。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)


