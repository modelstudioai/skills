# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与职责分离。所有权限策略均与业务空间绑定，且受地域约束，不支持跨地域复用。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用**：控制特定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持请求数（QPM）与 [Token](../concepts/token.md) 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型调优（训练）**：控制是否允许在业务空间内对指定模型执行微调（Fine-tuning），以及调优后是否允许部署（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型部署**：控制是否允许直接将支持部署的模型发布为服务实例。
- **控制台页面权限**：按菜单粒度控制 RAM 用户可访问的控制台功能（如“模型体验”“批量推理”“模型观测”等），但**不影响其 API Key 的调用能力**。
- **API Key 全生命周期管理**：包括创建、查看、删除及 IP 白名单设置（仅华北2北京地域支持），且单个 API Key 严格绑定一个地域+一个业务空间+一个用户（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间（Default Workspace）**无法配置任何模型级权限限制**（调用、调优、部署均无限制），也不支持限流；生产环境应避免使用默认空间。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `地域（Region）` | 业务空间与 API Key 均强绑定地域，不可跨地域共享或迁移 | 华北2（北京）、新加坡、弗吉尼亚、中国香港等独立空间 |
| `QPM 限流` | 每分钟最大请求数，作用于模型级调用（控制台 & API） | 需超级管理员在全局管理菜单中为业务空间配置 |
| `Token 限流` | 每分钟最大 [Token](../concepts/token.md) 消耗量，作用于模型级调用 | 同上，与 QPM 独立配置 |
| `API Key 归属` | 每个 API Key 仅归属一个业务空间和一个用户，不可转移 | 自 2026-03-25 起，华北2（北京）新创建的 API Key 默认归属主账号 |
| `IP 白名单` | 仅华北2（北京）地域的 API Key 支持设置 | 控制台权限管理页签中配置，不影响其他地域 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略（参考 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“设置超级管理员”章节）。
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”权限。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)）中为业务空间启用目标模型的“调用”“调优”或“部署”开关——此操作**独立于用户权限配置**，未开通则后续用户授权无效。

3. **用户级控制台权限分配**  
   在业务空间内进入 **权限管理 → 用户管理 → 编辑用户 → 权限配置**，勾选对应功能模块（如“模型体验-操作”“批量推理-操作”）。

4. **API 调用授权**  
   - 创建 API Key：在 **权限管理 → API Key 管理** 中为用户生成 Key（需已授予“API-Key 管理”权限）；
   - OpenAPI 权限：若需调用应用数据、知识库等 OpenAPI，必须由主账号在 RAM 控制台额外授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“OpenAPI 接口权限”章节）。

## 限制和注意事项

- **地域隔离刚性**：业务空间、API Key、模型限流策略均不可跨地域生效；例如在北京空间配置的 QPM 限流，对新加坡空间完全无效。
- **默认空间无权限控制能力**：默认业务空间无法设置模型调用/调优/部署开关，也无法配置限流，**严禁用于生产环境**。
- **API Key 权限 ≠ 账号控制台权限**：用户被禁止访问控制台某页面（如“模型调优”），**不影响其 API Key 调用已开通模型的能力**；反之亦然。
- **OpenAPI 权限需显式授予**：RAM 用户默认无权调用任何应用类 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt.md)），必须由主账号在 RAM 控制台单独授权策略（`AliyunBailianData*Access`），该策略与百炼控制台内的权限配置完全解耦。
- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台配置，**不在百炼控制台内管理**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


