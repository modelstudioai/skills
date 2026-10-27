# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 调用等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三级职责，确保生产环境隔离性与安全合规性。所有权限策略均与业务空间绑定，不支持跨地域共享。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用控制**：在业务空间粒度启用/禁用指定模型（含文生文、文生图、语音合成等），并设置 QPM（每分钟请求数）与 Token 限流；*默认业务空间无法配置此限制* [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）控制**：控制是否允许在该业务空间内对支持调优的模型进行训练及训练后部署；*默认业务空间默认全部开放* [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型直接部署控制**：控制是否允许在该业务空间内将支持部署的模型一键发布为服务。
- **控制台页面级权限**：为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型观测-操作”等细粒度菜单权限，影响其在控制台的功能可见性与可操作性。
- **OpenAPI 接口权限**：通过 RAM 策略（如 `AliyunBailianDataFullAccess`）控制 RAM 用户能否调用应用数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI；*该权限需主账号在 RAM 控制台显式授予，不继承自业务空间权限* [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用、调优、部署限制”，但未明确说明该限制是否适用于所有地域。实践中，北京、新加坡、弗吉尼亚、中国香港四地默认空间行为一致，但建议在非默认空间中统一配置以保障策略一致性。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `business_space_id` | 业务空间唯一标识，按地域隔离，不可跨地域复用 | 必填，由控制台生成或 API 返回 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`） | 需已在该地域该空间内开通调用权限 |
| `qpm_limit` / `token_limit` | 每分钟请求上限、每分钟 Token 上限 | 整数，≥0；设为 0 表示禁用该模型调用 |
| `api_key_scope` | API Key 绑定范围：仅限单地域 + 单业务空间 + 单用户 | 不可迁移、不可跨空间复用 |
| `ip_whitelist` | API Key 的 IP 访问白名单 | 仅华北2（北京）地域支持 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置。  
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理 → 选择目标业务空间 → 「模型管理」→ 勾选待开通模型 → 设置 QPM/Token 限流值。

3. **用户控制台权限分配（超级管理员或业务空间管理员）**  
   控制台左侧导航栏 → 「权限管理」→ 选择用户 → 勾选所需功能权限（如“模型体验-操作”）。

4. **API Key 创建与授权（超级管理员或业务空间管理员）**  
   「权限管理」→ 「API Key 管理」→ 为用户开启「创建/删除/查看」权限 → 用户自行在「API Key」页签生成密钥；密钥生效范围自动继承其归属业务空间的模型权限。

5. **OpenAPI 权限开通（仅主账号）**  
   前往 [RAM 控制台](https://ram.console.aliyun.com/users) → 为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

## 限制和注意事项

- **地域强隔离**：业务空间严格绑定单一地域，北京、新加坡等地的空间互不相通，模型权限、API Key、用户列表均独立维护。
- **默认空间无管控能力**：所有默认业务空间（如 `default-workspace`）均无法配置模型调用/调优/部署限制，**生产环境必须使用自定义业务空间**。
- **API Key 权限继承性**：API Key 的模型可用性与限流策略完全继承自其归属业务空间，**不受用户控制台页面权限影响**；即用户即使无“模型体验”权限，仍可通过 API Key 调用已开通模型。
- **主账号特权**：开通 AI 安全护栏、模型监控、应用观测等功能，以及设置 OpenAPI 权限、购买预付费资源，**必须使用阿里云主账号操作**，RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法替代。
- **失效规则**：RAM 用户被移出业务空间时，其名下 API Key **临时失效**，重新加入后自动恢复；若在 RAM 控制台删除该用户，则 API Key **永久失效且不可恢复**。
- **时间敏感变更**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号，不再支持绑定 RAM 用户。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


