# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、模型级与页面级的精细化控制能力，支撑组织架构隔离、成本分账与生产环境安全治理。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间内资源管控与受限使用三种能力层级。所有权限策略均需结合 RAM 系统策略与百炼控制台配置协同生效。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全部模型类型进行空间级开关控制与限流（QPM / [Token](../concepts/token.md)/s），但[默认业务空间无法设置此限制](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持在指定业务空间内启用/禁用模型微调能力，并控制调优后模型的部署权限；同样，[默认业务空间无法设置此限制](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持控制特定模型是否可在该业务空间直接部署为服务端点，部署权限独立于调用与调优权限。
- **OpenAPI 接口访问**：默认关闭；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用组件相关 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)等）——详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 & API） | `true` / `false`；仅超级管理员可配置 |
| `qpm_limit` | 每分钟请求数上限 | ≥ 0；0 表示不限流；默认业务空间不支持设置 |
| `token_per_second_limit` | 每秒 [Token](../concepts/token.md) 消耗上限 | ≥ 0；0 表示不限流；默认业务空间不支持设置 |
| `api_key_region_binding` | API Key 绑定地域与业务空间，不可跨地域迁移 | 单一地域 + 单一空间；参见 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `ip_whitelist` | 北京地域 API Key 支持 IP 白名单（CIDR 格式） | 最多 10 个条目；仅华北2（北京）支持 |

> **注意**：文档中多次提及“默认业务空间无法设置模型调用/调优/部署限制”，但未明确定义何为“默认业务空间”。根据控制台实际行为，其指代各地域下自动创建且名称为 `default` 的初始空间；该空间无权限编辑入口，且其模型权限继承自主账号全局配额，**不可通过任何界面或 API 修改**。

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户担任，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置空间与用户。
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中，为 RAM 用户授予「管理员」权限。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为指定业务空间**启用目标模型的调用、调优或部署能力**；此操作独立于用户级权限，未开通则后续任何用户授权均无效。

3. **用户级控制台权限分配**  
   在业务空间「权限管理」页签中，为 RAM 用户勾选以下功能权限（按需组合）：
   - `模型体验-操作`：控制台模型交互（含调用、评测）
   - `批量推理-操作`：启用批量推理功能
   - `模型调优-操作` + `我的模型-操作` + `模型部署-操作`：完整调优工作流
   - `数据管理-操作`：上传/管理调优数据集

4. **API 调用授权**  
   - 创建归属该业务空间的 API Key（由超级管理员或具备 API Key 管理权限的业务空间管理员操作）；
   - API Key 的模型可用性与限流策略**完全继承自所属业务空间配置**，与用户控制台权限无关；
   - 若需调用应用类 OpenAPI，必须额外在 RAM 控制台为该 RAM 用户附加 `AliyunBailianDataFullAccess` 或只读策略。

## 限制和注意事项

- **地域强隔离**：业务空间严格绑定单一地域，跨地域资源（如模型、API Key、账单）不可共享；即使名称相同，北京与新加坡的 `default` 空间也是完全独立实体。
- **API Key 生命周期**：自 2026年3月25日起，华北2（北京）新创建的 API Key **不再与 RAM 用户绑定**；删除 RAM 用户不会级联删除此类 Key，但将其移出业务空间会导致 Key 失效（重新加入即恢复）。
- **默认空间不可控**：`default` 业务空间不提供模型开关、限流、调优开关等配置入口，所有模型默认全开且无配额限制；生产环境**严禁使用默认空间**，应按[应用于生产环境](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)建议新建独立空间。
- **OpenAPI 权限独立于控制台**：用户拥有控制台「模型体验-操作」权限，不代表能调用 `/v1/chat/completions` 等 OpenAPI；必须单独配置 RAM 策略，否则返回 `403 Forbidden`。
- **账单与预付费权限需显式授权**：RAM 用户默认无法查看账单或购买资源包，须在 RAM 控制台添加 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` 策略，且该授权影响全阿里云产品，非百炼专属。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


