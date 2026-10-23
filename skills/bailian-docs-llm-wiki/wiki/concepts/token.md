# Token 管理

Token 管理是百炼平台对模型调用过程中输入与输出文本（及多模态内容）所消耗的计算单元（Token）进行计量、配额控制、实时校验与用量观测的核心机制。它贯穿 API 调用生命周期，既是资源约束的执行层，也是成本控制与系统稳定性的基础保障。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用配额控制**：通过 `Token Plan` 机制实现精细化配额分配。开发者在请求中显式指定 `plan`（如 `personal`、`team`、`coding`），系统据此校验单次 `max_tokens` 上限、并发请求数及当日总 Token 消耗量。未指定时按账号身份自动 fallback，配额按自然日（UTC+8）重置。

- **组织级资源编排**：企业管理员通过 `Token Plan API` 统一购买、分配和管理 Token 席位（`seat_type: standard/pro/enterprise`），将配额绑定至成员或 API Key，并实时查询订阅用量。该层不直接操作模型，而是为上层调用提供可计量、可审计、可伸缩的资源底座。

- **可观测性与优化闭环**：在 `Model Monitoring` 中，`TotalToken 数` 是核心用量指标，支持按模型、API Key、时间范围多维统计；同时可基于 Token 消耗突增配置告警，并结合审计日志分析具体请求的 `input_tokens` 与 `output_tokens`，驱动 Prompt 优化、`max_tokens` 合理设置等降本实践。

- **基础调用约束**：所有模型 API 请求均隐式参与 Token 管理——`input.messages` 内容与 `parameters.max_tokens` 共同决定本次调用的 Token 预估与实际消耗；系统在响应头中返回 `X-RateLimit-Remaining` 等字段，供客户端实时感知配额余量。

- **安全与稳定性边界**：Token 管理与 `preparations` 中的 `api_key` 认证、`base_url` 地域隔离协同工作——同一 API Key 的 Token 配额仅在指定地域生效；超限触发 `429 Too Many Requests` 时，必须依据 `X-RateLimit-Reset` 实现指数退避，而非无差别重试。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 是否必填 |
|------|------|------|------|----------|
| `plan` | Header (`X-Plan`) 或 Body 顶层 | string | 指定 Token Plan 类型，决定配额策略；取值如 `personal`、`team`、`coding` | 推荐显式声明（部分接口默认 fallback） |
| `max_tokens` | Body `parameters` 内 | integer | 单次请求最大输出 Token 数，不可超过当前 Plan 允许上限（如 `personal`: 4096） | 否（有模型默认值），但强烈建议显式设置以控本防超限 |
| `org_id` | Token Plan API 请求路径/Body | string | 组织唯一标识，用于席位分配与用量归属 | 是（Token Plan API 所有接口） |
| `seat_type` | Token Plan API（席位类） | string | 席位规格，对应不同 Token 配额包（`standard` / `pro` / `enterprise`） | 是（席位操作接口） |
| `X-RateLimit-Remaining` | 响应 Header | string | 当前周期剩余 Token 配额（权威值，优先于控制台显示） | —— |
| `X-RateLimit-Reset` | 响应 Header | integer (Unix timestamp) | 配额重置时间戳（秒级 UTC 时间） | —— |

> ⚠️ 注意：  
> - Token 计费粒度为整数，精确累加 `input_tokens + output_tokens`，空格、标点、特殊字符、Base64 编码图像块均计入；  
> - 同一请求不可跨 Plan 拆分计费；  
> - 自定义训练模型（Fine-tuned Model）与 BYOM 场景**不适用** Token Plan 约束。

## 面向开发者，简洁实用

- ✅ **立即生效**：在请求 Header 加 `X-Plan: team` 或 Body 加 `"plan": "team"`，即可启用团队级配额，无需额外开通。  
- ✅ **查用量**：调用 `GET /v1/usage/token-plan` 获取当前周期剩余 Token 与并发余量；或访问控制台「用量统计」页面按模型/API Key 筛选。  
- ✅ **控成本**：始终设置合理的 `max_tokens`；用轻量模型处理简单任务；批量任务优先走 OpenAI 兼容 Batch 接口。  
- ✅ **防失败**：收到 `429` 时，读取 `X-RateLimit-Reset` 并实现指数退避（如 `2^retry * 100ms`），避免请求风暴。  
- ✅ **看明细**：开启审计日志后，在监控页查看每条请求的 `input_tokens` 和 `output_tokens`，精准定位高消耗请求。  
- ❌ **不推荐**：硬编码 `api_key` 或 `base_url`；忽略 `X-RateLimit-*` 响应头；在流式响应中依赖中间 chunk 的 `output.text` 完整性。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [model monitoring](../guides/model-monitoring.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)


