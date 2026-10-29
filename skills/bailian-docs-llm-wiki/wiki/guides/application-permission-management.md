# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、模型级的精细化控制能力，支持对模型调用、调优、部署、API Key 及控制台页面访问等维度进行独立授权与限流。该体系基于阿里云 RAM 架构设计，兼容主账号与子账号（RAM 用户）协同管理，适用于开发、测试、生产等多环境隔离场景。详细背景请参阅 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限管理覆盖以下核心能力：

- **模型调用控制**：按业务空间粒度开关特定模型的调用权限（含控制台体验与 OpenAPI 调用），并支持设置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）控制**：控制是否允许在指定业务空间内对支持调优的模型执行数据准备、训练、评测、快照管理等全流程操作。
- **模型部署控制**：控制是否允许将调优后的模型或基础模型直接部署为可调用服务。
- **控制台页面级权限**：为 RAM 用户分配具体菜单项（如“模型体验-操作”“批量推理-操作”“模型调优-操作”等）的查看与操作权限。
- **API Key 全生命周期管理**：包括创建、删除、查看、IP 白名单设置（仅华北2北京地域支持），且 Key 权限严格继承归属业务空间的模型策略。
- **OpenAPI 接口权限**：需显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 等 RAM 策略，否则默认无权调用应用相关 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)等接口）——详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限配置（调用、调优、部署均全量开放且不可限流），生产环境应避免使用，默认空间仅用于快速体验。此限制在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确强调。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `workspace_id` | 业务空间唯一标识符，调用 API 时必须传入（与 `app_id` 配合使用） | 由百炼控制台生成，不可修改；获取方式见 [获取Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `qpm_limit` / `token_limit` | 模型级限流阈值，单位分别为 QPM 和 tokens/minute | 仅对非默认业务空间生效；超级管理员在全局管理菜单中配置 |
| `api_key` | 绑定至单一地域+单一业务空间+单一 RAM 用户的凭证 | 不可跨空间/跨用户迁移；状态随用户移出空间自动失效（重新加入后恢复）；华北2（北京）新创建 Key 默认归属主账号（自2026-03-25起） |
| `ram_policy` | 控制 OpenAPI 访问权限的 RAM 策略，如 `AliyunBailianDataFullAccess` | 必须由阿里云主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 显式授予；普通 RAM 用户无法自助开通 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 管理所有地域/空间。  
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中授予「管理员」权限，仅可管理该空间内用户与资源。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为**目标业务空间**启用指定模型的调用、调优或部署权限（默认空间跳过此步）。该配置是后续用户级权限生效的前提 —— 参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的“业务空间权限”表格。

3. **用户级权限分配**  
   - **控制台使用**：在业务空间「权限管理」页签中，为 RAM 用户勾选对应功能模块权限（如“模型体验-操作”“模型调优-操作”）。  
   - **API 调用**：为该用户在目标业务空间创建 API Key（需已授予 `API-Key 管理` 权限），Key 自动继承空间级模型策略。

4. **OpenAPI 授权（独立步骤）**  
   若需调用应用类 OpenAPI（如 `/v1/knowledge_bases`），必须由主账号在 RAM 控制台为该 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略 —— 此权限**不依赖**业务空间管理员配置，且未在控制台 UI 中暴露。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域资源不可共享；同一业务空间名称在不同地域代表完全独立的实体。
- **默认空间限制**：默认业务空间无法配置模型权限与限流，所有模型默认全开，**严禁用于生产环境**。
- **API Key 绑定刚性**：Key 一旦创建即锁定地域、业务空间、用户三元组，不可解绑或转移；删除用户或将其移出空间将导致其所有 Key 失效（主账号 Key 除外）。
- **页面权限 ≠ API 权限**：用户在控制台的菜单可见性/操作权限（如“模型调优-操作”）**不影响**其 API Key 的调用能力；API 调用权限完全由业务空间模型策略 + RAM OpenAPI 策略共同决定。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需主账号在 RAM 控制台单独授权，不包含在百炼原生策略中。

> **注意**：文档中关于“OpenAPI 接口权限”的描述存在关键矛盾：正文称“RAM 用户默认无权调用……需要主账号在 RAM 控制台添加权限”，但表格中又将该项列为“超级管理员/业务空间管理员/普通用户”三列均为“不支持”。实际行为以正文为准——即**所有 RAM 用户（无论角色）均需额外 RAM 策略才能调用应用 OpenAPI**，该权限不随业务空间管理员身份自动授予。此不一致已在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中体现，开发者应以 RAM 策略配置为唯一依据。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


