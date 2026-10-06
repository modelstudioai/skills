# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、音视频、客服、法律、金融、数据挖掘、多模态交互等多个垂直场景。所有应用均基于百炼统一模型服务底座构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需从零训练模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型能力与业务逻辑，例如：
- `通义听悟Agent` 基于语音识别（ASR）+ 语义理解（NLU）+ 对话生成（LLM）三阶段流水线；
- `通义 UI Agent` 依赖多模态视觉理解（Qwen-VL）与动作规划模型协同；
- `千问联网检索Agent` 集成 RAG 框架与实时网页抓取模块，支持动态知识注入。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入输出 Schema、支持的文件类型、调用链路图）请参考其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tongyi-farui`），可在控制台「应用广场」页面获取；
- `input`：JSON 格式，结构由具体应用定义（如 `xiyan-gbi` 要求 `{"query": "...", "tables": [...]}`）；
- `timeout`：最大执行时长（单位：秒），默认 60，部分长任务应用（如 `tongyi-deepsearch`）建议设为 120+；
- `stream`：布尔值，仅部分应用（如 `lingque-ccai-voice-dialogue-robot`）支持流式响应。

> **注意**：`web-search-agent` 的 `input.query` 字段在 [千问联网检索Agent](../../raw/application-user-guide/application-gallery/web-search-agent.md) 中要求为纯文本，但旧版文档曾允许传入 HTML 片段——该用法已废弃，以当前 SDK 示例为准。

## 使用方式

1. **控制台接入**：进入百炼控制台 → 应用广场 → 选择目标应用 → 点击「调试」或「API 接入」，复制 `app_id` 与示例请求体；
2. **API 调用**：向 `POST /v1/applications/{app_id}/invoke` 发送请求（需携带 `Authorization: Bearer <api_key>`）；
3. **SDK 调用**：使用 `alibabacloud_bailian20231219` SDK，调用 `InvokeApplicationRequest` 方法（Python 示例见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)）。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含 base64 编码图像/音频）；
- 免费试用额度按应用独立计算，超出后按 [应用广场](../../raw/application-user-guide/application-gallery.md) 中公示的计费规则扣费；
- `tongyi-dianjin` 与 `xiyan-gbi` 当前不支持自定义模型替换，仅限使用平台指定版本；
- 所有应用均**不支持跨区域调用**（如华东1区创建的应用不可通过华北2区 endpoint 访问）。

> **注意**：`quanmiao-light-application-series` 文档中提及“支持私有化部署”，但该能力尚未对公测用户开放；实际部署权限需联系客户成功团队确认，以 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md) 最新修订版为准。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


