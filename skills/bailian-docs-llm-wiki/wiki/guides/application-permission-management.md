# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台功能访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别承担全局管理、空间级管理和资源使用职责。所有权限策略均与业务空间强绑定，且 API Key 的行为严格继承其归属空间的模型与限流配置。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台与 OpenAPI 层面对指定模型的调用许可、QPM（每分钟请求数）与 [Token](../concepts/token.md) 限流；
- **模型调优（训练）**：允许/禁止在业务空间内对支持调优的模型进行微调、LoRA 训练等操作；
- **模型部署**：控制是否允许将调优后的模型或基础模型直接部署为服务；
- **控制台页面级权限**：按菜单项（如“模型体验”“批量推理”“模型观测”）授予 RAM 用户可见性与操作权；
- **API Key 全生命周期管理**：创建、删除、查看、IP 白名单设置（仅限华北2北京地域）；
- **OpenAPI 接口权限**：通过 RAM 策略（如 `AliyunBailianDataFullAccess`）控制应用层数据、知识库、Prompt 工程等接口的调用能力。

> **注意**：默认业务空间不支持任何模型级权限限制（调用、调优、部署均全开），如需精细化管控，必须新建非默认业务空间。详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用 | `true` / `false`（由超级管理员在全局管理菜单中配置） |
| `qpm_limit` | 每分钟请求上限 | ≥ 0；0 表示不限流；默认业务空间不可设 |
| `token_limit_per_minute` | 每分钟 [Token](../concepts/token.md) 总消耗上限 | ≥ 0；0 表示不限流；默认业务空间不可设 |
| `api_key_ip_whitelist` | API Key 绑定的 IPv4/IPv6 白名单 | 仅华北2（北京）地域支持；格式为 CIDR 或单 IP，最多 10 条 |
| `workspace_region` | 业务空间所属地域 | 不可跨地域共享；同一地域内空间相互隔离 |

所有模型级限流参数均作用于**整个业务空间**，而非单个用户或 API Key。API Key 的实际调用能力完全继承自其归属空间的配置，与用户账号的控制台权限无关。

## 使用方式

### 1. 角色配置
- **超级管理员**：需主账号或已授予 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 中统一管理多空间模型、用户与 API Key。  
- **业务空间管理员**：由超级管理员或同空间其他管理员，在控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，获得该空间内用户、页面、模型调用等管理权。  
- **普通用户**：仅能使用被显式授权的控制台功能与模型；其 API Key 调用能力取决于空间级模型开关与限流策略，无需额外赋权。

### 2. 模型权限开通流程
1. 超级管理员在全局管理菜单中为业务空间启用目标模型的「调用」「调优」或「部署」权限（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）；  
2. 业务空间管理员在「权限管理」页签中为用户分配对应控制台操作权限（如「模型体验-操作」）；  
3. 若需 API 调用，须为该用户在空间内创建 API Key —— 此 Key 自动继承空间模型开关与限流配置，无需重复设置。

### 3. OpenAPI 权限开通
RAM 用户默认无权调用应用层 OpenAPI（如知识库、Prompt 工程）。需主账号在 [RAM 控制台](https://ram.console.aliyun.com/users) 显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。该策略独立于百炼控制台权限，必须单独配置。详情见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格绑定单一地域，跨地域资源（如模型、API Key、账单）不可共享。北京、新加坡、弗吉尼亚、中国香港等地域的默认空间互为独立实体。
- **API Key 不可迁移**：一个 API Key 仅归属一个地域内的一个业务空间与一个用户，创建后无法转移至其他空间或用户。
- **默认空间无权限控制**：所有模型在默认业务空间中均默认开放调用、调优、部署，且不支持限流配置。生产环境务必使用新建的非默认空间。
- **主账号特权**：AI 安全护栏、模型监控、应用观测等功能的首次开通，以及 OpenAPI 权限、账单与预付费产品管理，**必须由阿里云主账号操作**；RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法替代完成（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域所有新创建 API Key 均归属主账号；且仅该地域支持 IP 白名单功能。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


