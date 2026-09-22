# llm application

`llm application` 是百炼平台提供的 LLM 应用构建能力，支持开发者快速创建面向终端用户的可部署应用，涵盖智能体、工作流、高代码及文件问答等多种形态。所有应用均基于平台统一的推理服务与上下文管理机制，可通过 API 或嵌入式 SDK 集成。详细背景和设计目标见 [应用开发](../../raw/application-user-guide/llm-application.md)。

## 支持的模型与功能

- **模型兼容性**：支持百炼全量托管模型（如 Qwen 系列、Qwen2-VL、Qwen3）及用户自定义模型（需通过 `model_id` 显式指定）。不支持直接调用非百炼托管的第三方模型 API。
- **应用类型**：
  - 新版智能体应用（Agent 2.0）：支持多工具动态编排、状态感知与自主决策，推荐用于复杂任务场景；
  - 工作流应用：基于可视化节点编排，适合确定性逻辑强、需人工审核或外部系统集成的流程；
  - 高代码应用：允许编写 Python 脚本控制完整执行链路，适用于算法定制或私有协议对接；
  - 文件问答：支持上传 PDF/DOCX/TXT 等格式，自动切片、向量化与[检索增强生成](../concepts/rag.md)（RAG），但仅限单次会话内生效；
  - （已弃用）智能体应用（Agent 1.0）：功能已被 Agent 2.0 全面覆盖，[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 文档明确建议迁移。

> **注意**：原始文档中 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md) 的接口路径 `/v1/applications/agent1/run` 已于 v2024.07 起返回 `410 Gone`，实际调用应使用 Agent 2.0 的 `/v1/applications/agent2/run`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `application_id` | string | 是 | 应用唯一标识，创建后由平台分配，可在控制台或 API 响应中获取 |
| `inputs` | object | 否 | 用户输入数据，结构由应用 schema 定义；Agent 2.0 和工作流应用支持 `files` 字段传入 Base64 编码文件内容 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应（仅限非工作流类应用） |
| `user_id` | string | 否 | 用于会话隔离与审计，建议传入业务侧用户 ID |

## 使用方式

1. **创建应用**：在控制台「应用开发」页选择类型，配置 [prompt](prompt.md)、工具集（Agent）、节点逻辑（Workflow）或代码（Rich Code）；
2. **发布应用**：点击「发布」生成 `application_id`，仅已发布应用可被 API 调用；
3. **调用 API**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/applications/{application_id}/run \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"inputs": {"query": "今天北京天气如何？"}}'
   ```
   更多请求示例与错误码说明见 [应用开发](../../raw/application-user-guide/llm-application.md)。

## 限制和注意事项

- 单次请求最大 `inputs` 大小为 1MB；文件问答类应用单次上传文件总大小 ≤ 50MB；
- Agent 2.0 默认最大工具调用深度为 8 层，超限时返回 `TOOL_CALL_DEPTH_EXCEEDED` 错误，可通过 `max_iterations` 参数调整（上限 20）；
- 所有应用默认启用敏感词过滤与输出长度截断（max_tokens=4096），不可关闭；
- 工作流应用不支持流式响应（`stream=true` 将被忽略），且 `inputs.files` 中的文件不会自动解析为文本——需显式添加「文件解析」节点。该行为与 [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md) 的自动处理逻辑不同，请按场景选型。

## 来源文档

- [应用开发](../../raw/application-user-guide/llm-application.md)


