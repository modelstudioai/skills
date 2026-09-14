# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可通过控制台或 API 快速接入大模型服务。本文档汇总启动所需的核心信息，涵盖模型支持范围、关键参数配置、调用方式及常见约束，适用于首次集成或快速验证场景。所有功能均以 [开始使用](../../raw/application-user-guide/start-using.md) 为基础依据。

## 支持的模型/功能

当前平台支持调用通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等开源模型，以及部分闭源增强模型（如 qwen-max、qwen-plus）。应用层功能包括知识库问答、工作流编排、Agent 能力封装等，具体模型列表与能力矩阵请参考 [开始使用](../../raw/application-user-guide/start-using.md) 中的“可用模型”章节。> **注意**：文档中提及的“0代码构建问答应用”链接指向外部帮助中心页面，其功能范围可能滞后于控制台实际能力；建议以控制台「应用市场」实时模型列表为准。

## 关键参数

调用模型时需指定 `model`（必填，如 `qwen-max`）、`input`（结构化输入，含 `messages` 或 `prompt` 字段）和 `parameters`（可选，含 `temperature`、`top_p`、`max_tokens` 等）。`stream` 参数控制流式响应，默认为 `false`。所有参数语义与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)保持一致，详细说明见 [开始使用](../../raw/application-user-guide/start-using.md) 的“API 请求格式”小节。

## 使用方式

- **控制台方式**：登录百炼控制台 → 创建应用 → 选择模型 → 配置提示词与参数 → 在调试面板发起测试请求  
- **API 方式**：使用 `POST /v1/services/aigc/text-generation/generation` 接口，携带 `Authorization: Bearer <api_key>` 请求头。SDK 支持 Python/Java/Go，初始化示例见官方 SDK 文档  
- **嵌入式集成**：通过 iframe 或 Web Component 加载预置组件（如知识库问答弹窗），需传入 `app_id` 与 `access_token`，配置细节参见 [开始使用](../../raw/application-user-guide/start-using.md)

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 32 轮对话历史，总 token 数受所选模型上下文长度限制（如 qwen-max 为 32768）  
- 免费额度仅限新用户首月，超出后按用量计费；API 调用频率默认限流 10 QPS（可提工单申请提升）  
- 知识库问答类应用不支持直接上传 `.xlsx` 文件，仅接受 `.txt`、`.md`、`.pdf`、`.docx` 格式，该限制在 [开始使用](../../raw/application-user-guide/start-using.md) 中未明确说明，需以控制台上传界面提示为准

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


