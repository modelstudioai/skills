# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保生产环境隔离性与安全合规性。所有权限策略均与阿里云 RAM 深度集成，需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：

- **模型调用控制**：支持对指定模型开启/关闭调用权限（控制台 & API），并设置请求数（QPM）和 [Token](../concepts/token.md) 限流；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）控制**：支持控制模型是否可在该业务空间进行调优（Fine-tuning）及调优后部署；默认业务空间不限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型直接部署控制**：支持控制模型是否可在该业务空间直接部署为服务。
- **控制台页面级权限**：支持为 RAM 用户分配特定功能模块（如“模型体验-操作”“批量推理-操作”“模型观测-操作”）的访问与操作权限。
- **API Key 全生命周期管理**：支持创建、删除、查看归属本空间的所有 API Key，并可配置 IP 白名单（仅华北2（北京）地域支持）。
- **OpenAPI 接口权限**：通过 RAM 策略控制应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt.md)、[长期记忆](../concepts/memory.md)等）的读写访问能力，需显式授权 [AliyunBailianDataFullAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailiandatafullaccess) 或 [AliyunBailianDataReadOnlyAccess](https://help.aliyun.com/zh/ram/developer-reference/aliyunbailiandatareadonlyaccess) [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：`OpenAPI 接口权限` 无法通过百炼控制台配置，必须由阿里云主账号在 RAM 控制台完成授权；且该权限与业务空间内用户控制台权限完全解耦——即使用户无控制台访问权，只要其 API Key 有效且具备对应 RAM 策略，仍可调用 OpenAPI。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `业务空间（Workspace）` | 权限管理最小单元，**严格绑定单一地域**，不可跨地域存在；不同地域的同名默认空间实为独立实体。 | 单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可迁移。 |
| `QPM / Token 限流` | 按模型粒度配置，作用于该业务空间内所有调用来源（控制台 + API）。 | 默认业务空间不支持设置限流。 |
| `API Key IP 白名单` | 仅华北2（北京）地域支持；白名单生效后，仅允许列表内 IP 发起请求。 | 其他地域 API Key 不支持该功能。 |
| `RAM 策略` | 如 `AliyunBailianFullAccess`（超级管理员）、`AliyunBailianDataFullAccess`（OpenAPI 全读写）等，必须通过 RAM 控制台附加至用户。 | `AliyunBailianFullAccess` 是使用全局管理菜单的前提，但**不自动授予 OpenAPI 调用权**。 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已绑定 `AliyunBailianFullAccess` 的 RAM 用户担任，通过 [全局管理菜单](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 统一管理多空间资源。  
   - 业务空间管理员：由超级管理员在百炼控制台「权限管理」页签中为 RAM 用户授予「管理员」角色，仅对该空间内用户、模型、API Key 有管理权。

2. **模型权限开通流程**（以调用为例）  
   - 步骤1（超级管理员）：在全局管理菜单中为该业务空间启用目标模型的「调用」权限并配置限流。  
   - 步骤2（超级/空间管理员）：在业务空间「权限管理」→「用户权限」中，为 RAM 用户分配「模型体验-操作」等控制台功能权限。  
   - 步骤3（超级/空间管理员）：为该用户创建 API Key（归属该空间），其调用能力自动继承空间级模型权限。

3. **OpenAPI 调用授权**  
   - 必须由阿里云主账号登录 [RAM 控制台](https://ram.console.aliyun.com/users)，为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。  
   - 授权后，用户使用其所属业务空间的 API Key 即可调用对应 OpenAPI（如 `/v1/knowledge_bases`）。

## 限制和注意事项

- **地域强绑定**：业务空间、API Key、模型限流策略均与地域强绑定，跨地域调用需分别配置；例如新加坡空间的 API Key 无法调用北京空间模型。
- **默认空间限制**：所有默认业务空间（如 `default-workspace`）**不支持**模型调用/调优/部署的开关控制与限流配置，仅可用于快速体验。
- **API Key 生效逻辑**：API Key 权限 = 所属业务空间模型权限 + 所属用户 RAM 策略（仅影响 OpenAPI），**不受该用户在控制台的页面权限影响**。
- **主账号特权**：阿里云主账号无需显式授权即可访问所有业务空间全部功能；但开通 AI 安全护栏、模型监控等增值服务，**建议使用主账号一次性完成控制台授权** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **失效场景**：RAM 用户被移出业务空间时，其 API Key **临时失效**，重新加入后自动恢复；若在 RAM 控制台删除该用户，则 API Key **永久失效且不可恢复**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


