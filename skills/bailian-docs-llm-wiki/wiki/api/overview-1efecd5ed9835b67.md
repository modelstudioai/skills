# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 面向工作空间粒度设计，所有操作均需绑定有效 workspace_id 并通过 API Key 认证。其响应结构统一、分页机制明确，适用于自动化集成与平台级 Skill 运维场景。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 类型）、删除自定义 Skill  
- **版本管理**：为自定义 Skill 创建新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（通过预签名 URL）  
- **状态驱动行为**：支持 `checking`、`active`、`rejected`、`deleted` 四种状态，不同状态影响可见性与可操作性（例如官方 Skill 仅 `active` 版本可被访问）  
- **元数据与分类**：官方 Skill 返回 `classification` 和 `meta_info`，自定义 Skill 对应字段为 `null`；展示名称与描述优先取自 SKILL.md 中的 `name`/`description` 字段  

> **注意**：[原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 明确说明“官方 Skill 仅 `active` 版本可被访问”，但部分旧版文档未强调此限制，实际调用时若请求 `checking` 或 `rejected` 官方版本将返回 404（按不存在处理），请以本页为准。

## 关键参数

- `workspace_id`：必需路径参数，从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单中复制，构成完整 endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`  
- 分页参数（用于 `/skills` 和 `/skills/{skill_id}/versions`）：  
  - `pageNo`（integer，默认 1，最小 1）  
  - `pageSize`（integer，默认 20，范围 1–100）  
  - `pageNo × pageSize ≤ 10000`，响应中 `Page` 结构包含 `total`、`page_no`、`page_size` 供分页计算  
- `skill_id`：Skill 唯一标识，由 API 返回（如 `sk_abc123`），用于路径参数和版本关联  
- `version`：语义化版本号（格式 `major.minor`，如 `1.0`），用于版本详情与下载接口  

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并获取 `workspace_id`  
2. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`（详见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 中的[认证](../../raw/application-api-reference/overview/authentication-26822a11844efd00.md)说明）  
3. **调用示例（创建 Skill）**：  
   ```bash
   curl -X POST "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
     -H "Authorization: Bearer <api_key>" \
     -F "file=@skill-package.zip"
   ```  
4. **错误处理**：统一响应结构含 `success`、`error_code`、`error_msg` 字段；具体错误码见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 引用的 [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)

## 限制和注意事项

- **可见性规则严格**：按 `skill_id` 访问的接口（如 GET `/skills/{skill_id}`）会先校验可见性；对不可见对象（如已 `deleted` 的自定义 Skill 或非 `active` 的官方 Skill）一律返回 404，而非权限错误  
- **版本下载时效性**：`/versions/{version}/content` 接口返回的 `file_url` 为预签名 URL，有效期仅 **2 小时**，需及时下载  
- **安全扫描阻断流**：上传 ZIP 后进入 `checking` 状态，期间无法调用 `active` 相关功能；若扫描失败（`rejected`），可通过 `additional_properties.error_info` 获取具体文件路径与问题描述  
- **删除行为不可逆**：DELETE `/skills/{skill_id}` 将**永久删除该 Skill 及其所有版本**，无回收站机制  
- **官方 Skill 不可修改**：仅支持查询与下载，不支持创建、更新或删除官方 Skill；其 `source` 字段恒为 `official`，且 `classification` 与 `meta_info` 由平台维护

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


