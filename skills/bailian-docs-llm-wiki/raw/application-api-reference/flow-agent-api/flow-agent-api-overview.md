# 概览

Flow Agent API 覆盖应用调用与 Flow Agent 组件类接口。

Flow Agent API 覆盖应用调用与 Flow Agent 组件类接口：

-   **应用调用**：通过 DashScope 应用网关调用已发布的智能体应用与工作流应用，Base URL 为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。
-   **Prompt 模板、长期记忆（旧）与其他组件**：百炼 OpenAPI（`bailian.{regionId}.aliyuncs.com`），按工作空间路径调用。

两类接口的鉴权方式不同，详见[认证](raw/application-api-reference/flow-agent-api/flow-agent-api-authentication.md)；错误处理见[错误码](raw/application-api-reference/flow-agent-api/flow-agent-api-errors.md)。
