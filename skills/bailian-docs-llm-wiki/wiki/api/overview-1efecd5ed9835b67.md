# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 采用 RESTful 设计，所有操作均基于工作空间隔离，需通过 API Key 认证。详细错误处理机制和响应规范请参考 [Skill API 错误码](../../raw/overview/errors-9f5f81ed72f2a1c6.md)。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 来源）、删除自定义 Skill。
- **版本管理**：为自定义 Skill 上传新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（返回 2 小时有效期预签名 URL）。
- **状态驱动行为**：Skill 主记录与版本分别维护独立状态（`checking`/`active`/`rejected`/`deleted`），影响可见性与可操作性（详见 [可见性](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 小节）。
- **元数据支持**：`SkillDTO` 中 `meta_info` 仅对官方 Skill 有效；`SkillVersionDTO` 的 `additional_properties.error_info` 在安全扫描失败时提供路径级问题明细。

## 关键参数

- **Endpoint 路径变量**：`{workspace_id}` 必须为当前工作空间 ID，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`（见 [Endpoint](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)）。
- **分页参数**（`GET /skills` 和 `GET /skills/{skill_id}/versions`）：
  - `pageNo`: 整数，最小值 1，默认 1；
  - `pageSize`: 整数，范围 1–100，默认 20；
  - `pageNo × pageSize ≤ 10000`，否则返回错误。
- **状态枚举**：`status` 字段取值严格限定为 `checking`、`active`、`rejected`、`deleted`；`source` 仅允许 `customer` 或 `official`。

## 使用方式

1. **前置准备**：确保已开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并从控制台复制工作空间 ID。
2. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`（认证机制详见 [认证](../../raw/overview/authentication-26822a11844efd00.md)）。
3. **调用示例**（创建 Skill）：
   ```bash
   curl -X POST "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
     -H "Authorization: Bearer ak-xxx" \
     -F "file=@skill.zip"
   ```
4. **响应解析**：所有接口统一返回标准结构（`success`/`error_code`/`data`/`request_id`），成功时 `error_code` 和 `error_msg` 为 `null`（见 [响应结构](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)）。

## 限制和注意事项

- **可见性规则差异**：按 `skill_id` 查询时，自定义 Skill 只要未删除即可见（含 `checking`/`rejected` 版本），而官方 Skill 的版本仅 `active` 状态才可访问 —— 此逻辑可能导致相同接口在不同 `source` 下返回 404 或空列表，开发时需结合 `source` 和 `status` 判断。
- **删除行为不可逆**：`DELETE /skills/{skill_id}` 将永久删除该 Skill 及其所有版本，无回收站机制。
- > **注意**：文档中 `SkillDTO.classification` 字段说明为“官方 Skill 有值，自定义 Skill 为 `null`”，但实际部分新版自定义 Skill 已支持分类设置；若调用时该字段非空，不应视为异常，以实际 API 响应为准。
- **ZIP 包限制**：上传 Skill ZIP 包大小上限为 50 MB，文件结构必须包含 `SKILL.md`；安全扫描失败时，`additional_properties.error_info` 提供具体文件路径与问题描述，便于调试。
- **请求 ID 追踪**：所有响应头含 `X-Request-Id`，建议日志中持久化该值，便于问题排查（该字段亦在响应体 `request_id` 中重复返回）。

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


