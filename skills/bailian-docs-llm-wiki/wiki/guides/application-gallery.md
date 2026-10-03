# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业场景解决方案与技术能力组件。所有应用均基于通义系列大模型构建，支持直接调用、快速集成或二次开发。应用按功能类型分类组织，部分应用需开通对应模型权限后方可使用。

## 支持的模型/功能

应用广场中的应用底层依赖不同通义模型能力，例如：
- 通义法睿、析言GBI 等法律/商业智能类应用主要调用 `qwen-max` 或 `qwen-plus`；
- 通义听悟Agent、伶鹊CCAI 系列语音对话应用依赖 `qwen-audio` 和 `qwen-vl` 多模态模型；
- 通义 UI Agent、千问联网检索Agent 等需启用 `qwen-websearch` 插件能力。

具体模型绑定关系详见 [应用广场](../../raw/application-user-guide/application-gallery.md) 中各子应用链接所指向的文档，例如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 明确声明其音频理解模块强制使用 `qwen-audio-20240910` 版本。

> **注意**：[官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md) 文档中提及的 `qwen-turbo` 调用方式，与当前平台控制台实际可用模型列表（v2024.10）不一致；请以控制台「模型管理」页显示的已授权模型为准，该应用实际运行时将自动降级至 `qwen-plus`。

## 关键参数

调用应用广场中的应用时，通用参数包括：
- `app_id`：应用唯一标识（如 `tingwu-agent-v1`），可在应用详情页或 [应用广场](../../raw/application-user-guide/application-gallery.md) 列表中获取；
- `input`：结构化输入对象，字段因应用而异（如 `audio_url`、`image_base64`、`query`）；
- `stream`：布尔值，控制是否启用流式响应（仅部分应用支持，如 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md)）；
- `timeout`：最大执行时长（单位秒），默认 30s，上限为 300s。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」页面；
2. 选择目标应用，点击「立即体验」或「接入 API」；
3. 若为 API 接入，复制生成的 `app_id` 与鉴权 `API-Key`；
4. 构造 HTTP POST 请求至 `/v1/apps/{app_id}/chat`，`input` 字段需严格遵循对应应用文档定义（参考 [官方应用-通义数据挖掘](../../raw/application-user-guide/application-gallery/tongyi-docmining.md) 的 input schema 示例）；
5. 建议在生产环境配置重试逻辑与错误码处理（如 `429 Too Many Requests` 表示超出应用 QPS 限制）。

## 限制和注意事项

- 所有应用均受账户级配额约束（QPS、总调用量、单次输入长度），具体限额见控制台「配额管理」；
- 部分应用（如 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md)）要求输入文本长度 ≤ 8192 tokens，超长将被截断且不报错；
- 应用间不共享上下文，每次请求均为无状态调用；
- 自定义微调模型不可用于应用广场应用——所有应用仅绑定平台托管模型，此限制在 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md) 的 FAQ 中已明确说明。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


