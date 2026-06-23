# application permission management

阿里云百炼平台提供基于控制台页面级和模型级的多维度权限控制体系，支持多地域、多用户的复杂组织架构。通过[业务空间](../concepts/workspace.md)作为最小管理单元，实现精细化的用户权限、模型访问和 API Key 管理。详细说明参见[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 身份与角色体系

百炼的权限管理基于三种角色：

| 角色 | 说明 | 典型账号 |
|------|------|----------|
| **超级管理员** | 可跨空间统一管理用户权限、模型、限流和 API Key | 阿里云主账号，或拥有 `AliyunBailianFullAccess` 系统策略的 RAM 用户 |
| **[业务空间](../concepts/workspace.md)管理员** | 仅管理特定[业务空间](../concepts/workspace.md)内的用户权限和资源 | 拥有某[业务空间](../concepts/workspace.md)"权限管理"页面访问权的 RAM 用户 |
| **普通用户** | 根据分配的权限使用资源 | 被授权的 RAM 用户 |

各角色的权限对比：

| 权限项 | 超级管理员 | [业务空间](../concepts/workspace.md)管理员 | 普通用户 |
|--------|-----------|---------------|---------|
| 模型调用 & 限流管理 | 支持 | 不支持 | 不支持 |
| 模型调优管理 | 支持 | 不支持 | 不支持 |
| 模型部署管理 | 支持 | 不支持 | 不支持 |
| 用户管理 | 支持 | 支持 | 不支持 |
| 页面权限管理 | 支持 | 支持 | 不支持 |
| API Key 管理 | 支持 | 支持 | 不支持 |
| 访问已授权资源 | 支持 | 支持 | 支持 |
| OpenAPI 接口权限 | 需额外授权 | 需额外授权 | 需额外授权 |

## [业务空间](../concepts/workspace.md)与权限管理

[业务空间](../concepts/workspace.md)是百炼进行精细化权限管理的最小单元。需要注意以下关键点：

- **地域隔离**：单个[业务空间](../concepts/workspace.md)不能跨地域存在，即使各地域的默认[业务空间](../concepts/workspace.md)也是独立的空间。
- **默认空间限制**：默认业务空间无法限制模型调用、调优和部署，所有模型均可使用且无法设置限流。

业务空间可管理的权限维度包括：

1. **模型调用限制**：控制某模型可否在该空间调用（控制台和 API），并设置请求数限流（QPM）和 Token 限流。
2. **模型训练限制**：控制某模型可否在该空间进行调优及调优后部署。
3. **模型部署限制**：控制某模型可否在该空间直接部署。
4. **用户控制台权限**：管理 RAM 用户能否使用该空间控制台的特定功能页面（不影响 API Key 调用）。

## API Key 权限

API Key 的管理规则如下：

- 单个 API Key 只能归属一个地域内的一个业务空间和一个用户，不可转移。
- API Key 的可调用功能和模型限流与**归属业务空间**的权限一致，不受用户控制台权限影响。
- 无需为不同模型类型（文生文、文生图、语音合成等）创建不同的 API Key。

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域的所有新创建 API Key 均归属主账号。

API Key 状态随账号操作变化的关键行为：

- **删除 API Key**：永久失效，不可恢复。
- **将账号移出业务空间**：对应 RAM 账号的 API Key 失效，重新加入后恢复。
- **在 RAM 控制台删除账号/角色**：对应 API Key 永久失效，不可恢复。
- **IP 白名单**：华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

## OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)及长期记忆等功能的 OpenAPI。如需调用，需要阿里云主账号在 RAM 控制台为 RAM 用户添加以下权限之一：

- **AliyunBailianDataFullAccess**：可调用百炼应用 API 目录下的所有 API。
- **AliyunBailianDataReadOnlyAccess**：仅可调用只读类 API（如查询文件状态、查询知识库创建任务状态等）。

## 生产环境最佳实践

根据[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)中的建议，生产环境应关注以下策略：

### 空间规划

- **按环境划分（推荐）**：为开发、测试、预发和生产环境创建独立业务空间，实现严格的环境隔离。例如 `project-dev-workspace`、`project-test-workspace`、`project-prod-workspace`。
- **按业务线划分**：为不同业务部门创建独立业务空间，便于权限和成本管理。

### 限流策略

将主账号总配额按比例分配给各业务空间，并预留缓冲。例如总配额 1000 QPM 时：

- 生产空间：600 QPM（60%）
- 测试空间：200 QPM（20%）
- 开发空间：100 QPM（10%）
- 预留缓冲：100 QPM（10%）

## 常用配置步骤

### 设置超级管理员

需要阿里云主账号或具备 `AliyunRAMFullAccess` 策略的 RAM 用户操作：

1. 在 RAM 控制台为 RAM 用户添加 `AliyunBailianFullAccess` 和 `AliyunBSSOrderAccess` 权限。
2. 通过百炼全局管理菜单即可跨地域、跨空间授权。

### 设置模型调用权限

1. 非默认业务空间需由超级管理员开通模型调用权限。
2. 控制台调用需在权限管理页签为 RAM 用户添加"模型体验-操作"、"批量推理-操作"、"模型观测-操作"等权限。
3. API 调用需在对应业务空间为 RAM 用户创建或分配 API Key。

### 设置模型调优权限

控制台调优需为 RAM 用户添加模型体验、模型调优、我的模型、模型部署、模型评测、数据管理、模型观测等操作权限。API 调优则需创建对应业务空间的 API Key。

## 账单与预付费权限

RAM 用户默认无权查看账单或购买预付费产品，需在 RAM 控制台添加权限。更多细节参见[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)原始文档。

- **AliyunBSSReadOnlyAccess**：查看阿里云所有产品的账单。
- **AliyunBSSOrderAccess**：购买阿里云所有预付费产品。

> **注意**：以上两个权限作用于阿里云所有产品而非仅限百炼，请谨慎授权。

## 常见问题

- **获取业务空间 ID**：参考应用开发文档中的"获取 Workspace ID"部分。
- **子业务空间调用模型**：无需特殊设置，使用子业务空间的 API Key 即可。
- **使用特定业务空间的应用**：API 调用时需同时设置 APP ID 和 Workspace ID。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)




