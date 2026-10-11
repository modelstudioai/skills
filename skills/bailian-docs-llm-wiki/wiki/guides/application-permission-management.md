# application permission management

百炼平台的应用权限管理机制用于控制不同用户或角色对应用（如工作流、API 服务、Bot）的访问与操作权限，支持细粒度的读写、执行、配置等能力划分。该机制基于 RBAC 模型实现，与百炼统一身份体系（IAM）深度集成。开发者可通过控制台或 OpenAPI 配置权限策略，所有变更实时生效。

## 支持的模型/功能

- 支持为「应用」（Application）实体分配权限，包括：`view`（查看配置与日志）、`execute`（调用 API 或运行 Bot）、`edit`（修改流程、提示词、参数）、`manage_permissions`（管理他人权限）  
- 权限作用域支持三级粒度：**租户级**（全应用）、**应用级**（单个应用 ID）、**版本级**（特定 workflow version 或 bot revision）  
- 当前仅对 `workflow` 和 `bot` 类型应用启用完整权限控制；`api_service` 类型暂不支持 `edit` 和 `manage_permissions`，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md)

## 关键参数

调用权限管理 OpenAPI（`POST /v1/applications/{app_id}/permissions`）时需指定：
- `principal_type`: `user` 或 `role`（目前仅支持 `user`，`role` 功能仍在灰度中，参见 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md)）  
- `principal_id`: 用户 UID（非邮箱或用户名）  
- `actions`: 字符串数组，如 `["view", "execute"]`；不支持通配符，必须显式声明  
- `scope`: 必须为 `application` 或 `version`，且 `version` 仅在应用类型为 `workflow` 时有效  

> **注意**：文档中曾提及 `principal_type: "group"` 的支持，但当前 API 实际返回 `400 Unsupported principal_type`，该描述已过时，请以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中最新 OpenAPI Schema 为准。

## 使用方式

1. **控制台操作**：进入应用详情页 → 「权限」标签页 → 点击「添加成员」→ 输入用户 UID → 勾选所需操作权限 → 保存  
2. **OpenAPI 调用**：使用 `X-DashScope-Token` 认证，请求体示例：
   ```json
   {
     "principal_type": "user",
     "principal_id": "usr-abc123",
     "actions": ["view", "execute"],
     "scope": "application"
   }
   ```
3. **批量设置**：暂不支持批量接口，需循环调用单条授权 API；批量需求可参考 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中推荐的脚本化方案。

## 限制和注意事项

- 单个应用最多绑定 500 个独立权限条目（用户 × 操作 × 作用域组合）  
- `manage_permissions` 权限不可继承，必须由租户管理员或应用创建者显式授予  
- 删除用户账号后，其名下所有应用权限自动失效，但历史审计日志仍保留 90 天  
- 权限变更不触发应用重启或缓存刷新，`execute` 权限生效延迟 ≤ 2 秒

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


