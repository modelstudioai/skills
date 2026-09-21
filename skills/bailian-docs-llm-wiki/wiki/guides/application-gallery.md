# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、法律、金融、客服、数据处理、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次定制。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型/功能

应用广场中的每个应用均绑定特定模型能力与业务逻辑，例如：
- 通义拍照解题辅导依赖多模态理解（图文识别+数学推理）模型；
- 通义听悟Agent 基于语音识别（ASR）、说话人分离与会议摘要模型；
- 通义法睿 使用法律领域微调的大语言模型与判例检索增强模块；
- 通义 UI Agent 集成视觉理解（VLM）与动作规划模型，支持网页/APP 自动化操作。

具体能力细节请参阅各应用文档，如 [官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md)、[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用应用广场应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用广场」页获取 |
| `input` | object | 是 | 输入数据结构，格式因应用而异（如 `image_url`、`audio_url`、`text` 等） |
| `parameters` | object | 否 | 可选配置项，例如 `max_output_tokens`、`temperature`、`enable_rag` 等 |

> **注意**：部分旧版文档（如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md)）中仍列出已弃用的 `voice_style` 参数，实际应使用 `voice_config` 对象；请以最新 SDK 示例和 API 文档为准。

## 使用方式

1. **控制台调用**：进入百炼控制台 →「应用广场」→ 选择目标应用 → 点击「在线调试」填写输入后执行；
2. **API 调用**：通过 `POST /v1/applications/{app_id}/invoke` 接口发起请求，需携带有效 `Authorization` 头；
3. **SDK 集成**：使用 `BailianClient.invoke_application()` 方法（Python SDK v1.8.0+），示例见 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 文档。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 20 MB（含图片、音频等二进制内容 Base64 编码后长度）；
- 音频类应用（如听悟Agent、语音对话机器人）仅支持 WAV/MP3/AMR 格式，采样率须为 8kHz 或 16kHz；
- 所有应用默认启用流式响应（`stream=true`），若需完整响应请显式设置 `stream=false`；
- 应用权限受项目空间（Project）隔离，跨空间调用需申请授权；
- [官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md) 当前仅支持中文语境下的意图识别与槽位填充，不支持多语言混合输入。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


