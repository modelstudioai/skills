# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准 API（OpenAI 兼容、DashScope 原生、Anthropic 兼容）快速集成千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，只需完成账号开通、API Key 配置与 Base URL 设置，即可发起首次调用。本文聚焦模型调用的起点，涵盖核心能力、关键参数、接入方式及必须注意的限制条件。

## 支持的模型/功能

百炼支持[多模态](../concepts/multimodal.md)、多场景模型，覆盖文本生成、图像/视频理解与生成、语音识别与合成、向量嵌入、重排序及世界模型等。主力文本模型包括：

- **qwen3.8-max**：旗舰级模型，适合复杂多步任务；最新版推理能力全面超越前代，推荐选用  
- **qwen3.8-plus**：效果、速度与成本均衡，是多数生产场景的**推荐选择**  
- **qwen3.8-flash**：高性价比、低延迟，适合简单高频任务  
- **qwen3.8-omni-flash**：全模态模型，支持音视频分析与文本生成，详见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)  

此外还提供 DeepSeek、Kimi、GLM、MiniMax、Tripo 等第三方模型，以及语音（ASR/TTS）、图像生成（qwen-image-3.0-pro）、3D 生成（Tripo-H3.1）等垂直能力模型。所有模型均按地域独立提供，具体可用模型请以[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)实时列表为准。

> **注意**：文档 2 中称“DeepSeek 仅支持北京地域”，但文档 4 的模型列表未标注地域限制；实际调用前请务必在目标地域控制台确认模型可用性，避免因地域不匹配导致 404 错误。

## 关键参数

调用模型时需明确以下核心参数，缺一不可：

- **`model`**：模型标识符，如 `"qwen3.8-plus"`，必须与所选地域支持的模型完全一致（区分大小写与版本后缀）。模型列表见 [选择模型](raw/model-user-guide/get-started-with-models/models.md)。  
- **`api_key`**：通过 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 页面创建，**必须与 Base URL 所属地域和计费方案严格匹配**（例如 [Token](../concepts/token.md) Plan 的 Key 不能用于按量付费域名）。  
- **`base_url`**：决定请求路由与服务保障等级。必须使用与地域、计费方案（按量/[Token](../concepts/token.md) Plan/Coding Plan）对应的域名，详见 [Base URL总览](raw/model-user-guide/get-started-with-models/base-url.md)。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）为生产环境推荐。  
- **`workspace_id`**：仅华北2（北京）、新加坡、日本（东京）、德国（法兰克福）、中国香港、美国（弗吉尼亚）地域需显式填入，从[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面获取。  

> **注意**：文档 1 和文档 2 均给出 Python 示例，但文档 1 使用 `qwen3.8-max` 而文档 2 强调 `qwen3.8-plus` 是“推荐选择”；实际应以业务场景为准——高精度需求选 max，平衡性需求选 plus，非紧急验证可优先用 plus 降低限流风险。

## 使用方式

### 1. 基础准备
- 注册阿里云账号并完成实名认证  
- 开通百炼服务，进入[控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)  
- 创建 API Key，并根据使用场景选择权限范围（如需限制可调用模型，创建时开启“访问模型范围”开关）  
- 获取业务空间 ID（WorkspaceId），若使用业务空间专属域名  

### 2. 配置环境
- 将 `DASHSCOPE_API_KEY` 设为环境变量（Linux/macOS 推荐写入 `~/.bashrc` 或 `~/.zshrc`；Windows 通过系统属性配置），避免硬编码泄露  
- 确保 Python ≥ 3.9，安装 SDK：`pip install -U openai`（OpenAI 兼容）或 `pip install -U dashscope`（DashScope 原生）  

### 3. 发起调用（OpenAI 兼容示例）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为真实 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.8-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

完整流程与多语言（Node.js、curl）示例见 [首次调用千问API](raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 限制和注意事项

- **地域隔离**：各地域 API Key、Base URL、模型列表、计费策略均不通用，**严禁跨地域混用**。例如北京地域的 Key 无法调用新加坡域名。  
- **限流机制**：  
  - 大部分主力模型（如 `qwen3.8-max`, `qwen3.8-flash`）采用[动态限流](raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值按账号月消费金额分档调整（如北京地域消费 ¥10万~¥100万，qwen3.8-max TPM 为 1000万）  
  - 非动态限流模型（如 `qwen3.7-plus-2026-05-26`）有固定 RPM/TPM 上限（如 600/1,000,000），详见 [限流](raw/model-user-guide/get-started-with-models/rate-limit.md)  
  - 触发限流返回 HTTP 429，通常 1 分钟内自动恢复；可通过添加备选模型、平滑请求速率等方式规避  
- **请求体限制**：不含 Base64 的请求体最大 16 MiB；含 Base64 时单个内容最大 20–32 MiB，整体请求体最大 64 MiB（解码后仍不得超过 16 MiB，否则返回 413）  
- **免费额度**：新用户享北京地域专属免费额度，用完后自动转为按量付费（已认证用户）或停止服务（未认证用户）。可开启“免费额度用完即停”避免意外扣费。  
- **域名迁移**：DashScope 域名（`dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日起停止支持新特性，**生产环境必须迁移至业务空间专属域名**，迁移步骤见 [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


