# application permission management

阿里云百炼平台提供基于业务空间的多维度权限管理体系，涵盖控制台页面级、模型级和 API 级的精细化权限控制。通过业务空间隔离与三级角色模型（超级管理员、业务空间管理员、普通用户），可以满足多地域、多用户的复杂组织架构需求。详细说明请参考[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 身份与角色体系

百炼权限管理基于三种角色，各角色权限范围逐级递减：

| 角色 | 权限范围 | 身份要求 |
|------|---------|---------|
| **超级管理员** | 跨空间管理用户、模型、限流和 API Key | 阿里云主账号，或拥有 `AliyunBailianFullAccess` 系统策略的 RAM 用户 |
| **业务空间管理员** | 管理特定业务空间内的用户权限和资源 | 拥有该空间"权限管理"页面访问权限的 RAM 用户 |
| **普通用户** | 使用被授权的空间、页面和资源 | 被分配到业务空间的 RAM 用户 |

超级管理员可通过百炼的全局管理菜单进行多业务空间管理，包括新建空间、模型管理与限流、用户管理和 API Key 管理。

> **注意**：开通 AI 安全护栏服务、模型监控、应用观测等功能，建议使用阿里云主账号在控制台进行一次性授权。

## 业务空间权限管理

业务空间是百炼进行精细化权限管理的最小管理单元。单个业务空间不能跨地域存在，即使各个地域的默认业务空间也是不同的空间。

### 权限能力矩阵

| 业务空间权限 | 超级管理员 | 业务空间管理员 | 普通用户 |
|------------|-----------|-------------|---------|
| 允许特定模型调用 & 限流 | 支持 | 不支持 | 不支持 |
| 允许特定模型调优 | 支持 | 不支持 | 不支持 |
| 允许特定模型部署 | 支持 | 不支持 | 不支持 |
| 用户管理 | 支持 | 支持 | 不支持 |
| 用户可用页面管理 | 支持 | 支持 | 不支持 |
| API Key 管理 | 支持 | 支持 | 不支持 |
| 访问/使用被授权的资源 | 支持 | 支持 | 支持 |
| OpenAPI 接口权限 | 需额外授权 | 需额外授权 | 需额外授权 |

### 模型权限控制

在非默认业务空间中，超级管理员可以对模型进行以下维度的控制：

- **限制模型调用**：控制模型是否可在该空间调用（控制台和 API），并设置请求数限流和 Token 限流
- **限制模型训练**：控制模型是否可在该空间进行调优和调优后部署
- **限制模型部署**：控制模型是否可在该空间直接部署

> **注意**：默认业务空间无法设置上述限制，所有模型均可调用且无法限流。

### 用户控制台权限

超级管理员和业务空间管理员可管理 RAM 用户对该空间控制台功能的访问权限，但无法限制归属该用户的 API Key 的调用权限。如需了解完整的权限设置方式，请参考[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)中的常用设置部分。

## API Key 权限

API Key 的权限特点：

- 单个 API Key 只能归属一个地域内的一个业务空间和一个用户，且不能转移
- API Key 可调用的功能和模型限流与归属业务空间的权限保持一致
- API Key 不受用户控制台权限管理的影响
- 无需为不同模型（文生文、文生图、语音合成）创建不同的 API Key

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

### API Key 状态变化

| 触发操作 | 主账号的 API Key | RAM 账号的 API Key |
|---------|----------------|-------------------|
| 主动删除 API Key | 失效，不可恢复 | 失效，不可恢复 |
| 将账号移出业务空间 | -- | 失效（重新加入后恢复） |
| 在 RAM 控制台删除账号/角色 | -- | 失效，不可恢复 |
| 设置 IP 访问白名单 | 华北2（北京）支持 | 华北2（北京）支持 |

## OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)及长期记忆等功能的 OpenAPI。若需调用，需要阿里云主账号在 RAM 控制台为 RAM 用户添加以下权限之一：

- **AliyunBailianDataFullAccess**：可调用百炼应用 API 目录下的所有 API
- **AliyunBailianDataReadOnlyAccess**：可调用百炼应用 API 目录下的只读类 API

## 生产环境实践建议

### 空间规划策略

- **按环境划分（推荐）**：为开发、测试、预发和生产环境创建独立的业务空间，实现严格的环境隔离
  - `project-dev-workspace` / `project-test-workspace` / `project-prod-workspace`
- **按业务线划分**：为不同业务部门创建独立的业务空间，便于权限和成本管理

### 限流策略

将主账号总配额按比例分配给各业务空间，并预留缓冲以应对突发流量。例如总配额 1000 QPM 时：

| 空间 | 配额 | 占比 |
|-----|------|-----|
| `project-prod-workspace` | 600 QPM | 60% |
| `project-test-workspace` | 200 QPM | 20% |
| `project-dev-workspace` | 100 QPM | 10% |
| 预留缓冲 | 100 QPM | 10% |

## 账单与预付费权限

RAM 用户默认无权查看阿里云账单和购买预付费产品。如需开通，需在 RAM 控制台添加对应权限：

- **AliyunBSSReadOnlyAccess**：查看阿里云所有产品的账单
- **AliyunBSSOrderAccess**：购买阿里云所有预付费产品

> **注意**：以上权限将授予 RAM 用户查看或购买阿里云所有产品的相关权限，请谨慎授权。

## 常用配置步骤

1. **设置超级管理员**：在 RAM 控制台为 RAM 用户添加 `AliyunBailianFullAccess` 和 `AliyunBSSOrderAccess` 权限
2. **设置业务空间管理员**：在百炼控制台权限管理页签内为 RAM 用户添加管理员权限
3. **设置模型调用权限**：确保业务空间已开通模型调用权限，并为用户添加"模型体验-操作"等控制台权限，或分配 API Key
4. **设置模型调优权限**：开通模型调优权限后，为用户添加模型体验、模型调优、我的模型、模型部署、模型评测、数据管理和模型观测等操作权限

更多配置细节请参考[权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)原始文档。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


