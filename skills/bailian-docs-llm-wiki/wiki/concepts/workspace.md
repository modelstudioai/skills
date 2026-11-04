# 业务空间（Workspace）

业务空间（Workspace）是百炼平台中用于组织、隔离和管理模型调用、应用部署与数据资源的核心逻辑单元。每个业务空间对应一个唯一标识符（`workspace_id`），作为 API 调用的上下文边界，实现资源权限控制、流量计量、服务路由与地域绑定的统一载体。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（基础 API）**：生产环境必须使用业务空间专属 Base URL（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），该域名提供更高并发、3600 秒超时及 WebSocket/AOQ 支持；SDK 初始化时需显式传入 `workspace` 参数（如 `Client(api_key=..., workspace="llm-xxxx", region="cn-beijing")`），否则默认降级至共享域名，受限于试用级限流（RPM 1000）且无 SLA 保障。

- **RAG 知识库服务**：所有 RAG API 的 Endpoint 均以 `https://{workspace_id}.{region}.maas.aliyuncs.com` 为根路径；`workspace_id` 是知识库、Agent、文档等资源的隐式归属标识，决定其可见性与操作权限范围——跨 Workspace 的知识库无法被其他 Workspace 的 Agent 引用。

- **Flow Agent 应用调用**：在调用子业务空间下发布的智能体时，需通过请求 Header `X-DashScope-WorkSpace: {workspace_id}` 显式声明目标 Workspace；若省略，则默认使用 API Key 所属主 Workspace。

- **Application Component（数据连接 & 知识库 OpenAPI）**：所有组件类接口（如 `/indices`, `/files`, `/promptTemplates`）均强制要求在 URL 路径中携带 `WorkspaceId`（如 `/bailian/2023-12-29/indices?WorkspaceId=llm-xxxx`），这是资源隔离与 RAM 权限校验的强制维度，缺失将返回 `400 InvalidParameter`。

- **模型管理与配额控制**：模型级限流（QPS/TPM）与授权策略（App ID 白名单）均按业务空间粒度生效；同一模型在不同 Workspace 中可配置完全独立的配额与访问策略，互不影响。

## 关键参数和配置

- **`workspace_id`（必需）**  
  - 格式：固定前缀 + 12 位十六进制字符串（如 `llm-abcdef123456`），从[百炼控制台 → 业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)获取；  
  - 用途：构造 Base URL、SDK 初始化、Header 透传、OpenAPI 路径参数；  
  - 注意：不可跨地域复用，`workspace_id` 与 `region` 绑定（如 `llm-xxx.cn-beijing` 仅适用于北京地域）。

- **地域绑定（region）**  
  - 每个 `workspace_id` 仅在一个地域有效，调用时必须匹配对应地域的接入点（如 `cn-beijing`, `ap-southeast-1`）；  
  - 错误示例：在北京 Workspace 下使用新加坡 Base URL 将导致 `401 Unauthorized` 或 `404 Not Found`。

- **权限继承关系**  
  - API Key 的调用权限范围由其创建时所选业务空间决定；  
  - RAM 用户策略需显式授予 `bailian:WorkspaceAccess` 权限，并指定 `Resource: "acs:bailian:{region}:{account_id}:workspace/{workspace_id}"` 才能操作该 Workspace 下的资源。

## 面向开发者，简洁实用

- ✅ **必做**：生产环境务必使用 `workspace_id` 构造专属 Base URL，并在 SDK 初始化或 Header 中显式传入；  
- ✅ **必查**：确认 `workspace_id` 与 `region` 完全匹配，二者不一致是 401/404 最常见原因；  
- ✅ **必审**：RAM 授权策略中，`WorkspaceId` 必须作为 Resource ARN 的精确组成部分；  
- ❌ **禁用**：不要在客户端硬编码 `workspace_id`；应通过环境变量（如 `BAILIAN_WORKSPACE_ID`）或配置中心注入；  
- ⚠️ **注意**：`workspace_id` 不是模型名、App ID 或 API Key，三者逻辑独立，不可混用或相互推导。

## 关联主题页

- [preparations](../api/preparations.md)
- [rag api](../api/rag-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [application component api reference](../api/application-component-api-reference.md)
- [model management](../api/model-management.md)


