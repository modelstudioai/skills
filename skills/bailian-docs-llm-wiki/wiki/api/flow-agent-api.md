# flow agent api

Flow Agent API 是百炼平台提供的核心能力接口，用于在应用中集成基于流程编排的智能体（Agent）调用能力。它支持将多个组件（如 LLM 调用、工具执行、条件分支等）串联为可复用的业务流程，并通过统一 HTTP 接口对外暴露。该 API 适用于需结构化决策逻辑、多步推理或人机协同的生产级场景。

## 支持的模型与功能

- **模型兼容性**：当前仅支持百炼平台托管的 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 系列模型；不支持第三方模型接入。  
- **核心功能**：支持流程触发、异步任务轮询、状态查询、输入变量注入、节点级日志回溯；支持通过 [Prompt 模板](../../raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md) 实现动态提示工程。  
- **记忆机制**：[长期记忆](../concepts/long-term-memory.md)功能已迁移至新版向量存储服务，旧版 [长期记忆（旧）](../../raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md) 文档中的接口已废弃，实际开发请参考最新记忆管理 API。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，需在控制台创建 Flow Agent 应用后获取 |
| `inputs` | object | 否 | JSON 对象，键为流程定义中声明的 input 变量名，值为运行时传入的数据 |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时启用 SSE 流式响应（仅限同步调用） |
| `trace_id` | string | 否 | 用于全链路追踪的自定义 ID，建议与上游系统保持一致 |

> **注意**：`stream=true` 时不可同时使用异步模式（即 `async=false` 为隐式前提），否则返回 400 错误；该约束在 [概览](../../raw/application-api-reference/flow-agent-api/flow-agent-api-overview.md) 中未明确说明，但已在 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md) 的 `INVALID_PARAMETER` 分类下补充验证逻辑。

## 使用方式

1. **认证**：使用 Bearer [Token](../concepts/token.md) 方式，在 `Authorization` Header 中传入 `Bearer <access_token>`；[Token](../concepts/token.md) 需通过 [认证](../../raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md) 文档所述流程获取（推荐使用 AK/SK 签名生成）。  
2. **调用入口**：`POST https://dashscope.aliyuncs.com/api/v1/agents/{app_id}/run`  
3. **响应解析**：同步调用返回 `status`（`success`/`failed`/`running`）、`output`（最终结果对象）和 `task_id`（异步场景必需）；流式响应按事件类型分块（`event: output`, `event: error`, `event: done`）。

## 限制和注意事项

- 单次请求 `inputs` 总大小上限为 512 KB；单个 input 字段值长度不得超过 64 KB。  
- 异步任务最长保留 7 天，超时后 `task_id` 不可再查询。  
- 流程中若包含外部工具调用（如 HTTP 请求节点），其超时时间由流程配置决定，默认 30 秒，不可在 API 请求层覆盖。  
- 所有错误响应均遵循统一格式，具体含义请查阅 [错误码](../../raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md) 文档。

## 来源文档

- [Flow Agent API](../../raw/application-api-reference/flow-agent-api.md)


