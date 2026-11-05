# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、模型级的精细化控制能力，覆盖控制台操作、API 调用、模型调用/调优/部署、限流及账单分账等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，且 API Key 的生命周期与归属空间强绑定，不随用户控制台权限变化而动态调整。详细设计原则与行为边界请参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限控制（含控制台体验与 OpenAPI 调用），并可配置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。
- **模型调优（训练）**：支持为指定模型开通调优权限，包括数据集管理、训练任务提交、快照保存、评测与部署全流程。
- **模型部署**：支持独立控制“直接部署”能力（即非调优模型的在线服务部署），与调优后部署权限分离。
- **页面级功能控制**：通过细粒度菜单权限（如“模型体验-操作”“批量推理-操作”“模型观测-操作”等）控制用户在控制台可访问的功能模块。
- **OpenAPI 接口权限**：需显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用层 API（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)等），该能力**不继承自业务空间管理员角色**，详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：默认业务空间（default workspace）**无法设置任何模型级权限限制**（调用、调优、部署均全部开放），也不支持限流配置。生产环境必须使用显式创建的非默认业务空间以启用权限管控，此约束在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中多次强调。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `region` | API Key 和业务空间强绑定的地域标识 | 华北2（北京）、新加坡、弗吉尼亚、中国香港等，**不可跨地域复用** |
| `workspace_id` | 业务空间唯一标识符 | 每个地域内独立命名，不同地域同名空间视为不同实体 |
| `qpm_limit` | 模型每分钟请求上限 | 整数，0 表示禁用该模型调用；需由超级管理员在全局管理菜单中配置 |
| `token_limit_per_minute` | 模型每分钟 [Token](../concepts/token.md) 消耗上限 | 整数，0 表示禁用；仅对已开通调用权限的模型生效 |
| `api_key_status` | API Key 状态（active/inactive） | 由归属用户是否在业务空间内决定；移出空间即失效（RAM 用户创建的 Key），主账号 Key 不受影响 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：需主账号或具备 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 显式授权；其权限覆盖所有地域与空间，是配置模型权限、API Key 和空间拓扑的前提。  
   - 业务空间管理员：由超级管理员或同空间其他管理员，在控制台 **权限管理 → 用户管理** 中为 RAM 用户分配“管理员”角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员须先在全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)）中为指定业务空间开通目标模型的「调用」「调优」或「部署」权限。未开通则后续用户权限配置无效 —— 此流程在 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确定义。

3. **用户权限分配**  
   - 控制台操作：在业务空间内 **权限管理 → 页面权限** 中勾选对应菜单项（如“模型调优-操作”）。  
   - API 调用：为用户创建 API Key（归属该空间），Key 自动继承空间级模型权限与限流策略，无需额外配置模型白名单。

4. **API Key 管理**  
   - 创建/删除/查看权限需在 **权限管理 → API Key 权限** 中显式授予用户；  
   - 华北2（北京）地域支持 IP 白名单；  
   - 2026年3月25日后创建的 Key 不与 RAM 用户级联，删除用户不影响 Key 生效。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格按地域划分，同一空间无法跨地域存在；全局管理菜单需按地域分别访问（如 [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)），此设计直接影响权限策略的部署范围。
- **默认空间无权限控制能力**：所有模型权限、限流、部署开关在默认业务空间中均不可配置，必须新建业务空间并迁移资源。
- **API Key 权限不继承用户控制台权限**：即使某用户被禁止在控制台访问“模型调优”页面，只要其持有有效 API Key，仍可通过 API 调用已开通权限的模型（前提是空间级模型调优权限已开启）。
- **OpenAPI 权限需独立授权**：业务空间管理员角色**不包含任何 OpenAPI 调用权限**，必须由主账号在 RAM 控制台单独附加 `AliyunBailianDataFullAccess` 或只读策略，否则调用应用层 API 将返回 `Forbidden` 错误。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不随百炼角色自动赋予。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


