# Token 计费与管理

Token 计费与管理是百炼平台统一的资源计量与成本控制核心机制，以输入/输出 Token 为最小计费单元，贯穿模型调用、评测、训练、部署等全生命周期；所有费用结算、配额限制、预算管控和资源预留均基于精确的 Token 消耗量进行。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：每次 API 请求按实际消耗的输入 Token（[prompt](../guides/prompt.md)）和输出 Token（completion）分别计费，单价依模型、地域、阶梯用量浮动；免费额度自动优先抵扣，额度耗尽后按量扣费。
- **Token Plan 配额管控**：通过 `X-Token-Plan-ID` 请求头绑定预设的 Token Plan，实现单次请求最大 Token 数（`quota`）、突发容量（`burst_quota`）及周期性重置（`reset_interval_seconds`）的硬性约束，适用于多环境隔离、成本封顶与流量整形。
- **模型评测**：当使用「评测数据集」触发被测模型推理时，产生标准推理 Token 费用；若启用大模型评估（裁判模型），其评分过程也按 Token 单独计费。
- **吞吐预留（TPM）**：购买的吞吐资源（如 200 kTPM 输入）本质是 Token 消耗速率承诺，系统按每分钟实际 Token 吞吐量动态校验并保障服务水位，超限将触发限流而非额外计费。
- **模型训练与微调**：训练费用 = 训练数据总 Token 数 × 训练轮数 × 单价，图像/视频任务还叠加 `max_pixels` 等因子换算为等效 Token，体现多模态统一计费抽象。
- **异步任务与文件处理**：异步图像/视频生成任务按最终输出内容的 Token 当量（或等效 Token）计费；上传文件解析（如 PDF 文本提取）产生的中间 Token 消耗亦计入总账单。

## 关键参数和配置

| 参数 | 说明 | 典型值/约束 | 生效位置 |
|------|------|-------------|----------|
| `input_tokens`, `output_tokens` | 实际消耗的 Token 数，由服务端精确统计并返回在响应 `usage` 字段中 | 整数，≥0；多模态模型含视觉 Token 换算 | 所有模型 API 响应体 |
| `token_plan_id` | Token Plan 唯一标识符，用于启用配额控制 | 如 `tp-abc123`，控制台创建分配 | 请求 Header：`X-Token-Plan-ID` |
| `quota` | 单次请求允许消耗的最大 Token 总数（输入+输出） | ≥100，≤1,000,000 | Token Plan 配置项 |
| `burst_quota` | 突发配额上限，支持短时超限 | 默认 `quota × 2`，需连续 3 个周期未超限才生效 | Token Plan 配置项 |
| `reset_interval_seconds` | 配额重置周期 | 支持 `60`（1 分钟）、`300`（5 分钟）、`3600`（1 小时） | Token Plan 配置项 |
| `override_quota` / `override_burst_quota` | 动态覆盖配额（需 `token_plan:override` 权限） | Query 参数，如 `?override_quota=5000` | HTTP 请求 Query |
| 免费额度（Free Tier） | 新人自动发放的 Token 抵扣额度 | 华北2（北京）地域有效，90 天有效期，仅限实时推理 | 账户级自动应用，无需显式配置 |

> ⚠️ 注意：Token Plan 与模型版本强绑定（v2.3+ 接口默认启用），且不支持跨 Region 复用；使用 Token Plan 专属 API Key 时，**不享受免费额度**，图像/视频模型调用将直接报错，必须改用通用 API Key 或 Skill 接入。

## 面向开发者，简洁实用

- ✅ **必做**：始终检查响应中的 `"usage": {"input_tokens": X, "output_tokens": Y}` 字段，用于本地监控、成本归因与预算预警。
- ✅ **推荐**：高并发生产环境避免依赖「免费额度用完即停」或「预算达限即停」，建议结合 Token Plan 设置 `quota` + `burst_quota` 实现主动限流，保障服务稳定性。
- ✅ **降本技巧**：
  - 评测阶段优先复用已有的「推理结果集」，避免重复调用被测模型；
  - 异步任务开启事件驱动回调（EventBridge），替代高频轮询，减少无效 Token 消耗；
  - 多模态输入前预估文本长度，合理设置 `max_output_tokens` 防止长输出失控。
- ❌ **禁止**：在前端代码中暴露 API Key；使用临时 Key 时 `expire_in_seconds` 不得超过 180 秒；Token Plan 不可与 Coding Plan 同时启用。
- 🔧 **调试工具**：使用 OpenAPI Explorer 或 dashscope CLI（`dashscope api call --model qwen-plus --input-text "hello"`）快速验证 Token 消耗与配额行为。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [more about models](../api/more-about-models.md)


