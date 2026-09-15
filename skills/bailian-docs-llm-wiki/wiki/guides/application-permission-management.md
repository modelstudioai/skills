# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用/调优/部署、用户页面访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，支持策略复用与细粒度审计。

## 支持的模型/功能

- **模型级操作控制**：支持对单个模型配置调用（含控制台体验与批量推理）、调优（训练）和部署权限，但**默认业务空间不支持限制**，所有模型均默认开放（详见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **页面级访问控制**：业务空间管理员可为 RAM 用户分配具体控制台页面权限（如“模型体验-操作”“批量推理-操作”“模型观测-操作”），但该控制**不影响 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用相关 OpenAPI（如知识库、Prompt 工程、[长期记忆](../concepts/long-term-memory.md)等），需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（参见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **账单与预付费管理**：RAM 用户需额外授权 `AliyunBSSReadOnlyAccess`（查看账单）或 `AliyunBSSOrderAccess`（购买预付费产品），且该授权影响全阿里云产品，非百炼专属（见 [账单查看与预付费权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `business_space_id` | 业务空间唯一标识，**严格绑定地域**，不可跨地域复用 | 由控制台生成，格式如 `bs-xxxxxx`；同一地域内唯一 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`） | 必须已在该业务空间开通调用/调优/部署权限（由超级管理员配置） |
| `qpm_limit` / `tpm_limit` | 每分钟请求数限流 / 每分钟 Token 数限流 | 整数 ≥ 0；设为 0 表示禁用该模型调用 |
| `api_key_scope` | API Key 绑定范围 | 固定为「单地域 + 单业务空间 + 单 RAM 用户」，不可转移或跨空间复用 |
| `ram_policy` | RAM 策略名称 | 如 `AliyunBailianFullAccess`, `AliyunBailianDataReadOnlyAccess`, `AliyunBSSReadOnlyAccess` |

> **注意**：文档中多次提及“华北2（北京）地域新 API Key 默认归属主账号”，但未明确是否适用于所有新创建空间。实践中应以控制台实际创建流程为准，避免依赖地域性默认行为。

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置空间与用户。
   - 业务空间管理员：由超级管理员在目标空间的「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置）**  
   超级管理员需先在全局管理菜单中为业务空间启用目标模型的「调用」「调优」或「部署」权限（默认业务空间跳过此步）。

3. **用户权限分配**  
   - 控制台页面权限：在业务空间「权限管理」→「用户权限」中勾选对应功能项（如“模型体验-操作”）。  
   - API Key 权限：在「权限管理」→「API Key 管理」中为用户开启「创建/删除/查看本空间 API Key」权限，再由该用户自行创建 Key。

4. **OpenAPI 调用授权**  
   主账号需登录 [RAM 控制台](https://ram.console.aliyun.com/users)，为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略 —— 此步骤**独立于百炼控制台操作**，且必须完成才能调用应用类 OpenAPI。

## 限制和注意事项

- **地域强绑定**：业务空间与地域一一对应，跨地域资源（如模型、API Key、账单）不可共享；北京地域 API Key 自 2026-03-25 起强制归属主账号，其他地域策略可能不同。
- **默认空间无限制能力**：默认业务空间无法设置模型调用/调优/部署限制，也不支持限流，生产环境**必须创建独立业务空间**。
- **API Key 权限继承空间策略**：Key 的模型可用性与限流规则完全继承其归属业务空间的配置，**不受用户页面权限影响**；删除用户或移出空间将导致其 API Key 失效（重新加入可恢复）。
- **OpenAPI 权限不自动同步**：即使用户在控制台拥有某模型的调用权限，若未在 RAM 控制台授予 `AliyunBailianData*Access` 策略，其调用 OpenAPI 仍会返回 `Forbidden` 错误。
- **账单权限粒度粗**：`AliyunBSSReadOnlyAccess` 授予的是全产品账单查看权，无法限制仅查看百炼消费，需谨慎授权。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


