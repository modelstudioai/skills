# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，支持快速集成与二次开发。所有应用均基于百炼统一模型服务底座构建，具备标准化 API 接口和可配置参数。开发者可通过控制台或 OpenAPI 直接调用，无需自行部署模型或编写底层推理逻辑。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型能力与业务场景，例如：
- `通义听悟Agent` 基于语音识别（ASR）+ 语义理解（NLU）+ 对话生成（LLM）多阶段流水线；
- `通义 UI Agent` 依赖多模态理解（VLM）与代码生成模型协同完成界面操作；
- `千问联网检索Agent` 集成 Qwen-72B + RAG 检索增强模块，支持实时网页内容获取。

所有应用能力均源自平台已上线的[原文标题](../../raw/application-user-guide/application-gallery.md)，其功能边界与模型选型以该文档所列清单为准。

## 关键参数

各应用通过 `app_id` 标识唯一实例，调用时需传入以下通用参数：
- `app_id`：必填，从应用广场控制台获取（如 `tingwu-agent-v1`）；
- `input`：JSON 对象，结构依应用而异（如 `audio_url` 用于听悟Agent，`screenshot_base64` 用于 UI Agent）；
- `parameters`：可选，用于覆盖默认配置（如 `max_search_results: 5` 适用于 `web-search-agent`）。

参数定义与校验规则详见各子应用文档，例如 `通义数据挖掘` 的字段映射规则见[原文标题](../../raw/application-user-guide/application-gallery/tongyi-docmining.md)；`伶鹊CCAI-对话分析AIO` 的会话格式要求见[原文标题](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-dialogue-analysis-aio.md)。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即使用」获取 `app_id`；
2. 调用 `/v1/applications/{app_id}/invoke` 接口（POST），携带 `input` 和 `parameters`；
3. 响应体为标准 JSON，含 `output` 字段（结构化结果）与 `trace_id`（用于问题排查）。

> **注意**：部分旧版文档（如 `quanmiao-light-application-series.md`）中提及的 `sync_mode=true` 参数已被弃用，当前所有应用默认异步执行，需轮询 `GET /v1/tasks/{task_id}` 获取结果 —— 请以最新 OpenAPI 文档为准。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 10 MB（含 base64 编码图像/音频）；
- `web-search-agent` 默认禁用 JavaScript 渲染，不支持动态加载内容；
- 所有应用均不支持跨区域调用（如华东 region 创建的应用仅可在华东 endpoint 调用）；
- 应用权限继承自当前账号的模型调用配额，超出将返回 `429 Too Many Requests`。

如遇模型响应异常或功能不符预期，请优先核对所用 `app_id` 是否与[原文标题](../../raw/application-user-guide/application-gallery.md)中列出的官方应用标识完全一致。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


