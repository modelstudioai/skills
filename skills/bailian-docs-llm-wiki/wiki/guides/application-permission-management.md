# application permission management

百炼平台的权限管理以“业务空间”为最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台功能访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、空间级管理和资源使用能力。所有 API Key 的调用权限严格继承自其归属业务空间的模型授权策略，与用户账号的控制台权限解耦。

## 支持的模型/功能

- **模型调用**：支持对文生文、文生图、语音合成等全类型模型的调用权限开关与限流（QPM / [Token](../concepts/token.md)/s），需在业务空间维度显式开通；默认业务空间不支持此限制 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持开启/关闭特定模型在业务空间内的微调能力（含 LoRA、全参微调等），并控制调优后模型的自动部署权限；该能力同样不适用于默认业务空间 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持控制是否允许在业务空间内直接部署官方模型或调优后模型（如 vLLM、Triton 部署形态）。
- **控制台页面权限**：支持按菜单项（如“模型体验”“批量推理”“Prompt 工程”）为 RAM 用户分配操作权限，但**不影响其 API Key 的实际调用能力**。
- **OpenAPI 接口权限**：需通过 RAM 控制台单独授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用层 OpenAPI（如知识库、数据连接、[长期记忆](../concepts/long-term-memory.md)等）；该权限与业务空间模型权限正交，且**当前文档明确指出 RAM 用户默认无权调用** [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `model_call_enabled` | 模型是否可在该业务空间被调用（控制台 & API） | `true` / `false`；默认业务空间恒为 `true` |
| `qpm_limit` | 每分钟请求数上限 | ≥ 0；0 表示不限流；受主账号总配额约束 |
| `token_per_second_limit` | 每秒 [Token](../concepts/token.md) 处理上限 | ≥ 0；0 表示不限流 |
| `tuning_enabled` | 是否允许在该空间进行模型调优 | `true` / `false`；默认业务空间恒为 `true` |
| `deployment_enabled` | 是否允许在该空间部署模型（含调优后模型） | `true` / `false`；默认业务空间恒为 `true` |
| `api_key_region_binding` | API Key 严格绑定单地域 + 单业务空间 + 单用户，不可迁移 | 不可修改；创建时确定 |

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未说明其是否可被删除或降级。实践中应避免在默认空间承载生产流量，建议统一使用显式创建的业务空间。

## 使用方式

1. **角色配置**  
   - 超级管理员：需主账号或持有 `AliyunBailianFullAccess` 策略的 RAM 用户，在 [RAM 控制台](https://ram.console.aliyun.com/users) 授予该策略，并通过百炼全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）执行跨空间操作。  
   - 业务空间管理员：由超级管理员或同空间管理员在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色。  

2. **模型权限开通（超级管理员操作）**  
   进入全局管理 → 选择目标业务空间 → **模型管理** 页签 → 开启目标模型的“调用”“调优”“部署”开关，并设置限流值。

3. **用户控制台权限分配（超级管理员/业务空间管理员操作）**  
   进入业务空间 → **权限管理 → 用户管理** → 选择用户 → 分配具体菜单权限（如“模型体验-操作”“批量推理-操作”）。

4. **API Key 创建与授权（超级管理员/业务空间管理员操作）**  
   进入业务空间 → **权限管理 → API Key 管理** → 为用户创建 Key；该 Key 自动继承业务空间的模型调用/限流策略，无需额外配置模型白名单。

## 限制和注意事项

- **地域隔离刚性**：业务空间严格绑定单一地域，跨地域资源（如模型、知识库、API Key）不可共享；即使名称相同，北京与新加坡的 `prod-workspace` 是完全独立的实体。
- **API Key 权限继承性**：API Key 的模型可用性、限流策略**100%继承自归属业务空间**，与其所属用户的控制台权限无关；禁止通过用户角色控制 API 调用范围。
- **OpenAPI 权限需独立开通**：即使某用户拥有业务空间全部模型调用权限，若未被授予 `AliyunBailianDataFullAccess`，仍无法调用 `/v1/knowledge_bases` 等应用层 OpenAPI。
- **默认业务空间限制**：所有精细化权限（调用/调优/部署开关、限流）均**不适用于默认业务空间**，必须新建业务空间方可启用。
- **主账号特权**：AI 安全护栏、模型监控、应用观测等功能的首次开通，以及中国香港地域的 OpenAPI 权限添加，**仅支持阿里云主账号操作**，RAM 用户无法替代。
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域所有新创建 API Key 默认归属主账号，且主账号 Key 不支持“移出空间后恢复”逻辑。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


