# 模型上下文协议（MCP）

模型上下文协议（Model Context Protocol，简称 MCP）是百炼平台定义的标准化工具集成协议，用于在大模型推理过程中安全、可控地注入外部服务能力。它通过统一的服务注册、发现、调用与生命周期管理机制，使智能体能在生成响应时动态调用地图、搜索、数据库等真实世界能力，并将结果作为上下文无缝融入模型推理链路。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）开发**：在 Managed Agent 或 Flow Agent 中，开发者可在「应用配置 > 工具」或流程图节点中添加 MCP 服务；智能体运行时自动识别用户意图，按需调用并注入返回结果作为上下文，无需编写调用逻辑或处理参数映射（Flow Agent 中可手动配置输入/输出字段映射）。  
- **工作流（Workflow）编排**：MCP 以独立节点形式嵌入流程图，支持设置超时、重试、错误分支；每个节点绑定一个已开通的 MCP 服务（如 `amap.maps.geocode`），输入参数通过上游节点输出或常量指定。  
- **外部系统集成**：通过百炼提供的 [OpenAI 兼容接口](openai-compatible-interface.md)（`/v1/chat/completions`）或专用 MCP SDK（`mcp` Python 包），第三方应用可直接调用 MCP 工具，例如 `mcp.call("websearch.search", {"query": "阿里云百炼最新特性"})`；CLI 工具 `bl mcp call` 也支持快速调试。  
- **自定义能力扩展**：开发者可通过三种方式部署自定义 MCP 服务：① 脚本部署（本地 Python 服务 + `mcp-server` 启动）；② AI 网关导入（将已有 HTTP API 封装为 MCP 标准）；③ 阿里云 OpenAPI 导入（自动解析 OpenAPI Spec 生成 MCP 接口）。所有自定义 MCP 均纳入统一服务管理控制台，支持启停、版本更新与监控。

## 关键参数和配置

- **服务标识**：`mcp_code`（如 `amap.maps`）为全局唯一服务编码，由平台分配或用户自定义（自定义 MCP）；工具级调用需拼接为 `{mcp_code}.{tool_name}`（如 `websearch.search`）。  
- **认证方式**：所有 MCP 调用统一使用 `DASHSCOPE_API_KEY` 鉴权，**不单独申请密钥**；敏感凭证（如高德 API Key）必须通过阿里云 KMS 加密后存入凭据管理，MCP 运行时自动解密注入。  
- **部署模式**（仅自定义 MCP）：  
  - `basic`（基础模式）：按调用时长计费（0.000156 元/秒），无部署成本，适合低频、测试场景；  
  - `pro`（极速模式）：预热实例 + 固定资源，额外收取部署费（0.000036 元/秒），适用于高并发、低延迟生产场景。  
- **调用参数**：工具调用请求体为标准 JSON 对象，字段名与类型由 MCP 服务 Schema 定义（如 `{"query": "北京天气", "city": "beijing"}`）；平台自动校验必填项与类型，非法参数直接返回 `400 Bad Request`。  
- **状态约束**：MCP 服务必须处于 `enabled` 状态才可被调用；自定义 MCP 在 `deploying` 或 `running` 状态下禁止更新配置或执行启停操作。

## 面向开发者，简洁实用

- ✅ **开箱即用**：官方 MCP（如高德地图、WebSearch）开通即用，无需部署；One Key 服务一键接入，免配置。  
- ✅ **零侵入集成**：在智能体中添加 MCP 后，模型自动理解何时调用、如何传参、怎样融合结果——你只需关注业务语义，不用写 glue code。  
- ✅ **安全可控**：所有敏感参数经 KMS 加密；自定义 MCP 默认隔离网络（不可访问本地资源）；调用行为全链路审计（含 `request_id` 日志追踪）。  
- ⚠️ **注意避坑**：  
  - 官方 MCP 的 `env` 配置（如 `{"AMAP_MAPS_API_KEY": "xxx"}`）与自定义 MCP 的 `mcp_config` 结构不同，**不可混用**；  
  - MCP 返回内容计入模型输入 Token，请在 Prompt 设计时预留足够上下文空间；  
  - 自定义 MCP 更新代码后，必须重新部署（npx/uvx 方式不会自动热更新）。

## 关联主题页

- [overview](../api/overview.md)
- [agent store](../guides/agent-store.md)
- [agent development](../guides/agent-development.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


