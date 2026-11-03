# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和[多模态](../concepts/multi-modal.md)能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化调用与轻量定制。开发者可通过 API 或控制台直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定特定模型栈与功能边界，例如：
- `通义听悟Agent` 依赖 ASR + LLM + TTS 多阶段流水线，专用于会议纪要生成与语音内容结构化；
- `通义 UI Agent` 基于视觉语言模型（VLM）与动作规划模块，支持网页/APP 界面理解与自动化操作；
- `千问联网检索Agent` 集成 Qwen-Plus 与实时搜索插件，提供带来源引用的回答。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。各子应用的技术细节（如输入格式、输出 Schema、支持的文件类型）请查阅其独立文档，例如 [官方应用-通义音频播客生成](../../raw/application-user-guide/application-gallery/official-application-aipodcast.md) 和 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（如 `tongyi-farui`、`web-search-agent`），必须与 [应用广场](../../raw/application-user-guide/application-gallery.md) 中列出的 ID 完全一致；
- `input`：JSON 对象，结构依应用而异（如 `tongyi-dianjin` 要求 `{"query": "...", "industry": "finance"}`，而 `ui-agent` 要求 `{"screenshot": "base64..."}`）；
- `parameters`（可选）：覆盖应用默认配置，常见字段包括 `max_steps`（仅限 Agent 类应用）、`temperature`（LLM 温度值）、`enable_citation`（是否返回引用片段）。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md)）中仍标注 `callback_url` 为必填参数，但自 v2.3.0 起该字段已废弃，实际调用将被忽略——请以最新 SDK 示例为准。

## 使用方式

1. **获取 app_id**：从 [应用广场](../../raw/application-user-guide/application-gallery.md) 列表中确认目标应用 ID；
2. **构造请求体**：按对应子应用文档定义 `input` 结构（如 [通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 要求上传 PDF 并指定 `task_type: "entity_extraction"`）；
3. **发起调用**：使用 `/v1/applications/{app_id}/invoke` 接口（HTTP POST），携带 `Authorization: Bearer <api_key>`；
4. **处理响应**：同步调用返回 JSON；异步任务（如长耗时[多模态](../concepts/multi-modal.md)处理）返回 `task_id`，需轮询 `/v1/tasks/{task_id}` 获取结果。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含 base64 图片、PDF 等二进制内容）；
- `web-search-agent` 和 `tongyi-deepsearch` 默认启用实时网络访问，若在 VPC 环境中使用，需确保工作节点具备公网出口或配置代理；
- 所有应用均不支持跨区域调用（如杭州集群部署的应用不可通过北京 endpoint 调用）；
- 自定义微调模型无法直接挂载至应用广场应用——如需私有化适配，请基于 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 构建自有应用。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


