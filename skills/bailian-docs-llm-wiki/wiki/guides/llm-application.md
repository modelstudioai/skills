# llm application

`llm application` 是百炼平台提供的核心应用构建能力，用于将大语言模型能力封装为可部署、可调用的服务。它支持从低代码智能体到高代码自定义逻辑的多种应用形态，适用于对话交互、任务编排、文档理解等场景。开发者可通过控制台或 OpenAPI 快速创建、调试和发布应用。

## 支持的模型与功能

- **模型支持**：应用可绑定平台托管的 LLM（如 Qwen 系列、Qwen-VL）、Embedding 模型及 Rerank 模型；部分高代码应用还支持 BYOM（Bring Your Own Model）接入 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。
- **应用类型**：
  - 智能体应用（Agent 1.0 和 Agent 2.0）：支持工具调用、多轮记忆、结构化输出；
  - 工作流应用：基于可视化节点编排 LLM、条件判断、[函数调用](../concepts/function-calling.md)等步骤；
  - 高代码应用：通过 Python SDK 编写完整业务逻辑，直接访问底层模型接口；
  - 文件问答：专用于上传文档后的语义检索与问答，依赖内置分块与向量化流程 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

> **注意**：Agent 1.0 已进入维护模式，新项目应优先使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，其在工具调度稳定性、上下文管理及错误恢复方面有显著改进。

## 关键参数

- `model_id`：必需，指定基础 LLM（如 `qwen-max`）；
- `prompt_template`：可选，支持 Jinja2 语法，用于预置系统提示与变量注入；
- `temperature` / `top_p` / `max_tokens`：标准采样参数，作用于所有应用类型；
- `enable_search`（仅工作流/Agent 应用）：启用联网搜索插件时需显式开启；
- `retrieval_config`（仅文件问答）：控制召回数量、相似度阈值等，详见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)。

## 使用方式

1. **控制台创建**：进入「应用开发」→「新建应用」→ 选择类型 → 配置模型与参数 → 发布；
2. **API 调用**：使用 `/v1/applications/{app_id}/chat` 接口发起请求，`input` 字段传入用户消息，支持 `files` 数组上传文档（仅文件问答类应用）；
3. **SDK 集成**：Python SDK 提供 `ApplicationClient` 类，支持同步/异步调用及流式响应处理。

## 限制和注意事项

- 单次请求最大输入长度受所选模型 context window 限制（如 `qwen-plus` 为 32768 tokens），超长文本将被截断；
- 文件问答应用单次最多支持 50 个文件，总大小不超过 200 MB，且仅支持 PDF/DOCX/TXT/MD 等常见格式；
- Agent 2.0 默认启用自动工具选择，但若 `tools` 列表为空或未配置有效 tool spec，将降级为纯 LLM 模式，不报错也不触发工具调用；
- 所有应用默认启用内容安全过滤，敏感词拦截策略不可关闭，如需调整需联系技术支持。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


