# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 采用 RESTful 设计，所有操作均基于工作空间隔离，需通过 API Key 认证。详细错误处理机制和响应规范请参考 [Skill API 错误码](../../raw/overview/errors-9f5f81ed72f2a1c6.md)。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 来源）、删除自定义 Skill。
- **版本管理**：为自定义 Skill 上传新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（返回 2 小时有效期预签名 URL）。
- **状态驱动可见性**：官方 Skill 仅 `active` 状态可被访问；自定义 Skill 的版本在 `checking` 或 `rejected` 状态下仍可查询（见 [可见性](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 小节），但不可调用执行。

## 关键参数

- **Endpoint 模板**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`，其中 `workspace_id` 必须从[百炼控制台](https://bailian.console.aliyun.com/)右上角复制，不可替换为区域或服务域名（> **注意**：部分旧文档示例中误写为 `maas.aliyuncs.com/{region}`，以本页 [Endpoint](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 定义为准）。
- **分页参数**：`pageNo`（默认 1，≥1）、`pageSize`（默认 20，范围 1–100），且 `pageNo × pageSize ≤ 10000`。
- **枚举值**：
  - `status`：`checking` / `active` / `rejected` / `deleted`
  - `source`：`customer`（自定义） / `official`（官方）

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并获取工作空间 ID。
2. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`（认证细节见 [authentication-26822a11844efd00.md](../../raw/overview/authentication-26822a11844efd00.md)）。
3. **调用示例（创建 Skill）**：
   ```bash
   curl -X POST "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
     -H "Authorization: Bearer <your_api_key>" \
     -F "file=@skill.zip"
   ```
4. **响应解析**：所有接口统一返回 `success`, `error_code`, `error_msg`, `data`, `request_id` 字段（结构见 [响应结构](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)）。

## 限制和注意事项

- **权限隔离**：仅主账号及所属工作空间内创建的自定义 Skill 可被管理；官方 Skill 仅可读，不可删除或修改版本。
- **删除行为**：调用 DELETE `/skills/{skill_id}` 将**级联删除该 Skill 下所有版本**，不可恢复。
- **ZIP 包要求**：创建 Skill 或版本时上传的 ZIP 必须包含 `SKILL.md`（定义元信息），且文件路径、权限需符合安全扫描规则；失败时 `additional_properties.error_info` 返回具体问题文件及原因。
- **时效性**：`VersionDownloadResponse.file_url` 有效期严格为 2 小时，超时需重新调用下载接口。
- > **注意**：`SkillDTO.classification` 和 `meta_info` 字段对自定义 Skill 恒为 `null`，部分 SDK 示例代码中尝试填充该字段会导致校验失败，请以 [数据结构](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 定义为准。

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


