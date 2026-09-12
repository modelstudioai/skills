# application permission management

百炼平台的应用权限管理用于控制不同用户或角色对应用（如模型调用、工作流执行、数据访问等）的操作权限。它基于 RBAC（基于角色的访问控制）模型实现，支持细粒度的权限分配与继承。开发者可通过控制台或 OpenAPI 管理权限策略，确保最小权限原则落地。

## 支持的模型/功能

- **角色类型**：内置 `Admin`（全权限）、`Developer`（可编辑应用配置与调试）、`Viewer`（仅查看运行日志与结果）三类系统角色；支持自定义角色并绑定细粒度权限项（如 `app:invoke`、`app:edit-prompt`、`app:manage-tracing`）。  
- **作用范围**：权限可作用于整个工作空间（Workspace-level）、单个应用（App-level）或特定版本（Version-level），其中 Version-level 权限仅在 [原文标题](../../raw/application-user-guide/application-permission-management.md) 中明确说明支持。  
- **集成能力**：支持与阿里云 RAM 角色同步，但需注意 RAM 同步策略不覆盖 Version-level 权限设置——该限制在 [原文标题](../../raw/application-user-guide/application-permission-management.md) 的“权限继承规则”小节中有明确定义。

## 关键参数

调用 `/v1/apps/{app_id}/permissions` 接口时需指定以下关键参数：  
- `principal_type`: `user` / `ram_role` / `workspace_group`  
- `principal_id`: 对应主体的唯一标识（如阿里云 UID 或 RAM Role ARN）  
- `effect`: `allow`（必填，暂不支持 `deny`）  
- `actions`: 字符串数组，例如 `["app:invoke", "app:read-config"]`；完整动作列表见 [原文标题](../../raw/application-user-guide/application-permission-management.md) 附录 A。

## 使用方式

1. **控制台操作**：进入「应用详情页 → 权限管理」标签页，点击「添加权限」，选择主体、作用域和权限动作后保存。  
2. **OpenAPI 调用**：使用 `PUT /v1/apps/{app_id}/permissions` 提交 JSON body（含 `principal_type`, `principal_id`, `effect`, `actions`）；调用前需确保 AK/SK 具备 `bailian:UpdateAppPermission` 权限。  
3. **批量配置**：通过 `POST /v1/workspaces/{workspace_id}/permissions/batch` 批量为多个应用设置相同权限策略（仅限 Workspace-level 和 App-level）。

## 限制和注意事项

- 单个应用最多绑定 500 条权限策略（含继承策略），超出后 API 返回 `400 Bad Request`。  
- Version-level 权限**不继承**父应用的权限，且无法通过控制台 UI 创建（仅 OpenAPI 支持），此行为与早期文档中“所有层级权限均支持图形化配置”的描述存在冲突；> **注意**：该过时描述已从最新版 [原文标题](../../raw/application-user-guide/application-permission-management.md) 中移除，请以当前 API 文档为准。  
- 删除应用时，其绑定的所有权限策略将被级联清除，但 Workspace-level 权限不受影响。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)



