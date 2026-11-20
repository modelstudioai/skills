# Token 计量与管理

Token 计量与管理是百炼平台对大模型调用行为进行精细化用量度量、成本归因与资源调控的核心横切能力。它以输入/输出 Token 数为统一计量单位，贯穿模型推理、知识检索、多模态解析等各类 AI 调用场景，并直接驱动计费结算、监控告警、限流控制与成本优化决策。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理（Generation / Chat Completions）**：所有通义千问系列（如 `qwen-plus`、`qwen3.8-max`）、文本嵌入（`text-embedding-v4`）、重排（`qwen3-rerank`）等模型调用均按实际消耗的 **input_tokens + output_tokens** 精确计量。Token 数在 API 响应的 `usage` 字段中返回（如 `"input_tokens": 127, "output_tokens": 89`），是计费与监控的唯一权威依据。

- **Agent 与 Flow 应用**：Managed Agents 和 Flow Agent 中的每一步模型调用（含工具调用触发的子模型、知识库路由/召回/问答阶段的向量模型与排序模型）均独立计量 Token。例如一次 RAG 问答可能涉及：`text-embedding-v4`（输入 query）→ `qwen3-rerank`（重排 TopK 文档）→ `qwen3.8-max`（生成答案），三者 Token 分别计费、分别监控。

- **ParseX 多模态解析**：虽不直接暴露 Token，但底层统一折算为等效 Token 量参与用量统计与配额管控。文档页、音视频秒数等原始计量单位，在费用中心和用量 API 中会映射为标准化的 `equivalent_tokens`，用于跨服务统一限额（如免费额度抵扣）与告警联动。

- **高速推理能力（Prime / TPM 预留 / DTU）**：Token 计量逻辑保持一致，但计费单价或折算方式可能调整。例如吞吐预留响应中返回的 `provisioned_tokens` 是经长输入阶梯折扣与前缀缓存优化后的**折算 Token 量**，用于精准计费；DTU 方案则按 `TPM × 时长` 折算为等效 Token 消耗，体现物理算力占用。

- **监控与告警**：`模型消耗 TotalToken 数` 是核心可观测指标，支持分钟级聚合、跨模型对比与阈值告警（如“单模型 TPM 突增 300%”）。Token 用量趋势与失败率、延迟等健康指标交叉分析，可快速定位低效 Prompt、冗余召回或模型降级问题。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 示例值 |
|--------|----------|------|--------|
| `input_tokens` / `output_tokens` | 所有模型 API 响应 | 实际消耗的输入/输出 Token 数，只读字段，不可配置 | `"input_tokens": 256, "output_tokens": 103` |
| `total_tokens` | 所有模型 API 响应 | `input_tokens + output_tokens`，用于快速汇总 | `359` |
| `provisioned_tokens` | 吞吐预留（TPM Reservation）响应 | 经缓存、长输入优化后的折算 Token 量，用于计费 | `281`（低于原始 `total_tokens`） |
| `equivalent_tokens` | ParseX、知识库等组件用量 API | 将页/秒/RCU 等非 Token 单位折算后的统一计量值，用于配额与告警 | `12000`（对应 120 页 PDF 解析） |
| `token_limit`（请求头） | 高级调用控制（可选） | 通过 `X-DashScope-Token-Limit` 请求头硬性限制本次调用最大 output_tokens，防失控生成 | `X-DashScope-Token-Limit: 512` |

> ⚠️ 注意：  
> - Token 计量以模型服务端实际分词结果为准，客户端预估（如 tiktoken）可能存在偏差，**务必以 API 响应 `usage` 字段为准**；  
> - 免费额度、节省计划、资源包均按 `equivalent_tokens` 或 `total_tokens` 抵扣，不区分 input/output；  
> - `token_limit` 为软限制，部分模型（如流式响应）可能略超，建议预留 5–10% 余量。

## 面向开发者，简洁实用

- ✅ **必查**：每次模型调用后，立即解析响应中的 `usage` 字段，记录 `input_tokens` 和 `output_tokens`，用于本地用量审计与成本归因。  
- ✅ **必用**：通过 [用量 API](https://bailian.console.aliyun.com/managed-agent/usage) 按工作空间/Agent/Session 维度拉取 Token 汇总数据，结合时间窗口做趋势分析。  
- ✅ **必控**：对高风险场景（如用户自由输入、长文档摘要）启用 `X-DashScope-Token-Limit` 头，避免意外超长输出导致 Token 爆涨。  
- ✅ **必优**：在知识库检索链路中，降低 `TopK`、关闭重排、选用轻量嵌入模型（如 `text-embedding-v3-small`），可显著减少排序与生成阶段的 Token 消耗。  
- ❌ **勿信**：不要依赖客户端 tokenizer 估算 Token 数做计费预算——百炼使用自研分词器，结果更准确且与计费完全一致。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [preparations](../api/preparations.md)
- [model monitoring](../guides/model-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


