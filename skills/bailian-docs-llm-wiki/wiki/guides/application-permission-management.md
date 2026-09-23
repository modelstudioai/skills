# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用/调优/部署、用户访问、API Key 管理及 OpenAPI 接口调用等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，支持基于策略的细粒度授权。

## 支持的模型/功能

- **模型级操作权限**：支持对特定模型启用/禁用以下能力（需超级管理员在业务空间维度配置）：
  - 模型调用（控制台 & API），并可设置请求数限流（QPM）和 [Token](../concepts/token.md) 限流；
  - 模型调优（训练）及调优后部署；
  - 模型直接部署（非调优场景下的独立部署）。
- **控制台页面级权限**：业务空间管理员可为 RAM 用户分配具体菜单项权限，如“模型体验-操作”“批量推理-操作”“模型观测-操作”等，但**不控制 API Key 的实际调用行为**（详见 [API-Key 权限](https://help.aliyun.com/zh/model-studio/application-permission-management-overview#f2704153a055r)）。
- **OpenAPI 接口权限**：默认关闭；需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用相关 OpenAPI（如知识库、[Prompt 工程](../concepts/prompt-engineering.md)等）[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **账单与预付费权限**：RAM 用户默认无权查看账单或购买预付费产品，需额外授予 `AliyunBSSReadOnlyAccess` 或 `AliyunBSSOrderAccess` 策略——该能力**独立于百炼业务空间权限体系**，由阿里云 BSS 系统统一管控。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明其是否支持 OpenAPI 权限开通。根据 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“OpenAPI 接口权限”章节，该权限**仅能通过主账号在 RAM 控制台配置，与业务空间类型无关**，因此默认空间用户只要获得对应 RAM 策略，即可调用 OpenAPI。

## 关键参数

| 参数 | 说明 | 来源约束 |
|------|------|----------|
| `region` | 业务空间所属地域（如 `cn-beijing`），API Key 与业务空间强绑定于单一地域，**不可跨地域复用** | [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) |
| `workspace_id` | 业务空间唯一标识，用于 OpenAPI 请求头 `x-bailian-workspace-id`，决定模型可用性与限流策略生效范围 | — |
| `qpm_limit` / `token_limit` | 模型级限流参数，由超级管理员在业务空间模型管理页配置，单位分别为 QPS 和 tokens/minute | — |
| `ip_whitelist` | 仅华北2（北京）地域的 API Key 支持设置 IP 白名单，其他地域不生效 | — |
| `AliyunBailianFullAccess` | 超级管理员必需系统策略，赋予全局业务空间管理能力（含模型、用户、API Key） | — |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或已绑定 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)｜[新加坡](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置。  
   - 业务空间管理员：由超级管理员在目标业务空间的「权限管理」页签中，为 RAM 用户授予「管理员」角色。

2. **模型权限开通流程**  
   - 超级管理员 → 进入全局管理 → 选择业务空间 → 「模型管理」→ 开启目标模型的「调用」「调优」「部署」开关；  
   - 业务空间管理员 → 进入该空间「权限管理」→ 为用户分配「模型体验-操作」等控制台功能权限；  
   - API 调用 → 为用户创建 API Key（归属该空间），Key 自动继承空间级模型权限与限流策略。

3. **OpenAPI 调用授权**  
   - 主账号登录 RAM 控制台 → 找到目标 RAM 用户 → 添加 `AliyunBailianDataFullAccess`（读写）或 `AliyunBailianDataReadOnlyAccess`（只读）策略 → 调用时需在请求头携带 `x-bailian-workspace-id`。

## 限制和注意事项

- **业务空间不可跨地域**：即使名称相同，北京与新加坡的同名业务空间是完全隔离的实体，权限、模型配置、API Key 均不互通。
- **默认业务空间权限固定**：无法配置模型限流或禁用调优/部署，仅适用于快速体验；生产环境**必须创建自定义业务空间**。
- **API Key 绑定不可迁移**：一个 API Key 仅归属单一地域+单一业务空间+单一用户，创建后无法转移至其他空间或用户。
- **控制台权限 ≠ API 权限**：用户在控制台被禁止访问某模型页面，**不影响其 API Key 调用该模型的能力**（只要空间级模型调用权限已开启）。
- **时间敏感变更**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 默认归属主账号，不再支持归属 RAM 用户 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **OpenAPI 权限特殊性**：该权限不由百炼控制台配置，**必须通过 RAM 控制台单独授权**，且策略作用域为整个阿里云账号，与业务空间无直接映射关系。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


