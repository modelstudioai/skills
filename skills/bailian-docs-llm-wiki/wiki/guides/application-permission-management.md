# application permission management

百炼平台的权限管理基于“业务空间”这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别承担全局管理、空间级管理和资源使用职责。所有 API Key 的调用能力严格继承自其归属业务空间的模型权限配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限开关与限流（QPM / Token/s），需在业务空间维度显式开通；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持为特定模型开启/关闭调优权限，并控制调优后模型是否允许直接部署；该能力仅在非默认业务空间中可配置 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持按模型粒度控制是否允许在业务空间内执行一键部署（含推理服务发布），部署权限独立于调用和调优权限。
- **控制台页面权限**：支持为 RAM 用户分配“模型体验-操作”“批量推理-操作”“模型观测-操作”等细粒度菜单权限，但**不影响其 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：RAM 用户默认无权调用应用层 OpenAPI（如知识库、Prompt 工程、[长期记忆](../concepts/memory.md)等），必须由主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该限制是否适用于所有地域。实践中发现华北2（北京）默认空间已支持基础限流配置，建议以控制台实际功能为准，避免依赖文档绝对表述。

## 关键参数

| 参数 | 说明 | 取值范围 | 生效层级 |
|------|------|----------|----------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 & API） | `true` / `false` | 业务空间 |
| `qpm_limit` | 每分钟请求次数上限 | ≥ 0（0 表示不限） | 业务空间 + 模型 |
| `token_per_second_limit` | 每秒 Token 消耗上限 | ≥ 0（0 表示不限） | 业务空间 + 模型 |
| `tuning_enabled` | 是否允许对该模型执行调优（SFT/RLHF） | `true` / `false` | 业务空间 + 模型 |
| `deployment_enabled` | 调优完成后是否允许一键部署为在线服务 | `true` / `false` | 业务空间 + 模型 |
| `ip_whitelist` | API Key 绑定的 IP 白名单（仅华北2支持） | CIDR 格式列表，最多 10 个 | API Key 级 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置。
   - 业务空间管理员：由超级管理员在对应空间的「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单 → 「模型管理」中为指定业务空间启用目标模型的调用、调优或部署能力。

3. **用户控制台权限配置**  
   在业务空间「权限管理」→「用户权限」中，为 RAM 用户勾选：
   - `模型体验-操作`（控制台单次调用）
   - `批量推理-操作`（批量任务提交）
   - `模型观测-操作`（Token 消耗查看）

4. **API Key 创建与绑定**  
   - 在「权限管理」→「API Key 管理」中为用户创建 Key；
   - Key 自动继承所属业务空间的模型权限（如某空间仅开通 Qwen2-72B 调用，则该 Key 无法调用 Qwen-VL）；
   - 华北2 地域支持设置 `ip_whitelist`，其他地域暂不支持。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一名称的空间（如 `prod-workspace`）在北京与新加坡是两个完全独立的实体。
- **默认空间限制**：所有模型在默认业务空间中均默认可调用、可调优、可部署，且**无法配置任何限流或禁用策略** —— 生产环境务必使用自建业务空间。
- **API Key 绑定刚性**：一个 API Key 仅归属一个地域 + 一个业务空间 + 一个用户，不可迁移；若用户被移出空间，Key 将失效（重新加入后恢复）。
- **OpenAPI 权限独立授权**：即使用户拥有业务空间全部模型权限，若未在 RAM 控制台显式授予 `AliyunBailianDataFullAccess`，仍无法调用 `/v1/knowledge_bases` 等应用层接口。
- **账单与预付费权限分离**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不随百炼角色自动继承。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


