# application permission management

百炼平台的权限管理基于业务空间（Workspace）这一最小管理单元，提供跨地域、多角色、细粒度的模型调用、训练、部署及控制台页面访问控制。权限体系分为超级管理员、业务空间管理员和普通用户三类角色，分别对应全局管理、单空间管理和资源使用能力。所有 API Key 的调用权限继承自其归属业务空间的模型配置，与用户账号的控制台权限相互独立。

## 支持的模型/功能

权限管理覆盖以下核心能力：
- **模型调用**：控制台体验、批量推理、API 调用（含 Token/请求数双限流），需在业务空间级开通模型可用性，并为用户授予 `模型体验-操作`、`批量推理-操作` 等控制台权限 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型调优（训练）**：支持对指定模型进行微调（Fine-tuning），需业务空间级启用“允许特定模型调优”，且用户需具备 `模型调优-操作` 权限 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **模型部署**：支持将调优后模型或基础模型直接部署为服务，依赖业务空间级“允许特定模型部署”开关。
- **页面级权限**：可精确控制 RAM 用户在控制台中可见及可操作的菜单项（如知识库、Prompt 工程、应用观测等），但**不影响 API Key 的调用能力**。
- **OpenAPI 接口权限**：默认禁用，需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略，方可调用应用相关 OpenAPI [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。

> **注意**：文档中多次强调“默认业务空间无法设置模型调用/调优/部署限制”，但未明确说明该空间是否支持 OpenAPI 调用。根据 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中 OpenAPI 权限章节，其授权逻辑与业务空间无关，仅取决于 RAM 用户是否被授予对应系统策略，因此默认空间下 RAM 用户仍需单独授权才能调用 OpenAPI。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `业务空间地域` | 业务空间绑定唯一地域（如 `cn-beijing`），不可跨地域共享 | 每个空间仅属一个地域；北京、新加坡、弗吉尼亚、中国香港等已上线地域均独立建空间 |
| `模型限流` | 分为 QPM（每分钟请求数）和 TPM（每分钟 Token 数）两级控制 | 仅对非默认业务空间生效；数值 ≥ 0，0 表示禁止调用 |
| `API Key 归属` | 每个 API Key 唯一绑定一个地域 + 一个业务空间 + 一个 RAM 用户 | 不可迁移；2026年3月25日起，华北2（北京）新创建 Key 默认归属主账号 |
| `IP 白名单` | 仅华北2（北京）地域支持为 API Key 配置 IPv4 白名单 | 单 Key 最多 10 个 IP 或 CIDR 段 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：由阿里云主账号或已授 `AliyunBailianFullAccess` 的 RAM 用户在 [RAM 控制台](https://ram.console.aliyun.com/users) 配置；  
   - 业务空间管理员：由超级管理员或同空间管理员在百炼控制台 **权限管理 → 用户管理** 中为 RAM 用户勾选“管理员”角色。

2. **模型权限开通（超级管理员操作）**  
   进入全局管理菜单（如 [北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management)），选择目标业务空间 → **模型管理** → 开启指定模型的“调用”、“调优”、“部署”开关。

3. **用户权限分配（超级管理员 / 业务空间管理员操作）**  
   在业务空间内进入 **权限管理 → 用户管理** → 选择 RAM 用户 → 勾选所需控制台权限（如 `模型体验-操作`、`模型调优-操作`）。

4. **API Key 创建与授权**  
   - 在 **权限管理 → API Key 管理** 中为用户创建 Key；  
   - Key 自动继承该业务空间的模型可用性与限流配置；  
   - 如需 OpenAPI 调用，须额外在 RAM 控制台授予 `AliyunBailianDataFullAccess` 等策略。

## 限制和注意事项

- **默认业务空间无权限管控能力**：所有模型默认可调用、可调优、可部署，且不支持限流设置，**不适用于生产环境**；生产建议按环境或业务线新建隔离业务空间 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)。
- **API Key 权限 ≠ 账号控制台权限**：即使用户被移出业务空间，其已有 API Key 在重新加入后自动恢复；但若 RAM 账号被删除，则 Key 永久失效。
- **OpenAPI 权限需主账号显式授权**：RAM 用户默认无权调用任何应用类 OpenAPI（如知识库、数据连接、[长期记忆](../concepts/memory.md)），必须由阿里云主账号在 RAM 控制台完成策略绑定，业务空间管理员无此能力。
- **账单与预付费权限独立于百炼权限体系**：查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需在 RAM 控制台单独配置，不通过百炼控制台管理。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


