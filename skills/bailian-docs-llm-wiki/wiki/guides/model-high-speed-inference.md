# model high speed inference

百炼平台提供两种面向高吞吐、低延迟推理场景的加速能力：**Prime 模式**（轻量级性能增强）和**吞吐预留**（专属容量保障）。二者均通过模型标识符（`model` 参数）启用，无需修改 API 协议或 endpoint，但适用场景、资源隔离级别与计费模型存在本质差异。开发者应根据业务对稳定性、确定性及成本敏感度的要求进行选型。

## 支持的模型/功能

- **Prime 模式**：面向通用高速输出场景，提供 1.5~2 倍于标准 API 的 TPS，适用于 AI 编程助手、Agent 多步推理、实时对话等对首 token 延迟和输出流速敏感的用例。其本质是共享资源池内的调度优化，**不提供容量独占保障**。支持模型包括 `glm-5.2-fast-preview`、`qwen3.8-max-prime`、`wan3.0-video-prime` 等，具体列表见 [Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

- **吞吐预留**：为指定模型锁定专属推理容量（以 kTPM 为单位），确保业务高峰期不受公共限流影响。支持「标准模式」（TPS 与标准 API 一致）和「高速模式」（TPS 提升 1.5~2 倍，即 PTU 部署形态），后者在功能上与 Prime 模式性能对标但具备刚性容量保障。支持模型范围更广，覆盖 Qwen、GLM、DeepSeek、Kimi 等系列主力模型，详见 [吞吐预留 (raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。

> **注意**：文档 1 中称 `glm-5.2-fast-preview` 是 Prime 模式专用模型 ID；而文档 2 在“性能模式”选项中明确指出「高速模式」对应 PTU 部署，且支持 `GLM-5.2`（非 `-fast-preview` 后缀）。这表明 `glm-5.2-fast-preview` 仅用于 Prime 模式调用，而 `GLM-5.2`（配合吞吐预留专属 model code）可用于同等性能的专属高速模式。二者路径不同，不可混用。

## 关键参数

| 参数 | Prime 模式 | 吞吐预留 |
|------|------------|-----------|
| **启用方式** | 直接使用预定义 model ID（如 `glm-5.2-fast-preview`） | 使用系统生成的专属 model code（如 `tpm-xxx`） |
| **性能档位** | 固定高速（1.5~2× TPS） | 可选：标准模式 / 高速模式（PTU） |
| **容量保障** | 无专属容量，依赖平台剩余资源；实际可用 TPS 不低于限流值 | 专属 kTPM 容量刚性兑付，溢出策略可配（自动降级 or 429） |
| **计费单位** | 按 token 计费（输入/输出/缓存命中） | 预付费按天购买 kTPM（输入/输出分离），预留内调用不额外计费；溢出部分按 token 计费 |
| **缓存折扣** | 支持（如 `glm-5.2-fast-preview` 输出单价含缓存命中优惠） | 支持，且不同模型缓存折扣率不同（如 `glm-5.2` 为 25%） |

## 使用方式

- **Prime 模式**：  
  仅需将请求中的 `model` 字段设为对应 Prime 模型 ID，并使用兼容模式 endpoint：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`。无需额外 header 或 query 参数。[示例代码见 Prime 模式 (raw/model-user-guide/model-high-speed-inference/fast-mode.md)](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)。

- **吞吐预留**：  
  1. 在控制台创建预留实例，选择模型、性能模式（标准/高速）、输入/输出 kTPM 及溢出策略；  
  2. 获取生成的专属 `model` code（如 `tpm-abc123`）；  
  3. 将 API 请求中的 `model` 替换为该 code，endpoint 保持标准兼容模式地址（如 `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`）；  
  4. **注意预热**：短时间内请求量快速拉升时，系统需短暂预热，期间可能出现延迟波动，建议客户端实现排队或重试机制。

## 限制和注意事项

- **模型能力一致性**：Prime 模式与吞吐预留所绑定的基础模型，在功能、上下文长度、输出格式（如 `reasoning_content` 字段）、错误码语义等方面，均与原版模型完全一致，详见两篇原始文档的“模型支持的能力、使用限制与原版模型相同”说明。
  
- **地域与模型可用性**：模型支持列表、价格、TPM 步长等均因地域（如华北2、新加坡）而异，且可能动态调整。**务必以百炼控制台实时展示为准**，文档中表格仅为参考快照。

- **计费周期差异**：吞吐预留的「按天」计费按**自然日**结算（从生效时刻至次日 00:00:00），非连续 24 小时。例如 16:00 购买 1 天预留，实际有效期约 8 小时。强烈建议开启「到期自动续费」避免服务中断。

- **专属 model code 生效前提**：吞吐预留实例状态必须为「运行中」，专属 model code 才有效；实例到期后 2 小时内仍可调用，但 14 小时后彻底释放且 code 失效。

- **缩容与退订**：吞吐预留支持归零扩缩容（输入/输出 TPM 设为 0），code 保留但不再产生费用；退订后 code 立即失效，请求回退至公共资源处理。退费按 `max(0, 降量部分预付费 − 降量部分预付费 × 已用时长/购买时长 × 1.2)` 公式计算。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/fast-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


