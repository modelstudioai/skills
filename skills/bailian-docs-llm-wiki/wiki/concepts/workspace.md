# 业务空间

业务空间（Workspace）是阿里云百炼平台进行资源隔离与精细化权限管理的最小单元。每个业务空间归属于特定地域，拥有独立的用户权限、模型访问控制、API Key 和用量统计体系。

## 核心特性

- **地域绑定**：单个业务空间不能跨地域存在。即使各地域的默认业务空间，也是彼此独立的空间。
- **默认空间与自定义空间**：每个地域自动创建一个默认业务空间，默认空间无法限制模型调用、调优和部署。自定义空间则可进行细粒度的模型权限与限流配置。
- **Workspace ID**：业务空间的唯一标识。调用子业务空间下的应用或 API 时，需在请求中携带 Workspace ID。

## 权限管理

业务空间是权限控制的核心维度，支持以下管控能力：

| 权限维度 | 说明 |
|---------|------|
| 模型调用限制 | 控制特定模型在该空间内的可用性，设置 QPM 和 Token 限流 |
| 模型训练限制 | 控制模型调优及调优后部署的权限 |
| 模型部署限制 | 控制模型直接部署的权限 |
| 用户控制台权限 | 管理 RAM 用户对控制台功能页面的访问 |

业务空间内的角色分为三级：

- **超级管理员**：可跨空间统一管理，需阿里云主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户。
- **业务空间管理员**：管理特定空间内的用户权限和 API Key。
- **普通用户**：根据被分配的权限使用资源。

## API Key 与业务空间

API Key 与业务空间紧密绑定：

- 每个 API Key 只能归属一个地域内的一个业务空间和一个用户，不可转移。
- API Key 的可调用功能和模型限流继承自其归属业务空间的配置，与用户控制台权限无关。
- 删除 API Key 或从 RAM 控制台删除对应账号后，API Key 永久失效。将用户移出业务空间会导致其 API Key 临时失效，重新加入后恢复。

## API 调用中的 Workspace ID

在以下场景中需要提供 Workspace ID：

- **应用调用**：通过 DashScope API 或 Responses API 调用子业务空间下的应用时，需在请求中指定 Workspace ID。
- **组件 API**：百炼应用组件 API（数据连接、知识库、Prompt 模板等）的所有接口均需在业务空间上下文中调用。
- **监控统计**：模型用量数据按业务空间维度统计，不支持按账号维度直接汇总。

## 生产环境空间规划

推荐的空间划分策略：

- **按环境划分（推荐）**：为开发、测试、预发、生产环境创建独立业务空间，实现严格的环境隔离。例如 `project-dev-workspace`、`project-prod-workspace`。
- **按业务线划分**：为不同业务部门创建独立空间，便于权限和成本管理。

限流配额分配示例（总配额 1000 QPM）：

| 空间 | 配额分配 |
|------|---------|
| 生产空间 | 600 QPM（60%） |
| 测试空间 | 200 QPM（20%） |
| 开发空间 | 100 QPM（10%） |
| 预留缓冲 | 100 QPM（10%） |

## 监控与观测

业务空间是监控数据的基本聚合维度：

- **模型用量**：按业务空间统计各模型的调用量和 Token 消耗，支持按模型类型和时间范围筛选。
- **应用观测**：查看业务空间内应用的完整调用链路追踪，获取延时、Token 用量等指标。
- **外部监控集成**：高级监控数据支持通过 `workspace_id` 标签过滤，可接入 Grafana 等系统。

## 关联主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application permission management](../guides/application-permission-management.md)
- [model monitoring](../guides/model-monitoring.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application monitoring](../guides/application-monitoring.md)


