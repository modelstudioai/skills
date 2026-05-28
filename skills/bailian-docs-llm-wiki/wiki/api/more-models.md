# [[more|more]] models

本页面汇总了百炼平台提供的垂直领域与能力增强型模型，涵盖检索重排序、法律垂域大语言模型及意图解析路由服务。开发者可根据 RAG 架构增强、合规业务问答或 Agent 工具调度等场景，直接调用对应模型的能力接口。所有模型均支持标准鉴权，并可通过 HTTP 或官方 SDK 快速集成至现有系统。

## 支持的模型/功能

| 模型标识 | 核心能力 | 典型场景 | 详情索引 |
|:---|:---|:---|:---|
| `qwen3-rerank`<br>`qwen3-vl-rerank`<br>`gte-rerank-v2` | 文本/多模态相关性重排序。支持跨语言、图像、视频的混合检索打分。 | 搜索引擎召回精排、[[rag]] 知识库切片匹配、向量检索后处理 | [文本排序](../../raw/model-api-reference/[[more|more]]-models/text-rerank-api.md) |
| `farui-plus` | 法律行业垂直大模型。具备法律文书起草、条款审查、类案检索与法理推理能力。 | 企业法务助手、合规审查流水线、法律智能客服 | [通义法睿大语言模型](../../raw/model-api-reference/[[more|more]]-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 百毫秒级意图分类与函数路由。支持纯意图标签输出、仅[[function-calling|函数调用]]或混合模式。 | Agent 意图识别、动态工具分发、对话状态管理 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |

## 关键参数

- **通用鉴权与环境**：所有接口要求 `Authorization: Bearer <DASHSCOPE_API_KEY>`，推荐通过环境变量注入以保障安全（参考 [[api-key-配置]]）。
- **Rerank 参数差异**：
  - `qwen3-rerank`：顶层参数接收 `instruct`（控制排序策略，如 `"Given a web search query..."`）与 `top_n`。
  - `qwen3-vl-rerank` / `gte-rerank-v2`：参数嵌套于 `input` 与 `parameters` 中。多模态查询需使用 `{"text/image/video": "value"}` 结构；视频处理通过 `fps` 控制抽帧比例 `[0, 1]`。
- **法睿模型**：标准 Generation 参数集。最大上下文 12K，输入上限 12K Token，输出上限 2K Token。
- **意图模型**：无独立业务参数，完全依赖 `system` 提示词注入。若需极低延迟，建议将意图字典映射为单字符（如 `"A": "查天气"`），模型将强制输出单 Token。

## 使用方式

- **HTTP 直调**：Rerank 提供两套端点。`qwen3-rerank` 使用兼容路由 `/compatible-api/v1/reranks`，其余模型使用原生路由 `/api/v1/services/rerank/text-rerank/text-rerank`。请求体结构与响应格式（如 `results` 位于顶层或 `output` 内）互不兼容，需按模型严格区分。
- **SDK 调用**：Python SDK (`dashscope`) 对 HTTP 嵌套结构进行了扁平化封装。例如 HTTP 中的 `input.query` 在 SDK 中直接作为顶层 `query` 参数传入。法睿与意图模型推荐使用 `dashscope.Generation.call` 或 OpenAI 兼容客户端，通过维护 `messages` 列表即可实现 [[多轮对话]] 与 [[流式输出]]。
- **响应解析**：意图模型的返回体包含自定义 XML 标签 `<tags>`、`<tool_call>` 与 `<content>`。后端服务需使用正则表达式或 JSON 解析器提取 `tool_call` 数组，进而触发对应业务逻辑。

## 限制和注意事项

- 单次请求总 Token 计算方式为 `Query Tokens × Document 数量 + Document Tokens 总和`，超出模型阈值将自动截断，可能导致排序结果失真。
- `gte-rerank` 已进入下线周期，将于 2026-05-30 停止服务，存量代码建议尽快迁移至 `qwen3-rerank`。
- 意图理解模型的 100 万 Token 免费额度仅在百炼平台开通后 90 天内有效，超时后将恢复标准计费。
- 法睿模型输出上限为 2K Token，长篇幅法律文书生成建议结合流式接口分段接收，或在前置环节进行上下文裁剪。

> **注意**：不同文档在 Rerank 参数层级描述上存在历史差异。若使用 `qwen3-vl-rerank` 或 `gte-rerank-v2`，请勿直接套用 `qwen3-rerank` 的兼容格式参数，否则会触发 `InvalidParameter` 或结构解析失败。同时，HTTP 接口返回的 `code`/`message` 仅在失败时出现，而 SDK 成功响应会额外包裹空的 `code`/`message` 字段，上层逻辑需做好字段判空处理。详细错误码对照请参考 [[错误码排查]]，并发限制请遵循 [[限流策略]]。

## 来源文档

- [文本排序](../../raw/model-api-reference/more-models/text-rerank-api.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)

