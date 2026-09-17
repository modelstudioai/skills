# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**Prime 模式（轻量级高速输出）** 和 **吞吐预留（专属容量保障）**。二者均通过模型标识符（`model` 参数）切换，无需修改 SDK 或协议，适用于 AI 编程助手、实时对话、Agent 多步推理等对响应速度和稳定性要求严苛的生产场景。核心差异在于：Prime 模式共享优化资源池，侧重单请求 TPS 提升；吞吐预留则锁定独占 TPM 容量，保障业务高峰期的确定性 SLA。

## 支持的模型与功能

- **Prime 模式**：面向输出速度敏感场景，提供 1.5~2 倍于标准 API 的 TPS，**不改变模型能力与限制**，仅提升推理调度与输出效率。支持模型包括 `glm-5.2-fast-preview`、`qwen3.8-max-prime`、`wan3.0-video-prime` 等（详见 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。  
- **吞吐预留**：为指定模型（如 `Qwen3.8-Max`、`GLM-5.2`、`DeepSeek-v4-Pro` 等）锁定专属输入/输出 TPM 容量，支持「标准模式」与「高速模式」两种性能档位。高速模式下同样可获得 1.5~2 倍 TPS 提升，且容量刚性兑付，不受公共限流影响（详见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。  
- > **注意**：文档 1 中称 `glm-5.2-fast-preview` 是 Prime 模式专用模型 ID；而文档 2 在「创建 吞吐预留」章节明确指出 `GLM-5.2` 可用于吞吐预留，并在「性能模式」中支持「高速模式」。二者并非互斥——`glm-5.2-fast-preview` 是 Prime 模式的预置轻量入口，而 `GLM-5.2` + 吞吐预留高速模式是资源独占的增强方案。实际选型应依据是否需要容量保障而非仅看模型名。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **核心标识** | 使用预置模型 ID（如 `glm-5.2-fast-preview`） | 使用控制台生成的专属 `model code`（非原始模型名） |
| **性能提升** | TPS 提升 1.5~2 倍（共享资源池） | TPS 提升 1.5~2 倍（仅「高速模式」档位），且容量独占 |
| **计费单位** | 按 token 计费（输入/输出/缓存命中） | 预付费按 kTPM·天（输入/输出分开计价），溢出部分按 token 计费（若启用自动溢出） |
| **限流行为** | 达限流值后，平台有余力时仍可服务（实际可用 TPS ≥ 限流值） | 预留容量内无限流；超出后按所选溢出策略处理（429 或自动降级） |
| **接入域名** | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/compatible-mode/v1`（或同区域兼容域名） |

## 使用方式

- **Prime 模式**：直接将 `model` 参数设为对应 Prime 模型 ID（如 `"glm-5.2-fast-preview"`），其余参数与标准 API 完全一致。流式响应中需分别处理 `delta.reasoning_content` 与 `delta.content` 字段（详见 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。  
- **吞吐预留**：  
  1. 在控制台创建实例，选择目标模型与「高速模式」；  
  2. 复制生成的专属 `model code`；  
  3. 将 API 请求中的 `model` 替换为该 code（**必须替换，不可复用原模型名**）；  
  4. 注意预热期：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议客户端实现排队或重试机制。  

## 限制和注意事项

- **模型能力一致性**：Prime 模式与吞吐预留均**不改变底层模型的能力、上下文长度、功能开关（如 `thinking_budget`）或使用限制**，仅优化推理执行层（详见两篇原文中多次强调的“模型支持的能力、使用限制与原版模型相同”）。  
- **地域与模型覆盖**：Prime 模式与吞吐预留支持的模型列表、价格及性能参数因地域（如华北2 vs 新加坡）而异，务必以百炼控制台实时展示为准。文档中表格仅为示例，可能滞后。  
- **吞吐预留有效期**：「按天」付费周期按**自然日**计算（从生效时刻至次日 00:00:00），非连续 24 小时。例如 16:00 购买，当日 00:00 即到期，有效时长约 8 小时。强烈建议开启「到期自动续费」避免服务中断（详见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。  
- **错误处理**：吞吐预留在「仅使用预留容量」策略下超限返回 `429 Too Many Requests`；Prime 模式超限行为由平台动态调度，不保证固定错误码。所有错误码解释请参考 [错误码](raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


