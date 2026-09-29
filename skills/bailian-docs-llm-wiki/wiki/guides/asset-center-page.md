# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理服务、[Prompt 工程](../concepts/prompt-engineering.md)产物等）的核心页面，为开发者提供可视化操作界面与标准化 API 接口。所有通过控制台或 OpenAPI 创建的模型资产均在此集中展示、筛选、调试与下线。该页面的设计遵循 RBAC 权限模型，支持团队级资产隔离与审计追踪。

## 支持的模型/功能

- 微调模型（Fine-tuned Models）：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Baichuan2、GLM4 等主流开源基座的 LoRA/Full 参数微调产物  
- 推理服务（Inference Endpoints）：基于模型部署的 HTTP 服务，支持同步/异步调用、流式响应及自定义请求头  
- Prompt 模板（Prompt Templates）：结构化存储的 Prompt 版本化资产，可绑定变量、设置默认参数并直接调试  
- 向量模型（Embedding Models）：支持 text-embedding-v3、bge-m3 等嵌入模型的托管与批量向量化任务触发  
> **注意**：文档 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中提及的 “支持 Llama3-8B 微调模型” 已过时；当前平台仅支持 Llama3-8B 的推理服务托管，不支持其微调训练流程，详见 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的「模型兼容性表」章节。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 平台分配的唯一资产 ID（如 `ft-qwen2-7b-20240512-abc123`），非用户自定义名称 |
| `visibility` | enum | 否 | 取值 `private`（仅创建者可见）、`team`（同团队可见）、`public`（仅限白名单租户）；默认为 `private` |
| `endpoint_type` | enum | 否 | 仅对推理服务有效，取值 `sync` / `async` / `stream`；未指定时默认为 `sync` |
| `timeout` | integer | 否 | 单位秒，范围 1–300；超时后返回 `504 Gateway Timeout`；[资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 明确要求 `timeout > 0` |

## 使用方式

- **控制台操作**：登录后进入「模型服务 → 资产中心」，支持按 `model_id`、`name`、`status`（active/pending/failed）或 `created_at` 时间范围筛选；点击资产卡片右上角「调试」可打开交互式 API 测试面板  
- **OpenAPI 集成**：调用 `GET /v1/assets` 列表接口（需 `Authorization: Bearer <token>`），支持 `?status=active&limit=20&offset=0` 分页参数；单个资产详情使用 `GET /v1/assets/{model_id}`  
- **CLI 工具**：`bailian-cli asset list --status active --format json`，适用于 CI/CD 流水线集成  

## 限制和注意事项

- 单租户最多创建 200 个活跃资产（`status=active`），超出后需先下线旧资产；此配额不可申请提升  
- `model_id` 一旦生成不可修改，且在租户内全局唯一；重命名仅影响 `name` 字段，不影响 API 路径或 SDK 引用  
- 删除资产（`DELETE /v1/assets/{model_id}`）为**软删除**：资产元数据保留 30 天以支持恢复，但立即停止计费与服务暴露；30 天后自动物理清除  
- 所有资产默认启用日志采集（含输入 [prompt](prompt.md)、输出 token 数、延迟 ms），日志保留 7 天；如需延长，请调用 `PATCH /v1/assets/{model_id}/logging` 启用 SLS 投递  
> **注意**：原始文档 [资产中心](../../raw/model-user-guide/asset-center-page.md) 中“删除即刻释放资源”的描述与实际行为不符；真实行为为软删除，以保障误操作可逆性——请以 [资产中心](../../raw/model-user-guide/asset-center-page/asset-center.md) 的「生命周期管理」章节为准。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


