# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的调用权限严格继承自其归属业务空间的模型授权策略，与用户账号的控制台权限解耦。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台交互式体验、批量推理、API 调用（含 [Token](../concepts/token.md)/请求数双维度限流）；
- **模型调优（训练）**：支持在业务空间内对指定模型进行微调（Fine-tuning）及调优后部署；
- **模型部署**：允许将支持部署的模型（如部分 SFT 后模型）直接发布为服务端点；
- **控制台页面级权限**：按菜单项（如“模型体验”“批量推理”“模型观测”）授予或禁用 UI 操作能力；
- **API-Key 全生命周期管理**：创建、查看、删除、IP 白名单设置（仅华北2地域支持）；
- **OpenAPI 接口权限**：需显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则 RAM 用户默认无权调用应用相关 OpenAPI [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)在“设置模型调用权限”小节中又指出“需保证业务空间已经为特定模型开通了[模型调用](raw/application-user-guide/application-permission-management/application-permission-management-overview.md)权限”，此处存在表述矛盾——实际行为是：**默认业务空间虽不可主动配置限制，但仍需由超级管理员显式启用模型可用性**，否则模型不可见、不可调用。开发者应以控制台实际可操作性为准，而非依赖“默认即开放”的假设。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `region` | 业务空间所属地域（如 `cn-beijing`），API Key 与业务空间强绑定于同一地域，**不支持跨地域复用** | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `workspace_id` | 业务空间唯一标识，所有权限策略（模型限流、用户授权等）均作用于该 ID 下 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `qpm_limit` / `tpm_limit` | 每分钟请求数（QPM）与每分钟 [Token](../concepts/token.md) 数（TPM）限流值，单位为整数，设为 `0` 表示禁止调用 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `ip_whitelist` | IPv4 地址或 CIDR 段列表，仅华北2（北京）地域的 API Key 支持配置 | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置；  
   - 业务空间管理员：由超级管理员在目标空间的「权限管理」页签中为 RAM 用户勾选「管理员」权限；  
   - 普通用户：由管理员分配具体模型与页面权限（如「模型体验-操作」「批量推理-操作」）。

2. **模型权限开通流程**  
   - 超级管理员在全局管理菜单 → 「模型管理」中为某业务空间启用指定模型，并设置 QPM/TPM 限流；  
   - 业务空间管理员在该空间「权限管理」→ 「用户权限」中为 RAM 用户分配对应模型的控制台操作权限；  
   - 若需 API 调用，须为该用户在空间内生成 API Key —— 其可调用模型范围与限流策略**完全继承自业务空间配置**，与用户账号权限无关。

3. **OpenAPI 调用授权**  
   必须由阿里云主账号在 RAM 控制台为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 系统策略，否则即使拥有 API Key 也无法调用应用数据、知识库等 OpenAPI [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间严格绑定单一地域，跨地域资源（如模型、API Key、账单）不可共享；  
- **默认业务空间特权缺失**：无法配置模型限流、调优开关或部署控制，建议生产环境始终使用显式创建的非默认空间；  
- **API Key 不可迁移**：单个 API Key 仅归属一个地域+一个业务空间+一个用户，创建后不可转移或跨空间复用；  
- **主账号特权例外**：AI 安全护栏、模型监控、应用观测等功能开通必须使用阿里云主账号操作，RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法完成 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)；  
- **账单与预付费权限独立**：RAM 用户需额外授予 `AliyunBSSReadOnlyAccess`（查账单）或 `AliyunBSSOrderAccess`（购预付费）策略，该权限不属于百炼原生权限体系。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


