# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音分析、数据挖掘、UI 自动化、深度搜索、法律推理、金融分析等垂直场景。例如，[官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md) 基于多模态理解与数学推理链，[官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 集成语音转写、摘要与意图识别三阶段 pipeline，[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 则依赖视觉定位 + 操作规划双模型协同。

> **注意**：部分文档中提及的“支持 Qwen1.5 系列模型”已过时；当前所有上架应用均要求最低运行环境为 Qwen2 或更高版本，详见 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 的 runtime 兼容性说明。

## 关键参数

调用任一应用时，需传入以下通用参数：
- `app_id`：应用唯一标识（可在控制台应用详情页获取）；
- `input`：JSON 格式输入，结构由具体应用定义（如 `edu-tutor.md` 要求 `{"image_url": "...", "question": "..."}`）；
- `parameters`（可选）：用于覆盖应用默认配置，常见字段包括 `temperature`（0.0–1.0）、`max_output_tokens`、`enable_citation`（是否返回引用来源）等；
- `stream`（布尔值）：启用流式响应需显式设为 `true`，否则返回完整结果。

## 使用方式

1. **控制台接入**：进入「应用广场」页面，点击目标应用 → 「立即使用」→ 配置参数并测试；
2. **API 调用**：向 `POST /v1/applications/{app_id}/chat` 发送请求（需携带 `Authorization: Bearer <api_key>`）；
3. **SDK 调用**：Python SDK 示例：`client.applications.chat(app_id="xxx", input=..., parameters={...})`。

所有应用均遵循统一鉴权与限流策略，详细接口规范见 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的 API 参考章节。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 10 MB（含图像、音频等二进制 base64 内容）；
- 流式响应下不支持 `enable_citation: true`，该参数仅在非流式模式生效；
- 应用间**不共享上下文**，连续对话需由调用方维护 `session_id` 并透传；
- 非官方应用（如用户自建并发布至广场的应用）未经过平台安全扫描，建议仅在可信团队内使用；
- 部分应用（如 [通义法睿](../../raw/application-user-guide/application-gallery/tongyi-farui.md)）对输入文本长度有额外限制（≤ 8192 tokens），超出将被截断且不报错。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


