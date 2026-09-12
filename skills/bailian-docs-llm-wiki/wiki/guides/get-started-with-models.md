# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。核心包括模型选择、API 调用方式、关键参数配置及基础限制说明。所有操作均基于标准 RESTful API 接口，无需额外 SDK（但推荐使用官方 SDK 简化鉴权与重试逻辑）。

## 支持的模型与功能

百炼平台当前支持通义千问（Qwen）系列主流版本，包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen2.5-*` 等推理模型；部分模型还支持[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应（stream=true）和多模态输入（需显式启用 `enable_multimodal`）。完整模型列表及能力矩阵请参考 [选择模型](../../raw/model-user-guide/get-started-with-models.md) 中的官方链接。注意：`qwen-vl` 已于 2024 年 Q3 下线，其功能由 `qwen2.5-vl` 替代，详见 [选择模型](../../raw/model-user-guide/get-started-with-models.md)。

## 关键参数

调用 `/v1/chat/completions` 接口时，必需参数为 `model` 和 `messages`；推荐显式设置 `temperature`（默认 0.85）、`max_tokens`（默认 2048）以提升可复现性。`top_p`、`stop`、`seed` 等参数行为与 OpenAI 兼容，但 `frequency_penalty` 和 `presence_penalty` 当前不生效（后端忽略）。Base URL 必须根据所选地域指定，例如杭州地域为 `https://dashscope.aliyuncs.com/api/v1`，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models.md)。

## 使用方式

1. **获取 API Key**：在 [阿里云 RAM 控制台](https://ram.console.aliyun.com/) 创建具有 `AliyunDashScopeFullAccess` 权限的 AccessKey  
2. **构造请求**：使用 `POST /v1/chat/completions`，Header 中携带 `Authorization: Bearer ${API_KEY}`  
3. **发送示例**：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/chat/completions" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-turbo",
           "messages": [{"role": "user", "content": "你好"}]
         }'
   ```
> **注意**：原始文档中 [首次调用千问API](../../raw/model-user-guide/get-started-with-models.md) 提供的 Python 示例仍使用已废弃的 `dashscope` v1.x SDK 初始化方式（`dashscope.api_key = ...`），实际应升级至 v2.x 并使用 `dashscope.init(api_key=...)` —— 该差异已在最新 SDK 文档中修正，此处以 SDK v2.0+ 行为为准。

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（含 system [prompt](prompt.md)），超限将返回 `400 Bad Request`  
- 默认调用频率限制为 10 QPS / 1000 RPM（按 AccessKey 维度），可通过 [动态限流](../../raw/model-user-guide/get-started-with-models.md) 页面申请提升  
- 模型输出长度受 `max_tokens` 与模型自身 context 长度共同约束；例如 `qwen-turbo` 最大 context 为 8192，若输入占 6000 tokens，则 `max_tokens` 实际有效上限约为 2192  
- 所有请求必须指定 `region`（如 `cn-hangzhou`），否则可能因路由失败返回 `503 Service Unavailable`；地域与接入域名映射关系见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models.md)

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


