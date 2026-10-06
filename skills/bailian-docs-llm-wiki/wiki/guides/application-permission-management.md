# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，开发者需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用**：控制指定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持请求数（QPM）与 [Token](../concepts/token.md) 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型调优（训练）**：控制是否允许在业务空间内对支持调优的模型执行训练任务及后续部署（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型部署**：控制是否允许直接将模型（含调优后模型）部署为服务实例。
- **控制台页面权限**：按菜单粒度控制 RAM 用户可访问的控制台功能（如“模型体验”“批量推理”“模型观测”），但**不影响 API Key 的实际调用能力**。
- **API Key 全生命周期管理**：包括创建、删除、查看、IP 白名单设置（仅限华北2地域），且单个 API Key 严格绑定一个地域+一个业务空间+一个用户（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间不支持任何模型级权限限制（调用、调优、部署均全部开放），生产环境应避免使用默认空间，而应新建独立业务空间进行管控。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `business_space_id` | 业务空间唯一标识，按地域隔离，不可跨地域复用 | 必填，由控制台生成 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl`），需已在该空间启用 | 仅当空间已开通对应模型权限后才生效 |
| `qpm_limit` / `token_limit` | 每分钟请求数上限 / 每分钟 [Token](../concepts/token.md) 总量上限 | 限流值需 ≤ 该账号在该地域的总配额；默认空间不支持设置 |
| `api_key_scope` | API Key 绑定范围：`region + business_space_id + user_id` | 不可修改，不可迁移；2026年3月25日起，华北2新 API Key 默认归属主账号 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略（参考 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“设置超级管理员”章节）。
   - 业务空间管理员：由超级管理员或同空间管理员在百炼控制台「权限管理」页签中为 RAM 用户授予「管理员」权限。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等），为指定业务空间启用目标模型的「调用」「调优」「部署」开关。

3. **用户级控制台权限配置（超级管理员或业务空间管理员操作）**  
   在业务空间内「权限管理」→「用户权限」中，为 RAM 用户勾选所需功能，例如：
   - `模型体验-操作`：启用控制台单次推理
   - `批量推理-操作`：启用批量任务提交
   - `模型观测-操作`：查看 [Token](../concepts/token.md) 消耗统计

4. **API 调用授权**  
   - 创建 API Key：在「权限管理」→「API Key 管理」中为用户生成 Key（自动继承所属空间的模型与限流策略）。
   - OpenAPI 权限：RAM 用户需额外被授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“OpenAPI 接口权限”章节）。

## 限制和注意事项

- **地域强隔离**：业务空间与模型权限均按地域划分，北京空间的配置对新加坡空间完全无效；跨地域需分别配置。
- **API Key 与用户权限解耦**：用户在控制台的页面权限（如禁用“模型体验”）**不影响其 API Key 的实际调用能力**；API Key 权限仅取决于所属业务空间的模型开通状态与限流设置。
- **OpenAPI 默认禁用**：RAM 用户即使拥有 API Key，若未在 RAM 控制台显式授予 `AliyunBailianData*Access` 策略，将无法调用应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt.md)相关接口）。
- **账单与预付费权限独立**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不随百炼内置策略自动授予。
- **默认空间不可控**：所有默认业务空间（如 `default-workspace`）均无法配置模型级权限，也不支持限流，**严禁用于生产环境**。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


