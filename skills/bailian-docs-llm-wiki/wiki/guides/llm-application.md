# llm application

`llm application` 是百炼平台提供的面向大语言模型应用的统一构建与部署能力，支持从低代码智能体到高代码定制化应用的全栈开发范式。开发者可通过可视化编排或代码集成方式快速构建生产级 LLM 应用，底层自动对接模型服务、RAG、工具调用等核心能力。该能力在 [应用开发](../../raw/application-user-guide/llm-application.md) 文档中有基础分类说明。

## 支持的模型与功能

- **应用类型**：支持五类应用形态，包括智能体应用（Agent 1.0 和 Agent 2.0）、工作流应用、高代码应用、文件问答应用；其中 Agent 2.0 为当前主推架构，具备更灵活的工具编排与状态管理能力。详细对比见 [应用开发](../../raw/application-user-guide/llm-application.md)。
- **模型接入**：所有应用类型均支持调用百炼托管的主流开源及自研模型（如 Qwen 系列），也可通过 `custom_model` 参数接入用户自有 API 模型服务。
- **扩展能力**：原生支持 RAG（知识库检索）、[函数调用](../concepts/function-calling.md)（Function Calling）、多轮对话上下文管理、异步流式响应等关键功能。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台创建应用后分配的唯一 ID，用于路由至对应应用实例 |
| `input` | object | 是 | 用户输入，结构为 `{ "query": "..." }`；文件问答类需额外传入 `file_ids` 数组 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应 |
| `parameters` | object | 否 | 覆盖应用配置中的推理参数，如 `temperature`, `top_p`, `max_tokens` 等 |

> **注意**：`parameters` 中的 `max_tokens` 在工作流应用中实际受节点级限流约束，与 [应用开发](../../raw/application-user-guide/llm-application.md) 所述全局生效存在差异，应以节点配置为准。

## 使用方式

1. **创建应用**：在百炼控制台「应用管理」中选择类型（如「智能体应用」），完成提示词、知识库、工具等配置并发布；
2. **调用接口**：使用 SDK 或 HTTP POST 请求 `/v1/applications/{app_id}/chat`，示例：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/applications/<app_id>/chat \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"input":{"query":"你好"},"stream":false}'
   ```
3. **调试与监控**：通过控制台「调用日志」查看 trace 详情，支持按 `app_id` + `request_id` 追踪完整链路。

## 限制和注意事项

- 单次请求 `input.query` 长度上限为 32768 字符；文件问答类单次最多上传 10 个文件（总大小 ≤ 512 MB）；
- Agent 2.0 应用不兼容 Agent 1.0 的旧版工具定义格式，迁移需重写工具 Schema；
- 高代码应用的自定义代码运行环境仅支持 Python 3.9，且禁止执行系统命令、网络外连（除白名单 API 外）；
- 所有应用默认启用内容安全过滤，若需关闭需在应用配置中显式设置 `enable_safety_check: false` —— 此行为已在新版文档中明确，但部分旧版示例未同步更新，请以 [应用开发](../../raw/application-user-guide/llm-application.md) 最新描述为准。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


