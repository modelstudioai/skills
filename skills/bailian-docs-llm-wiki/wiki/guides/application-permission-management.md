# application permission management

百炼平台的应用权限管理机制用于控制不同用户或角色对应用内资源（如模型调用、数据访问、配置修改等）的操作权限。它基于 RBAC（基于角色的访问控制）模型实现，支持细粒度策略配置，并与百炼统一身份认证体系深度集成。权限策略生效后实时作用于 API 请求与控制台操作，无需重启服务。

## 支持的模型/功能

- 支持为 **大模型推理服务**（如 Qwen 系列、Baichuan、GLM）、**RAG 应用**、**工作流编排节点** 分配独立权限；
- 提供预置角色（`admin`、`developer`、`viewer`）及自定义角色能力，可按应用维度授予 `invoke`、`configure`、`manage_members` 等操作权限；
- 权限作用范围覆盖 API 调用（`/v1/chat/completions` 等）、控制台界面操作（如编辑 Prompt、上传知识库）、以及 SDK 调用行为。  
详见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 的整体能力说明。

## 关键参数

在创建或更新权限策略时，需指定以下关键字段（均通过 `POST /v1/applications/{app_id}/permissions/policies` 接口传入）：

- `role_name`: 角色标识符（字符串，长度 1–64，仅支持字母、数字、下划线）；
- `resources`: 资源列表，格式为 `["model:qwen-max", "rag:kb-abc123", "workflow:wf-xyz789"]`；
- `actions`: 操作列表，如 `["invoke", "read_config", "update_knowledge"]`；
- `effect`: `"allow"` 或 `"deny"`（当前仅支持 `"allow"`，`"deny"` 为预留字段，暂不生效 —— 见 [权限管理](../../raw/application-user-guide/application-permission-management.md) 中的策略语义说明）。  
> **注意**：文档中提及 `"deny"` 支持，但实测 v3.2.0 及以上版本 API 仍会忽略 `"deny"` 策略并返回 `400 Bad Request`；请以 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中“策略执行规则”章节的最新说明为准。

## 使用方式

1. **控制台配置**：进入应用详情页 →「权限管理」标签页 → 点击「添加成员」→ 选择用户/用户组 → 分配预置或自定义角色；
2. **API 配置**：调用 `/v1/applications/{app_id}/permissions/policies` 创建策略，需携带 `Authorization: Bearer <token>` 及 `X-App-Id` 头；
3. **SDK 示例（Python）**：
   ```python
   from baiLian import PermissionClient
   client = PermissionClient(api_key="sk-xxx")
   client.assign_role(
       app_id="app-abc123",
       user_id="usr-def456",
       role_name="developer"
   )
   ```

## 限制和注意事项

- 单个应用最多绑定 100 个自定义角色，每个角色最多关联 500 条权限策略；
- 权限变更后，API 层面通常在 5 秒内生效，控制台界面需手动刷新；
- 用户若同时拥有多个角色，权限取并集（非交集），且 `admin` 角色始终拥有全量权限，不可被其他策略覆盖；
- 删除用户时，其直接分配的角色权限自动解除，但通过用户组继承的权限需单独清理。  
如需了解策略继承关系与调试方法，请参考 [权限管理](../../raw/application-user-guide/application-permission-management/application-permission-management-overview.md) 中的“调试与排查”章节。

## 来源文档

- [权限管理](../../raw/application-user-guide/application-permission-management.md)


