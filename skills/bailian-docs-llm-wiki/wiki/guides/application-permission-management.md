# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间级管理和资源使用能力。所有 API Key 的调用权限均继承自其归属业务空间的配置，与用户账号的控制台权限相互独立。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限开关与限流（QPM / [Token](../concepts/token.md)/s），需在业务空间维度显式开通；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持开启/关闭特定模型在业务空间内的微调能力（含 LoRA、全参微调等），并控制调优后模型的自动部署权限；默认业务空间默认全部开放 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持控制是否允许在业务空间内直接部署官方模型或调优后模型（如 vLLM、Triton 部署），该权限独立于调用与调优权限。
- **控制台页面权限**：支持按菜单项（如“模型体验”“批量推理”“模型观测”）为 RAM 用户分配操作权限，但**不影响其 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用层 OpenAPI（如知识库、Prompt 工程、长期[记忆](../concepts/memory.md)等）；该能力**不随业务空间权限自动继承** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围 | 生效层级 |
|------|------|----------|----------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 + API） | `true` / `false` | 业务空间级（超级管理员设置） |
| `qpm_limit` | 每分钟请求数上限 | ≥ 0（0 表示不限） | 业务空间级（超级管理员设置） |
| `token_per_second_limit` | 每秒 [Token](../concepts/token.md) 处理上限 | ≥ 0（0 表示不限） | 业务空间级（超级管理员设置） |
| `tuning_enabled` | 是否允许在该业务空间进行模型调优 | `true` / `false` | 业务空间级（超级管理员设置） |
| `deployment_enabled` | 是否允许在该业务空间直接部署模型 | `true` / `false` | 业务空间级（超级管理员设置） |
| `console_permission` | 控制台菜单项操作权限（如 `model_experience:operate`） | 布尔值或策略标签 | 用户级（空间管理员设置） |

> **注意**：`qpm_limit` 和 `token_per_second_limit` 仅作用于该业务空间下所有 API Key 的聚合流量，**不支持按单个 API Key 单独配置**；若需更细粒度限流，须结合网关层实现。

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一管理多空间。
   - 业务空间管理员：由超级管理员在目标空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为业务空间启用目标模型的调用、调优或部署权限 —— 此步不可跳过，否则后续用户权限配置无效。

3. **用户权限分配**  
   - 控制台权限：在业务空间「权限管理」→「用户权限」中，勾选对应菜单项（如 `模型体验-操作`）。
   - API Key 权限：在「权限管理」→「API Key 管理」中，为用户开启「创建/删除/查看本空间所有 API Key」权限；API Key 创建后即自动继承该空间的模型调用与限流策略。

4. **OpenAPI 授权（独立流程）**  
   必须在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则即使拥有业务空间权限，也无法调用 `/v1/applications/`、`/v1/knowledgebases/` 等 OpenAPI。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域（如 `cn-beijing`），跨地域空间完全独立，权限、配额、API Key 均不互通。
- **默认空间限制**：所有“默认业务空间”（系统自动创建）**无法配置模型调用/调优/部署开关及限流**，仅适用于快速试用；生产环境必须新建业务空间。
- **API Key 绑定不可变**：一个 API Key 仅归属一个地域 + 一个业务空间 + 一个用户，创建后不可迁移或解绑；华北2（北京）地域自 2026-03-25 起新 API Key 默认归属主账号。
- **权限继承关系**：API Key 的模型调用能力 = 业务空间模型开关 + 业务空间限流策略；**不受用户控制台权限影响**（例如：用户无「模型体验」权限，但仍可用其 API Key 调用模型）。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，**不包含在 `AliyunBailianFullAccess` 中**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


