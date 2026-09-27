# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、客服、音视频、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一运行时构建，支持快速集成、参数化配置与轻量级定制。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义听悟Agent` 基于 Qwen-Audio 模型，支持语音转写、会议摘要与对话结构化；
- `通义 UI Agent` 依赖 Qwen-VL + Qwen2.5-72B，实现网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen2.5-72B 与实时搜索插件，支持动态知识增强。

所有官方应用的详细能力说明见 [应用广场](../../raw/application-user-guide/application-gallery.md)；各子应用的技术规格（如输入格式、输出 schema、支持的 media 类型）请参阅对应文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)。

## 关键参数

调用任一应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用广场」页获取，如 `tingwu-agent-v1` |
| `input` | object | 是 | 输入数据，结构因应用而异（如 `audio_url`、`text`、`image_base64`） |
| `parameters` | object | 否 | 可选配置项，如 `max_output_tokens`、`temperature`、`enable_search` 等 |

> **注意**：`parameters` 中的 `temperature` 在部分旧版应用（如 `xiyan-gbi`）中已被弃用，实际行为由服务端固定策略控制；最新行为以 [官方应用-析言GBI](../../raw/application-user-guide/application-gallery/xiyan-gbi.md) 文档为准。

## 使用方式

1. **控制台调用**：进入「应用广场」→ 选择目标应用 → 点击「试用」，填写输入并提交；
2. **API 调用**：使用 `POST /v1/applications/{app_id}/invoke` 接口，需携带 `Authorization: Bearer <api_key>`；
3. **SDK 调用**（Python 示例）：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client('<access_key_id>', '<access_key_secret>', '<region>')
   response = client.invoke_application(
       app_id="tingwu-agent-v1",
       input={"audio_url": "https://example.com/audio.mp3"}
   )
   ```

完整接口定义与错误码详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 50 MB（含 base64 编码膨胀），多模态应用（如 `ui-agent`、`multimodal-products`）需特别注意图像/视频尺寸；
- 所有应用默认启用流式响应（`stream=true`），若需完整响应，请显式设置 `stream=false`；
- 免费试用额度仅限控制台交互，API 调用需绑定计费项目并确保配额充足；
- 部分应用（如 `tongyi-farui`、`tongyi-dianjin`）对输入文本长度有领域特定限制（如法条引用不得超过 2000 字符），具体阈值请查阅对应子文档，例如 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


