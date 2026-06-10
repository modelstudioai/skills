# application permission management

阿里云百炼平台提供基于控制台页面级和模型级的多维度权限控制体系，通过[业务空间](../concepts/workspace.md)（Workspace）作为最小管理单元，实现精细化的用户、模型和 API Key 权限管理。该体系支持多地域、多用户的复杂组织架构，满足从开发到生产环境的权限隔离需求。

## 角色与权限模型

百炼的权限管理基于三种角色，详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)：

| 权限项 | 超级管理员 | [业务空间](../concepts/workspace.md)管理员 | 普通用户 |
|--------|-----------|--------------|---------|
| 模型调用 & 限流管理 | ✅ | ❌ | ❌ |
| 模型调优 / 部署管理 | ✅ | ❌ | ❌ |
| 用户管理 | ✅ | ✅ | ❌ |
| 用户可用页面管理 | ✅ | ✅ | ❌ |
| API Key 管理 | ✅ | ✅ | ❌ |
| 访问被授权的资源 | ✅ | ✅ | ✅ |
| OpenAPI 接口权限 | 需主账号在 RAM 控制台单独授权 | 需主账号在 RAM 控制台单独授权 | 需主账号在 RAM 控制台单独授权 |

### 超级管理员

包含两类账号：
- **阿里云主账号**：天然拥有最高权限。
- **拥有 `AliyunBailianFullAccess` 策略的 RAM 用户**：可跨地域、跨空间管理所有权限（OpenAPI 接口权限除外）。

### [业务空间](../concepts/workspace.md)管理员

拥有某个[业务空间](../concepts/workspace.md)**权限管理**页面访问权的 RAM 用户，管理员权限自动包含该空间下所有页面的访问权限。

## [业务空间](../concepts/workspace.md)权限管理

[业务空间](../concepts/workspace.md)按地理区域划分，**单个[业务空间](../concepts/workspace.md)不能跨地域存在**。根据 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 文档，[业务空间](../concepts/workspace.md)支持以下权限维度：

- **模型调用控制**：管理模型是否可在该空间调用（控制台及 API），并设置请求数限流和 Token 限流。
- **模型训练控制**：管理模型是否可进行调优及调优后部署。
- **模型部署控制**：管理模型是否可直接部署。
- **用户控制台权限**：管理 RAM 用户对该空间控制台功能的访问权限。

> **注意**：默认[业务空间](../concepts/workspace.md)无法设置模型调用、调优和部署的限制，所有支持的模型均可使用且无法限流。

## API Key 权限

- 单个 API Key 只能归属**一个地域**内的**一个业务空间**和**一个用户**，不可转移。
- API Key 的可调用功能和限流与归属业务空间一致，**不受用户控制台权限管理影响**。
- 无需为不同模型类型（文生文、文生图、语音合成等）创建不同的 API Key。

API Key 状态变更规则：

| 操作 | 主账号 API Key | RAM 账号 API Key |
|------|--------------|-----------------|
| 主动删除 | 失效，不可恢复 | 失效，不可恢复 |
| 账号移出业务空间 | — | 失效（重新加入后恢复） |
| RAM 控制台删除账号 | — | 失效，不可恢复 |

> **注意**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号。

## OpenAPI 接口权限

RAM 用户默认**无权**调用百炼应用的数据、知识库、Prompt 工程及长期记忆等功能的 OpenAPI。需由阿里云主账号在 RAM 控制台授予以下权限之一：

- **`AliyunBailianDataFullAccess`**：可调用百炼应用 API 目录下的所有 API。
- **`AliyunBailianDataReadOnlyAccess`**：仅可调用只读类 API。

## 常用配置指南

### 设置超级管理员

1. 在 RAM 控制台为 RAM 用户添加 `AliyunBailianFullAccess` 和 `AliyunBSSOrderAccess` 权限。
2. 通过全局管理菜单为任意 RAM 用户授权任意地域、任意空间的权限。

### 设置模型调用权限

1. 非默认业务空间需由超级管理员开通特定模型的调用权限。
2. **控制台调用**：为 RAM 用户添加「模型体验-操作」、「批量推理-操作」、「模型观测-操作」页面权限。
3. **API 调用**：在对应业务空间为 RAM 用户创建或分配 API Key。

### 设置模型调优权限

需为 RAM 用户添加以下页面权限：模型体验-操作、模型调优-操作、我的模型-操作、模型部署-操作、模型评测-操作、数据管理-操作、模型观测-操作。

## 生产环境最佳实践

参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中推荐的策略：

### 空间规划

- **按环境划分（推荐）**：为开发、测试、生产环境创建独立空间，如 `project-dev-workspace`、`project-prod-workspace`。
- **按业务线划分**：为不同部门创建独立空间，便于权限和成本管理。

### 限流策略

将主账号总配额按比例分配给各业务空间，建议预留 10% 作为缓冲。例如总配额 1000 QPM：生产 600 QPM（60%）、测试 200 QPM（20%）、开发 100 QPM（10%）、缓冲 100 QPM（10%）。

## 账单与预付费权限

RAM 用户默认无权查看账单或购买预付费产品，需在 RAM 控制台添加：

- **`AliyunBSSReadOnlyAccess`**：查看所有阿里云产品账单。
- **`AliyunBSSOrderAccess`**：购买所有阿里云预付费产品。

> **注意**：以上两项权限作用于阿里云所有产品（不仅限百炼），请谨慎授权。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)






