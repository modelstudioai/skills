# 业务空间

业务空间（Workspace）是阿里云百炼平台中进行精细化权限管理和阿里云账单分账的最小管理单元，用于按业务线或环境隔离模型调用权限、用户访问范围和 API Key 归属。

## 基本概念

每个业务空间按地理区域划分，单个业务空间不能跨地域存在。即使是各地域的默认业务空间，也是彼此独立的空间。百炼平台中的业务空间分为两类：

- **默认业务空间**：所有模型均可调用、调优、部署，无法设置限流或权限限制。
- **子业务空间**：支持精细化权限控制，可限制模型调用、训练和部署，并设置请求数限流和 [Token](token.md) 限流。

## 使用场景

### API 调用中的空间隔离

调用子业务空间下的应用或特定地域（德国、华北2、新加坡、日本）的模型时，必须在请求中提供 **Workspace ID**。默认业务空间的 API Key 拥有所有模型的调用权限，而子业务空间的 API Key 仅能调用该空间已授权的模型。

获取方式：在百炼控制台右上角图标处查看，目前不支持通过 API 或 CLI 查询。

### 权限管理

业务空间内围绕三种角色进行权限管理：

| 角色 | 权限范围 |
|------|----------|
| 超级管理员 | 跨空间统一管理用户权限、空间可用模型、模型限流和 API Key |
| 业务空间管理员 | 管理该特定空间内的用户权限和资源，含该空间所有页面的访问权限 |
| 普通用户 | 根据分配的权限使用资源 |

### 应用组件 API

应用组件 API（`bailian/2023-12-29`）的所有接口均需传入 `WorkspaceId` 参数。RAM 子账号必须先获取对应权限策略并加入业务空间后才能调用。

### 应用观测与数据管理

应用观测功能按业务空间隔离观测数据。数据管理功能统一管理业务空间下的大模型训练集与评测集。

### 安全与合规

推荐按环境（dev/test/prod）或业务线划分业务空间实现隔离。可将主账号总配额按比例分配给各业务空间并预留缓冲，例如总配额 1000 QPM 时分配 prod 600 / test 200 / dev 100，预留 100。

## 关键参数

| 参数 | 说明 |
|------|------|
| `WorkspaceId` | 业务空间唯一标识，调用子业务空间 API 时必传 |
| 模型调用限流 | 可按空间设置请求数限流和 [Token](token.md) 限流（仅子业务空间） |
| 模型训练授权 | 控制某模型是否可在该空间进行调优及部署（仅子业务空间） |
| 模型部署授权 | 控制某模型是否可在该空间直接部署（仅子业务空间） |

## API Key 与业务空间的关系

单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移。API Key 的可调用功能与模型限流与归属业务空间的权限保持一致。将 RAM 账号移出业务空间会使其 API Key 失效（重新加入后恢复），在 RAM 控制台删除账号则永久失效。

自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，并支持设置 IP 访问白名单。

## 关联主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [application permission management](../guides/application-permission-management.md)
- [more about models](../api/more-about-models.md)
- [application monitoring](../guides/application-monitoring.md)
- [model data overview](../guides/model-data-overview.md)
- [security and compliance](../guides/security-and-compliance.md)


