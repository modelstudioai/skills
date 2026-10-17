# Token

Token 是百炼平台对模型输入与输出内容进行细粒度计量与计费的核心单位，表示模型实际处理的文本、图像或音视频语义单元（如子词、视觉 patch、音频帧等）。在百炼中，Token 不仅是计费基础，也直接关联配额控制、吞吐限制、缓存计价与资源调度策略。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与资源管理（[test 1](../guides/test-1.md)）**：所有实时推理调用均按「输入 Token + 输出 Token」实际消耗计费；免费额度、按量付费、节省计划、吞吐预留（TPU/PTU）均以 Token 为统一计量单位。长上下文（如 >32K）可能触发阶梯折算系数（如 3x/6x），缓存命中部分按折扣系数（如 0.1–0.25）计费。
- **配额管控（[token plan guide](../guides/token-plan-guide.md)）**：Token Plan 的 `daily_quota`（日千 Token 配额）和 `model_specific_quota`（模型级配额）直接限制账户或模型的日 Token 消耗总量；超限后返回 HTTP 429 及 `quota_exceeded` 错误，不依赖请求次数。
- **API 调用（[qwen api reference](../api/qwen-api-reference.md) / image-generation / video-generation-api）**：  
  - 文本模型：Token 数由输入 `messages` 和输出 `content` 经 tokenizer 实际分词得出，空格、标点、特殊字符均计入；  
  - [多模态](multimodal.md)模型（Qwen-VL、Qwen-Audio、WanX、Vidu 等）：图像按分辨率折算为视觉 Token（如 1024×1024 ≈ 1024 视觉 Token），音频按采样率与时长转为声学 Token，系统自动完成跨模态 Token 汇总；  
  - 所有 API 响应中均包含 `usage` 字段（如 `"input_tokens": 127, "output_tokens": 89`），供开发者实时监控消耗。
- **缓存与优化（[test 1](../guides/test-1.md) / [qwen api reference](../api/qwen-api-reference.md)）**：显式缓存（`cache_control: {type: "ephemeral"}`）可复用前缀 Token，命中时仅对新增 Token 计费；创建缓存本身按更高单价（如 125%）计费，但不占用免费额度。
- **批量与异步任务（[test 1](../guides/test-1.md) / image-generation / video-generation-api）**：Batch 接口 Token 单价为实时推理的 50%，但**不支持免费额度抵扣**；异步视频/图像任务仍按最终生成内容的 Token 总量计费（含 prompt 解析、参考图编码、输出帧解码等全链路）。

## 关键参数和配置

- `max_tokens_per_request`（Token Plan）：单次请求最大输出 Token 数，硬性截断阈值（默认 2048，上限 8192）；超出部分被静默丢弃，不影响输入 Token 计费。
- `daily_quota`（Token Plan）：账户级日 Token 配额（单位：千 Token），北京时间每日 00:00 重置；优先级高于全局 `burst_limit`（TPS 流量整形参数）。
- `model_specific_quota`（Token Plan 团队版）：为指定模型（如 `qwen3.8-max`）单独设置日配额，优先级高于 `daily_quota`。
- `input_tokens` / `output_tokens`（API 响应 `usage` 字段）：只读字段，反映本次请求真实消耗，用于调试、审计与成本归因；开发者不可写入或覆盖。
- 阶梯系数（test 1）：部分模型（如 `qwen3.7-flash`）对超长输入启用动态折算（如 32K–64K 输入按 ×3 计费，>64K 按 ×6），具体规则见各模型定价页。

## 面向开发者，简洁实用

- ✅ **务必检查响应中的 `usage` 字段**：它是唯一权威的 Token 消耗依据，不要自行估算（如按字符数）。
- ✅ **[多模态](multimodal.md)调用需关注 Token 构成**：一张 2048×2048 图像可能贡献数百视觉 Token，远超文本提示词；使用 `qwen-image-*` 时建议先试小图确认 Token 成本。
- ✅ **Token Plan 必须显式绑定**：通过请求 Header `X-Model-Plan-ID` 指定，否则走账户默认 Plan；旧版 `X-Plan-ID` 已废弃。
- ⚠️ **免费额度有地域与调用方式双重限制**：仅适用于同一地域的实时 API 调用，且**不可与 Token Plan 专属 API Key 共用**。
- ⚠️ **流式响应（`stream: true`）的 Token 消耗与完整响应一致**：即使提前中断连接，已生成的输出 Token 仍全额计费。
- 🛑 **禁止前端暴露 API Key 或 Token Plan ID**：所有敏感参数必须在服务端透传，避免密钥泄露导致配额盗用或意外扣费。

## 关联主题页

- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


