# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系围绕超级管理员、业务空间管理员和普通用户三级角色展开，支持控制台操作与 API 调用双路径管控，并与阿里云 RAM 和账单系统深度集成。所有权限策略均以业务空间为作用域，**不支持跨地域共享**。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的启用/禁用控制，并可配置 QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流。默认业务空间无法设置此限制，所有模型均可无限制调用 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持开启/关闭特定模型在业务空间内的微调能力（含 LoRA、全参微调等），以及调优后模型的自动部署权限。该能力仅对非默认业务空间生效，且需超级管理员先行授权 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **[模型部署](../concepts/model-deployment.md)**：支持控制模型是否可在该业务空间内直接部署为在线服务（如 API Endpoint）。部署权限独立于调用权限，需显式开启。
- **控制台页面级权限**：支持按菜单项（如“模型体验”“批量推理”“模型观测”）为 RAM 用户分配可见性与操作权，但**不影响其 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用层 OpenAPI（如知识库、Prompt 工程、[长期记忆](../concepts/memory.md)相关接口），必须由主账号在 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围 | 作用域 |
|------|------|----------|--------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 & API） | `true` / `false` | 业务空间级（超级管理员配置） |
| `qpm_limit` | 每分钟最大请求数 | ≥ 0（0 表示不限流） | 业务空间 + 模型粒度 |
| `token_limit_per_minute` | 每分钟最大 [Token](../concepts/token.md) 消耗量 | ≥ 0（0 表示不限流） | 业务空间 + 模型粒度 |
| `tuning_enabled` | 是否允许对该模型执行调优任务 | `true` / `false` | 业务空间 + 模型粒度 |
| `deployment_enabled` | 是否允许将该模型（含调优后版本）部署为服务 | `true` / `false` | 业务空间 + 模型粒度 |
| `console_permission` | 控制台菜单项操作权限（如 `model-experience:operate`） | 布尔值 | 用户 + 业务空间粒度 |

> **注意**：`qpm_limit` 和 `token_limit_per_minute` 对 API Key 生效，但**不区分调用来源（SDK/HTTP/API Key）**；而控制台页面权限仅影响 UI 可见性与按钮可用性，与 API Key 实际能力无关。

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或具备 `AliyunBailianFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 为指定 RAM 用户附加该策略。  
   - 业务空间管理员：由超级管理员或同空间其他管理员，在百炼控制台「权限管理」页签中为 RAM 用户勾选「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)）中为业务空间启用目标模型的调用、调优或部署能力 —— 此步不可跳过，否则下游用户权限配置无效。

3. **用户级权限分配**  
   - 控制台权限：在业务空间「权限管理」→「用户权限」中，为 RAM 用户勾选对应菜单项（如 `模型体验-操作`）。  
   - API 调用权限：为用户创建 API Key（归属该业务空间），其能力继承自业务空间模型配置，无需额外策略。

4. **OpenAPI 权限开通**  
   必须由阿里云主账号在 RAM 控制台为 RAM 用户单独添加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess`，**业务空间内配置对此无影响**。

## 限制和注意事项

- **地域隔离强制约束**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域资源（如 API Key、模型限流配置）不可复用或迁移。同一业务名称在不同地域视为完全独立的空间。
- **默认业务空间无权限控制能力**：所有模型默认开放调用、调优、部署，且无法配置限流。生产环境务必使用**显式创建的业务空间**。
- **API Key 绑定不可变**：一个 API Key 仅归属一个地域、一个业务空间、一个 RAM 用户，创建后不可转移或解绑。华北2（北京）地域自 2026-03-25 起，新 API Key 默认归属主账号。
- **控制台权限 ≠ API 权限**：为用户关闭「模型体验-操作」仅隐藏控制台入口，若其持有有效 API Key，仍可调用对应模型接口。
- **账单与预付费权限需独立配置**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台手动授予，百炼控制台不提供快捷入口。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


