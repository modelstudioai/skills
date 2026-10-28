# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态能力封装。所有应用均基于平台统一的 Runtime 执行环境部署，支持快速集成、参数化配置与轻量定制。开发者可通过控制台或 OpenAPI 直接调用，无需从零构建底层模型链路。

## 支持的模型与功能

应用广场中的每个应用均已绑定适配的底层模型（如 Qwen-VL、Qwen-Audio、Qwen2.5-72B 等）及配套工具集，覆盖教育辅导、语音分析、数据挖掘、UI 自动化、深度搜索、法律推理、金融分析等垂直场景。例如，[官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md) 基于多模态理解模型实现图像到解题步骤的端到端生成；[通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 依赖视觉定位+动作规划双模块协同完成跨应用界面操作；[通义法睿](../../raw/raw/application-user-guide/application-gallery/tongyi-farui.md) 则集成法律知识图谱与判例检索增强机制。> **注意**：部分文档中提及的“Qwen1.5-7B”模型引用已过时，当前所有上线应用实际运行于 Qwen2 系列及以上版本，详见 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 的 runtime 版本说明。

## 关键参数

各应用对外暴露标准化输入参数，主要包括：
- `input`：主输入内容（文本、base64 图片、音频 URL 或结构化 JSON）
- `parameters`：可选配置项，如 `max_steps`（Agent 最大执行步数）、`enable_citation`（是否返回引用来源）、`language`（目标语言，仅多语言类应用支持）
- `tools`：显式指定启用的工具子集（如 `web_search`, `doc_retrieval`, `code_executor`），未声明则使用默认工具集  
参数格式与校验逻辑严格遵循 OpenAPI 3.0 Schema，具体字段定义以各应用详情页为准。

## 使用方式

1. **控制台调用**：进入「应用广场」页面，点击目标应用 → 「在线调试」填写参数 → 执行  
2. **API 调用**：使用 `POST /v1/applications/{app_id}/invoke` 接口，`app_id` 可在应用详情页 URL 或列表响应中获取（如 `edu-tutor`, `tongyi-farui`）  
3. **嵌入集成**：通过 SDK 初始化 `ApplicationClient` 实例，调用 `.invoke()` 方法传入参数字典（Python/Java/Go SDK 均支持）  
所有方式共享同一鉴权体系（AccessKey + Sign v4），无需额外配置模型 endpoint。

## 限制和注意事项

- 单次请求最大输入长度为 128KB（含图片/音频 base64 编码后体积），超限将返回 `413 Payload Too Large`  
- 免费试用应用有调用频次限制（默认 5 QPS，100 次/日），商用需开通对应应用的计费套餐  
- 音频类应用（如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)）仅接受 MP3/WAV 格式，采样率须为 16kHz 或 44.1kHz  
- 多模态应用（如 [官方应用-多模态交互开发套件](../../raw/application-user-guide/application-gallery/multimodal-products.md)）暂不支持视频流式输入，需上传完整文件  
- 应用间**不可共享 session 状态**，连续多轮交互需由客户端自行维护 history 并通过 `conversation_id` 显式传递

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


