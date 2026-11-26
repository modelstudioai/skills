# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 采用 RESTful 设计，所有操作均基于工作空间隔离，需通过 API Key 认证。详细错误处理机制和响应规范请参考 [Skill API 错误码](../../raw/overview/errors-9f5f81ed72f2a1c6.md)。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 来源）、删除自定义 Skill。
- **版本管理**：为自定义 Skill 上传新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（返回 2 小时有效期预签名 URL）。
- **状态驱动可见性**：官方 Skill 仅 `active` 状态可见；自定义 Skill 的版本在 `checking` 或 `rejected` 状态下仍可查询（见 [可见性](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)#可见性），但不可调用执行。
- 所有接口均遵循统一响应结构，详见 [响应结构](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)#响应结构。

## 关键参数

- **Endpoint 路径变量**：`{workspace_id}` 必须为当前工作空间 ID，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`。
- **分页参数**（适用于 `/skills` 和 `/skills/{skill_id}/versions`）：
  - `pageNo`: 整数，最小值 1，默认 1；
  - `pageSize`: 整数，范围 1–100，默认 20；
  - `pageNo × pageSize ≤ 10000`，否则返回 400 错误。
- **枚举字段**：
  - `status`: `checking` / `active` / `rejected` / `deleted`；
  - `source`: `customer`（自定义）或 `official`（官方）。

## 使用方式

1. **前置准备**：确保已开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并从[百炼控制台](https://bailian.console.aliyun.com/)复制工作空间 ID。
2. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`（参见 [认证](../../raw/overview/authentication-26822a11844efd00.md)）。
3. **调用示例（创建 Skill）**：
   ```bash
   curl -X POST "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
     -H "Authorization: Bearer <your_api_key>" \
     -F "file=@skill-package.zip"
   ```
4. **解析响应**：始终检查 `success` 字段；失败时 `error_code` 和 `error_msg` 提供定位依据；`request_id` 用于问题排查。

> **注意**：`SkillDTO` 中 `classification` 和 `meta_info` 字段对自定义 Skill 恒为 `null`，但部分旧文档示例中误将其列为可选非空字段——以本 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 定义为准。

## 限制和注意事项

- **权限隔离**：仅主账号及所属工作空间内创建的自定义 Skill 可被管理；官方 Skill 仅可读，不可删除或修改版本。
- **删除行为**：调用 DELETE `/skills/{skill_id}` 将**级联删除该 Skill 下所有版本记录**，且不可恢复。
- **ZIP 包约束**：上传 Skill ZIP 时，顶层必须包含 `SKILL.md`；文件总大小上限为 50 MB（具体限制见 [创建 Skill](../../raw/overview/overview/create-44cf2cde0a7d9a72.md)）。
- **安全扫描异步性**：新创建 Skill 或版本初始状态为 `checking`，需等待扫描完成（通常数秒至数分钟）才可能变为 `active` 或 `rejected`；期间调用 `GET /skills/{id}` 返回 `checking`，但 `GET /skills/{id}/versions/{v}` 仍可访问元数据。
- **可见性校验逻辑**：按 `skill_id` 访问单个资源时（如 `GET /skills/{id}`），若 Skill 不满足可见性规则（例如官方 Skill 为 `rejected`），API 直接返回 404，而非 403 —— 此行为与常规权限模型不同，请务必在客户端做好容错。

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


