# model high speed inference

百炼平台提供两种面向高吞吐、低延迟场景的推理加速能力：**Prime 模式**（轻量级高速输出）和**吞吐预留**（专属容量保障）。二者均通过模型标识符（`model` 参数）启用，无需修改请求结构或 SDK，但适用场景、计费逻辑与资源隔离级别存在本质差异。开发者应根据业务对确定性、成本敏感度与流量可预测性的要求选择合适方案。

## 支持的模型/功能

- **Prime 模式**：面向对输出速度敏感的通用场景（如 AI 编程助手、Agent 多步推理、实时对话），提供 1.5~2 倍于标准 API 的 TPS，**不隔离资源**，依赖平台剩余算力动态提升实际可用吞吐。支持模型包括 `glm-5.2-fast-preview`、`qwen3.8-max-prime`、`wan3.0-video-prime` 等，具体列表见 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。
  
- **吞吐预留**：为指定模型锁定专属 TPM（[Token](../concepts/token.md)s Per Minute）容量，实现刚性容量兑付，确保高峰期不受公共限流影响。支持模型范围更广，覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，含 `Qwen3.8-Max`、`GLM-5.2`、`DeepSeek-v4-Pro-0813` 等，完整清单以控制台为准，详见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：`glm-5.2-fast-preview` 在 Prime 模式文档中被列为独立模型 ID，而在吞吐预留文档中仅支持基础版 `GLM-5.2`（无 `-fast-preview` 后缀）。二者不可混用——调用 `glm-5.2-fast-preview` 不触发吞吐预留容量，调用 `GLM-5.2` 的专属 model code 也不启用 Prime 模式的加速逻辑。功能正交，需按目标能力严格匹配模型标识符。

## 关键参数

| 能力         | 核心参数                     | 说明                                                                 |
|--------------|------------------------------|----------------------------------------------------------------------|
| **Prime 模式** | `model`                      | 必须设为对应 Prime 模型 ID（如 `glm-5.2-fast-preview`），无额外参数。 |
|              | 接入域名                       | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（北京）或对应地域域名。 |
| **吞吐预留**   | `model`                      | 必须替换为控制台生成的**专属模型 code**（非原始模型名），否则不生效。     |
|              | `input_tpm` / `output_tpm`     | 预留容量单位为 kTPM（1 kTPM = 1000 tokens/分钟），需按业务负载预估。      |
|              | `overflow_strategy`            | 创建时指定：`auto_fallback`（默认，超容自动降级按量）或 `reject`（超容返回 429）。 |

## 使用方式

- **Prime 模式**：直接使用对应模型 ID 发起标准 OpenAI 兼容 API 请求。例如：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```
  流式响应中需分别处理 `delta.reasoning_content` 和 `delta.content` 字段（[详见 Prime 模式文档](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)）。

- **吞吐预留**：获取专属 model code 后，**仅替换 `model` 参数**，其余请求字段（`messages`、`stream`、`temperature` 等）与标准调用完全一致。示例：
  ```python
  client.chat.completions.create(
      model="tpm-reserved-abc123xyz",  # 替换为此 code
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```
  > **注意**：吞吐预留实例创建后需等待状态变为「运行中」方可调用；短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议客户端实现排队或重试机制（[参见吞吐预留文档](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。

## 限制和注意事项

- **资源隔离性**：Prime 模式共享公共资源池，虽有“特殊限流”机制，但**不保证容量独占**；吞吐预留则提供专属 TPM 容量，是唯一能规避公共限流的方案。
  
- **计费差异**：
  - Prime 模式：**纯按 token 计费**，与标准 API 一致，无预付费。
  - 吞吐预留：**预付费模式**，按天计费（自然日结算），预留容量内调用免费，超额部分按策略处理（降级按量或拒绝）。费用以控制台实时价格为准（[计费说明见吞吐预留文档](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)）。

- **模型能力一致性**：两种方案下，模型的基础能力（上下文长度、[多模态](../concepts/multi-modal.md)支持、工具调用等）与对应原版模型完全一致，但 Prime 模式可能引入特定字段（如 `reasoning_content`），而吞吐预留不改变模型输出结构。

- **地域与模型绑定**：所有 Prime 模型和吞吐预留实例均**绑定创建时选定的地域**（如华北2、新加坡），跨地域调用无效，且 model code 无法复用至其他地域。

- **缓存与长输入**：吞吐预留支持缓存折扣与长输入阶梯系数（如 `glm-5.2` 输入缓存折扣 0.25），而 Prime 模式未明确说明此类优化，实际效果以实测为准。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


