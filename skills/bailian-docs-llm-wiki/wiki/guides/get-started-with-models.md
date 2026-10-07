# get started with models

阿里云百炼提供开箱即用的大模型服务，开发者可通过标准化 API 快速集成千问（Qwen）及主流第三方模型。本文档聚焦模型调用的起点，涵盖模型选择、核心配置、调用方式与关键约束，助您在 5 分钟内完成首次成功请求。

## 支持的模型/功能

百炼支持多模态、全场景模型，覆盖文本生成、图像/视频理解与生成、语音识别与合成、[向量嵌入](../concepts/embedding.md)、决策推理等能力。主力文本模型包括：

- **qwen3.8-max**：旗舰级模型，适合复杂多步任务；  
- **qwen3.7-plus**：效果、速度与成本均衡，为多数场景的**推荐选择**；  
- **qwen3.8-flash**：高性价比、低延迟，适用于简单高频任务；  
- **qwen3.8-omni-flash** 及 **qwen3.8-omni-flash-realtime**：全模态模型，分别面向离线音视频分析与实时端到端语音对话；  
- 第三方模型如 `deepseek-v4-pro-0813`、`kimi-k3`、`glm-5.3` 等亦全面支持（部分仅限华北2北京地域）[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：文档 2 中称 `qwen3.8-max` 是“最新的 qwen3.8-max 推理能力全面超越前代”，但文档 3 的模型列表未标注版本时效性，且文档 6 的限流表中同时存在 `qwen3.8-max` 与多个带日期后缀的快照模型（如 `qwen3.8-max-0902`）。实际调用时应以控制台[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)或 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中当前可选的最新稳定版为准，避免使用已归档的快照模型。

## 关键参数

调用模型需明确以下三个核心参数：

- **`model`**：字符串，指定模型 ID（如 `"qwen3.7-plus"`），必须与所选地域支持的模型一致；  
- **`base_url`**：API 入口地址，**必须与地域和计费方案严格匹配**。生产环境强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其具备更高吞吐、更低时延与流量隔离能力 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
- **`DASHSCOPE_API_KEY`**：通过[API Key 页面](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)创建，建议配置为环境变量以规避密钥泄露风险 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

此外，`messages`（OpenAI 兼容）或 `content`（DashScope 原生）为必填输入，`max_tokens`、`temperature` 等为可选控制参数。

## 使用方式

### 1. 准备工作
- 注册阿里云账号并完成实名认证；  
- 开通百炼服务，在[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页获取 `WorkspaceId`（华北2、新加坡等需显式配置）；  
- 创建 API Key 并配置环境变量 `DASHSCOPE_API_KEY`（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 推荐系统属性配置）[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

### 2. 调用示例（OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",  # 替换为真实 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

> **注意**：文档 2 和文档 5 均明确列出各地域的 `base_url` 格式，但文档 1 的 Python 示例中误将 `qwen3.8-max` 写为 `qwen3.8-max`（正确应为 `qwen3.8-max`），而文档 3 的模型列表中该模型名称拼写一致。此处以文档 3 和控制台为准，调用时请严格使用模型市场公示的准确名称。

### 3. 多语言支持
除 Python 外，Node.js、curl 等方式均受支持，详见 [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的代码片段。

## 限制和注意事项

- **地域隔离**：各地域（如华北2、新加坡、美国弗吉尼亚）的 API Key、`base_url`、模型列表完全独立，**不可跨地域混用** [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；  
- **限流机制**：  
  - `qwen3.8-max`、`qwen3.8-flash` 等主力模型采用**动态限流**，TPM 阈值按账号月消费金额分档（如北京地域消费 ¥10万~¥100万档对应 TPM 1000万），且为软限流（实际可用值 ≥ 限流值）[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；  
  - 其他模型（如 `qwen-plus-2025-07-28`）采用固定 RPM/TPM 限流（如 RPM=60, TPM=1,000,000），超限返回 `429 Too Many Requests`；  
- **试用约束**：试用域名（`trial.*`）RPM 仅为 1000，不提供 SLA，**严禁用于生产环境** [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；  
- **费用控制**：免费额度耗尽后，若未开启“免费额度用完即停”，将自动转为按量付费；充值不影响限流阈值，仅保障账户可用性 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


