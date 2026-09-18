# application [support](support.md)

application [support](support.md) 是百炼平台为应用开发者提供的模型调用与服务集成支持能力，涵盖模型选型、参数配置、请求方式及服务边界说明。开发者可通过标准 API 接口或 SDK 快速接入，适用于对话、文本生成、结构化输出等典型场景。具体能力与约束详见下文。

## 支持的模型/功能

当前支持 Qwen 系列大语言模型（如 qwen-max、qwen-plus、qwen-turbo）及部分多模态模型（如 qwen-vl），覆盖文本理解、生成、推理、代码编写、多轮对话等能力。图像理解、语音转写等扩展功能需结合对应专用模型调用。所有可用模型列表及能力说明见 [服务支持](../../raw/application-user-guide/application-support.md)。

## 关键参数

核心请求参数包括：  
- `model`：必需，指定模型 ID（如 `"qwen-max"`）；  
- `input.messages`：必需，消息数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`；  
- `parameters.temperature`：控制生成随机性（0.0–1.0，默认 0.8）；  
- `parameters.max_tokens`：最大输出 token 数（默认 1024，上限依模型而异）；  
- `parameters.top_p`、`stop`、`tools` 等高级参数按需启用。  
完整参数定义与取值范围请参考 [服务支持](../../raw/application-user-guide/application-support.md) 中的接口规范附录。

## 使用方式

推荐通过 REST API 调用，需在请求头中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`。SDK（Python/Java/Node.js）已封装标准调用逻辑，支持流式响应（`stream=true`）和异步任务提交。初始化示例见 [服务支持](../../raw/application-user-guide/application-support.md) 的“快速开始”章节。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含历史上下文）不得超过模型 context length（如 qwen-max 为 32768 tokens），超长将被截断且不报错；  
- 免费试用额度仅限新用户首月，商用需绑定计费账户；  
- > **注意**：原始文档中提及的“售后说明”文件（[售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)）所列 SLA（99.9% 可用性）仅适用于企业版实例，基础版不承诺该指标；  
- 图像输入暂不支持 Base64 内联，必须传公网可访问 URL；  
- `tools` 调用需显式声明 function schema，且当前仅支持同步执行模式，异步工具链能力尚未开放。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


