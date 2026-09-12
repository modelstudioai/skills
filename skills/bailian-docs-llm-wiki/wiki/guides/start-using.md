# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可通过控制台或 API 快速接入大模型服务。本文档梳理了核心支持范围、关键配置项、调用方式及常见约束，适用于首次集成或评估平台能力的开发者。所有功能均以 [开始使用](../../raw/application-user-guide/start-using.md) 为基础依据。

## 支持的模型/功能

- 支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等开源模型，以及部分闭源模型（如 Qwen-Max、Qwen-Plus）；
- 提供零代码问答应用构建能力，支持知识库上传、RAG 配置与多轮对话管理，详见 [开始使用](../../raw/application-user-guide/start-using.md)；
- 应用功能持续迭代，最新特性（如[流式输出](../concepts/streaming.md)增强、工具调用 Beta 支持）请参考 [应用功能动态](../../raw/application-user-guide/start-using.md)。

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-max`、`qwen2.5-72b-instruct`），需与实际开通权限一致；
- `input.messages`: 至少包含一个 `role`（`user`/`assistant`/`system`）和 `content` 字段，`content` 支持纯文本或结构化 multimodal 输入（仅限支持多模态的模型）；
- `parameters.temperature`、`top_p`、`max_tokens` 等为可选控制参数，具体取值范围见各模型文档；  
- 所有参数命名与语义严格遵循 [开始使用](../../raw/application-user-guide/start-using.md) 中定义的 API 规范。

## 使用方式

1. **控制台快速体验**：登录百炼控制台 → 创建应用 → 选择模型 → 在「调试」页直接发送请求；
2. **API 调用**：使用 `POST /v1/services/aigc/text-generation/generation` 接口，需携带 `Authorization: Bearer <api_key>` 头；
3. **SDK 集成**：推荐使用 `dashscope` Python SDK（v1.18.0+）或 `@alibabacloud/pop-core` Node.js SDK，初始化时传入 `api_key` 和 `base_url`（默认为 `https://dashscope.aliyuncs.com/api/v1`）。

## 限制和注意事项

- 免费额度仅限新用户首月，调用频次与并发数受配额限制，超出后返回 `429 Too Many Requests`；
- Qwen-VL/Qwen-Audio 模型暂不支持 `stream=true` 流式响应，该限制与 [开始使用](../../raw/application-user-guide/start-using.md) 当前描述一致；
> **注意**：原始文档中链接 [0代码构建问答应用](https://help.aliyun.com/zh/model-studio/build-knowledge-base-qa-assistant-without-coding) 已重定向至新版知识库构建流程页，旧版 UI 路径已下线，实际操作请以控制台最新界面为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


