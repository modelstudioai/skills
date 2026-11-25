# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（容量保障）、批量推理（异步降本）及专属部署（物理隔离）。所有方案均基于标准 API 协议兼容设计，开发者可按业务 SLA、成本敏感度与运维复杂度选择组合策略。

## 支持的模型/功能

- **Prime 模式**：专为输出速度敏感场景优化，TPS 提升 1.5~2 倍，适用于 AI 编程助手、Agent 多步推理、实时对话等。支持模型包括 `glm-5.3-prime`、`glm-5.2-fast-preview`、`wan3.0-video-prime` 等，详见 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属输入/输出 TPM 容量，确保高峰期不受公共限流影响。支持标准模式与高速模式双轨并行，覆盖 Qwen、GLM、DeepSeek、Kimi 等主流系列，具体支持列表以控制台为准 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)。
- **批量推理（Batch Inference）**：异步处理大批量请求，成本约为实时推理的 50%，适用于模型评测、数据标注等非实时场景。支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.6-flash`、`qwen-vl-ocr` 等数十种文本生成与多模态模型 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **专属部署（DTU/MU）**：提供物理隔离的独占算力，DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费，均支持微调模型部署与自定义性能指标 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

> **注意**：文档 14（吞吐预留概述）中称 `GLM-5.3` 在华北2（北京）**不支持高速模式**，但文档 1（Prime 模式）明确列出 `glm-5.3-prime` 为可用模型且提供高速计费单价（¥16/¥56 per million tokens）。该矛盾表明 `glm-5.3-prime` 是 GLM-5.3 的高速变体，其高速能力通过独立 model ID 实现，而非吞吐预留的“高速模式”开关。实际使用应以 `glm-5.3-prime` model ID 调用为准。

## 关键参数

| 参数 | 说明 | 取值示例 | 来源 |
|------|------|----------|------|
| `model` | 启用高速能力的核心标识符 | `"glm-5.2-fast-preview"`（Prime）、`"your-dedicated-model-code"`（吞吐预留）、`"auto-model-abcd1234"`（[智能路由](../concepts/model-routing.md)） | [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)、[创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md) |
| `service_tier` | 响应头字段，标识本次调用消耗的容量类型 | `"ptu_fast"`（命中高速预留）、`"ptu_default"`（命中标准预留）、`null`（未命中，按量计费） | [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) |
| `provisioned_tokens` | 响应中返回的实际消耗预留容量（已折算），单位为 token | `"usage.prompt_tokens_details.provisioned_tokens"`（输入侧） | [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) |
| `cached_tokens` | 输入中命中前缀缓存的 token 数，用于验证缓存收益 | `"usage.prompt_tokens_details.cached_tokens"` | [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) |

## 使用方式

1. **Prime 模式**：无需额外参数，仅需将 `model` 设为对应 Prime model ID（如 `glm-5.2-fast-preview`），调用标准 `/chat/completions` 接口即可。接入域名与标准 API 一致（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
2. **吞吐预留**：
   - 在控制台创建预留，获取专属 `model code`；
   - 将 API 请求中的 `model` 参数替换为该 code；
   - 验证是否命中：检查响应中 `service_tier` 字段是否为 `ptu_fast` 或 `ptu_default` [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
3. **批量推理**：
   - 构造符合规范的 JSONL 文件（每行一个 POST 请求对象，含 `custom_id`, `method`, `url`, `body`）；
   - 通过控制台或 OpenAPI 提交任务；
   - 任务完成后下载结果文件（成功响应）与错误文件（失败详情）。
4. **专属部署（DTU）**：通过 API 创建时指定 `"plan": "dtu"`，并在 `deploy_spec` 中声明规格（如 `"Fast"`），输入/输出 TPM 需为基准值的整数倍 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。

## 限制和注意事项

- **Prime 模式无额外限流**：当调用量达到账号级限流值时，若平台仍有剩余资源，Prime 请求仍可继续执行，因此**实际可用 TPS 不低于限流值**；但此特性不改变计费逻辑，仍按实际输入/输出 token 计费 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **吞吐预留容量按折算后消耗**：购买的 kTPM 并非直接对应原始 token 数。长输入超出阶梯边界部分会被放大（如 `(32K,256K]` 区间乘 3x），而缓存命中的 token 会按系数折扣（如 `0.25`）。务必使用 [TPM 容量计算器](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) 并结合折算规则估算，否则易因容量不足导致溢出 [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)。
- **批量推理不返回思考内容**：即使在 JSONL 中设置 `"enable_thinking": true`，结果文件中 `choices[0].message` 仅包含 `content` 和 `role` 字段，**不包含 `reasoning_content`**。如需完整思考过程，请改用实时 API 调用 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **模型部署计费方式不可变更**：服务创建后无法切换计费模式（如从 [Token](../concepts/token.md) 按量改为 DTU），必须下线原服务后重新部署 [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)


