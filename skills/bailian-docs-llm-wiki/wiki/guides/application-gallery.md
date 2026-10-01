# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、法律、金融、客服、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼托管模型构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需自行部署底层模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义听悟Agent` 基于 Qwen-Audio 模型，支持语音转写、会议摘要与对话洞察；
- `通义 UI Agent` 依赖 Qwen-VL + Qwen2.5-72B 组合，实现网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen2.5-72B 与实时搜索插件，提供带来源引用的动态问答能力。

完整应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各应用的底层模型版本与能力边界，请同步参考其子页面，如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 和 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md)。

## 关键参数

调用应用广场应用时，需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用广场」页获取 |
| `input` | object | 是 | 输入内容，结构因应用而异（如 `text`、`audio_url`、`image_url` 等） |
| `parameters` | object | 否 | 可选配置项，例如 `max_output_tokens`、`temperature`（仅对支持 LLM 推理的应用生效） |

> **注意**：`parameters` 中的 `temperature` 对 `通义多模态翻译` 等非生成类应用无实际影响；该限制在 [官方应用-通义多模态翻译](../../raw/application-user-guide/application-gallery/official-application-tongyi-translate.md) 文档中未明确说明，但实测无效，建议以 [应用广场](../../raw/application-user-guide/application-gallery.md) 的通用调用规范为准。

## 使用方式

1. **控制台接入**：登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即使用」获取 `app_id` 与示例代码；
2. **API 调用**：向 `POST /v1/apps/{app_id}/chat` 发起请求（需携带 `Authorization: Bearer <api_key>`）；
3. **SDK 调用（Python）**：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client('<access_key_id>', '<access_key_secret>', '<region_id>')
   response = client.chat(app_id='app-xxx', input={'text': '你好'})
   ```

详细接口定义与错误码请查阅 [应用广场](../../raw/application-user-guide/application-gallery.md) 中的「API 参考」章节。

## 限制和注意事项

- 单应用默认 QPS 限流为 5，可通过工单申请提升；
- 音视频类应用（如 `通义听悟Agent`、`通义音频播客生成`）要求输入 URL 可公开访问且响应头含 `Content-Type`；
- 所有应用均不支持跨区域调用（例如华东1区创建的应用不可在华北2区调用），该约束在 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md) 文档中被遗漏，但已在 [应用广场](../../raw/application-user-guide/application-gallery.md) 的「常见问题」中统一说明；
- `全妙轻应用系列` 与 `全妙解决方案类产品` 共享同一套资源配额，不可叠加开通。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


