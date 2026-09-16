# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和[多模态能力](../concepts/multi-modal.md)封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音内容结构化；
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen-Plus 与实时搜索插件，提供带来源引用的回答。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入格式、输出 Schema、支持的文件类型）请查阅其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tingwu-agent`, `ui-agent`），可在控制台或 [应用广场](../../raw/application-user-guide/application-gallery.md) 文档中查得；
- `input`：JSON 对象，结构依应用而异（如 `tingwu-agent` 接受 `audio_url` 或 `base64_audio`，`ui-agent` 要求 `screenshot` + `instruction`）；
- `parameters`（可选）：覆盖默认推理配置，如 `temperature`、`max_output_tokens`，但部分应用（如 `tongyi-farui`）锁定核心参数以保障法律推理一致性。

> **注意**：`web-search-agent` 的 `enable_web_search` 参数在 [官方应用-千问联网检索Agent](../../raw/application-user-guide/application-gallery/web-search-agent.md) 中为必填布尔值，而旧版文档曾允许省略，默认为 `true`；当前 API 严格校验该字段，以避免非预期的网络请求。

## 使用方式

1. **控制台调用**：进入「应用广场」页，选择目标应用 → 「调试」→ 填写 input → 执行；
2. **API 调用**：使用 `POST /v1/applications/{app_id}/invoke`，Header 需含 `Authorization: Bearer <api_key>`；
3. **SDK 集成**：Python SDK 示例：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client("<access_key_id>", "<access_key_secret>", "cn-beijing")
   response = client.invoke_application("ui-agent", input={"screenshot": "...", "instruction": "点击登录按钮"})
   ```

## 限制和注意事项

- 所有应用共享账户级 QPS 与并发限制，具体配额见控制台「配额管理」；
- 输入内容长度、文件大小、超时时间（默认 120s）等硬性约束因应用而异，例如 `tongyi-docmining` 单次最多处理 50 页 PDF，详见对应子文档；
- 应用间**不共享上下文**：连续多次调用同一 `app_id` 不构成会话，如需状态保持，须由上层业务自行维护 session ID 并传入 `parameters.session_id`（仅部分应用支持，如 `lingque-ccai-voice-dialogue-robot`）；
- `multimodal-products`（多模态交互开发套件）已整合进新版 `ui-agent`，原链接 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 文档处于归档状态，建议优先使用 `ui-agent`。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


