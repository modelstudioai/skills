# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、参数配置、调用方式及售后保障等环节。开发者可通过该支持体系快速集成大模型能力，并获得必要的技术兜底与问题响应。所有支持内容均以 [服务支持](../../raw/application-user-guide/application-support.md) 文档为权威依据。

## 支持的模型/功能

当前 `application support` 支持通过 API 调用百炼平台已发布的全部托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），并兼容标准 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/v1/chat/completions`）。不支持直接调用未发布至应用中心的私有微调模型或本地部署模型。功能上覆盖文本生成、[多模态](../concepts/multi-modal.md)推理、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）等核心场景，具体能力边界请参考 [服务支持](../../raw/application-user-guide/application-support.md) 中“支持范围”章节。

## 关键参数

调用时需在请求头（Header）中携带 `Authorization: Bearer <api_key>`，并在请求体中指定以下必选参数：
- `model`: 模型 ID（如 `qwen-max`、`qwen-plus`），必须与 [服务支持](../../raw/application-user-guide/application-support.md) 中列出的可用模型一致；
- `messages`: 符合 OpenAI 格式的对话数组；
- `stream`: 布尔值，控制是否启用流式响应（默认 `false`）。

可选参数包括 `temperature`（0.0–2.0）、`max_tokens`（最大输出长度）、`tools`（函数工具定义）等，其取值范围和行为语义严格遵循平台最新运行时规范。

## 使用方式

1. 在百炼控制台「应用管理」中创建应用，获取 `API Key`；
2. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/chat/completions`；
3. 设置请求头 `Content-Type: application/json` 和 `Authorization`；
4. 发送 JSON 请求体，示例见 [服务支持](../../raw/application-user-guide/application-support.md) 的“调用示例”小节。

> **注意**：部分旧版文档（如 `raw/legacy-api-reference/v1.md`）中提及的 `/v1/applications/{app_id}/chat` 路径已废弃，当前仅支持统一 `/v1/chat/completions` 接口，以 [服务支持](../../raw/application-user-guide/application-support.md) 为准。

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（具体依模型而异，`qwen-turbo` 为 8192）；
- 免费额度按自然月重置，超出后按用量计费，计费规则详见 [服务支持](../../raw/application-user-guide/application-support.md) 的“售后说明”链接；
- 不支持跨区域调用（例如华东1区应用密钥不可用于华北2区 endpoint）；
- 流式响应中 `delta.content` 字段可能为空（尤其在 tool call 场景下），客户端需容错处理。

> **注意**：若发现控制台显示的模型列表与 [服务支持](../../raw/application-user-guide/application-support.md) 中所列不一致，请以控制台实时列表为准——文档可能存在数小时延迟，平台优先保障控制台数据时效性。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)



