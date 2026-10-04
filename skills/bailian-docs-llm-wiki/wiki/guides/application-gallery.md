# application gallery

应用广场是百炼平台提供的预置能力集合，面向开发者提供开箱即用的行业级 Agent 应用与多模态工具链，可直接调用或作为模板快速二次开发。所有应用均经过平台统一接入验证，支持标准 API 调用与低代码配置。当前版本聚焦教育、音视频、客服、金融、法律、数据智能等垂直场景，覆盖文本、语音、图像、表格等多模态交互需求。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与功能模块，例如：
- `通义听悟Agent` 基于 Qwen-Audio 模型，支持语音转写、会议摘要与发言角色分离；
- `通义 UI Agent` 依赖 Qwen-VL 与 Qwen2.5-72B，实现网页截图理解、操作意图识别与自动化点击；
- `千问联网检索Agent` 集成 Qwen2.5-72B + 自研检索增强模块，支持实时网络结果融合生成。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入格式、输出 Schema、支持的 media type）请参考其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需在请求体中指定以下必选参数：
- `application_id`: 应用唯一标识（如 `tingwu-agent`, `ui-agent`），取值必须来自 [应用广场](../../raw/application-user-guide/application-gallery.md) 中列出的 ID；
- `input`: 结构化输入对象，字段依应用而异（如 `audio_url` 用于听悟Agent，`screenshot_base64` 用于 UI Agent）；
- `parameters`: 可选 JSON 对象，用于控制行为（如 `max_output_tokens`, `enable_citation`, `language`）。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）仍标注 `model_name` 为必需参数，但自 v2.3.0 起该字段已废弃，实际以 `application_id` 绑定模型，忽略 `model_name`。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」页，复制目标应用的 `application_id`；
2. 调用 `/v1/applications/{application_id}/invoke` 接口（HTTP POST），携带认证 Header（`Authorization: Bearer <api_key>`）；
3. 请求体示例（以 `web-search-agent` 为例）：
   ```json
   {
     "input": {"query": "2024年Q2中国新能源汽车出口量"},
     "parameters": {"max_results": 5, "enable_citation": true}
   }
   ```
详细接口规范与 SDK 示例见 [应用广场](../../raw/application-user-guide/application-gallery.md) 所引各子文档。

## 限制和注意事项

- 单次调用最大输入长度：文本类应用 ≤ 32k tokens，多模态应用（如 UI Agent）单张截图分辨率上限为 1920×1080；
- 免费试用额度仅适用于首次部署的前 3 个应用实例，超出后需绑定计费项目；
- `通义深度搜索` 与 `千问联网检索Agent` 均依赖外部网络访问，若企业 VPC 未放行 `*.bailian.aliyuncs.com` 及搜索引擎域名，将返回 `NETWORK_UNREACHABLE` 错误；
- 所有应用不支持跨 Region 调用，`application_id` 仅在其部署地域内有效（如杭州地域创建的 `xiyan-gbi` 无法在北京地域调用）。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


