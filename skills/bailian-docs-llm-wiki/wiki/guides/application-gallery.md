# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、[多模态](../concepts/multimodal.md)交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需自行部署模型或编写底层推理逻辑。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义听悟Agent` 基于 Qwen-Audio 模型，支持语音转写、会议摘要与发言分析；
- `通义 UI Agent` 依赖 Qwen-VL + Qwen2.5-72B，实现网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen2.5-72B 与实时搜索引擎插件，提供动态知识增强问答。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入格式、输出 Schema、支持的文件类型）请参考其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tingwu-agent`, `farui`），可在控制台应用详情页获取；
- `input`：JSON 对象，结构依应用而异（如 `tingwu-agent` 要求 `audio_url` 字段，`ui-agent` 要求 `screenshot_base64` + `task_description`）；
- `parameters`（可选）：用于覆盖应用默认配置，如 `temperature`、`max_output_tokens`，但**并非所有应用均支持参数覆盖**——具体支持项以各应用文档为准。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）仍列出已废弃的 `stream` 参数，实际调用中该参数已被忽略，应以最新 SDK 文档为准。

## 使用方式

1. **控制台方式**：登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「在线调试」填写 input 并执行；
2. **API 方式**：调用 `POST /v1/applications/{app_id}/invoke`，Header 中携带 `Authorization: Bearer <api_key>`；
3. **SDK 方式**：使用 `dashscope` Python SDK（≥1.20.0）：
   ```python
   from dashscope import Application
   resp = Application.call(app_id='tingwu-agent', input={'audio_url': '...'}, api_key='...')
   ```

完整调用示例与错误码说明见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含 base64 编码后的图像/音频）；
- 部分应用（如 `通义深度搜索`、`千问联网检索Agent`）依赖外部服务，可能出现临时不可用，建议添加重试与降级逻辑；
- 应用 ID 区分大小写，且不支持自定义别名；若在文档中看到形如 `web-search-agent` 的 ID，不可写作 `websearchagent` 或 `WebSearchAgent`；
- 所有应用均遵循百炼平台统一配额管理，超出后返回 `429 Too Many Requests`，具体配额策略参见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


