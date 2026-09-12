# application permission management

应用权限管理用于控制不同用户或角色对百炼应用的访问与操作权限，包括调用、配置、调试、发布等关键能力。它基于 RBAC（基于角色的访问控制）模型实现，支持细粒度的权限策略配置。权限策略通过平台控制台或 OpenAPI 进行管理，适用于多租户协作场景。

## 支持的模型/功能

- 支持为应用分配 **Viewer（只读）**、**Editor（编辑）**、**Admin（管理员）** 三类内置角色，也可通过自定义策略扩展权限范围  
- 支持按用户、用户组或 RAM 角色绑定权限策略  
- 支持对单个应用实例独立授权，不跨应用继承权限  
- 权限生效范围覆盖控制台操作（如调试、版本发布）、API 调用（`/v1/applications/{app_id}/invoke` 等）及 SDK 使用行为  
- 具体权限项详见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)，该文档同步维护了各操作对应所需的最小权限集  

## 关键参数

在通过 OpenAPI 配置权限时，核心参数包括：  
- `PolicyName`: 自定义策略名称（需全局唯一）  
- `Effect`: `"Allow"` 或 `"Deny"`（当前仅支持 `Allow`）  
- `Action`: 如 `"bailian:InvokeApplication"`、`"bailian:UpdateApplication"`（完整列表见 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview)）  
- `Resource`: 必须为具体应用 ARN 格式，例如 `acs:bailian:cn-shanghai:1234567890123456:application/app-xxxxxx`；不支持通配符 `*` 或跨区域资源  

## 使用方式

1. **控制台方式**：进入「应用详情页 → 权限管理 → 添加成员」，选择用户/用户组并指定角色  
2. **OpenAPI 方式**：调用 `AttachPolicyToUser` 或 `AttachPolicyToGroup`（需先创建策略），参考 [权限管理](https://help.aliyun.com/zh/model-studio/application-permission-management-overview) 中的策略模板示例  
3. **Terraform 方式**：使用 `alicloud_bailian_application_permission` 资源（v1.12.0+），注意其 `policy_document` 字段需严格遵循最小权限原则  

## 限制和注意事项

- 单个应用最多绑定 100 个独立权限策略（含内置角色隐式策略）  
- 权限变更后最长 5 分钟内全量生效（缓存刷新周期），调试接口可能短暂出现 403 延迟响应  
- **不支持**对子应用（如嵌套在工作流中的子应用）单独授权；子应用权限继承父应用策略  
> **注意**：原始文档中提及“可通过 `ListApplicationPermissions` 查询所有权限绑定关系”，但该 API 已于 v2.3.0 版本下线，实际应使用 `ListPoliciesForApplication` 替代，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md)  
- 删除用户时，其直接绑定的权限策略自动解绑，但所属用户组的策略仍保留；建议定期审计 `GroupPolicyAttachment` 关系  
- 所有权限操作均记录于 ActionTrail，可用于合规审计，日志字段 `eventSource` 为 `bailian.aliyuncs.com`

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


