# Token 计量与消耗

Token 计量与消耗是百炼平台对模型调用资源进行精细化计费与成本控制的核心机制，指系统依据实际输入（Input）、输出（Output）及缓存（Cached）Token 数量，结合模型单价与使用场景，实时统计并扣减对应资源额度（如 Credits 或按量费用）的过程。该机制贯穿所有模型调用路径，是开发者评估、监控和优化 AI 应用成本的底层依据。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型 API 调用（含 Token Plan 与按量模式）**：每次 `chat/completions` 或多模态请求均按 `input_tokens + output_tokens + cached_tokens` 三部分计量；其中 `cached_tokens` 指模型复用历史上下文缓存所节省的计算量，但按平台规则仍计入消耗（如 `qwen3.6-plus` 示例中缓存 Token 占比超 80%）。Token Plan 使用 Credits 抵扣，按量模式直接计费。

- **智能体（Agent）与工作流（Flow Agent）**：Token 消耗发生在每个“计费节点”——包括大模型节点、Rerank 排序节点、知识库问答模型、记忆库检索模型等。多个知识库并行检索时，Token 消耗量按知识库数量线性叠加；Rerank 开启与否直接影响排序阶段的 Token 用量（`top_k` 越大，排序 Token 越高）。

- **ParseX 文档解析**：图文解析按页计量（每页隐含文本 Token），音视频按秒转为文本/特征后计量；字段抽取若复用解析结果，可跳过重复 Token 解析，显著降低 Token 消耗。

- **安全高级防护**：内容检测服务将输入内容按 Token 量换算为 Credits（1 Credit ≈ 数十至数百 Token，依模型而异），每日每席位 300 Credits 免费额度即基于此换算逻辑。

- **模型监控与用量分析**：`模型消耗 TotalToken 数` 是核心用量指标，支持分钟级聚合与告警，用于识别异常调用、定位高消耗节点（如未设 `max_tokens` 的长输出、未关 Rerank 的高频检索），但注意：监控数据延迟约 1 分钟，**不作为计费依据**，最终以账单为准。

## 关键参数和配置

| 参数 | 说明 | 开发建议 |
|------|------|----------|
| `input_tokens` / `output_tokens` | 请求中实际发送的输入 Token 数与模型生成的输出 Token 数，由 SDK 或平台自动统计 | 显式设置 `max_tokens` 防止意外长输出；压缩 Prompt、移除冗余注释可减少 input_tokens |
| `cached_tokens` | 缓存命中带来的 Token 节省量，但平台仍按比例计入消耗（如 50% 缓存命中率 ≈ 50% 输入 Token 计费） | 无需手动干预，但需知其存在——相同 Prompt 多次调用仍产生消耗，非零成本 |
| `top_k`（知识库/记忆库） | 初检返回的候选数，直接影响后续 Rerank 模型的输入 Token 量 | 高频低成本场景建议调低（如 `top_k=10`），可降低 60%+ 排序 Token |
| `plan_version=Lite`（记忆库） | 关闭 Rerank 的轻量策略，大幅减少排序 Token 消耗 | 适用于对精度要求不高、QPS 敏感的检索场景 |
| `stream=false`（默认） | 非流式响应会一次性返回全部 output_tokens，更易统计；流式响应需客户端累加 `usage` 字段 | 生产环境建议优先使用非流式，便于用量归因与告警 |
| `model`（必需） | 不同模型 Token 单价差异极大（如 `qwen3.8-flash` 单价约为 `qwen4-max` 的 1/5） | 成本敏感场景应主动选型，避免使用 `auto` 模型（不支持 `tool_choice` 等关键参数，且单价不可控） |

> ⚠️ 注意：`sk-sp-`（Token Plan）与 `sk-`（百炼通用）API Key 的 Token 计量逻辑完全隔离——前者抵扣 Credits，后者触发按量计费；混用将导致计费异常或鉴权失败。

## 面向开发者，简洁实用

- **查用量**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看明细，或调用 `POST /usage/summary` API 获取结构化数据。
- **省 Token**：  
  - 知识库：关 Rerank + 降 `top_k` + 复用 ParseX 解析结果；  
  - 智能体：避免无意义长对话上下文，定期清理沙箱快照（`snapshot_retention_hours` 影响存储费，间接关联 Token 复用效率）；  
  - 模型调用：设 `max_tokens`、精简 system prompt、禁用非必要工具（`tool_choice="none"`）。
- **避坑提示**：  
  - Token Plan 仅限交互式开发，**严禁用于后台脚本或生产服务**，否则订阅可能被暂停；  
  - 所有免费额度（Token Plan、资源包、账户余额）严格按类型隔离，知识库免费时长 ≠ 模型 Token 免费；  
  - 夜间折扣（22:00–08:00）仅限指定模型，调用前请确认控制台实时价格。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [token plan guide](../guides/token-plan-guide.md)
- [token plan personal](../guides/token-plan-personal.md)
- [token plan team edition](../guides/token-plan-team-edition.md)
- [token plan best practice](../guides/token-plan-best-practice.md)
- [model monitoring](../guides/model-monitoring.md)


