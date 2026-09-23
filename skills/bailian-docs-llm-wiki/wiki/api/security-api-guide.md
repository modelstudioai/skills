# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于统一鉴权机制，通过阿里云百炼 API Key 访问，基地址按工作空间与地域拼装。该 API 当前仅支持 `cn-beijing` 地域，面向开发者提供结构化、可编程的安全可观测能力。

## 支持的模型/功能

Security API 不涉及大模型推理，而是聚焦于 Agent 全生命周期安全治理的数据面能力，主要包括以下五类功能：

- **防护概况**：获取最近 24 小时防护总览（`/overview`）与 Agent 资产挂载统计（`/asset_summary`），含能力开关状态、各模块覆盖情况及拦截/扫描量汇总。
- **策略管理**：查询全量 11 条安全策略（`/policies`），包括启用状态、所属风险域（如 `model_interaction`、`runtime_tool`）及是否免费，详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警查询**：支持游标分页检索告警列表（`/agent_logs`），可按风险等级、处置状态、资产类型等多维条件筛选；并支持单条告警详情查询（`/agent_logs/{alert_id}`），返回原始风险上下文与拦截话术。
- **告警导出**：通过 `/export_agent_logs` 提交导出任务，支持按当前筛选条件导出全部记录；再通过 `/export_status` 查询进度与下载链接。
- **通用能力**：所有接口共享统一响应结构与错误码体系，例如 `12000094` 表示告警查询失败，建议重试 —— 具体错误码定义见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

> **注意**：文档 5 中 `asset_type` 参数支持值包含 `channel` 和 `memory`，但文档 6 的响应体说明中将 `asset_type` 示例值写为 `"app"`，与文档 5 列表字段定义不一致；实际调用应以文档 5 的枚举为准（`agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`），文档 6 中 `"app"` 属于过时描述。

## 关键参数

- **Endpoint 拼装**：必须使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 为控制台右上角获取的实际 ID，地域固定为 `cn-beijing`。
- **鉴权头**：`Authorization: Bearer <your-api-key>`，API Key 需通过 [控制台](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。
- **分页与筛选**：
  - 告警列表（`/agent_logs`）支持 `current_page`、`page_size`、`risk_level`、`status_list`、`asset_type` 等参数；
  - 导出请求（`/export_agent_logs`）的 `params` 字段需传入 JSON 字符串（非对象），且键名首字母大写（如 `"CurrentPage"`），与列表接口参数名不一致，需严格按示例格式序列化。
- **时间范围**：防护总览（`/overview`）固定查询最近 24 小时，无时间参数；其他接口未限定时间窗口，数据默认为全量历史（受后台保留策略约束）。

## 使用方式

1. **初始化配置**：确认已开通百炼服务，创建 API Key 并获取 `workspace_id`；
2. **构造请求**：按接口路径拼接 URL，设置 `Authorization` 头，补充必要参数或请求体；
3. **处理响应**：
   - 所有接口均返回标准结构 `{"success": boolean, "data": ...}`；
   - 单项数据不可用时，对应字段返回 `null`（如 `asset_summary` 中未挂载技能则 `skill: null`），而非 `0` 或空数组；
   - 告警列表响应中 `next_page` 为 `null` 表示末页，需据此终止分页循环；
4. **导出流程**：
   - 先调用 `POST /export_agent_logs` 获取 `export_id`；
   - 再轮询 `GET /export_status?export_id=...`，待 `export_status == "success"` 且 `link` 非空后下载 Excel。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing`，尝试其他 region 将导致连接失败；
- **策略数量固定**：`/policies` 接口始终返回 11 条策略，不分页，不可增删改；
- **导出任务时效性**：导出链接（`link`）具有有效期，需在 `export_status` 变为 `success` 后尽快下载，超时失效；
- **字段兼容性**：文档 2 中 `capabilities` 的 `key` 列表包含 `agent_identity` 等 5 项，而文档 4 中策略 `policy_code` 包含 `content_safety` 等 11 项，二者语义层级不同（前者是能力开关，后者是检测策略），不可混用；
- **错误处理**：遇到 `503` 错误码（如 `12000093`、`12000094`）时，应实施指数退避重试，而非立即报错中断。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


