# 业务空间

业务空间（Workspace）是阿里云百炼平台中用于资源隔离、权限控制和账单分账的最小管理单元。每个业务空间归属于一个地域，不可跨地域存在，平台上的 API Key、模型调用、数据资源等均以业务空间为边界进行管理。

## 核心作用

业务空间在百炼平台中承担三项核心职责：

- **资源隔离**：不同业务空间的数据、应用、知识库等资源相互独立，互不可见。
- **权限管控**：通过角色体系（超级管理员、业务空间管理员、普通用户）实现精细化的用户和模型权限管理。
- **费用归集**：模型用量和费用按业务空间维度统计，便于多团队、多项目的成本核算。

## 权限角色

| 角色 | 权限范围 |
|------|---------|
| 超级管理员 | 跨地域、跨空间管理所有权限，包括模型调用与限流、模型调优与部署、用户管理、API Key 管理 |
| 业务空间管理员 | 管理特定业务空间内的用户权限和资源，自动拥有该空间所有页面的访问权限 |
| 普通用户 | 根据分配的权限使用资源 |

> 默认业务空间无法限制模型调用、调优和部署，所有支持的模型均可使用。

## API Key 与业务空间

- 单个 API Key 只能归属**一个地域**内的**一个业务空间**和**一个用户**，不可转移。
- API Key 的可调用功能和限流继承自所属业务空间的配置，不受用户控制台权限的影响。
- 无需为不同模型类型（文生文、文生图、语音合成等）创建不同的 API Key。
- API Key 状态会随用户被移出业务空间而失效，重新加入后可恢复。

## API 调用中的 WorkspaceId

调用百炼应用组件 API（`bailian/2023-12-29`）时，`WorkspaceId` 是大多数接口的必传参数，用于指定操作所在的业务空间。典型场景包括：

- 创建和管理数据类目、文件、连接器
- 管理 Prompt 模板、知识库
- 管理长期记忆等应用组件

RAM 用户在调用这些 API 前，需先被加入目标业务空间，并在 RAM 控制台获得 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 权限。

## 监控与用量

模型用量和监控数据按业务空间维度汇总，包括：

- 各模型的调用量和 Token 消耗
- 免费额度使用情况和"用完即停"开关
- 性能指标（调用时长、首 Token 延时、RPM、TPM）
- 告警规则和费用预警

> 用量不支持按阿里云账号维度直接统计。如需账号级汇总，需在账单详情页导出数据。

## 生产环境最佳实践

**空间规划**：
- 按环境划分（推荐）：为开发、测试、生产创建独立业务空间（如 `project-dev-workspace`、`project-prod-workspace`），实现环境隔离。
- 按业务线划分：为不同部门创建独立空间，便于权限和成本管理。

**限流策略**：
- 将主账号总配额按比例分配给各业务空间，预留缓冲应对突发流量。

**安全存储**：
- 百炼提供安全存储业务空间，支持在私有网络环境中部署应用，数据存储在客户自有的 ElasticSearch、AnalyticDB 和 OSS 中。

## 关联主题页

- [application component api reference](../api/application-component-api-reference.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


