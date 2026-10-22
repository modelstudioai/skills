# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理服务、Prompt 模板等）的核心页面，为开发者提供可视化操作界面与标准化 API 接口。所有通过控制台或 SDK 创建的模型相关资产均在此集中展示、检索和生命周期管理。该页面不直接执行推理，而是作为资产元数据与部署状态的聚合视图。

## 支持的模型/功能

- 微调模型（Fine-tuned Models）：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan2、GLM4 等主流开源基座的 LoRA/Full 微调产物  
- 推理服务（Inference Endpoints）：已部署的 HTTP 服务实例，含自动扩缩容状态与健康指标  
- Prompt 工程资产：结构化 Prompt 模板（含变量占位符与示例）、Prompt 版本快照及 A/B 测试配置  
- 向量库关联项：绑定至 RAG 应用的向量数据库索引（仅显示绑定关系，非管理入口）  
详情见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的能力边界说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_type` | string | 是 | 取值：`fine_tuned_model` / `endpoint` / `prompt_template` / `vector_index_ref` |
| `status` | string | 否 | 过滤状态：`active` / `failed` / `pending` / `deleting`；默认返回全部 |
| `page` / `page_size` | integer | 否 | 分页参数，`page_size` 最大支持 100，超出将被截断 |
| `sort_by` | string | 否 | 支持 `created_at`（默认）、`updated_at`、`name` |

> **注意**：文档 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 中列出的 `sort_by=last_used` 已于 v3.2.0 下线，实际调用将忽略该字段并按 `created_at` 回退 —— 请以 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的最新接口定义为准。

## 使用方式

- **控制台操作**：登录后进入「模型服务」→「资产中心」，支持按类型筛选、关键词搜索（匹配 `name` 和 `description`）、批量导出元数据（JSON 格式）  
- **API 调用**：调用 `GET /v3/assets`（需 `Authorization: Bearer <token>`），响应体为分页列表，每项含 `id`、`name`、`asset_type`、`status`、`created_at` 等标准字段  
- **SDK 示例（Python）**：
  ```python
  from alibabacloud_bailian20231229 import models as bailian_models
  client = bailian_models.Client(...)
  req = bailian_models.ListAssetsRequest(asset_type="endpoint", status="active")
  resp = client.list_assets(req)
  ```

## 限制和注意事项

- 单次 API 请求最多返回 100 条记录（`page_size=100` 为硬上限），无游标式分页，需配合 `page` 参数遍历  
- `prompt_template` 类型资产不支持通过 API 删除，仅可在控制台操作（因涉及版本依赖校验）  
- 向量库索引（`vector_index_ref`）仅作为只读引用展示，其生命周期由向量库模块独立管理，删除资产中心条目不会影响底层向量数据  
- 所有资产 ID 全局唯一，但命名（`name`）在同类型内允许重复；建议在 `description` 中补充业务标识。更多约束详见 [资产中心](../../raw/model-user-guide/asset-center-page.md) 的“使用限制”章节。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


