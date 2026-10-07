# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可快速集成大模型能力至自有系统，或零代码搭建知识库问答等典型应用。本文档梳理了平台当前支持的核心能力、关键配置项、调用方式及常见约束，适用于首次接入的开发者。

## 支持的模型/功能

百炼平台当前支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等多模态模型，并开放[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、[长上下文](../concepts/long-context.md)（最高 32K tokens）等能力。知识库问答、Agent 工作流、RAG 增强推理等功能可通过控制台可视化配置或 API 直接调用。详细模型列表与能力矩阵请参见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用 API 时需关注以下必填/常用参数：  
- `model`：模型标识符（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），必须与 [开始使用](../../raw/application-user-guide/start-using.md) 中公布的可用模型一致；  
- `input.messages`：消息数组，格式为 `[{ "role": "user", "content": "..." }]`，系统角色（`system`）支持但非必需；  
- `parameters.temperature`：控制生成随机性（0.0–2.0），默认 0.8；  
- `parameters.top_p`：核采样阈值（0.0–1.0），默认 0.8；  
- `stream`：布尔值，启用流式响应需设为 `true`。  
> **注意**：部分旧文档中将 `top_k` 列为推荐参数，但自 v2024.07 起该参数已废弃，实际调用无效，请以 [开始使用](../../raw/application-user-guide/start-using.md) 中最新参数说明为准。

## 使用方式

1. **API 调用**：通过 HTTPS POST 请求 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，携带 `Authorization: Bearer <api_key>` 头；  
2. **SDK 快速接入**：官方 Python SDK（`dashscope` v1.20.0+）和 Node.js SDK（`@alibabacloud/dashscope` v1.15.0+）已内置百炼适配，初始化后调用 `Generation.call()` 即可；  
3. **零代码应用构建**：登录控制台 → 创建应用 → 选择「知识库问答」模板 → 上传文档并发布，全程无需编码，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- 免费额度按自然月重置，超出后需绑定付费账号；  
- 单次请求最大输入长度为 32768 tokens，输出长度上限为 8192 tokens（具体依模型而异）；  
- 知识库问答应用默认启用敏感词过滤与内容安全审核，不可关闭；  
- 流式响应中 `event: error` 事件不保证包含完整错误码，建议同时检查 HTTP 状态码与响应体 `code` 字段；  
- 模型版本迭代可能导致行为微调（如系统提示词默认注入逻辑），建议在生产环境锁定 `model` 版本标识（如 `qwen-max-20240801`），而非使用别名。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


