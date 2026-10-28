# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、细粒度的模型调用、调优、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间级管理和资源使用能力。所有 API Key 的权限继承自其归属业务空间，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对指定模型开启/关闭控制台与 OpenAPI 调用权限，并可配置 QPM（每分钟请求数）和 [Token](../concepts/token.md) 限流。默认业务空间不支持此限制 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持在业务空间维度开通/禁用特定模型的调优权限，包括数据集管理、训练任务提交、快照保存等全流程操作。
- **模型部署**：支持控制是否允许在该业务空间内将调优后的模型或基础模型直接部署为服务。
- **应用与组件权限**：包括 [Prompt 工程](../concepts/prompt-engineering.md)、知识库、[长期记忆](../concepts/long-term-memory.md)、数据连接等应用级功能的 OpenAPI 访问控制，需显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **细粒度控制台页面权限**：如“模型体验-操作”“批量推理-操作”“模型调优-操作”等，按菜单项独立授权，不影响 API Key 行为。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用、调优、部署限制”，但未明确说明该限制是否适用于所有地域。实际配置时请以控制台最新行为为准；若发现某地域默认空间已支持限流，请参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中关于地域差异的说明。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `workspace_id` | 业务空间唯一标识，API 调用必需 | 由系统生成，不可修改；获取方式见 [获取Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `model_name` | 模型标识符（如 `qwen-max`, `qwen-plus`） | 必须已在该业务空间开通调用/调优权限 |
| `qpm_limit` | 每分钟请求上限 | ≥ 0；0 表示禁止调用 |
| `token_limit_per_minute` | 每分钟 [Token](../concepts/token.md) 消耗上限 | ≥ 0；0 表示禁止调用 |
| `api_key_scope` | API Key 绑定范围 | 固定为单地域 + 单业务空间 + 单 RAM 用户，不可迁移 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置空间与用户。  
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中授予「管理员」权限。

2. **模型权限开通（超级管理员操作）**  
   在全局管理菜单 → 「业务空间管理」→ 选择目标空间 → 「模型管理」中启用指定模型的「调用」「调优」「部署」开关。

3. **用户权限分配（超级管理员 / 业务空间管理员操作）**  
   进入目标业务空间的「权限管理」页签 → 选择 RAM 用户 → 勾选所需控制台权限（如 `模型体验-操作`、`模型调优-操作`）。

4. **API Key 创建与绑定**  
   在「权限管理」→ 「API Key 管理」中为用户创建 Key；该 Key 自动继承业务空间的模型权限与限流策略，无需额外配置模型白名单 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

5. **OpenAPI 权限开通（仅主账号可操作）**  
   主账号需登录 RAM 控制台，为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 系统策略。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；即使名称相同（如 `default`），北京与新加坡的默认空间也是完全独立的实体。
- **API Key 不可迁移**：一个 API Key 仅归属一个地域+一个业务空间+一个用户，创建后不可转移或复用至其他空间。
- **默认空间特权**：默认业务空间不支持模型级限流与权限开关，所有模型默认全开；生产环境强烈建议使用自定义业务空间替代。
- **OpenAPI 权限特殊性**：RAM 用户默认无权调用应用相关 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)），且该权限**必须由阿里云主账号在 RAM 控制台显式授予**，业务空间管理员无权配置。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需主账号在 RAM 控制台单独授权，不包含在 `AliyunBailianFullAccess` 中。
- **华北2（北京）地域特殊规则**：自 2026年3月25日起，该地域新创建的 API Key 默认归属主账号，且支持 IP 白名单；其他地域暂不支持白名单。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


