# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度沙箱开发的全场景需求。开发者可根据业务复杂度、可控性要求和运维能力选择合适的 Agent 类型。所有类型均基于平台统一的执行引擎与可观测能力构建。

## 支持的模型/功能

- **Managed Agent**：面向业务逻辑封装的托管式 Agent，内置意图识别、工具调用编排与错误恢复机制，适合快速上线标准化服务。  
- **Flow Agent**（即 LLM Application）：基于可视化流程图的声明式开发方式，支持节点化编排 LLM 调用、条件分支、变量传递与外部 API 集成，详见 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Sandbox Agent**：提供 Python 运行时沙箱，允许编写任意逻辑（含自定义工具、状态管理、异步处理），适用于需要精细控制执行流或集成私有 SDK 的场景，其能力边界与安全约束在 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 中明确定义。

## 关键参数

- `model_id`：必须指定，仅支持平台白名单内的推理模型（如 `qwen-max`, `qwen-plus`），不支持第三方模型直连；具体兼容列表见 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 文档。  
- `timeout_ms`：全局执行超时，默认 30000（30 秒），Sandbox Agent 可设为最高 60000，Flow Agent 不可超过 45000；该限制在 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 和 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 中存在不一致描述。  
> **注意**：`timeout_ms` 在 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 中标注上限为 45000，但 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md) 标注为 60000；实际生效值以创建时平台返回的校验错误为准，建议首次部署时显式设置并测试。

- `enable_tracing`：启用后可接入百炼 Trace 系统，用于调试执行路径与延迟分析（默认 `false`）。

## 使用方式

1. 通过控制台「应用开发」→「新建 Agent」选择类型（Managed / Flow / Sandbox）；  
2. 按向导填写基础配置（名称、描述、模型）、定义核心逻辑（如 Managed 的 YAML Schema、Flow 的节点图、Sandbox 的 Python 代码）；  
3. 本地调试可通过 `bailian-cli run --agent-id <id>` 触发，日志与 trace 数据实时同步至控制台；完整 CLI 用法参考 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
4. 发布后通过 `/v1/agents/{id}/chat` 接口调用，请求体需包含 `messages` 数组及可选 `session_id`。

## 限制和注意事项

- 所有 Agent 实例共享账户级并发配额（默认 5 QPS），超出将触发 429 响应；  
- Sandbox Agent 禁止访问外网（除已授权的百炼内置工具外），且无法持久化磁盘文件；  
- Flow Agent 的循环节点深度限制为 5 层，嵌套过深会导致编译失败——该规则未在 [Flow Agent](../../raw/application-user-guide/agent-development/llm-application.md) 中明确说明，但实测行为与 [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md) 一致；  
- 应用广场中的模板 Agent 仅提供初始化参考，实际部署前须审查其工具权限与数据流向，详情参见 [应用广场](../../raw/application-user-guide/agent-development/application-gallery.md)。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


