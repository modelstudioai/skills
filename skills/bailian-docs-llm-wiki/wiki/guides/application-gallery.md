# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次定制。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型/功能

应用广场中的每个应用均绑定特定模型栈与功能模块，例如：
- `通义拍照解题辅导` 基于 Qwen-VL 多模态模型实现图像理解与数学推理；
- `通义听悟Agent` 依赖 ASR + LLM + TTS 流式链路，支持会议纪要生成与要点提炼；
- `千问联网检索Agent` 集成 RAG 框架与实时网页抓取能力，需配合 `web_search` 插件启用。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

调用任一应用时，必须传入以下核心参数：
- `app_id`：应用唯一标识（如 `edu-tutor`、`tingwu-agent`），可在控制台「应用广场」页获取；
- `input`：结构化输入对象，字段因应用而异（如 `image_url` 用于拍照解题，`audio_url` 用于听悟）；
- `parameters`（可选）：用于覆盖默认配置，例如 `max_output_tokens`、`temperature`，具体支持项以各应用文档为准。

参数定义与示例请参考 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 中的 `input` schema 说明。

## 使用方式

1. **控制台调用**：进入「应用广场」→ 选择目标应用 → 点击「调试」，填写 input 后执行；
2. **API 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求，需携带 `Authorization: Bearer <api_key>`；
3. **SDK 集成**：使用 `dashscope` Python SDK 时，调用 `Application.invoke(app_id=..., input={...})`。

完整调用流程与错误码说明见 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的「接入指南」章节。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含文本、图片、音频等），超限将返回 `400 Bad Request`；
- 部分应用（如 `伶鹊CCAI-语音对话机器人`）依赖实时语音流，仅支持 WebSocket 接入，不支持 HTTP 同步调用；
- > **注意**：[官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md) 文档中描述的 `session_id` 自动续期机制，与当前 v2.3.1 平台实际行为不一致——现版本要求显式传入有效 `session_id`，否则会话状态无法持久化；
- 所有应用默认启用内容安全过滤，若需关闭需在创建应用实例时显式设置 `enable_safety_check=false`（仅限白名单用户）。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


