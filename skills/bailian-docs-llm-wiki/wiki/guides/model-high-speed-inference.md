# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括 Prime 模式（轻量级提速）、吞吐预留（专属容量保障）、独占吞吐（DTU）与[智能路由](../concepts/model-routing.md)（动态选模）。这些能力均基于标准 API 协议，无需修改客户端代码即可接入，适用于 AI 编程助手、实时对话、Agent 多步推理等对输出速度敏感的生产场景。

## 支持的模型/功能

百炼提供四类高速推理能力，适用模型与能力边界各不相同：

- **Prime 模式**：为特定模型提供 1.5~2 倍 TPS 提升，无需额外参数，仅需使用专用 model ID（如 `glm-5.2-fast-preview`）。支持文本生成与视频生成模型，但视频模型（如 `wan3.0-video-prime`）按秒计费，且价格与分辨率强相关 [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。  
- **吞吐预留（TPM Reservation）**：为指定模型锁定专属推理容量，分**标准模式**（TPS 与普通 API 一致）和**高速模式**（TPS 提升 1.5~2 倍）。支持 Qwen3.8-Max、Qwen3.7-Plus、GLM-5.2、DeepSeek-v4-Pro 等主流模型，但部分模型（如 GLM-5.3）在高速模式下暂未开放支持 [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。  
- **独占吞吐（DTU）**：面向新发布模型的独占算力方案，按输入/输出 TPM × 时长计费，提供物理隔离与性能保障。支持 `qwen3.8-flash`、`glm-5.3-flash`、`deepseek-v4-flash-0731` 等模型，并明确标注各规格（Efficient/Fast）的基准 TPM 与首字延迟指标 [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。  
- **[智能路由](../concepts/model-routing.md)**：通过 `auto-model-xxxx` model code 动态匹配最优模型，支持效果优先与成本优先策略。备选集包含 `qwen3.8-flash`、`deepseek-v4-pro-0813`、`glm-5.2` 等，但**仅限文本输入**，且不支持 DashScope 原生协议 [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。  

> **注意**：文档 3 与文档 12 对 `GLM-5.3` 的高速模式支持存在矛盾——文档 3 的表格中 `GLM-5.3` 在“高速模式”列标记为 “×”，而文档 12 的 DTU 价格表中明确列出 `glm-5.3` 和 `glm-5.3-flash` 的 Fast 规格及对应 TPM 与价格。应以 DTU 价格表为准，即 `GLM-5.3` 已支持高速模式，但其高速能力仅通过 DTU 方案提供，不纳入吞吐预留的高速模式列表。

## 关键参数

不同方案的关键控制参数如下：

| 方案 | 核心参数 | 说明 |
|------|----------|------|
| **Prime 模式** | `model` | 必须设为专用 model ID（如 `glm-5.2-fast-preview`），无额外参数；接入域名需为 `https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1` |
| **吞吐预留** | `model`, `service_tier`（响应字段） | `model` 替换为专属 model code；响应中 `service_tier: "ptu_fast"` 表示命中高速预留容量；`provisioned_tokens` 字段返回**折算后**的消耗量（已含长输入阶梯与缓存折算）[长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md) |
| **DTU / MU** | `plan`, `deploy_spec`, `capacity` | API 部署时：`plan="mu"` 或 `"lora"`；`deploy_spec`（如 `"MU1"`）决定算力规格；`capacity` 控制副本数（DTU 下该参数无效）；部署后调用时 `model` 为生成的 deployed_model ID |
| **[智能路由](../concepts/model-routing.md)** | `model`, `routing_strategy`（创建时） | 调用时 `model` 设为 `auto-model-xxxx`；策略（`EFFECT_FIRST`/`COST_FIRST`）在控制台创建时选定，不可运行时修改 |

## 使用方式

所有方案均兼容 OpenAI Chat Completions 协议，调用流程统一为：**替换 model 参数 → 发起请求 → 解析响应**。

- **Prime 模式**：直接使用专用 model ID 调用，例如：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model": "glm-5.2-fast-preview", "messages": [{"role":"user","content":"你好"}]}'
  ```

- **吞吐预留**：将 `model` 替换为控制台生成的专属 code，例如 `tpu-glm52-20250901-xxxx`；务必检查响应中的 `service_tier` 字段确认是否命中预留 [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。

- **DTU / MU 部署**：先通过 API 或控制台部署服务，获取 `deployed_model` ID；后续推理请求中 `model` 即为此 ID，**非原始基础模型名**。

- **智能路由**：调用时 `model` 设为 `auto-model-abcd1234`，响应体中 `model` 字段返回实际执行的模型名（如 `qwen3.7-plus`），便于监控与计费归因。

## 限制和注意事项

- **计费差异**：Prime 模式与吞吐预留高速模式均按 token 计费，但吞吐预留容量内调用**不额外收取 token 费用**；DTU 为预付费 TPM × 时长；智能路由与 Token 按量部署则严格按实际 token 用量计费。
- **协议限制**：吞吐预留的 Responses 协议端点（`/v1/responses`）**不消耗预留容量**，必须使用 `/v1/chat/completions` 或 Anthropic 协议；智能路由**不支持 DashScope 原生协议**，仅限 `maas.aliyuncs.com` 域名下的 OpenAI 兼容与 Anthropic 接口。
- **模型约束**：Token 按量部署**仅支持 LoRA 微调模型**，且一个月不使用将自动释放；批量推理不返回 `reasoning_content` 字段，需实时 API 获取思考过程 [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)。
- **容量折算**：吞吐预留与 DTU 的实际容量消耗受长输入阶梯系数与缓存折算系数影响（如 `qwen3.7-flash` 输入 >32K 部分按 3x 放大），购买前务必使用 [TPM 容量计算器](https://help.aliyun.com/zh/model-studio/tpm-reservation-long-input#tpm-long-input-calc-h2) 并参考折算规则校准。
- **地域与模型绑定**：所有高速能力均按地域（如华北2、新加坡）独立配置，模型支持列表与价格因地域而异，调用时必须使用对应地域的 endpoint 与 model code。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


