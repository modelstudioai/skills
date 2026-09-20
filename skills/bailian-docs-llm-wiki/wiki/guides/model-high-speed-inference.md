# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**Prime 模式**（轻量级高速输出）和**吞吐预留**（专属容量保障）。二者均通过模型标识符（`model` 参数）启用，无需修改调用协议，但适用场景、资源隔离级别与计费模型存在本质差异。开发者应根据业务对确定性、成本敏感度与流量可预测性的要求进行选型。

## 支持的模型/功能

- **Prime 模式**：面向对输出速度敏感的通用场景，提供 1.5~2 倍于标准 API 的 TPS 提升，适用于 AI 编程助手、Agent 多步推理、实时对话等。支持模型包括 `glm-5.2-fast-preview`（文本）、`wan3.0-video-prime`（视频）等，[详见原始文档](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。  
- **吞吐预留**：为指定模型锁定专属推理容量（TPM），确保高峰期不受公共资源限流影响。支持 Qwen、GLM、DeepSeek、Kimi 等主流大模型系列，覆盖华北2（北京）与新加坡地域，[详见原始文档](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。  
> **注意**：`glm-5.2-fast-preview` 在 Prime 模式中是独立模型 ID，而在吞吐预留中仅支持 `GLM-5.2`（非 `-fast-preview` 后缀）。两者模型标识不互通，不可混用。

## 关键参数

| 能力         | 核心参数                     | 说明                                                                 |
|--------------|------------------------------|----------------------------------------------------------------------|
| Prime 模式   | `model`                      | 必须设为对应 fast 模型 ID（如 `glm-5.2-fast-preview`），无额外参数。 |
| 吞吐预留     | `model` + 性能模式           | `model` 为系统生成的专属 code；创建时需选择「标准模式」或「高速模式」（后者等效于 PTU 部署，TPS 提升 1.5~2 倍）[原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。 |
| 吞吐预留     | 输入 TPM / 输出 TPM（kTPM）  | 单位为千 tokens/分钟，决定容量上限；支持叠加扩容，专属 model code 不变。 |

## 使用方式

- **Prime 模式**：直接使用兼容 OpenAI 的 `/v1/chat/completions` 接口，`base_url` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，`model` 设为 fast 模型 ID 即可启用。流式响应中 `reasoning_content` 与 `content` 分离推送。  
- **吞吐预留**：创建成功后，在控制台获取专属 `model` code，并将其填入标准 API 请求的 `model` 字段（`base_url` 仍为标准域名，如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。注意：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议实现请求排队或重试机制。  

## 限制和注意事项

- **计费差异**：Prime 模式按 token 计费，与标准 API 完全一致；吞吐预留为预付费 kTPM，预留容量内调用不额外计费，溢出部分按量计费（若选择「自动溢出」策略）。  
- **模型能力一致性**：Prime 模式下模型能力、使用限制与原版模型相同，但 `glm-5.2` 的 `thinking_budget` 参数在吞吐预留调用中不生效。  
- **地域与可用性**：Prime 模式与吞吐预留均需在对应地域（如华北2、新加坡）的业务空间中配置；吞吐预留实例状态变化（如到期后 14 小时释放）将导致专属 model code 失效，请求自动回退至公共资源。  
- **性能模式混淆风险**：吞吐预留的「高速模式」虽提升 TPS，但其底层为 PTU 专属部署，与 Prime 模式的轻量加速机制不同。二者不可叠加使用，且模型 ID 体系完全独立。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


