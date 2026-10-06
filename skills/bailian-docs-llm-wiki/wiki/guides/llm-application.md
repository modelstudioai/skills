# llm application

`llm application` 是百炼平台提供的核心应用构建能力，用于将大语言模型能力封装为可部署、可调用的服务。它支持从低代码智能体到高代码自定义逻辑的多种应用形态，适用于对话交互、流程编排、文档理解等典型场景。开发者可通过控制台或 OpenAPI 快速创建、调试和发布应用。

## 支持的模型与功能

当前 `llm application` 支持接入平台托管的全部 LLM 模型（如 Qwen 系列、Qwen2、Qwen3、Qwen-VL 等），并提供以下应用类型：  
- 新版智能体应用（Agent 2.0）：支持多工具动态调用、记忆管理与自主规划，详见 [新版智能体应用（Agent 2.0）](raw/application-user-guide/llm-application/new-single-agent-application.md)；  
- 智能体应用（Agent 1.0）：基于固定工具集的轻量级 Agent，已进入维护模式；  
- 工作流应用：通过可视化节点编排实现条件分支、循环、[函数调用](../concepts/function-calling.md)等复杂逻辑，参考 [工作流应用](raw/application-user-guide/llm-application/workflow-application.md)；  
- 高代码应用：允许上传 Python 代码并直接调用 SDK，适合深度定制，见 [高代码应用](raw/application-user-guide/llm-application/rich-code-application.md)；  
- 文件问答：专用于 PDF/Word/Excel 等格式的语义检索与问答，其能力边界请查阅 [文件问答](raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：Agent 1.0 文档 [智能体应用（Agent 1.0）](raw/application-user-guide/llm-application/single-agent-application.md) 中描述的“自动工具发现”功能在当前生产环境已下线，实际行为以 [新版智能体应用（Agent 2.0）](raw/application-user-guide/llm-application/new-single-agent-application.md) 为准。

## 关键参数

创建或调用 `llm application` 时需关注以下核心参数（均通过 `POST /v1/applications/{app_id}/chat` 或控制台配置）：  
- `inputs`: JSON 对象，传递用户输入变量（如 `{"query": "今天天气如何？", "user_id": "u123"}`）；  
- `user`: 可选字符串，用于会话隔离与审计追踪；  
- `stream`: 布尔值，启用流式响应（仅部分应用类型支持，详见 [应用类型介绍](raw/application-user-guide/llm-application/application-introduction.md)）；  
- `response_mode`: 可选 `"blocking"` 或 `"streaming"`，与 `stream` 参数协同控制返回方式。

## 使用方式

1. **控制台创建**：进入「应用开发」→「新建应用」→ 选择类型 → 配置模型、提示词、工具/工作流 → 发布；  
2. **API 调用**：使用 `POST /v1/applications/{app_id}/chat`，需携带 `Authorization: Bearer <api_key>`；  
3. **调试验证**：控制台内置「测试面板」支持实时输入/输出预览，调试日志可在 [应用类型介绍](raw/application-user-guide/llm-application/application-introduction.md) 中查看结构说明。

## 限制和注意事项

- 单次请求 `inputs` 总大小上限为 1MB；  
- 工作流应用最大执行时长为 120 秒，超时将终止并返回 `504 Gateway Timeout`；  
- 文件问答类应用仅支持 UTF-8 编码文本提取，非文本 PDF（如扫描件）需先经 OCR 预处理；  
- 所有应用默认开启敏感词过滤，若需关闭须在发布前勾选「跳过内容安全检测」（不推荐用于面向公网服务）。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


