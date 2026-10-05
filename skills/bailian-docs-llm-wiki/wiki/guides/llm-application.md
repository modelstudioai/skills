# llm application

`llm application` 是百炼平台提供的核心应用构建能力，用于将大语言模型能力封装为可部署、可调用的服务。它支持从低代码智能体到高代码自定义逻辑的多种应用形态，适用于对话交互、自动化流程、文档分析等场景。开发者可通过控制台或 API 快速创建、调试和发布应用。

## 支持的模型与功能

- **应用类型**：当前支持五类应用形态：  
  - 新版智能体应用（Agent 2.0）——基于强化推理链与工具调用编排，推荐新项目首选；  
  - 智能体应用（Agent 1.0）——基础版自主决策智能体，已进入维护期；  
  - 工作流应用——可视化节点编排，支持条件分支与多模型串联；  
  - 高代码应用——完全开放 SDK 接口，允许嵌入自定义 Python 逻辑与外部服务；  
  - 文件问答——专用于上传文档后的语义检索与问答，底层集成 RAG 流程。  
  各类型能力细节见 [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)。

> **注意**：Agent 1.0 与 Agent 2.0 在工具调用协议、记忆管理机制上不兼容；[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 文档明确标注其为当前主推架构，而 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 中部分参数（如 `tool_choice` 的枚举值）已被弃用，实际调用时以 Agent 2.0 文档为准。

## 关键参数

- `model_id`：必需，指定后端模型（如 `qwen-max`, `qwen-plus`），需与应用类型兼容（例如文件问答仅支持 `qwen-turbo` 及以上）；  
- `stream`：布尔值，控制是否启用流式响应，默认 `false`；  
- `temperature` / `top_p`：影响输出随机性，范围 `[0.0, 1.0]`，仅对生成类应用生效；  
- `user_id`：用于会话隔离与审计追踪，建议传入业务侧唯一标识；  
- `files`（仅文件问答）：上传文件的 base64 编码或 OSS URL 列表，单次最多 10 个，总大小 ≤ 50MB。

## 使用方式

1. **控制台创建**：进入「应用开发」→「新建应用」→ 选择类型 → 配置模型、提示词、工具等 → 发布；  
2. **API 调用**：使用 `POST /v1/applications/{app_id}/chat`，请求体为 JSON 格式，示例见 [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 的调用章节；  
3. **SDK 集成**：Python SDK 提供 `ApplicationClient.chat()` 方法，自动处理鉴权与重试，详见 [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md) 的接入说明。

## 限制和注意事项

- 单次请求最大上下文长度受所选模型限制（如 `qwen-max` 为 32768 tokens），超出将触发截断；  
- Agent 2.0 应用默认启用工具自动发现，若需禁用，须在创建时显式设置 `enable_tool_discovery: false`；  
- 文件问答应用不支持实时上传后立即查询，需等待异步解析完成（通常 < 30s），状态轮询接口见 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)；  
- 所有应用均强制启用输入内容安全过滤，含敏感词的请求将直接拒绝并返回 `400 Bad Request`。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


