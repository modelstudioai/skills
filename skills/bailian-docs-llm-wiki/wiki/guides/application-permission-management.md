# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，开发者需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用**：控制指定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持请求数（QPM）与 [Token](../concepts/token.md) 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型调优（训练）**：控制是否允许在该业务空间内对支持调优的模型执行训练任务及训练后部署（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型部署**：控制是否允许直接将模型部署为服务（如 API 服务、Web 应用），仅限已开通部署权限的模型。
- **控制台页面权限**：按菜单粒度控制 RAM 用户可访问的控制台功能（如“模型体验”“批量推理”“模型观测”），但**不影响其所属 API Key 的调用能力**。
- **OpenAPI 接口权限**：默认禁用，需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限设置（调用/调优/部署限流均不可配），所有模型默认全开。生产环境务必使用自建业务空间。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `region` | 业务空间所属地域，**不可跨地域共享**；API Key 与业务空间强绑定于同一地域 | 如 `cn-beijing`、`ap-southeast-1`、`us-east-1` |
| `workspace_id` | 业务空间唯一标识，由百炼分配，用于 API 请求头 `x-bailian-workspace-id` | 字符串，长度 32+ |
| `qpm_limit` | 模型每分钟请求数上限 | ≥ 0，0 表示禁用调用 |
| `token_limit_per_minute` | 模型每分钟 [Token](../concepts/token.md) 消耗上限 | ≥ 0，0 表示禁用调用 |
| `api_key_scope` | API Key 权限范围：仅继承其归属业务空间的模型权限，**不受用户控制台权限影响** | 单一业务空间 + 单一 RAM 用户，不可迁移 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略（参考 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“设置超级管理员”章节）。
   - 业务空间管理员：由超级管理员或同空间管理员，在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)），选择目标业务空间 → **模型管理** → 开启指定模型的“调用”“调优”“部署”开关。

3. **用户控制台权限配置（超级/空间管理员）**  
   在业务空间内进入 **权限管理 → 用户管理** → 选择用户 → 勾选所需功能权限（如“模型体验-操作”“批量推理-操作”）。

4. **API Key 创建与授权（超级/空间管理员）**  
   在 **权限管理 → API Key 管理** 中为 RAM 用户创建 Key；该 Key 自动继承业务空间模型权限，无需额外配置模型白名单。

## 限制和注意事项

- **地域隔离刚性**：业务空间与 API Key 均严格绑定单一地域，跨地域调用需分别创建对应地域的业务空间和 API Key（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **默认空间无权限控制**：默认业务空间无法配置模型限流或开关，仅适用于快速试用，**严禁用于生产环境**。
- **API Key 权限不可继承用户页面权限**：即使用户被禁止访问“模型体验”页面，其 API Key 仍可调用已授权模型（只要业务空间允许）。
- **OpenAPI 权限独立于百炼控制台权限**：调用 `/v1/apps/...` 等应用类接口必须单独授予 `AliyunBailianDataFullAccess`，百炼控制台的“管理员”权限不自动赋予 OpenAPI 访问权。
- **华北2（北京）新 API Key 归属主账号**：自 2026年3月25日起，北京地域新创建的 API Key 默认归属主账号，不再关联 RAM 用户（见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“API-Key 权限”说明）。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


