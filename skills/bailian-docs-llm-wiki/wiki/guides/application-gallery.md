# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业场景解决方案和能力组件。所有应用均基于百炼模型服务构建，支持快速集成、调试与二次开发。开发者可通过控制台直接部署或调用其 API 接口，无需从零训练模型。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与功能模块，例如：
- 通义法睿（`tongyi-farui`）基于法律垂类微调模型，提供合同审查、法规检索等能力；
- 通义 UI Agent（`ui-agent`）依赖多模态理解+代码生成模型，支持截图解析与自动化 UI 操作；
- 伶鹊 CCAI 系列应用（如 [官方应用-伶鹊CCAI-语音对话机器人](../../raw/application-user-guide/application-gallery/official-application-lingque-ccai-voice-dialogue-robot.md)）统一使用 ASR+LLM+TTS 流式 pipeline。

> **注意**：部分应用文档中声明支持“自定义模型替换”，但 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 明确指出其检索增强模块仅兼容 `qwen-max` 和 `qwen-plus`，不支持任意第三方模型接入。

## 关键参数

各应用在 API 调用时需传入以下通用参数（具体以单个应用文档为准）：
- `app_id`：应用唯一标识，可在控制台「应用广场」列表页获取；
- `input`：结构化输入对象，字段因应用而异（如 `image_url` 用于多模态应用，`query` 用于检索类应用）；
- `stream`：布尔值，控制是否启用流式响应（默认 `false`）；
- `timeout`：最大等待时长（单位秒），建议设为 `60` 以上以兼容复杂任务。

部分应用还支持扩展参数，例如 [通义点金](../../raw/application-user-guide/application-gallery/tongyi-dianjin.md) 需额外指定 `industry` 和 `report_type`。

## 使用方式

1. **控制台部署**：登录百炼控制台 → 进入「应用广场」→ 点击目标应用卡片 → 「立即部署」→ 配置环境变量（如 API Key）→ 启动；
2. **API 调用**：部署后获取 `app_id` 与 `api_key`，按 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 中定义的 RESTful 接口规范发起 POST 请求；
3. **SDK 集成**：推荐使用 `dashscope` Python SDK，调用 `Application.call(app_id=..., input={...})` 方法（详见各应用文档的「SDK 示例」章节）。

## 限制和注意事项

- 所有应用默认受百炼平台配额限制（QPS、并发数、单次请求 token 上限），具体阈值见控制台「配额管理」；
- 应用间**不共享上下文状态**，即使同一 `app_id` 的多次调用也视为无状态请求（与 `ChatApp` 类型不同）；
- 多模态应用（如 `multimodal-products`）要求输入图片尺寸 ≤ 2048×2048 像素，且格式仅支持 JPEG/PNG；
- > **注意**：[官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md) 文档中提及的「支持私有化部署」与当前平台实际能力不符——该系列目前仅支持云上托管模式，私有化支持计划于 Q4 发布，届时将同步更新文档。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


