# application permission management

百炼平台的权限管理以“业务空间”为最小单元，提供跨地域、多角色、多维度的精细化控制能力，覆盖模型调用、调优、部署、API Key 管理及控制台页面访问等核心场景。权限体系严格区分超级管理员、业务空间管理员和普通用户三类角色，确保资源隔离与安全合规。所有权限策略均与阿里云 RAM 深度集成，开发者需结合 RAM 策略与百炼控制台配置协同生效。

## 支持的模型/功能

权限管理覆盖以下关键能力：
- **模型调用**：控制指定模型在业务空间内是否可通过控制台或 OpenAPI 调用，并支持请求数（QPM）与 [Token](../concepts/token.md) 限流（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型调优（训练）**：控制是否允许在该业务空间内对支持调优的模型执行训练任务及训练后部署（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **模型部署**：控制是否允许直接将模型部署为服务（如 API 服务、Web 应用），仅限已开通部署权限的模型。
- **控制台页面权限**：按菜单粒度控制 RAM 用户可访问的控制台功能（如“模型体验”“批量推理”“模型观测”），但**不影响其 API Key 的调用能力**。
- **OpenAPI 接口权限**：默认禁用，需主账号在 RAM 控制台显式授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

> **注意**：默认业务空间（Default Workspace）**不支持**任何模型级权限限制（调用、调优、部署均全开且不可限流），生产环境务必使用自建业务空间。

## 关键参数

| 参数 | 说明 | 取值范围/约束 |
|------|------|----------------|
| `region` | 业务空间所属地域，**不可跨地域共享** | `cn-beijing`, `ap-southeast-1`, `us-east-1`, `cn-hongkong` 等，需与 API Key 所属地域一致 |
| `workspace_id` | 业务空间唯一标识符，由百炼分配 | 字符串，全局唯一，不可修改 |
| `model_id` | 模型唯一标识（如 `qwen-max`, `qwen-vl-plus`） | 必须已在该业务空间中被超级管理员显式启用 |
| `qpm_limit` | 每分钟请求数上限 | ≥ 0；设为 `0` 表示禁止调用 |
| `token_limit` | 每分钟 [Token](../concepts/token.md) 消耗上限 | ≥ 0；设为 `0` 表示禁止调用 |
| `api_key_scope` | API Key 绑定范围 | 严格限定为 **单地域 + 单业务空间 + 单 RAM 用户**，不可转移 |

## 使用方式

1. **角色初始化**  
   - 超级管理员：主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户，通过全局管理菜单（[北京](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 等）统一配置。
   - 业务空间管理员：由超级管理员在目标业务空间的「权限管理」页签中为 RAM 用户授予「管理员」角色。

2. **模型权限开通（必需前置步骤）**  
   超级管理员需先在全局管理菜单中为业务空间启用目标模型的「调用」「调优」或「部署」权限（见 [原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。

3. **用户权限分配**  
   - 控制台权限：在业务空间「权限管理」→「用户权限」中勾选对应菜单项（如“模型体验-操作”）。
   - API 调用权限：为用户创建 API Key（归属该业务空间），其能力自动继承业务空间模型权限。

4. **OpenAPI 权限开通**  
   主账号需在 [RAM 控制台](https://ram.console.aliyun.com/users) 为 RAM 用户附加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

## 限制和注意事项

- **地域强绑定**：业务空间、API Key、模型限流策略均严格绑定单一地域，跨地域调用需分别配置。
- **默认空间无权限控制**：默认业务空间无法设置模型限流或禁用调用，**严禁用于生产环境**。
- **API Key 与账号权限解耦**：用户控制台权限（如禁用“模型体验”菜单）**不影响其 API Key 的调用能力**；API Key 权限完全由所属业务空间的模型配置决定。
- **华北2（北京）特殊规则**：自 2026年3月25日起，该地域新创建的 API Key 默认归属主账号，不再支持归属 RAM 用户。
- **OpenAPI 权限独立授权**：应用相关 OpenAPI（数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等）**默认全部禁用**，必须由主账号在 RAM 控制台显式授权，与百炼控制台内的任何权限设置无关（[原文标题](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）。
- **账单与预付费权限需额外配置**：RAM 用户查看账单需 `AliyunBSSReadOnlyAccess`，购买预付费产品需 `AliyunBSSOrderAccess`，二者均需主账号在 RAM 控制台授予。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)


