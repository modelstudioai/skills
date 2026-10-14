# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过兼容 OpenAI 的 API 快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，仅需配置 API Key、Base URL 和模型名称，即可在几分钟内完成首次调用。平台同时覆盖文本、多模态、向量、决策等全类型模型能力，适用于从原型验证到高并发生产的各类场景。

## 支持的模型与功能

百炼提供开箱即用的模型服务，涵盖自研千问（Qwen）全系列及 DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，按模态和用途分类如下：

- **文本生成**：`qwen3.8-max`（旗舰）、`qwen3.8-plus`（推荐均衡）、`qwen3.8-flash`（高性价比），以及 `deepseek-v4-pro-0813`、`kimi-k3`、`glm-5.3` 等 [详见模型列表](raw/model-user-guide/get-started-with-models/models.md)；
- **多模态**：`qwen3.8-omni-flash`（离线音视频理解/生成）、`qwen3.8-omni-flash-realtime`（实时音视频对话）、`qwen-image-3.0-pro`（图像生成）、`wan3.0-video`（视频生成）；
- **语音与音频**：`qwen-audio-3.1-asr-flash-streaming`（流式语音识别）、`qwen-audio-3.0-tts-plus`（高质量语音合成）、`qwen-audio-3.1-realtime-plus`（端到端语音转语音）；
- **向量与重排序**：`qwen3.7-text-embedding-flash`（轻量嵌入）、`qwen3.7-text-rerank`（检索精排）；
- **决策模型**：`decision-model-preview`（结构化分类与置信度输出）；
- **世界模型与 3D**：`happyoyster-1.0-adventure`（开放式世界交互）、`Tripo/Tripo-H3.1`（文生3D）。

> **注意**：文档 1 中称 “DeepSeek 仅支持北京地域”，但文档 4 的模型列表中 `deepseek-v4-pro-0813` 和 `deepseek-v4.1-flash` 在新加坡地域亦有明确限流档位（见[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)），表明其实际支持多地域。请以控制台实时模型列表为准。

## 关键参数

调用模型需正确配置以下核心参数，缺一不可：

- **`api_key`**：通过 [API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 创建，不同地域的 Key 不通用；
- **`base_url`**：必须与 API Key 所属地域及计费方案严格匹配：
  - 生产环境**强烈推荐业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），提供更高吞吐、更低延迟与流量隔离；
  - DashScope 域名（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）为存量兼容方案，将于 2026 年 9 月 30 日起停止支持新特性 [详见 Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
  - 试用域名（如 `https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）仅限临时验证，RPM 限流仅为 1000；
- **`model`**：必须为平台当前地域可用的模型名（如 `"qwen3.8-plus"`），不可使用已下线或地域不支持的别名；
- **`messages`**：遵循 OpenAI 格式，`system`/`user`/`assistant` 角色需明确，内容字段类型依模型而异（文本模型为字符串，多模态模型为对象数组）。

## 使用方式

### 1. 准备工作
- 注册阿里云账号并完成实名认证；
- 开通百炼服务，创建业务空间（[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)）；
- 获取 API Key 与业务空间 ID（WorkspaceId）；
- 将 `DASHSCOPE_API_KEY` 配置为环境变量（[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供各系统详细配置指南）。

### 2. 发起调用（OpenAI SDK 示例）
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为实际 WorkspaceId
)

completion = client.chat.completions.create(
    model="qwen3.8-plus",
    messages=[{"role": "user", "content": "你是谁？"}],
)
print(completion.choices[0].message.content)
```

### 3. 其他接入方式
- **DashScope SDK**：适用于需要原生协议支持（如多模态）的场景，详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)；
- **curl**：适合调试，注意替换 `{WorkspaceId}` 并设置 `Authorization: Bearer $DASHSCOPE_API_KEY` 头；
- **Realtime API**：对低延迟有要求的音视频场景，支持 WebSocket/WebRTC/AOQ 协议 [详见 Realtime API 文档](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-protocol-selection)。

## 限制和注意事项

- **地域隔离**：各地域（北京、新加坡、美国弗吉尼亚等）的 API Key、Base URL、模型列表、监控数据完全独立，**严禁混用**。例如，北京地域的 Key 无法调用新加坡模型 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。
- **限流机制**：
  - 大部分模型采用**账号级 RPM/TPM 限流**（如 `qwen3.7-plus` 北京地域为 30,000 RPM / 5,000,000 TPM）；
  - `qwen3.8-max`、`qwen3.8-flash` 等主力模型采用**动态限流**，TPM 基线随百炼月消费金额自动提升（如北京地域消费 ¥10–100 万档对应 `qwen3.8-max` 1000 万 TPM），且为软限流（实际可用值 ≥ 基线）[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
  - 试用域名 RPM 严格限制为 1000，生产务必切换至业务空间专属域名。
- **费用与额度**：
  - 新用户享有北京地域免费额度，用完后已认证用户自动转按量付费，未认证用户将停服；
  - **务必开启“免费额度用完即停”开关**（仅北京地域有效），避免意外扣费；
  - 模型推理与知识库（RAG）计费完全独立，前者按 [Token](../concepts/token.md)，后者按规格时长。
- **安全与合规**：
  - 按量付费 API 和 [Token](../concepts/token.md) Plan 团队版**不会使用您的数据训练模型**；
  - **Coding Plan 个人版及 [Token](../concepts/token.md) Plan 个人版除外**，其输入/输出数据可能用于服务优化，详见 [合规资质与隐私说明](raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


