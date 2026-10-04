# Token

Token 是百炼平台中用于度量和计量模型输入与输出内容的基本单位，是资源配额、计费、监控与限流的核心粒度。一个 Token 通常对应一个子词（subword）或字符级单元（具体取决于模型分词器），而非固定字节数或字符数；多模态输入（如图像、音频）会按模型定义的换算系数折算为等效文本 Token。

## 在百炼平台的不同场景中，这个概念如何使用

- **资源配额与计费（Token Plan）**：Token 是 Token Plan 套餐的计量基础。每次调用（如 `/v1/chat/completions`）的 `input_tokens + output_tokens` 总和实时扣减所绑定套餐的当日配额。图像、音频等非文本输入按模型版本对应的系数折算（例如 Qwen-VL 中 1 张 512×512 图像 ≈ 1280 tokens），详见官方换算表。
  
- **用量监控（Model Monitoring）**：`/v1/monitoring/metrics` 接口及控制台「监控中心」中，“输入 Token 数”“输出 Token 数”是核心指标，支持按项目（`project_id`）聚合统计，用于容量规划与成本分析（v2.3+ 模型才提供精确 token 粒度）。

- **可观测性（AgentEval）**：在智能体全链路 Trace 中，每个模型调用节点自动记录 `input_tokens` 和 `output_tokens`，用于定位高消耗环节、分析 Prompt 效率，并支撑 LLM 评估器自身的调用计费（LLM 评估器产生的 token 按标准计费）。

- **API 资源治理（Token Plan API）**：组织管理员通过 `/v1/token-plan/seats/{seat_id}/quota` 等接口为席位或成员分配 Token 配额，单位为千 Token（k-tokens），最小值为 100（即 100,000 tokens）；配额变更仅对后续请求生效。

- **异步与多模态调用（More about Models）**：异步任务（如图像生成）虽不直接暴露 token 字段，但其底层推理仍计入调用者绑定的 Token Plan；上传图像等文件获取临时 URL 时，平台内部已预估并预留对应 token 消耗，确保调用时不会因配额不足失败。

## 关键参数和配置

- `max_tokens`（请求级）：硬性输出长度上限，超出将返回 `400 Bad Request`，不计入配额；建议设为合理值以避免意外超限。
- `temperature` / `top_p`（请求级）：影响输出多样性与长度，间接增加实际输出 token 数；高值易导致冗长或重复响应。
- `repetition_penalty`（请求级）：过高（>1.5）可能引发模型反复重写，显著抬升输出 token 消耗。
- `quota`（Token Plan API）：配额值，单位为千 Token（k-tokens），非“个 token”；例如 `quota: 500` 表示 500,000 tokens/日。
- 单次请求限制：`input_tokens + output_tokens ≤ 套餐单日上限 × 5%`（如 100 万套餐，单次最多 5 万 tokens）。

## 面向开发者，简洁实用

- ✅ **查用量**：调用 `/v1/usage` 获取当前 API Key 的当日剩余 token；  
- ✅ **看明细**：在控制台「监控中心」→「模型调用」页查看按小时/天聚合的 `input_tokens` 和 `output_tokens`；  
- ✅ **控配额**：用 Token Plan API 为团队成员设置独立配额，避免个别账号耗尽全局额度；  
- ✅ **避踩坑**：  
  - 流式响应中断后，已发送的 token 仍计费；  
  - 多模态输入务必参考最新换算系数（随模型版本更新）；  
  - 免费试用额度不适用于私有化模型，且不可叠加；  
  - 所有 token 统计延迟 ≤ 30 秒（Token Plan API）或 2–5 分钟（Model Monitoring），不适用于毫秒级熔断。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [agenteval](../guides/agenteval.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


