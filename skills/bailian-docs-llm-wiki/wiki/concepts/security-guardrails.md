# AI 安全护栏

AI 安全护栏是百炼平台面向模型输入与输出内容提供的实时、可配置的多维度安全检测能力，用于自动识别并拦截涉黄、涉政、暴恐、广告、违禁词等高风险内容，是保障 AI 应用合规上线与稳定运行的基础性防护机制。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用（文本/图片类）**：在调用 `ChatCompletion`、`TextToImage` 等模型接口时，通过请求头 `X-DashScope-DataInspection` 显式启用护栏，指定对 `input`（用户输入）和/或 `output`（模型生成）进行内容安全检测。例如：`{"input":"cip","output":"cip"}` 表示同时检测输入与输出。
- **Agent 全链路防护**：作为 Agent 治理“量·挡·记”闭环中的“挡”环节，默认开启基础内容安全检测（如输入过滤、输出过滤），并支持在高级安全策略中统一配置 7 类防护（含提示词攻击防御、敏感数据外泄阻断等），所有策略对当前阿里云账号下全部 Agent **全局生效**。
- **知识库与 RAG 场景**：在知识库文档上传、解析及[检索增强生成](rag.md)（RAG）过程中，护栏会自动扫描文件元数据、切片文本及最终生成答案，防止恶意内容注入或泄露。
- **安全运营联动**：检测拦截事件将实时上报至 Security API（`/api/v1/agentstudio/security`），开发者可通过 `/agent_logs` 查询告警详情，按 `risk_level`、`asset_type` 等字段筛选，并调用 `/export_agent_logs` 导出 Excel 进行审计分析。

> ⚠️ 注意：AI 安全护栏**仅在华北2（北京）地域可用**，且必须显式配置请求头才能生效；业务空间维度无独立开关，不启用即不检测。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `X-DashScope-DataInspection` | HTTP 请求头 | JSON 字符串 | 启用并指定检测范围 | `{"input":"cip","output":"cip"}`（`cip` 表示启用内容安全检测） |
| `risk_level` | Security API `/agent_logs` 查询参数 | string | 告警风险等级筛选 | `high` / `medium` / `low` |
| `asset_type` | Security API `/agent_logs` 查询参数 | string | 关联资产类型 | `agent` / `tool` / `knowledge_base` / `model` |
| `Credits` | 计费维度 | 数值 | 每个 Agent 席位每日默认 300 Credits，按检测内容 Token 量消耗（1 Credit ≈ 1 Token），不结转 | 超额部分按 0.0015 元/Credit 计费（限时免费中） |

- **配置方式**：
  - 控制台：暂无独立 UI 开关，需通过 API 或 SDK 设置请求头；
  - SDK（Python/Java）：无需额外代码，直接在请求中添加 `headers={"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'}`；
  - HTTP 调用：确保请求头中包含该字段，且值为合法 JSON 字符串（注意双引号转义）。

## 面向开发者，简洁实用

- ✅ **必做**：在北京地域调用模型前，务必添加 `X-DashScope-DataInspection` 请求头，否则无任何内容安全防护。
- ✅ **推荐**：对生产环境 Agent 统一启用 `{"input":"cip","output":"cip"}`，兼顾用户体验与合规底线。
- ✅ **可观测**：通过 Security API 的 `/overview` 查看 24 小时拦截统计（如 `content_safety.hit`），用 `/agent_logs` 定位具体拦截样本。
- ❌ **勿省略**：不要依赖“默认开启”——百炼平台所有安全策略均需显式启用，无隐式防护。
- ❌ **勿跨地域尝试**：在非北京地域设置该请求头将被忽略，且不报错，易造成防护盲区。

如需进一步定制检测规则（如自定义关键词库、白名单绕过），请通过工单申请企业级内容安全服务支持。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [agent billing](../guides/agent-billing.md)
- [application support](../guides/application-support.md)
- [more](../api/more.md)


