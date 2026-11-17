# agent development

百炼平台提供多种 Agent 开发与运行模式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适范式。所有 Agent 均基于平台统一的执行引擎与可观测基础设施。

## 支持的模型与功能

- **Managed Agent**：平台托管的声明式 Agent，支持通过 YAML 配置工具链、记忆策略与路由逻辑，适用于标准化任务（如客服问答、数据查询）。无需编写运行时代码，但扩展性受限。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：可视化流程编排 Agent，基于 LLM 应用构建器（LLM Application Builder）实现节点化逻辑流，支持条件分支、循环、多模型协同调用。适合中等复杂度业务流程。该能力在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有入口指引。
- **Sandbox Agent**：完全开放的 Python 沙箱环境，允许自定义 `run()` 函数、引入第三方库（需白名单）、访问平台提供的 `ToolClient` 和 `MemoryClient` SDK。适用于需要精细控制推理链路或集成私有服务的场景。详细约束见 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model_id` | string | 是 | 所选基础模型 ID（如 `qwen-max`, `qwen-plus`），需与 Agent 类型兼容；Managed Agent 仅支持部分模型 |
| `tools` | array | 否 | 工具列表（ID 或配置对象），仅 Flow Agent 和 Sandbox Agent 支持动态注册 |
| `memory_strategy` | string | 否 | 可选 `short-term` / `long-term` / `none`；Managed Agent 默认启用 long-term，Sandbox 需显式初始化 `MemoryClient` |
| `timeout_ms` | integer | 否 | 最大执行时长，默认 30000（30 秒），Sandbox Agent 可设至 120000，超过将强制终止 |

> **注意**：`memory_strategy=long-term` 在 Managed Agent 中自动绑定用户级持久化存储，但在 Sandbox 中需调用 `MemoryClient.put()` 显式写入，二者语义不一致，开发时须按实际运行环境适配逻辑。

## 使用方式

1. **创建 Agent**：在控制台「应用开发」→「Agent」页点击「新建」，选择类型（Managed / Flow / Sandbox）；
2. **配置与调试**：填写参数、绑定工具、上传代码（Sandbox）或拖拽节点（Flow），使用「实时调试」面板测试输入输出；
3. **部署与调用**：发布后获取 `agent_id`，通过 `/v1/agents/{agent_id}/chat` 接口发起 HTTP 请求，请求体需包含 `input` 字段（string 或 object）。

所有类型均支持异步调用与流式响应（`stream=true`），但 Managed Agent 的[流式输出](../concepts/streaming-output.md)仅限最终回复，中间步骤不可见；而 Sandbox Agent 可通过 `yield` 返回中间步骤（需配合 `stream=true` 与 `Content-Type: text/event-stream`）。

## 限制和注意事项

- 单次请求最大输入长度：Managed Agent ≤ 8192 tokens，Flow Agent ≤ 16384 tokens，Sandbox Agent ≤ 32768 tokens（受底层模型上下文窗口限制）；
- Sandbox Agent 不支持 fork 进程、系统调用、本地文件读写（除 `/tmp` 临时目录外），且依赖包安装需提前提交审核；
- 所有 Agent 默认开启输入内容安全过滤（含敏感词与恶意指令检测），若触发拦截，返回 `400 Bad Request` 并附 `error.code="content_blocked"`；
- Managed Agent 的 YAML 配置变更后需重新发布才生效，而 Sandbox Agent 的代码更新可热重载（仅限开发环境），生产环境仍需发布新版本。该差异已在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 的「部署说明」章节明确。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


