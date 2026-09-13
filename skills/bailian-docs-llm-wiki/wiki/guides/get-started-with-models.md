# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、调用方式、关键配置及使用约束。所有操作均基于标准 REST API 接口，无需额外 SDK 即可集成。建议首次使用者按“选择模型 → 配置认证 → 发送请求”流程实践。

## 支持的模型与功能

百炼平台提供多类大语言模型（如 Qwen 系列）、嵌入模型（如 text-embedding-v1）及[多模态](../concepts/multi-modal.md)模型（如 qwen-vl），覆盖文本生成、语义检索、图文理解等场景。模型列表及能力说明详见 [选择模型](../../raw/model-user-guide/get-started-with-models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（tool calling）和系统提示词（system [prompt](prompt.md)），具体以各模型文档为准。

## 关键参数

调用模型 API 时需指定以下必需参数：
- `model`：模型 ID（如 `qwen-max`、`text-embedding-v1`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models.md) 中公布的名称严格一致；
- `input`：输入内容结构，LLM 类为 `{ "messages": [...] }`，嵌入类为 `{ "texts": [...] }`；
- `parameters`（可选）：控制生成行为，如 `temperature`、`top_p`、`max_tokens`；  
- 认证头 `Authorization: Bearer <api_key>`，API Key 需通过 [阿里云访问控制 RAM](https://help.aliyun.com/zh/ram) 获取。

> **注意**：`base_url` 因地域而异，中国大陆用户默认使用 `https://dashscope.aliyuncs.com/api/v1`，但国际站用户须参考 [Base URL总览](../../raw/model-user-guide/get-started-with-models.md) 选择对应域名；若忽略地域适配，将导致 403 或连接超时。

## 使用方式

1. **获取 API Key**：在 [阿里云 RAM 控制台](https://ram.console.aliyun.com) 创建具有 `dashscope:InvokeModel` 权限的 AccessKey；
2. **构造请求**：使用 `POST /api/v1/services/aigc/text-generation/generation`（文本生成）或 `/api/v1/services/embeddings/text-embedding`（嵌入）等路径；
3. **发送调用**：推荐使用 `curl` 或 Python `requests` 库验证，例如首次调用千问 API 的完整示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models.md)。

## 限制和注意事项

- 每个 API Key 默认享有基础调用量配额，超出后触发限流；动态限流策略与账户等级强相关，详情参见 [动态限流](../../raw/model-user-guide/get-started-with-models.md)；
- 单次请求 `input.messages` 最多支持 32 轮对话历史，`input.texts` 在嵌入接口中最多支持 100 条文本；
- 模型服务部署受地域约束，务必确认所选模型在目标地域（如 `cn-beijing`、`ap-southeast-1`）可用，参考 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models.md)；
- `qwen-turbo` 等轻量模型不支持 `system` 角色消息，若误传将被静默忽略——此行为与 `qwen-max` 不同，需按模型能力差异化实现。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


