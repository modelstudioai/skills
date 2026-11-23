# get started with agents

百炼平台的 Agent 功能支持开发者快速构建具备规划、工具调用和多步推理能力的智能体应用。本文档梳理了 Agent 的核心能力边界、关键配置项及接入方式，适用于希望在生产环境中集成 Agent 的开发者。所有说明均基于当前稳定版 API（v1）和控制台功能。

## 支持的模型与功能

- **模型支持**：仅 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款 Qwen 系列大模型支持 Agent 模式；其他模型（如 `qwen2.5-7b`）调用 `/v1/agents/run` 接口将返回 `400 Unsupported model` 错误。  
- **核心功能**：包括自动工具选择（Tool Calling）、多轮任务分解（Planning）、内置知识检索（Knowledge Base Integration）及结构化输出（JSON Schema enforcement）。  
- **不支持能力**：流式响应（streaming）、自定义系统提示词覆盖（system prompt override）、以及非 JSON 格式的工具参数校验。详细能力矩阵见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)。

## 关键参数

调用 `/v1/agents/run` 时必需且影响行为的关键参数如下：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 仅限 `qwen-max`/`qwen-plus`/`qwen-turbo`，大小写敏感 |
| `tools` | array | 否（但无 tools 则退化为普通 chat） | 工具定义列表，需符合 OpenAPI 3.0 schema 片段格式；详见 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) |
| `max_iterations` | integer | 否，默认 10 | 单次请求中 Agent 最大规划+执行步数，超限将终止并返回 `"status": "stopped"` |
| `output_schema` | object | 否 | 强制输出 JSON 结构，若与工具返回或最终结果冲突，将触发 `validation_error` |

> **注意**：原始文档中提及 `temperature` 可用于控制 Agent 的探索性，但实测 v1 API 中该参数对规划行为无实际影响；请以 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md) 中的参数说明为准，避免依赖已失效的调试方式。

## 使用方式

1. **准备工具定义**：按平台要求编写工具描述（含 `name`、`description`、`parameters`），确保 `parameters` 符合 JSON Schema Draft-07；示例见 [开始使用](../../raw/application-user-guide/get-started-with-agents.md)。  
2. **发起请求**：使用 POST 方法调用 `https://dashscope.aliyuncs.com/api/v1/agents/run`，Header 中携带 `Authorization: Bearer <api_key>`。  
3. **处理响应**：检查 `response.status` 字段：`"success"` 表示完成；`"stopped"` 表示迭代超限或工具调用失败；`"failed"` 表示模型内部错误。完整响应结构参考 [Agent 服务概览](../../raw/application-user-guide/get-started-with-agents/agent-overview.md)。

## 限制和注意事项

- **配额限制**：单次 Agent 请求计入 `qwen-*` 模型的 tokens 总配额，且 `max_iterations=10` 时，实际 token 消耗可能达同等长度 chat 请求的 3–5 倍。  
- **工具调用约束**：工具函数名（`name`）必须为合法 Python 标识符（仅含字母、数字、下划线，且不以数字开头）；否则返回 `422 Unprocessable Entity`。  
- **调试建议**：首次集成时，务必设置 `max_iterations=3` 并启用 `verbose=true`（非公开参数，需联系技术支持开通），便于定位规划失败点。  
- **长期兼容性**：Agent 的工具 schema 解析逻辑与 OpenAI Function Calling 兼容性有限，不建议直接复用 OpenAI 的 `functions` 数组；请严格遵循百炼文档规范。

## 来源文档

- [开始使用](../../raw/application-user-guide/get-started-with-agents.md)


