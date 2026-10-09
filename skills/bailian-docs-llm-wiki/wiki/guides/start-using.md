# start using

`start using` 是百炼平台的入门引导模块，帮助开发者快速初始化应用、接入模型服务并构建基础 AI 功能。它不提供独立 API，而是通过控制台向导、SDK 初始化或低代码组件配置触发后续流程。所有操作均需先完成项目创建与身份鉴权。

## 支持的模型/功能

当前支持调用以下模型类型：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态）、Qwen-Audio（语音），以及部分第三方模型（如 Llama-3-8B-Instruct，需单独开通权限）。功能覆盖文本生成、知识库问答、多轮对话、RAG 检索增强、结构化输出（JSON Schema）等。完整能力列表见 [开始使用](../../raw/application-user-guide/start-using.md) 的子页面导航。

## 关键参数

初始化时需显式指定 `model`（必填）、`temperature`（默认 0.8）、`max_tokens`（默认 2048）、`top_p`（默认 0.95）。若启用流式响应，须设置 `stream: true` 并处理 `text/event-stream` 格式；启用 JSON Schema 输出需同时传入 `response_format: { "type": "json_object" }` 和 `tools` 定义。详细参数说明请参考 [开始使用](../../raw/application-user-guide/start-using.md) 中的“参数速查表”章节（该表位于其子文档 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的附录部分）。

## 使用方式

有三种主流接入路径：  
- **控制台向导**：进入「应用」→「新建应用」→ 选择模板（如「知识库问答」），按提示上传文档、配置检索策略，系统自动生成可部署 endpoint；  
- **SDK 初始化**：使用 `dashscope` Python SDK 或 `@alibabacloud/pop-core` Node.js SDK，调用 `Generation.call()` 或 `ChatCompletion.create()`，传入 `api_key` 与 `model`；  
- **低代码集成**：嵌入 `@alibabacloud/bailian-ui` 组件库中的 `<BaiLianChat />`，通过 `appId` 和 `apiKey` 属性连接后端服务。  
全部流程依赖 [开始使用](../../raw/application-user-guide/start-using.md) 提供的交互式指引，建议首次使用时优先走通控制台路径以验证环境。

## 限制和注意事项

- 免费试用额度为 1000 次 Qwen1.5-7B 调用/月，超出后自动转为按量计费；  
- 单次请求 `input` 长度上限为 32768 tokens（Qwen2.5-72B 为 8192 tokens），超长文本需预切分；  
- 知识库问答场景下，若未在控制台开启「自动 chunk 优化」，则原始文档需手动分块且每块 ≤ 2000 字符，否则影响召回率；  
> **注意**：[开始使用](../../raw/application-user-guide/start-using.md) 中提及的「零代码部署」功能在 v2.3.0 后已更名为「低代码构建」，且要求知识库至少包含 3 个有效文档才能启用自动测试；旧版文档中描述的「一键发布」按钮实际已被移至「部署」页签，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的更新说明。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


