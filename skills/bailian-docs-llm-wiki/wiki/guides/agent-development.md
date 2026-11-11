# agent development

百炼平台提供多种 Agent 开发范式，支持从低代码编排到高自由度代码沙箱的全栈开发路径。开发者可根据业务复杂度、可控性需求和运维能力选择合适模式，所有类型均统一接入百炼推理网关与可观测性体系。核心能力围绕 LLM 编排、工具调用、状态管理及安全隔离展开。

## 支持的模型/功能

- **Managed Agent**：平台托管的声明式 Agent，通过 YAML 配置定义工具链、记忆策略与终止条件，适合标准化客服、FAQ 等场景；不支持自定义 Python 逻辑 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Flow Agent**：可视化流程编排 Agent（即 LLM Application），支持节点化连接 LLM、工具、条件分支与变量，可导出为可复用的 Flow 模板 [Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- **Sandbox Agent**：基于 Python 的全控制沙箱环境，允许编写任意 `run()` 函数、调用 SDK 工具、管理 session state，并支持异步 I/O 和第三方库（需白名单）[Agent 开发运行](../../raw/application-user-guide/agent-development.md)。  
- 应用广场提供开箱即用的 Agent 模板，但其底层实现可能混合上述三种模式，具体以模板详情页标注为准。

## 关键参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model_id` | string | 必填；仅限平台已纳管的模型 ID（如 `qwen-max`），不支持传入自部署模型地址 |
| `enable_memory` | boolean | 默认 `true`；仅 Flow Agent 和 Managed Agent 生效；Sandbox 中需自行实现 memory 管理 |
| `timeout_ms` | integer | 默认 `30000`（30 秒）；Sandbox Agent 可设为 `60000`，超过将强制中断进程 |
| `tools` | array | 工具列表，格式为 `[{ "name": "...", "description": "...", "parameters": {...} }]`；Sandbox 中可通过 `self.tools` 动态注册 |

> **注意**：文档中曾提及 `max_iterations` 参数适用于所有 Agent 类型，但最新 SDK v2.3+ 已将其移除，仅在 Managed Agent 的 YAML schema 中保留；实际迭代控制应通过 `stop_condition` 或代码逻辑实现。

## 使用方式

1. **创建 Agent**：在控制台「Agent 开发」页选择类型，或通过 OpenAPI `POST /v1/agents` 提交配置；  
2. **调试与部署**：所有类型均支持在线 Playground 调试；Flow Agent 和 Managed Agent 可一键发布为 API；Sandbox Agent 需先构建镜像并绑定部署实例；  
3. **调用接口**：统一使用 `/v1/agents/{agent_id}/chat` 接口，请求体需包含 `messages` 数组（含 `role` 和 `content`），Sandbox Agent 还可选传 `session_id` 以维持上下文。

## 限制和注意事项

- Sandbox Agent 单次执行内存上限为 2GB，CPU 时间配额为 15 秒（非 wall-clock 时间）；超出将触发 OOM/Kill；  
- Flow Agent 的节点总数不得超过 50 个，嵌套子 Flow 深度限制为 3 层；  
- 所有 Agent 均禁止访问内网服务、本地文件系统（`/tmp` 除外）及未授权的外部域名；DNS 解析仅允许白名单内的 SaaS 服务；  
- Managed Agent 的 YAML 配置不支持 Jinja 模板语法，该能力仅存在于旧版文档草稿中，当前版本已废弃。

## 来源文档

- [Agent 开发运行](../../raw/application-user-guide/agent-development.md)


