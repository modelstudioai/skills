# 业务空间

业务空间（Workspace）是阿里云百炼平台的最小资源管理单元，用于隔离和组织模型调用权限、API Key、用户访问及监控数据。每个业务空间绑定单一地域，不可跨地域存在。

## 核心作用

业务空间在百炼平台中承担以下职责：

- **权限隔离**：以空间为边界划分模型调用权限、用户控制台访问权限和 API Key 归属。
- **资源组织**：所有应用组件 API 的请求路径均包含 `{WorkspaceId}`，数据连接、知识库、Prompt 工程等资源按空间维度管理。
- **成本管控**：监控数据和用量统计按空间维度采集，支持对单个空间设置请求数限流和 Token 限流。
- **安全边界**：支持创建安全存储业务空间，将数据存储在用户自有的私有网络资源中，实现物理级数据隔离。

## 关键特性

| 特性 | 说明 |
|------|------|
| 地域绑定 | 单个业务空间只能存在于一个地域，不可跨地域 |
| ID 格式 | `llm-xxxxxxxxxxxx` |
| 默认空间 | 每个地域自动创建一个默认业务空间，无法设置模型调用限制 |
| API Key 归属 | 一个 API Key 只能归属一个地域内的一个业务空间和一个用户 |
| 安全存储空间 | 需商务开通，数据存储在用户自有 OSS/ADB/ES 中 |

## 权限模型

业务空间内支持三种角色：

- **超级管理员**：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，可跨地域、跨空间管理所有权限。
- **业务空间管理员**：拥有该空间"权限管理"页面访问权的 RAM 用户，自动继承该空间下所有页面权限。
- **普通用户**：仅可使用被授权的资源。

空间级别可控制的权限维度包括：模型调用（含限流）、模型训练、模型部署、用户控制台功能访问。

## 常见配置场景

### 按环境划分空间

生产环境推荐为不同环境创建独立空间并分配配额：

```
project-dev-workspace   → 开发（10% 配额）
project-test-workspace  → 测试（20% 配额）
project-prod-workspace  → 生产（60% 配额）
缓冲预留               → 10% 配额
```

### API 调用接入

1. 在控制台创建或选择目标业务空间，获取 Workspace ID。
2. 在该空间下创建 API Key（自 2026 年 3 月 25 日起，北京地域新 Key 均归属主账号）。
3. 应用组件 API 请求路径中填入对应的 `WorkspaceId`。

### 模型监控与告警

监控数据按空间维度自动采集。通过 Prometheus HTTP API 查询指标时，可使用 `workspace_id` 标签筛选特定空间的数据。

## 注意事项

- 默认业务空间下所有支持的模型均可使用且无法限流，生产环境建议使用非默认空间。
- RAM 用户移出业务空间后，其名下该空间的 API Key 会立即失效（重新加入后恢复）。
- 安全存储业务空间的 OSS Bucket 或 ES 实例被释放将导致空间不可用且无法恢复。
- OpenAPI 接口权限需在 RAM 控制台单独授权（`AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`），与业务空间角色权限互相独立。

## 关联主题页

- [application permission management](../guides/application-permission-management.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application component api reference](../api/application-component-api-reference.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


