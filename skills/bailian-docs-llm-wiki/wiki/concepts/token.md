# Token

Token 是百炼平台中用于计量模型推理资源消耗的核心单位，表示模型在处理请求时实际消耗的语义级计算量。它统一涵盖输入（[prompt](../guides/prompt.md)）与输出（completion）两部分的文本/[多模态](multi-modal.md)语义单元，是配额管理、计费、限流与性能优化的基础度量标准。

## 在百炼平台的不同场景中，这个概念如何使用

- **Token Plan 配额管理**：Token 是 Token Plan 的计量基准。系统自动统计每次推理请求的 `prompt_tokens + completion_tokens` 总和，并从月度总配额中实时扣减；突发流量通过令牌桶算法（含 `burst_capacity`）平滑承载。
- **高速推理（High Speed Inference）**：TPM（Tokens Per Minute）预留机制以 Token 为单位预购吞吐能力，保障低延迟服务稳定性；`tpm_reservation` 值直接影响系统为该模型实例分配的最小并发处理能力。
- **API 调用与计费**：所有百炼托管模型（Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型）的在线推理调用均按实际消耗 Token 计费；输入中的图片/音频 base64 编码开销不计入，仅模型内部 consume 的语义 Token 生效。
- **模型评测**：评测任务执行期间，每条样本的推理请求同样消耗 Token，其总量计入当前账号的 Token Plan 配额（若已启用），影响评测并发规模与执行速度。
- **身份认证与 API 管理**：注意区分——`api_key`、`Bearer <token>` 中的 “token” 是身份凭证（OAuth-style access token），与本概念无关；后者属于安全认证范畴，不参与资源计量。

## 关键参数和配置

| 参数 | 所属模块 | 说明 | 典型值示例 |
|------|----------|------|------------|
| `prompt_tokens` / `completion_tokens` | 推理响应头 | 每次 API 调用返回的 `X-Embedding-Usage` 或 `X-Usage` 响应头中提供，用于精确追踪单次消耗 | `"prompt_tokens": 128, "completion_tokens": 64` |
| `total_tokens_per_month` | Token Plan | 月度总配额上限（输入+输出 Token 之和） | `10000000` |
| `rate_limit_per_second` | Token Plan | 每秒最大允许消耗 Token 数（硬限流阈值） | `5000` |
| `burst_capacity` | Token Plan | 短期突发容量（基于令牌桶算法），支持瞬时超限后平滑回落 | `10000` |
| `tpm_reservation` | 高速推理 | 预留的每分钟 Token 处理量，需提前购买并显式传入请求体 | `5000` |

> ⚠️ 注意：  
> - Token 统计不含 base64 编码膨胀、HTTP 协议开销或元数据字段长度；  
> - [多模态](multi-modal.md)输入中，图像/音频经模型编码器映射后的语义 Token 才被计入；  
> - 微调训练任务不消耗 Token Plan 配额；[OpenAI 兼容接口](openai-compatibility.md)调用非百炼托管模型亦不计入。

## 面向开发者，简洁实用

- ✅ **无需手动计算**：SDK 和 API 自动返回 `prompt_tokens` 与 `completion_tokens`，可直接用于监控与成本分析；
- ✅ **配额自动生效**：订阅 Token Plan 后，所有兼容模型的推理请求即自动受控，无需额外 header 或参数；
- ✅ **实时查询余量**：调用 `GET /v1/usage/token-plan`（需 `token_plan:read` 权限）获取当前剩余配额与重置时间；
- ✅ **限流有据可依**：收到 `429 Too Many Requests` 时，检查响应头 `X-RateLimit-Remaining` 和 `X-RateLimit-Reset`，结合 `rate_limit_per_second` 优化请求节奏；
- ❌ **避免常见误用**：不要将 `api_key` 或 `Bearer token` 与本概念混淆；不要对 base64 字符串长度做 Token 预估；不要在未启用 Token Plan 的账号下依赖配额保障。

如需进一步优化 Token 效率，建议：精简 [prompt](../guides/prompt.md) 模板、限制 `max_tokens`、启用 `stream=false`（尤其在 Prime 模式下）、优先选用 `qwen-turbo` 等高性价比模型。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


