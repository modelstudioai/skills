# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需自行部署模型或编写复杂推理逻辑。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型能力与业务逻辑，例如：
- `通义拍照解题辅导` 基于 Qwen-VL 多模态模型实现图像理解与数学推理；
- `通义听悟Agent` 依赖 Qwen-Audio 模型完成语音转写、摘要与意图识别；
- `千问联网检索Agent` 集成 Qwen2.5 + RAG 检索增强框架，支持实时网页内容获取与整合。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入输出格式、支持的文件类型）请参考其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 中明确列出了 MP3/WAV 输入限制与最大时长约束。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tongyi-farui` 或 `web-search-agent`），可在控制台应用详情页获取；
- `input`：JSON 对象，结构因应用而异（如 `ui-agent` 要求传入截图 base64 与自然语言指令）；
- `timeout`：可选，单位秒，默认 60，最大支持 300（部分长任务应用如 `tongyi-deepsearch` 建议设为 180+）。

> **注意**：部分文档中提及的 `model_version` 参数在当前 v3.2 API 中已废弃，实际调用时忽略该字段；以 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的最新接口定义为准。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即体验」获取 `app_id` 与示例请求；
2. 通过 `/v3/applications/{app_id}/invoke` 接口发起 POST 请求（需携带 `Authorization: Bearer <api_key>`）；
3. 开发者亦可基于 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 提供的 SDK 快速构建自定义前端界面。

## 限制和注意事项

- 所有应用共享账户级 QPS 与并发配额，超出后返回 `429 Too Many Requests`；
- 非白名单应用（如 `quanmiao-light-application-series`）仅对特定行业客户开放，调用前需确认权限；
- 输入文本长度上限为 32768 字符，图片尺寸建议 ≤ 2048×2048 像素（超限将被自动缩放，可能影响 `xiyan-gbi` 等分析类应用精度）；
- `lingque-ccai-voice-dialogue-robot` 当前仅支持中文语音输入，英文语音将触发静音失败（该限制未在 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md) 中明确说明，属已知行为差异）。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


