# [overview](overview.md) 1efecd5ed9835b67

Skill API 是百炼平台用于全生命周期管理 Skill（技能）的核心接口，支持自定义 Skill 与官方 Skill 的创建、查询、删除及版本控制。该 API 以 RESTful 风格设计，所有操作均基于工作空间隔离，需通过 API Key 认证。详细行为规范与错误处理逻辑请参见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)。

## 支持的模型/功能

- **Skill 管理**：创建、获取单个 Skill、分页列出全部 Skill（含 `customer` 和 `official` 类型）、删除自定义 Skill  
- **版本管理**：为自定义 Skill 创建新版本、分页列出版本、获取指定版本详情、下载 ZIP 包（预签名 URL，2 小时有效）  
- **状态驱动**：支持 `checking`（扫描中）、`active`（可用）、`rejected`（未通过安全扫描）、`deleted`（已删除）四类状态，不同状态影响可见性与可操作性  
- **元数据支持**：`SkillDTO` 返回 `classification` 和 `meta_info`（仅官方 Skill），`SkillVersionDTO` 提供 `additional_properties.error_info`（扫描失败明细）  
- 全量接口定义与语义说明详见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 中的「接口列表」章节。

## 关键参数

- **Endpoint 模板**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills`，其中 `workspace_id` 必须从[百炼控制台](https://bailian.console.aliyun.com/)右上角工作空间菜单复制，不可替换为区域或域名别名  
- **分页参数**（适用于 `/skills` 和 `/skills/{skill_id}/versions`）：  
  - `pageNo`：整数，最小值 1，默认 1  
  - `pageSize`：整数，范围 1–100，默认 20；`pageNo × pageSize ≤ 10000`  
- **路径参数**：`skill_id`（如 `sk_abc123`）、`version`（如 `1.0`）均为必填，且 `skill_id` 需区分大小写  
- **认证**：必须配置 API Key，具体方式见 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 中的「前提条件」部分  

## 使用方式

1. **前置准备**：开通百炼服务，[创建 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并获取工作空间 ID  
2. **调用示例（创建 Skill）**：  
   ```bash
   curl -X POST "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
     -H "Authorization: Bearer <api_key>" \
     -F "file=@skill-package.zip"
   ```  
3. **响应解析**：所有接口统一返回标准结构（含 `success`, `error_code`, `data`, `request_id`），无需额外适配不同接口的响应格式  
4. **版本下载流程**：先调用 `GET /skills/{skill_id}/versions/{version}/content` 获取 `file_url`，再发起 GET 请求下载 ZIP（注意 `file_url` 2 小时过期）

## 限制和注意事项

- **可见性规则严格**：按 `skill_id` 访问时，若 Skill 不可见（如 `source=official` 但 `status≠active`，或 `source=customer` 但非当前工作空间），API 直接返回 404（而非权限错误）  
- **官方 Skill 不可删除/修改**：`DELETE /skills/{skill_id}` 仅对 `source=customer` 生效；官方 Skill 的 `status=active` 才在列表中可见，`checking`/`rejected` 状态不返回  
- > **注意**：文档中 `SkillVersionDTO.additional_properties.error_info` 类型标注为 `map<string,string>`，但实际响应中可能为 `null` 或空对象；建议调用方做 `error_info?.hasOwnProperty(...)` 安全判断，避免空指针异常  
- **ZIP 包要求**：创建 Skill 或版本时上传的 ZIP 必须包含 `SKILL.md`（定义 `name`/`description`），否则 `display_name` 和 `display_description` 将为空字符串  
- 所有错误码定义与处理建议请查阅 [原文标题](../../raw/application-api-reference/overview-1efecd5ed9835b67.md) 引用的 [Skill API 错误码](../../raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md) 文档

## 来源文档

- [Skill API 概览](../../raw/application-api-reference/overview-1efecd5ed9835b67.md)


