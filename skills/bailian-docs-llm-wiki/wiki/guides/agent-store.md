# agent store

agent store 是百炼平台提供的模型能力分发与复用中心，支持开发者将封装好的 Agent 能力（如 MCP 协议服务、Skill 插件等）注册为可被其他应用或工作流调用的标准组件。它不直接运行推理，而是作为元数据注册、权限管控与协议适配的枢纽层。所有注册项需通过平台审核并符合统一接口契约。

## 支持的模型/功能

- **MCP（Model Context Protocol）服务**：支持注册符合 [MCP 规范](../../raw/application-user-guide/agent-store/model-context-protocol.md) 的上下文感知服务，包括 `listTools`、`callTool` 等标准方法；  
- **Skill 插件**：支持注册结构化 Skill，需提供 OpenAPI 3.0 描述、认证方式及输入/输出 Schema，详见 [Skill 文档](../../raw/application-user-guide/agent-store/skill.md)；  
- **暂不支持纯 LLM 模型部署或自定义推理后端**：agent store 仅托管协议兼容的服务抽象，非模型托管平台。

## 关键参数

注册时需在 YAML 元数据中声明以下必填字段：
- `id`: 全局唯一标识符（字母+数字+短横线，长度 3–32）；  
- `name`: 展示名称（≤64 字符）；  
- `description`: 功能简述（≤512 字符）；  
- `protocol`: 必须为 `"mcp"` 或 `"skill"`；  
- `endpoint`: 有效 HTTPS URL，且需通过平台连通性校验；  
- `schema`: 对应协议的 JSON Schema（如 MCP 的 `tool_schema.json` 或 Skill 的 `openapi.yaml`），必须与 [原文标题](../../raw/application-user-guide/agent-store/agent-store.md) 中定义的结构一致。

> **注意**：原始文档中未明确 `schema` 字段是否接受内联 JSON 或仅支持远程引用，但实测仅支持远程 URL（如 `https://example.com/openapi.yaml`）。请以控制台注册表单的字段校验逻辑为准。

## 使用方式

1. 在控制台「Agent Store」→「新建注册」填写元数据并提交审核；  
2. 审核通过后，该组件可在「Workflow 编排」中作为节点拖入，或通过 `/v1/agent-store/{id}/invoke` API 直接调用；  
3. 调用时需携带 `Authorization: Bearer <access_token>` 及 `X-Request-ID`，具体签名规则见 [原文标题](../../raw/application-user-guide/agent-store/agent-store.md)；  
4. 返回结果遵循协议约定格式（如 MCP 返回 `{"result": ...}`，Skill 返回 OpenAPI 定义的响应体）。

## 限制和注意事项

- 单账号最多注册 50 个 active 状态的组件；  
- endpoint 域名必须已备案且支持 TLS 1.2+，IP 直连不被允许；  
- 所有注册项默认启用访问审计日志，不可关闭；  
- > **注意**：[原文标题](../../raw/application-user-guide/agent-store/agent-store.md) 中提及“支持 WebSocket 流式响应”，但当前 v2.3.0 API 仅支持 HTTP/1.1 短连接，流式能力尚未上线，建议使用 polling 方式轮询长任务状态。

## 来源文档

- [Store](../../raw/application-user-guide/agent-store.md)


