# Token 计费与管理

Token 计费与管理是百炼平台核心的成本控制机制，指以模型实际消耗的输入（input）与输出（output）Token 数量为基本计量单位，按千 Token 或百万 Token 精确计费，并通过用量监控、免费额度、资源包及优化配置实现精细化成本治理的技术实践。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**（文本生成、嵌入、重排、路由等）：所有 LLM、Embedding、Rerank、Routing 类模型均按 `input_tokens` 和 `output_tokens` 分别计费，单价按模型类型和地域浮动（如 `text-embedding-v4`: 0.0005 元/千 Token）。Batch 调用享 50% Token 单价折扣，但计费逻辑不变。
- **Agent 应用运行**：Managed Agents、Flow Agent 中的模型节点、知识库 RAG 的向量检索/排序/问答环节，均独立产生 Token 消耗；Token 费用与运行时费、工具调用费分离，可单独优化。
- **ParseX 解析服务**：图文解析按页换算为 Token（含 OCR+结构化），音视频按秒转文字后计入 Token，统一纳入 Token 计费体系；免费额度（图文/音视频各 3,000 页/100 小时）直接抵扣 Token 消耗。
- **安全防护与监控**：Agent 安全高级防护中的 `credit_consumption` 按内容 Token 换算（1 Credit ≈ 1 Token），每日清零；模型监控中的 `模型消耗 TotalToken 数` 是核心告警指标，用于实时识别 Token 异常突增。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `input_tokens`, `output_tokens` | API 响应头 `X-DashScope-Token-Usage` 中返回的实际消耗值（整数），或用量 API 返回字段；按千 Token（K）或百万 Token（M）阶梯计费 | ✅ 必须在日志或监控中采集该值，用于成本归因与异常诊断 |
| `topk_vector` / `topk_keyword` | 知识库检索召回切片数，直接影响后续 Rerank 模型的 `input_tokens` 消耗量 | ⚠️ 降低至 10–30 可显著减少重排 Token，但可能影响召回质量，需 A/B 测试平衡 |
| 缓存命中折算系数（如 `0.125`） | 启用上下文缓存时，命中部分 Token 按系数折算计费（非免费） | ✅ 调用带缓存能力模型（如 `qwen3.8-max`）时，务必在请求中传入 `cache_enabled: true` 并校验响应头 `X-DashScope-Cache-Hit` |
| 免费额度余量 | 新用户华北2（北京）地域自动发放的 Token 免费额度（如 100 万 Tokens），90 天有效 | ⚠️ 免费额度不跨地域、不跨模型、不结转，用完即停；可通过 `/usage/summary` API 实时查询剩余量 |
| `model_id` + `region` 组合 | Token 单价由模型 ID 与调用地域共同决定（如 `qwen3.7-plus` 在北京 vs 新加坡价格不同） | ✅ 生产环境必须显式指定 `DASHSCOPE_BASE_URL` 并校验 `model_id`，避免因地域误配导致计费偏差 |

## 面向开发者，简洁实用

- **查用量**：调用 `POST /usage/summary`（按天）或 `POST /usage/trend`（按小时），传参 `metric=token_usage`，快速获取业务空间级 Token 消耗明细。
- **控成本**：
  - 优先启用上下文缓存（`cache_enabled: true`）；
  - 知识库场景关闭非必要重排、调低 `topk_vector`；
  - Agent 中避免无意义 AUTO 路由，显式指定轻量模型处理简单意图；
  - 批量任务强制走 Batch 接口（Token 半价）。
- **追账单**：账单明细中通过 `资产/资源实例ID` 字段（含 `;输入/输出类型;` 子串）精准定位 Token 费用归属，例如 `ApiKeyID;space-xxx;qwen3.8-max;input;api`。
- **设告警**：在「模型监控」中对 `模型消耗 TotalToken 数` 配置环比突增告警（如 1 小时内增长 >200%），第一时间发现 Prompt 注入、循环调用等异常。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [preparations](../api/preparations.md)


