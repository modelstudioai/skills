# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 应用能力，涵盖教育、音视频、多模态、金融、法律、客服、数据挖掘、搜索等多个垂直场景。所有应用均基于百炼托管模型构建，支持一键部署、参数微调与 API 集成。开发者可通过控制台或 OpenAPI 快速接入，无需从零训练模型。

## 支持的模型/功能

应用广场中的每个应用均绑定特定模型栈与功能模块，例如：
- 通义拍照解题辅导依赖 `qwen-vl-plus` 多模态理解能力与 OCR 后处理链路；
- 通义听悟Agent 基于 `qwen-audio` 实现语音转写、摘要与意图识别；
- 通义 UI Agent 使用 `qwen2.5-vl` + 自研 UI 解析器完成跨平台界面操作；
- 通义法睿、析言GBI 等专业应用则集成领域知识图谱与 RAG 检索增强模块。

完整应用列表及对应能力说明见 [应用广场](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

各应用在部署时支持以下通用参数（部分应用额外提供领域专属参数）：
- `temperature`: 控制生成随机性，范围 `[0.0, 1.0]`，默认 `0.3`；
- `max_tokens`: 输出最大 token 数，上限因应用而异（如通义听悟Agent 默认 `2048`，UI Agent 默认 `4096`）；
- `enable_search`: 布尔值，启用联网检索（仅限标注“支持深度搜索”的应用，如 [通义深度搜索](../../raw/application-user-guide/application-gallery.md) 和 [千问联网检索Agent](../../raw/application-user-guide/application-gallery.md)）；
- `top_k`: RAG 检索返回文档数，默认 `3`，最大 `10`。

> **注意**：`enable_search` 参数在 [通义数据挖掘](../../raw/application-user-guide/application-gallery.md) 文档中被错误描述为 `search_enabled`，实际 API 字段名统一为 `enable_search`，请以 OpenAPI Schema 为准。

## 使用方式

1. **控制台接入**：登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即使用」→ 配置参数并部署；
2. **API 调用**：调用 `/v1/applications/{app_id}/chat` 接口，请求体需包含 `messages` 和 `parameters` 字段（参考 [应用广场](../../raw/application-user-guide/application-gallery.md) 中各应用的示例请求）；
3. **SDK 集成**：使用 `dashscope` Python SDK 时，通过 `ApplicationClient(app_id=...)` 初始化，传入 `parameters` 字典即可。

## 限制和注意事项

- 所有应用均受百炼平台配额体系约束（QPS、并发数、总 token 消耗），具体限额见控制台「配额管理」；
- 非官方应用（如用户自建应用）不可发布至应用广场，仅支持内部共享；
- 多模态类应用（如通义音频播客生成、通义多模态翻译）输入文件大小上限为 `100 MB`，且仅支持指定格式（如 `.mp3`, `.mp4`, `.pdf`, `.jpg`）；
- 伶鹊CCAI 系列应用（如语音对话机器人、客服对话Agent）当前仅支持中文语音输入，不支持实时流式 ASR；
- 全妙轻应用系列已停止维护，其功能已整合进 [全妙解决方案类产品](../../raw/application-user-guide/application-gallery.md)，旧版 app_id 将于 2024-Q4 下线。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


