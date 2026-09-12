# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、功能扩展、参数配置及售后保障等环节。开发者可通过该支持体系快速集成大模型能力，并获得必要的技术兜底与问题响应。所有服务条款与范围以官方文档为准。

## 支持的模型/功能

当前 `application support` 支持通过 API 或 SDK 调用百炼平台托管的全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），并兼容自定义微调[模型部署](../concepts/model-deployment.md)后的推理调用。功能上覆盖文本生成、多模态理解、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）及 RAG 增强检索等核心场景。详细模型列表与能力矩阵请参见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 关键参数

调用时需在请求头或 payload 中明确以下关键参数：  
- `model`: 必填，指定模型 ID（如 `qwen-max`, `qwen-plus`）；  
- `stream`: 可选布尔值，启用[流式输出](../concepts/streaming-output.md)需设为 `true`；  
- `top_p` / `temperature`: 控制生成多样性，取值范围分别为 `[0.01, 1.0]` 和 `[0.01, 2.0]`；  
- `max_tokens`: 最大输出长度，默认 `2048`，上限依模型而异（如 `qwen-turbo` 为 `8192`）。  
完整参数说明见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 使用方式

1. 在百炼控制台创建应用，获取 `API Key` 与 `Endpoint`；  
2. 构造 HTTP POST 请求，`Content-Type: application/json`，Body 包含 `model` 和 `messages` 字段；  
3. 推荐使用官方 SDK（Python/Java/Node.js）自动处理鉴权、重试与错误解析。  
示例代码与调试工具集成路径详见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 限制和注意事项

- 免费额度仅限新用户首月，超出后按用量计费，具体计费规则以 [相关协议](https://help.aliyun.com/zh/model-studio/application-related-agreements) 为准；  
- 单次请求 `max_tokens` 不得超过模型上下文窗口的 80%，否则将被截断并返回 `400 Bad Request`；  
- > **注意**：原始文档中“售后说明”链接指向的页面已更新，旧版 [售后说明](https://help.aliyun.com/zh/model-studio/application-after-sales-service-scope) 中关于 SLA 响应时效的描述（如“2 小时内响应”）已被新版 SLA 文档覆盖，实际以 [服务支持](../../raw/application-user-guide/application-support.md) 中嵌入的最新帮助中心链接为准。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


