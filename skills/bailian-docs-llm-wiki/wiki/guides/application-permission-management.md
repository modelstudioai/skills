# application permission management

百炼平台的权限管理基于“业务空间”这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别承担全局管理、空间级管理和资源使用职责。所有 API Key 的调用能力严格继承自其归属业务空间的模型权限配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心模型能力：
- **模型调用**：支持对文生文、文生图、语音合成等各类模型的控制台体验与 OpenAPI 调用权限控制（含 QPM/TPM 限流）；
- **模型调优（训练）**：支持在指定业务空间内启用/禁用模型微调（Fine-tuning）、LoRA 训练等功能；
- **模型部署**：支持控制是否允许将调优后的模型或第三方模型直接部署为服务；
- **控制台页面权限**：可精细化控制 RAM 用户在业务空间内可见及可操作的菜单项（如“模型体验”“批量推理”“模型观测”等）；
- **OpenAPI 接口权限**：需通过 RAM 策略显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 才能调用应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)相关接口）[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限限制（调用、调优、部署均全量开放），生产环境应避免使用，默认空间仅适用于快速试用 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 来源层级 |
|------|------|----------|
| `model_call_enabled` | 控制某模型是否可在该业务空间被调用（控制台 & API） | 业务空间级（超级管理员设置） |
| `qpm_limit`, `tpm_limit` | 每分钟请求数、每分钟 Token 数限流阈值，作用于模型调用链路 | 业务空间级（超级管理员设置） |
| `fine_tuning_enabled` | 控制某模型是否可在该业务空间启动调优任务 | 业务空间级（超级管理员设置） |
| `deployment_enabled` | 控制某模型是否可在该业务空间直接部署为服务 | 业务空间级（超级管理员设置） |
| `console_permission` | 如 `model_experience:operate`、`batch_inference:operate` 等，控制用户在控制台的操作能力 | 用户级（业务空间管理员设置） |
| `api_key_scope` | 单个 API Key 严格绑定一个地域 + 一个业务空间 + 一个 RAM 用户，不可迁移 | API Key 级（自动继承空间权限） |

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户担任，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置；  
   - 业务空间管理员：由超级管理员在对应业务空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

2. **模型权限开通**  
   - 超级管理员进入「全局管理 > 业务空间 > 模型管理」，为指定空间启用目标模型的「调用」「调优」「部署」开关，并配置限流值。

3. **用户权限分配**  
   - 业务空间管理员进入该空间「权限管理 > 用户权限」，为 RAM 用户勾选所需控制台功能（如 `模型体验-操作`、`批量推理-操作`）；  
   - 同一页面中可为用户分配「API Key 管理」权限，使其可创建/删除本空间内 API Key。

4. **API 调用准备**  
   - 确保目标 RAM 用户已在该业务空间拥有有效 API Key；  
   - 若需调用应用层 OpenAPI（如 `/v1/knowledge_bases`），必须由主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或只读策略 —— 此权限**不随业务空间模型权限自动继承**。

## 限制和注意事项

- **地域隔离性**：业务空间严格按地域划分，北京地域的 `prod-workspace` 与新加坡地域的同名空间完全独立，权限、配额、API Key 均不互通；
- **API Key 绑定不可变**：单个 API Key 创建后无法变更所属地域、业务空间或用户；2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号；
- **控制台权限 ≠ API 权限**：用户在控制台被禁止访问「模型调优」页面，不代表其 API Key 无法调用训练接口；反之亦然 —— 二者权限体系正交；
- **OpenAPI 权限需显式授权**：即使某模型已在业务空间启用调用，RAM 用户仍需主账号在 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 才能调用 `/v1/applications` 等应用层接口 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)；
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台独立配置，不包含在百炼内置策略中。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


