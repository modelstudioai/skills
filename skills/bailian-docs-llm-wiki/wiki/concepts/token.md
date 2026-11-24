# Token

Token 是百炼平台对模型输入与输出内容进行标准化计量的基本单位，用于精确计费、配额控制与资源调度。一个 Token 通常对应一个子词（subword）或字符级单元，其具体切分逻辑由底层模型的 tokenizer 决定；平台统一按实际 tokenized 后的长度计量，不依赖用户原始文本字数。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有模型调用（含文本、图像、语音、视频、决策等多模态）均以 `input_tokens` 和 `output_tokens` 分别计费。例如调用 `qwen4-max` 时，Prompt 经 tokenizer 处理后为 1280 个 token，生成响应为 320 个 token，则本次调用消耗 1600 Token（输入/输出单价可能不同）。
- **Token Plan 资源包抵扣**：购买的 Token Plan（基础版/个人版/团队版）额度以 Token 为单位扣减。系统按请求头中指定的 `x-acs-token-plan-id` 或专属 API Key（如 `sk-sp-xxx`）自动匹配并消耗对应包内额度，支持跨模型通用（除明确标注“不支持”的微调/私有模型）。
- **吞吐预留（TPM）容量换算**：1 kTPM = 1,000 Tokens/分钟，用于定义模型服务的稳定并发能力。输入/输出流量分别按 token 速率折算为 TPM，长上下文或缓存命中会应用阶梯系数（如 3×、0.125×）动态调整等效 TPM 占用。
- **监控与告警**：模型监控中的 `TotalToken 数` 指标按分钟聚合各模型实际消耗的 token 总量，可配置告警（如“单模型每分钟 Token 消耗环比增长 >50%”），用于异常用量识别与成本风控。
- **免费额度与预算管理**：新人免费额度（90天/100万 Token）、月度预算上限均以 Token 为计量基准；当额度耗尽且开启“用完即停”时，请求将直接返回 HTTP 403 错误，而非降级或限流。
- **Batch 与异步任务**：Batch 调用按输入+输出 token 总量计费（单价为实时调用的 50%）；异步任务（如生图、生视频）虽不直接暴露 token 数，但后台仍基于 prompt 长度、分辨率、时长等参数折算为等效 token 进行结算。

## 关键参数和配置

- **无显式传参**：Token 是平台后端自动计算的隐式指标，开发者无需在请求体中传递 `input_tokens` 或 `output_tokens`。
- **必需鉴权标识**（决定 token 归属与扣减路径）：
  - Token Plan 基础版：HTTP Header 中必须携带 `x-acs-token-plan-id: tp-xxxxxx` 和 `x-acs-trace-id: trace-xxxxxx`；
  - Token Plan 个人版/团队版：使用专属 API Key（`sk-sp-xxx`）+ 正确 `base_url`，平台自动关联订阅与用量；
  - 免费额度/节省计划：使用百炼通用 API Key（`sk-xxx`），系统按预设优先级（免费额度 → 节省计划 → 按量付费）自动抵扣。
- **影响 token 计数的关键请求参数**：
  - `max_tokens`：限制输出长度，直接影响 `output_tokens` 上限；
  - `temperature` / `top_p` 等采样参数：不改变 token 数，但影响实际生成长度；
  - 多模态输入（如图片 Base64、音频 data URL）：经模型专用 encoder 处理后转换为等效 token 序列，计入 `input_tokens`；
  - `tool_choice` 或内置工具调用：工具执行过程产生的中间 token（如搜索结果摘要、代码执行输出）全部计入总消耗。

## 面向开发者，简洁实用

- ✅ **务必校验实际 token 数**：使用 [tokenizer 工具](https://help.aliyun.com/zh/model-studio/token-calculator) 或 SDK 的 `count_tokens()` 方法预估开销，避免因 prompt 过长导致意外超支。
- ✅ **优先复用 Token Plan**：对稳定业务流量，购买 Token Plan 比按量付费低 30–50%；个人/团队版还附带 Harness 工具权益，进一步摊薄单次调用成本。
- ⚠️ **注意 token 计费边界**：流式响应中若启用 `stream_options.include_usage=true`，会触发额外一次用量上报，导致重复扣减——生产环境请禁用该参数。
- ⚠️ **地域强约束**：Token Plan 个人版与团队版仅支持华北2（北京），跨地域调用将失败；免费额度也仅在北京地域生效。
- 📊 **监控必看指标**：在「模型监控」中重点关注 `模型消耗 TotalToken 数`（按模型聚合）与 `审计日志` 中的 `input_token_count` / `output_token_count` 字段，精准归因费用来源。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan personal](../guides/token-plan-personal.md)
- [token plan team edition](../guides/token-plan-team-edition.md)
- [token plan best practice](../guides/token-plan-best-practice.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)


