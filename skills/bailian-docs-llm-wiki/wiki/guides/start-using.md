# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可通过控制台或 API 快速集成大模型能力。本文档梳理核心使用路径、参数规范及约束条件，适用于初次接入的开发者。详细功能演进请参考 [应用功能动态](../../raw/application-user-guide/start-using.md)。

## 支持的模型/功能

- 支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型；
- 提供免代码问答应用构建能力，支持知识库上传、多轮对话配置、RAG 增强等 [0代码构建问答应用](../../raw/application-user-guide/start-using.md) 所述场景；
- 控制台支持应用模板一键部署，API 层支持 `chat`、`completion`、`embedding`、`audio_transcription` 等调用类型。

## 关键参数

- `model`: 必填，模型 ID（如 `qwen-max`、`qwen-plus`、`qwen2.5-7b-instruct`），需与实际部署实例匹配；
- `input.messages`: 对话类请求必填，格式为 `[{ "role": "user", "content": "..." }]`，系统角色（`system`）仅在部分模型支持；
- `parameters.temperature`: 浮点数（0.0–2.0），默认 1.0；`top_p` 默认 1.0，二者不可同时设为极端值（如 `temperature=0` 且 `top_p=0`）；
- `stream`: 布尔值，启用流式响应时需设置为 `true`，此时响应体为 SSE 格式——该行为与 [应用功能动态](../../raw/application-user-guide/start-using.md) 中 2024 年 Q3 的流式协议升级一致。

## 使用方式

1. **控制台快速启动**：登录百炼控制台 → 创建应用 → 选择模板（如“知识库问答”）→ 上传文档 → 发布应用；
2. **API 调用**：
   - 获取 `API Key`（控制台「API 密钥管理」）；
   - 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本生成）或对应服务端点；
   - 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
3. **SDK 集成**：推荐使用官方 Python/Java SDK（`dashscope` 包），自动处理鉴权、重试与流式解析。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限依模型而异（如 `qwen-max` 为 32768，`qwen-plus` 为 8192），超限将返回 `400 Bad Request`；
- 免费额度仅限新用户首月，后续按用量计费；知识库上传文件单个 ≤ 100 MB，格式限 PDF/DOCX/TXT/MD/CSV；
- > **注意**：原始文档中链接 [0代码构建问答应用](../../raw/application-user-guide/start-using.md) 指向阿里云帮助中心外部页面，其内容可能滞后于百炼控制台最新 UI（例如当前已移除“应用市场”入口，统一归入“模板中心”）；
- > **注意**：`system` 角色在 `qwen2.5-7b-instruct` 及更高版本中已全面支持，但 `qwen-plus` 仍不支持——该差异未在 [应用功能动态](../../raw/application-user-guide/start-using.md) 中明确说明，建议以模型文档为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


