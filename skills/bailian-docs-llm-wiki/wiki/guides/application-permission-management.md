# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制能力。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用权限。所有 API Key 的调用能力严格继承自其归属业务空间的模型权限配置，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限开关与限流（QPM / [Token](../concepts/token.md)/s），需在业务空间维度显式开通；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持开启/关闭特定模型在业务空间内的微调能力（含 LoRA、全参微调等），并控制调优后模型的自动部署权限；默认业务空间默认开放全部支持调优的模型 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持控制大模型是否可在该业务空间内直接部署为服务端点（如 vLLM、Triton 部署），仅对已授权模型生效。
- **控制台功能模块**：支持按菜单粒度分配权限，例如“模型体验-操作”、“批量推理-操作”、“模型观测-操作”等，影响用户在控制台的操作能力，但**不影响 API Key 的实际调用权限**。
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用层 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)、[长期记忆](../concepts/long-term-memory.md)等）；该权限与业务空间模型权限正交，且**当前不支持通过百炼控制台直接配置** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值示例 | 生效范围 |
|------|------|----------|----------|
| `model_call_enabled` | 模型是否允许在该业务空间被调用（控制台 & API） | `true` / `false` | 业务空间级（超级管理员设置） |
| `qpm_limit` | 每分钟请求次数上限 | `100` | 业务空间级（超级管理员设置） |
| `token_per_second_limit` | 每秒 [Token](../concepts/token.md) 处理上限 | `5000` | 业务空间级（超级管理员设置） |
| `tuning_enabled` | 是否允许在该业务空间进行模型调优 | `true` / `false` | 业务空间级（超级管理员设置） |
| `deployment_enabled` | 是否允许在该业务空间部署调优后模型 | `true` / `false` | 业务空间级（超级管理员设置） |
| `api_key_ip_whitelist` | API Key 的 IP 白名单（仅华北2北京地域支持） | `192.168.1.0/24,203.0.113.42` | API Key 级（空间管理员或超级管理员设置） |

> **注意**：`qpm_limit` 和 `token_per_second_limit` 是独立限流维度，二者同时生效；若任一维度超限，请求将被拒绝。限流策略不叠加，仅取业务空间配置的最终值。

## 使用方式

1. **配置业务空间模型权限**（需超级管理员）  
   进入全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) / [弗吉尼亚](https://bailian.console.aliyun.com/us-east-1?tab=globalset#/efm/business_management) / [中国香港](https://bailian.console.aliyun.com/cn-hongkong?tab=globalset#/efm/business_management)），选择目标业务空间 →「模型管理」→ 开启/关闭模型调用、调优、部署开关，并设置限流值。

2. **分配用户控制台权限**（超级管理员或业务空间管理员）  
   在业务空间内进入「权限管理」页签 → 选择 RAM 用户 → 勾选所需功能权限（如“模型体验-操作”、“批量推理-操作”等）。

3. **管理 API Key**（超级管理员或业务空间管理员）  
   在「权限管理」页签 → 「API Key 管理」→ 为用户创建/删除/查看 API Key；Key 的调用能力完全继承业务空间模型权限，无需额外配置模型白名单。

4. **开通 OpenAPI 权限**（仅阿里云主账号可操作）  
   前往 [RAM 控制台](https://ram.console.aliyun.com/users) → 为目标 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

## 限制和注意事项

- **地域隔离性**：业务空间严格绑定单一地域，跨地域资源不可共享；同一业务空间名称在不同地域代表完全独立的权限域。
- **默认业务空间限制**：默认业务空间无法配置模型调用/调优/部署开关，也无法设置限流，所有模型均默认可用且无流量约束。
- **API Key 绑定不可迁移**：单个 API Key 仅归属一个地域、一个业务空间、一个用户，创建后不可转移或复用至其他空间或用户。
- **主账号特权**：AI 安全护栏、模型监控、应用观测等功能的首次开通必须由阿里云主账号在控制台完成；RAM 用户即使拥有 `AliyunBailianFullAccess` 也无法代为开通。
- **IP 白名单地域限制**：仅华北2（北京）地域的 API Key 支持设置 `api_key_ip_whitelist`，其他地域暂不支持。
- **账单与预付费权限分离**：RAM 用户需单独授予 `AliyunBSSReadOnlyAccess`（查账单）或 `AliyunBSSOrderAccess`（购预付费）策略，这些权限不属于百炼原生权限体系，须在 RAM 控制台配置。

> **注意**：文档中提及“2026年3月25日起华北2（北京）新 API Key 默认归属主账号”，该时间点明显晚于当前年份（2025），属过时或笔误信息，实际策略请以控制台最新提示为准。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


