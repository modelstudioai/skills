# 模型直调与应用调用对比

百炼平台对外提供两类 API 调用路径：**模型直调**（直接调用 Qwen 等文本生成模型）与**应用调用**（调用在控制台预先编排好的智能体、工作流、Agent 2.0 应用）。两者底层都走 DashScope 网关并复用同一套 [API Key](../concepts/api-key.md)，但在调用对象、输入格式、能力范围与典型场景上有显著差异。本页面向做技术选型的开发者，按关键维度对比两种方案，帮助快速判断应走哪条路径。

## 关键维度对比

| 维度 | 模型直调（Qwen API） | 应用调用（Application API） |
| --- | --- | --- |
| 调用对象 | 单个文本生成模型（`model` 字段指定 Qwen 系列模型名） | 控制台已编排好的应用（智能体 / 工作流 / Agent 2.0），由 `APP_ID` 标识 |
| 核心入口 | OpenAI 兼容 Chat Completions / Responses、Anthropic 兼容 Messages、DashScope 原生 | OpenAI 兼容 Responses API（`/apps/agent/{APP_ID}/compatible-mode/v1/responses`）、DashScope 原生 API（`/apps/{APP_ID}/completion`） |
| 前置准备 | [API Key](../concepts/api-key.md)（`DASHSCOPE_API_KEY`） | [API Key](../concepts/api-key.md) + 应用 ID（`APP_ID`，控制台手动获取；子[业务空间](../concepts/workspace.md)还需 `Workspace ID`） |
| 输入格式 | `messages` 数组（OpenAI/Anthropic 兼容）或 Responses 的 `input`；需自行维护对话历史（Responses 接口除外） | `input.prompt` 字符串 / `input` 消息数组（OpenAI 兼容）；`input.prompt` + `parameters` + `biz_params`（DashScope 原生） |
| 对话历史 | 仅 OpenAI 兼容 Responses 由平台自动管理；其余接口调用方自行拼接 `messages` | 支持 `session_id`（云端托管，1 小时有效、最多 50 轮）或自行管理 `messages`；同时传两者时以 `messages` 为准 |
| 内置工具能力 | 联网搜索、代码解释器、网页内容提取仅 Responses 接口内置；其他接口需自行定义工具 | 应用编排阶段在控制台绑定插件 / 节点，调用时通过 `biz_params.user_defined_params` 透传业务参数，工具由应用内部装配 |
| 支持模型 | Qwen 全系列（含 VL 多模态），按 `model` 字段切换 | 由应用编排时所选模型决定（如智能体做图像输入需选 Qwen-VL 并设「自定义处理」） |
| [流式输出](../concepts/streaming-output.md) | 各接口均支持 `stream` 参数 | 同步调用支持 `stream=True`；[异步调用](../concepts/async-invocation.md)暂不支持流式；工作流需在输出节点启用「[流式输出](../concepts/streaming-output.md)」并重新发布 |
| 异步执行 | 由调用方自行实现 | OpenAI 兼容 Responses 支持 `background=True`，返回任务 ID 后轮询 `retrieve` 至终态 |
| 多模态 | 各接口按协议支持文本 / 图像 / 文件（`input_image` / `input_file`） | `input` 消息数组支持 `input_text` / `input_image` / `input_file`（`input_file` 仅[智能体应用](../concepts/agent-application.md)支持） |
| 计费方式 | 按 token 用量计费（输入 + 输出） | 按 token 用量计费；应用编排内部多步调用累计计费 |
| 功能完整度 | DashScope 原生接口参数最全；兼容接口为保证协议一致可能不暴露全部原生参数 | DashScope 原生 `/completion` 功能更全、性能更高；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)便于复用 OpenAI 生态 |
| 典型场景 | 单模型推理、文本生成、对话补全、从 OpenAI/Anthropic 平迁、需要精细采样参数 | 复用已编排的多步骤智能体 / 工作流、内置 RAG 与插件、长耗时异步任务、业务系统集成 |

## 选型建议

- **选模型直调**：当你只需要一个模型做单轮或多轮文本生成、补全、对话，且希望直接复用 OpenAI / Anthropic SDK 与既有代码库，或需要最全的采样参数与原生能力时。从外部平台迁入时优先评估兼容接口，需要极致功能时再切到 DashScope 原生接口。
- **选应用调用**：当业务逻辑已被编排成智能体或工作流（含 RAG、插件、多节点流程），希望把整套能力一次性集成进业务系统，而不是在调用方重新实现编排逻辑时。长耗时任务（报告生成、多步工具调用）选异步 `background=True`；需要复用 OpenAI 工具链选 Responses API，需要更全功能与更高性能选 DashScope 原生 `/completion`。
- **混合使用**：两者共用同一 `DASHSCOPE_API_KEY`，可在同一业务系统中并存——轻量推理走模型直调，复杂编排走应用调用，按场景而非按模型选路径。

## 注意事项

- **凭证管理**：API Key 推荐写入 `DASHSCOPE_API_KEY` 环境变量，不要在生产环境硬编码。
- **应用 ID 获取**：`APP_ID` 与 `Workspace ID` 目前只能在控制台手动复制，不支持 API / CLI 查询；RAM 子账号默认只能查看其已加入的[业务空间](../concepts/workspace.md)。
- **地域差异**：上述 Endpoint 默认适用于华北2（北京）；德国（法兰克福）、新加坡、日本（东京）等地域或调用子[业务空间](../concepts/workspace.md)下应用时，请求须包含 `Workspace ID`，且该 ID 是对应地域 Base URL 的组成部分。
- **兼容接口的功能取舍**：OpenAI / Anthropic 兼容接口为保证协议一致性，可能不暴露百炼原生全部参数；如需最全参数、插件或业务字段，应改用 DashScope 原生接口。
- **迁移评估**：从 OpenAI / Anthropic 迁移到模型直调时，先确认目标 Qwen 模型在对应兼容接口下是否支持所需参数（`temperature`、`tools`、`stream` 等）；迁移到应用调用时，注意异步不支持流式、多轮历史需自行管理（除非用 `session_id`）。

## 被对比主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


