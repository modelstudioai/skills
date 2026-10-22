# Token 计量与管理

Token 计量与管理是百炼平台统一的资源度量、配额控制与成本治理核心机制，以输入/输出 Token 为最小计费与限流单位，贯穿模型调用、监控、计费、预算及配额分配全链路。所有 API 调用（含同步/异步、流式/非流式、多模态）均实时计量 Token 消耗，并据此触发配额校验、限流响应与用量统计。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用时**：每次请求（如 `dashscope.Generation.call()`）自动计算 prompt_tokens + completion_tokens，并按模型规格（如 `qwen-max` 最大 context 32K）和阶梯规则折算长文本；缓存命中 Token 单独计费并享受折扣。
- **配额控制时**：Token Plan 绑定至工作空间或组织，通过 `X-Model-Quota-ID` 请求头或 SDK 的 `quota_id` 参数生效，优先级高于全局免费额度；超出 `total_quota` 或 `model_specific_quota` 将返回 `429 QUOTA_EXCEEDED`。
- **监控告警时**：模型监控页面的「调用量（Token总量）」指标即分钟级聚合的 TotalToken 数，支持配置阈值告警（如“1分钟内 Token 消耗 > 500k”），用于主动识别异常调用或配额瓶颈。
- **成本管控时**：免费额度（100万 Token/模型/90天）、节省计划、资源包、按量付费按严格优先级抵扣；预算管理仅覆盖 API 推理费用，且需开启「达到预算后立即停止」才可触发 429 熔断。
- **异步与多模态场景**：图像/视频/语音类[异步任务](asynchronous-task.md)在任务完成时一次性计量全部输入+输出 Token；多模态模型（如 `qwen-vl-plus`）对上传的图片/音频文件按像素/时长折算为等效 Token 后计入总用量。
- **运维与审计时**：审计日志必含 `prompt_tokens`、`completion_tokens`、`total_tokens` 字段；推理日志（开启后）可完整追溯 Token 拆分明细，用于 Prompt 优化与成本归因。

## 关键参数和配置

| 参数 | 说明 | 开发者操作建议 |
|------|------|----------------|
| `total_tokens` | 单次请求实际消耗的 Token 总数（含输入+输出），由服务端精确返回于响应体 `usage` 字段中 | 始终检查该字段，用于本地用量统计与熔断逻辑（如累计达配额 95% 时降级） |
| `max_tokens` | 请求级输出上限（默认 2048，最高 8192），直接影响 completion_tokens 上限 | 生产环境务必显式设置，避免意外长输出耗尽配额；流式场景注意首 Token 后仍受此约束 |
| `X-Model-Quota-ID` | HTTP 请求头，用于显式绑定 Token Plan | SDK v3.2+ 推荐直接传入 `quota_id=` 参数，比手动设 Header 更安全可靠 |
| `burst_ratio` | 突发流量倍率（团队版默认 1.5×，最高 3×），按自然日重置 | 高峰期前可临时提升，但需监控 `x-dashscope-ptu-overflow:true` 响应头判断是否已溢出 |
| 免费额度有效期 | 90 天（自开通/模型发布/申请通过日起算，以较晚者为准） | 在代码中记录首次调用时间，结合用量统计页数据，提前 7 天预警到期风险 |

> ⚠️ 注意：Token 计量**不依赖客户端估算**（如 tiktoken），平台服务端基于真实模型 tokenizer 精确计算；任何长度限制（如 `qwen-turbo` 的 8K context）均在计量前强制截断，超限部分不计费也不返回。

## 面向开发者，简洁实用

- ✅ **必做**：每次调用后解析响应 `usage.total_tokens`，与本地配额余额做差值校验；生产环境必须设置 `max_tokens` 和 `quota_id`。
- ✅ **推荐**：在监控告警中配置「限流错误次数（429）」+「Token总量」双指标联动，快速区分是配额不足还是模型自身限流。
- ✅ **避坑**：  
  - 不要依赖 `tiktoken` 或其他第三方库估算 token 数——百炼使用专属 tokenizer，结果可能偏差 10%+；  
  - 不要将临时文件 URL 用于生产——其 Token 计量与持久化存储一致，但过期后调用失败不返还配额；  
  - 不要忽略 `burst_ratio` 重置周期——它是自然日（非滚动小时），凌晨 0 点自动恢复。
- ✅ **调试技巧**：开启审计日志后，在控制台用量页按 `API-Key ID` 筛选，对比「调用量」与「调用次数」比值，若远大于 1，说明存在高 Token 单次请求，需检查 `max_tokens` 或 Prompt 长度。

## 关联主题页

- [preparations](../api/preparations.md)
- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [token plan api](../api/token-plan-api.md)
- [more about models](../api/more-about-models.md)


