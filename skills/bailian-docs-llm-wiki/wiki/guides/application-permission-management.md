# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，所有策略均与业务空间强绑定，且不支持跨地域共享。详细设计与行为约束请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

权限管理作用于以下关键能力维度：

- **模型调用**：控制指定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持按 QPM（每分钟请求数）和 [Token](../concepts/token.md) 数设置两级限流；
- **模型调优（训练）**：控制是否允许在该业务空间内对支持调优的模型执行微调任务及后续部署；
- **模型部署**：控制是否允许将模型（含调优后模型）直接部署为服务；
- **控制台页面权限**：为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型观测-操作”等细粒度菜单权限，仅影响控制台交互，**不影响 API Key 的实际调用能力**；
- **API Key 全生命周期管理**：包括创建、查看、删除及 IP 白名单设置（仅华北2（北京）地域支持）；
- **OpenAPI 接口权限**：需通过 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，否则默认无权调用应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt.md)等），详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 同时指出“超级管理员可对所有业务空间（含默认空间）进行模型管理”，此处存在表述矛盾。实际行为以控制台为准：**默认业务空间的模型权限开关始终为开启状态，且限流配置项不可编辑**。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识，与地域强绑定 | 每个地域下独立命名，不可跨地域复用 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`） | 必须已在该业务空间启用（由超级管理员开通） |
| `qpm_limit` | 每分钟请求上限 | ≥ 0；0 表示禁用调用 |
| `token_limit_per_minute` | 每分钟 [Token](../concepts/token.md) 总量上限 | ≥ 0；0 表示禁用调用 |
| `api_key_ip_whitelist` | IP 白名单（仅华北2（北京）支持） | CIDR 格式，最多 10 个条目 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置；  
   - 业务空间管理员：由超级管理员在对应业务空间的**权限管理 → 用户管理**中授予“管理员”角色；  
   - 普通用户：由超级管理员或业务空间管理员在**权限管理 → 用户管理**中添加并分配具体权限。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单 → **模型管理** 中为指定业务空间启用目标模型（如 `qwen-plus`），否则任何用户均无法调用或调优该模型 —— 此步骤在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确要求。

3. **API 调用授权**  
   - 为用户分配 API Key（归属单个业务空间+单个地域）；  
   - API Key 的模型可用性与限流策略**完全继承自其归属业务空间的配置**，与用户个人控制台权限无关；  
   - 若需调用应用层 OpenAPI（如知识库 CRUD），必须额外在 RAM 控制台为该 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格绑定单一地域，跨地域资源（如模型、API Key、账单）不可共享或迁移；
- **默认空间不可控**：默认业务空间的模型调用/调优/部署开关始终开启，且限流参数不可修改，生产环境应避免使用；
- **API Key 不可转移**：一个 API Key 仅归属一个地域内的一个业务空间和一个用户，创建后不可变更归属；
- **控制台权限 ≠ API 权限**：用户在控制台被禁止访问“模型体验”页面，不影响其 API Key 调用该模型的能力；
- **时间敏感变更**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 默认归属主账号，RAM 用户需主动申请分配；
- **账单与预付费权限分离**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独授权，与百炼自身权限策略无关。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


