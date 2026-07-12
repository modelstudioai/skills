# 业务空间（Workspace）

业务空间（Workspace）是阿里云百炼平台进行精细化权限管理、资源隔离和阿里云账单分账的**最小管理单元**。所有 OpenAPI 调用都需传入对应的 `WorkspaceId`，平台的模型授权、限流、用量统计、数据集管理等能力均以业务空间为边界组织。

## 核心特性

- **地域隔离**：百炼按地理区域划分资源，**单个业务空间不能跨地域存在**。即使是各地域的默认业务空间，也是彼此独立的不同空间。
- **最小管理单元**：权限（模型、用户、页面）与成本分账都以业务空间为粒度。
- **默认业务空间的特殊性**：默认业务空间无法设置模型调用/训练/部署的精细化限制——所有模型均可调用、调优、部署，且无法限流；其 API Key 拥有所有模型的调用权限。

## 在不同场景中的使用

### 1. 权限管理

业务空间是权限体系的核心边界，围绕三种角色展开：

- **超级管理员**：阿里云主账号，或拥有 `AliyunBailianFullAccess` 系统策略的 RAM 用户，可跨空间统一管理用户权限、可用模型、模型限流和 API Key。
- **业务空间管理员**：拥有某个业务空间「权限管理」页面访问权的 RAM 用户，仅管理该空间内的用户与资源，其权限包含该空间下所有页面。
- **普通用户**：按分配的权限使用被授权的空间、页面与资源。

非默认业务空间可在空间内进行三类精细化授权：

| 权限项 | 控制范围 |
| --- | --- |
| 限制模型调用 | 是否可调用（控制台 & API）+ 请求数限流 + Token 限流 |
| 限制模型训练 | 是否可调优及调优后部署 |
| 限制模型部署 | 是否可直接部署 |

> OpenAPI 接口权限**不通过**业务空间角色授予，必须由阿里云主账号在 RAM 控制台为 RAM 用户添加专用系统策略（如 `AliyunBailianDataFullAccess` / `AliyunBailianDataReadOnlyAccess`）。

### 2. API Key 归属

单个 API Key 只能归属**一个地域内的一个业务空间和一个用户**，且不能转移。API Key 可调用的功能和模型限流与**归属业务空间**的权限保持一致，不受用户控制台权限管理的影响。将 RAM 账号移出业务空间会使其 API Key 失效（重新加入后恢复）。

### 3. 模型调用与子业务空间

- 默认业务空间的 API Key 拥有所有模型调用权限。
- 使用子业务空间调用时，必须用**子业务空间自身的 API Key**；调用标准模型（如 `qwen-plus`）前需先为该空间设置模型调用权限。
- 在百炼上调优并部署的模型无需额外授权，但**仅能由其所在空间的 API Key 调用**。
- 新加坡等地域调用时需将 Endpoint 中的 `WorkspaceId` 替换为实际值。

### 4. OpenAPI 调用

应用组件 API（`bailian/2023-12-29`，数据连接、知识库、Prompt 模板、长期记忆等）所有接口均需传入 `WorkspaceId`。RAM 子账号需先获取对应权限策略并加入业务空间后才能调用。类目等资源也以空间为限额单位（如每空间最多 500 个类目）。

### 5. 监控与用量统计

- **应用观测**：端到端查看业务空间内应用（智能体、工作流、高代码应用）的调用链路与指标。若应用不属于当前业务空间，则不会出现在可观测列表中。
- **模型用量统计**：用量数据按**业务空间维度**统计（不支持按阿里云账号维度），可据此精细化管理模型成本。

### 6. 数据集管理

数据管理功能统一管理业务空间下的大模型训练集与评测集（该能力目前仅适用于华北2（北京）地域）。

## 关键参数与实践建议

- **`WorkspaceId`**：OpenAPI 调用的必填参数，标识目标业务空间。
- **空间规划**：推荐按环境（dev/test/prod）或业务线划分业务空间实现隔离，便于权限与成本管理。
- **限流分配**：将主账号总配额按比例分配给各空间并预留缓冲。例如总配额 1000 QPM，可分配 prod 600 / test 200 / dev 100，预留 100。

## 关联主题页

- [application component api reference](../api/application-component-api-reference.md)
- [application permission management](../guides/application-permission-management.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)
- [security and compliance](../guides/security-and-compliance.md)
- [model data overview](../guides/model-data-overview.md)



