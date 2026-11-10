# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、模型级与页面级的精细化控制能力，支撑组织架构隔离、成本分账与生产环境安全治理。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间内资源管控与受限使用三种能力层级。所有权限策略均需结合 RAM 系统策略与百炼控制台配置协同生效。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全部模型类型进行空间级开关控制与限流（QPM / [Token](../concepts/token.md)/s），但[默认业务空间无法设置此限制](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持在指定业务空间内启用/禁用模型微调能力，并控制调优后模型的部署与观测权限；同样，[默认业务空间无法设置此限制](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持控制特定模型是否可在该业务空间直接部署为服务端点，部署权限独立于调用与调优权限。
- **OpenAPI 接口访问**：默认关闭；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用组件相关 OpenAPI（如知识库、Prompt 工程等）——详见 [OpenAPI 接口权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 + API） | `true` / `false`，仅超级管理员可配置 |
| `qpm_limit` | 每分钟请求数上限 | ≥ 0，0 表示不限流；默认业务空间不支持设置 |
| `token_per_second_limit` | 每秒 [Token](../concepts/token.md) 消耗上限 | ≥ 0，0 表示不限流；默认业务空间不支持设置 |
| `api_key_region_binding` | API Key 绑定地域与业务空间 | 单向绑定，不可跨地域或跨空间迁移 |
| `ip_whitelist` | API Key 的 IP 访问白名单 | 仅华北2（北京）地域支持；格式为 CIDR 或单 IP |

> **注意**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号，不再与 RAM 用户级联；此前创建的 API Key 在删除 RAM 用户时将被同步清除且不可恢复 —— 该行为变更已在 [API-Key 权限](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中明确说明。

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已授予 `AliyunBailianFullAccess` 的 RAM 用户担任，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置。  
   - 业务空间管理员：由超级管理员或同空间管理员在控制台「权限管理」页签中为 RAM 用户分配「管理员」权限。

2. **模型权限开通**  
   - 超级管理员需先在全局管理中为业务空间启用目标模型的调用、调优或部署能力；  
   - 再由空间管理员在该空间「权限管理」页签中为具体 RAM 用户分配对应操作权限（如「模型体验-操作」「模型调优-操作」等）。

3. **API 调用授权**  
   - 为用户创建 API Key（归属单一地域+业务空间）；  
   - API Key 的模型可用性与限流策略完全继承自其归属业务空间的配置，**不受用户控制台权限影响**；  
   - 如需 OpenAPI 访问能力，必须额外在 RAM 控制台绑定 `AliyunBailianDataFullAccess` 或只读策略。

## 限制和注意事项

- **地域隔离刚性约束**：业务空间严格绑定单一地域，跨地域资源不可共享；即使名称相同（如各区域的“default”空间），也互为独立实体。
- **默认业务空间特权**：所有模型默认可调用、可调优、可部署，且不支持配置限流或开关 —— 生产环境务必创建独立业务空间替代默认空间。
- **API Key 生命周期解耦**：2026年3月25日后创建的 API Key 不再依赖 RAM 用户生命周期；但若用户被移出业务空间，其 API Key 将临时失效（重新加入即恢复）。
- **账单与预付费权限分离**：RAM 用户默认无权查看账单或购买预付费资源；需单独授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess`，且该授权作用于全阿里云产品，非百炼专属。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


