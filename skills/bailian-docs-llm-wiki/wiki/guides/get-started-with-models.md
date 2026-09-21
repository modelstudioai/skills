# get started with models

阿里云百炼提供开箱即用的大模型服务，支持通过标准 API（OpenAI 兼容、DashScope 原生、Anthropic 兼容）快速调用千问（Qwen）全系列及主流第三方模型。开发者无需部署运维，只需完成账号开通、API Key 配置与 Base URL 设置，即可在数分钟内发起首次推理请求。本文聚焦核心接入路径，涵盖模型选择、关键参数、调用方式及生产注意事项。

## 支持的模型/功能

百炼支持覆盖文本、图像、音频、视频、3D、向量与重排序等多模态能力的数十款模型，包括：

- **文本生成旗舰模型**：`qwen3.8-max`（推荐用于复杂任务）、`qwen3.7-plus`（效果/速度/成本均衡的默认推荐）、`qwen3.8-flash`（高性价比低延迟）；  
- **第三方模型**：`deepseek-v4-pro-0813`、`kimi/kimi-k3`、`glm-5.3` 等；  
- **全模态模型**：`qwen3.8-omni-flash`（离线音视频分析+文本生成）、`qwen3.8-omni-flash-realtime`（端到端实时语音对话）；  
- **专用能力模型**：嵌入向量（`qwen3.7-text-embedding-flash`）、重排序（`qwen3.7-text-rerank`）、语音识别（`qwen-audio-3.1-asr-flash-streaming`）、图像生成（`qwen-image-3.0-pro`）等。

所有模型均按地域独立提供，具体可用模型列表请参见[选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。> **注意**：文档 2 中提及“美国（弗吉尼亚）支持 DeepSeek”，但文档 3 的模型列表仅显示 DeepSeek 模型在华北2（北京）地域可用，且文档 7 明确指出“美国（弗吉尼亚）地域的部署模式已升级”，建议以控制台实际模型市场为准，避免跨地域调用失败。

## 关键参数

调用模型必需的核心参数包括：

- `model`：模型标识符，如 `"qwen3.8-plus"`，**必须与所选地域的模型列表一致**；  
- `api_key`：通过[API Key](../../raw/model-api-reference/preparations/get-api-key.md)页面创建，需与 Base URL 所属计费方案匹配（例如 Token Plan Key 不能用于按量付费域名）；  
- `base_url`：**必须严格匹配地域和服务类型**，常见组合如下：
  - 生产推荐：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（业务空间专属域名，需替换 `{WorkspaceId}`）；  
  - 兼容过渡：`https://dashscope.aliyuncs.com/compatible-mode/v1`（华北2）或 `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`（新加坡）；  
  - 临时测试：`https://trial.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（限流严格，不适用于生产）。  
- `messages`：标准 Chat Completions 格式，支持 `system`/`user`/`assistant` 角色；部分多模态模型（如视觉理解）需传入 Base64 编码的图片数据。

## 使用方式

### 1. 基础准备
- 开通百炼服务并完成实名认证；  
- 在目标地域创建[业务空间](../../raw/model-user-guide/get-started-with-models/regions.md)，获取 `WorkspaceId`；  
- 创建 API Key，并按[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)指南配置环境变量 `DASHSCOPE_API_KEY`。

### 2. 调用示例（OpenAI SDK）
```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://llm-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # 替换为实际 WorkspaceId
)

response = client.chat.completions.create(
    model="qwen3.8-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(response.choices[0].message.content)
```

### 3. 多语言支持
除 Python 外，官方提供 Node.js、curl 示例（见[什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)），并支持 Anthropic 协议（需使用对应 `/apps/anthropic` Base URL）。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，**严禁跨地域混用**（如北京 Key 不能调用新加坡模型）；  
- **限流机制**：  
  - 主账号维度统一计算 RPM（每分钟请求数）与 TPM（每分钟 Token 数），不同模型额度独立；  
  - `qwen3.8-max` 等主力模型采用[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)，TPM 阈值随月消费金额自动提升；  
  - 试用域名 RPM 仅为 1000，业务空间专属域名无此硬性限制，但受账号级配额约束；  
- **请求体限制**：不含 Base64 的请求体最大 16 MiB；含 Base64 时，单个 Base64 内容最大 32 MiB（Anthropic 协议）或 20 MiB（其他协议），整体请求体解码后仍不得超过 16 MiB；  
- **超时与协议**：业务空间专属域名支持 3600 秒超时及 WebSocket/WebRTC/AOQ 等高级协议，DashScope 域名仅支持 600 秒 HTTP/SSE；  
- **费用控制**：限流不等于费用控制——充值不影响限流阈值，仅确保不因欠费停服；如需防超额支出，应开启[免费额度用完即停](../../raw/model-user-guide/test-1/new-free-quota.md)或设置账单告警。

## 来源文档

- [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)
- [什么是阿里云百炼](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)
- [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)
- [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)
- [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)
- [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)


