# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 面向开发者提供标准化的 RESTful 接口，所有操作均基于工作空间隔离，并依赖统一认证机制。详细行为规范和错误处理逻辑请参阅 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 类型）、删除自定义 Skill。
- **版本管理**：为自定义 Skill 创建新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（通过预签名 URL）。
- **状态驱动**：支持 `checking`、`active`、`rejected`、`deleted` 四种状态，不同状态影响可见性与可操作性（例如官方 Skill 仅 `active` 版本可被调用方访问）。
- **元数据支持**：`SkillDTO` 和 `SkillVersionDTO` 包含展示名称、描述、分类、安全扫描结果（`error_info`）等结构化字段，详见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 中的数据结构定义。

## 关键参数

- **`workspace_id`**：必需路径变量，用于构造 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`），需从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单中复制。
- **分页参数**（适用于 `/skills` 和 `/skills/{skill_id}/versions`）：
  - `pageNo`：整数，最小值为 1，默认为 1；
  - `pageSize`：整数，取值范围 1–100，默认为 20；
  - `pageNo × pageSize ≤ 10000`，否则返回 400 错误。
- **版本号格式**：严格遵循 `major.minor` 格式（如 `1.0`、`2.1`），不支持 `1.0.0` 或 `v1.0` 等变体。
- **认证凭证**：必须在请求头中携带有效的 `Authorization: Bearer <API_KEY>`，API Key 需按 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 前提条件中所述方式创建。

## 使用方式

1. **准备环境**：确保已开通百炼服务，创建 API Key，并获取目标工作空间 ID。
2. **构造请求**：
   - 使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills` 作为基础 Endpoint；
   - 对于版本上传（`POST /api/v1/skills/{skill_id}/versions`），请求体为 `multipart/form-data`，包含 `file` 字段（ZIP 包）及可选 `version` 字段；
   - 所有响应均遵循统一结构（含 `success`、`error_code`、`data`、`request_id`），便于程序化解析。
3. **处理分页与状态**：根据响应中 `Page` 结构的 `total`、`page_no`、`page_size` 计算总页数；检查 `status` 字段决定是否可调用（如 `checking` 状态不可用）。

## 限制和注意事项

- **可见性规则差异**：官方 Skill 的版本仅 `active` 状态对调用方可见；而自定义 Skill 的版本（包括 `checking` 和 `rejected`）在 `GET /skills/{skill_id}/versions` 中均可列出。> **注意**：该规则与部分旧版文档中“所有 Skill 版本均按 status 过滤”的描述矛盾，请以 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 中“可见性”章节为准。
- **删除行为**：`DELETE /api/v1/skills/{skill_id}` 将永久删除该 Skill 及其所有版本，不可恢复；官方 Skill 不支持删除。
- **ZIP 包约束**：上传 ZIP 包须包含合法 `SKILL.md` 文件，且顶层目录不得嵌套；文件 URL 有效期仅 2 小时，需及时下载。
- **安全扫描强制性**：所有自定义 Skill 版本上传后自动触发安全扫描，`checking` 状态期间无法调用，`rejected` 状态需修正后重新上传。

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


