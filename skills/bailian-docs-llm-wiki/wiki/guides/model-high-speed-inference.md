# model high speed inference

百炼平台提供两种面向高吞吐与低延迟场景的推理加速能力：**吞吐预留（TPM 预留）** 和 **Prime 模式（高速模式）**。前者通过预付费锁定专属 TPM 容量，保障业务高峰期的容量刚性兑付；后者通过优化服务端调度与硬件资源分配，在标准按量计费基础上实现 1.5~2 倍 TPS 提升。二者可独立使用，也可组合（如在吞吐预留中启用 Prime 性能模式），适用于不同 SLA 要求与成本敏感度的生产场景。

## 支持的模型/功能

- **吞吐预留**：支持 Qwen、GLM、DeepSeek、Kimi 等主流模型的多个版本（如 `Qwen3.8-Max`、`GLM-5.3`、`DeepSeek-v4-Pro-0813`），覆盖华北2（北京）与新加坡地域。具体支持列表以控制台实时展示为准，部分新模型（如 `Qwen3.7-Flash-2026-07-15`）需联系商务经理开通。详情见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：当前支持 `qwen3.8-max-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等专用模型 ID，能力与对应基础模型一致，但输出速度显著提升。文本与视频生成模型均提供差异化定价。详情见 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
- > **注意**：文档 1 中将“高速模式”定义为吞吐预留的一种**性能模式选项**（与“标准模式”并列），而文档 2 中“Prime 模式”是独立于吞吐预留的、按 token 计费的加速通道。二者命名存在重叠但技术路径不同：前者是容量保障型加速（专属资源+TPM 锁定），后者是调度优化型加速（共享资源+TPS 提升）。实际使用时，`吞吐预留` 的“高速模式”即对应 PTU 专属部署能力，与 `Prime 模式` 不可混用同一 model ID —— 吞吐预留必须使用专属 model code，Prime 模式必须使用 `-prime` 或 `-fast-preview` 后缀的公开 model ID。

## 关键参数

| 参数 | 吞吐预留 | Prime 模式 |
|------|-----------|-------------|
| **核心指标** | 输入/输出 kTPM（千 tokens/分钟） | 实际 TPS（requests/second），标称提升 1.5~2× 标准 API |
| **性能档位** | 创建时选择：`标准模式`（等同标准 API）或 `高速模式`（即 PTU，TPS 提升 1.5~2×） | 固定高速，无显式档位配置 |
| **溢出策略** | 可选：`自动溢出至按量`（默认）或 `仅使用预留容量`（超限返回 429） | 无溢出概念；达限流阈值后，若平台有余量则仍可服务（实际可用 TPS ≥ 限流值） |
| **缓存折扣** | 支持（如 GLM-5.3 缓存命中按 25% 折算输入 TPM） | 支持（如 `glm-5.2-fast-preview` 缓存单价 4 元/百万 token） |
| **长输入阶梯系数** | 部分模型支持（如 `glm-5.1` 在 `[32K, 200K]` 区间输入系数 1.33） | 文档未提及阶梯系数，按基础模型规则继承 |

## 使用方式

- **吞吐预留**：创建成功后获取专属 `model code`（如 `tpm-qwen38max-cn-beijing-xxxxx`），**替换 API 请求中的 `model` 字段**即可生效。调用域名与标准 API 一致（`https://dashscope.aliyuncs.com/...`）。示例见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **Prime 模式**：直接使用专用 model ID（如 `glm-5.2-fast-preview`），**调用域名需切换为工作空间专属域名**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（地域需匹配）。无需额外 header 或参数。
- **组合使用**：若需同时满足“容量保障 + 高速输出”，应选择吞吐预留的 `高速模式`（即 PTU 方案），而非叠加 Prime 模式 —— 因 Prime 模式 model ID 无法用于吞吐预留实例。

## 限制和注意事项

- **预热要求**：吞吐预留实例在流量快速拉升时需短暂预热（数秒），期间可能出现延迟波动，建议客户端实现请求排队或指数退避重试机制。
- **计费周期**：吞吐预留“按天”计费按**自然日**结算（当日 00:00 到次日 00:00），非连续 24 小时；购买 1 天预留可能仅生效数小时，强烈建议开启“到期自动续费”。
- **专属 code 生命周期**：吞吐预留退订或到期 14 小时后，专属 model code 永久失效；而 Prime 模式 model ID 长期有效（只要模型未下线）。
- **模型能力一致性**：Prime 模式下模型能力、输入长度上限、思考字段（如 `reasoning_content`）等与对应基础模型完全一致，但返回结构中 `usage.completion_tokens_details.reasoning_tokens` 字段明确分离思考 token，便于精细化计费分析。
- > **注意**：文档 1 中提到 `GLM-5.2` 的 `thinking_budget` 参数在吞吐预留调用时不生效；而文档 2 的 Prime 模式示例返回中明确包含 `reasoning_tokens` 字段，表明其支持思考过程控制。开发者需确认：若业务强依赖 `thinking_budget`，应优先验证该参数在 Prime 模式下的实际行为，因其未在文档 2 中说明是否受限。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)


