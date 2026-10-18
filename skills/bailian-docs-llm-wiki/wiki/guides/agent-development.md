# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据任务复杂度、可控性需求和运维能力选择合适模式。所有 Agent 类型均统一接入百炼推理网关与可观测性体系。

## 支持的模型/功能

- **Managed Agent**：基于预置模板的托管式 Agent，内置工具调用、[记忆管理](../concepts/memory-management.md)与多轮对话状态机，适合快速上线标准业务场景。详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。
- **Flow Agent**：可视化流程编排 Agent，支持 LLM 节点、条件分支、[函数调用](../concepts/function-calling.md)节点及自定义 Python 逻辑块，适用于中等复杂度的决策链路。其能力边界与配置项在 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 中有明确说明。
- **Sandbox**：完全开放的 Python 沙箱环境，允许用户编写任意逻辑（含异步 I/O、第三方库导入），但需自行实现会话状态管理与错误恢复。该模式的资源限制与安全策略详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。

## 关键参数

- `model_id`：必须指定，仅支持百炼已纳管的 Agent 专用模型（如 `qwen-7b-agent`、`qwen2.5-72b-agent`），不兼容通用文本模型。
- `enable_memory`：仅 Flow Agent 和 Managed Agent 支持；Sandbox 中需手动实现记忆逻辑。
- `timeout_ms`：默认 30000（30 秒），Sandbox 模式下最大可设为 120000（2 分钟）；超过将触发硬中断。

## 使用方式

1. 创建 Agent 实例时，在控制台或 OpenAPI `CreateAgent` 请求体中指定 `type` 字段为 `"managed"` / `"flow"` / `"sandbox"`；
2. 根据类型上传对应配置：Managed Agent 使用 JSON Schema 描述工具集；Flow Agent 提交 `.flow.json` 流程定义；Sandbox 提交 `main.py` 入口文件；
3. 调用时通过 `/v1/agents/{agent_id}/chat` 接口发起请求，消息体结构与标准 Chat API 一致，但会自动注入 Agent 运行时上下文。

## 限制和注意事项

- Sandbox 模式禁止访问外网（包括 `requests.get("http://...")`）、读写宿主文件系统、执行系统命令（`os.system`, `subprocess`）；
- Managed Agent 的工具调用失败默认重试 2 次，不可配置；而 Flow Agent 中的函数节点可显式设置 `retry_times` 参数；
> **注意**：原始文档中 [Agent 开发运行](../../raw/application-user-guide/agent-development.md) 将 Sandbox 描述为“支持任意第三方库”，但实际仅预装 `requests`, `numpy`, `pandas` 等 12 个常用库，其余需通过 `pip install` 在初始化阶段动态安装（受 60 秒超时限制）。此差异已在最新控制台文档中修正。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


