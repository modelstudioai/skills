# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，覆盖实时流式响应（Prime 模式）、异步批量处理（Batch 推理）、资源独占部署（PTU/DTU/MU）、按量弹性调度（[Token](../concepts/token.md) 按量）及智能动态选模（智能路由）等路径。所有方案均基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，无需修改客户端核心逻辑即可接入。

## 支持的模型/功能

| 方案 | 核心能力 | 典型适用模型（北京） | 文档依据 |
|------|----------|----------------------|----------|
| **Prime 模式** | 输出 TPS 提升 1.5~2 倍，按 token 计费，不需额外参数，仅需指定专用 model ID（如 `glm-5.2-fast-preview`） | `glm-5.2-fast-preview`, `glm-5.3-prime`, `wan3.0-video-prime` | [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md) |
| **Batch 推理** | 异步批量处理，成本约为实时推理的 50%，支持 JSONL 输入、[多模态](../concepts/multi-modal.md)与向量模型 | `qwen3.8-max`, `qwen3.7-plus`, `qwen3-vl-plus`, `text-embedding-v3`, `qwen-vl-ocr` | [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) |
| **吞吐预留（TPM） / PTU** | 为指定模型锁定专属 TPM 容量，保障高峰期不受公共限流影响；支持「高速模式」获得 1.5~2 倍 TPS 提升 | `qwen3.8-max`, `glm-5.2`, `deepseek-v4-flash-0731`, `kimi-k2.6` | [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md) |
| **独占吞吐（DTU） / 模型单元（MU）** | 物理隔离 GPU 资源，支持自定义性能指标（首字延迟、每 token 延迟）、PD 分离计算模式 | `qwen3.7-plus-2026-05-26`, `glm-5.2`, `qwen3.5-35b-a3b`, `qwen3-rerank` | [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md) |
| **[Token](../concepts/token.md) 按量部署** | LoRA 微调模型专属计费方式，不使用不计费，适用于效果验证与低成本场景 | `qwen3-8b`, `qwen3-14b`, `qwen2.5-7b-instruct`, `qwen3-vl-8b-instruct`（仅 LoRA 微调后模型） | [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md) |
| **智能路由** | 动态分析请求内容，在备选模型集中自动匹配最优模型（效果优先 / 成本优先），返回 `x-dashscope-resolved-model` 标注实际执行模型 | `qwen3.8-flash`, `qwen3.7-plus`, `glm-5.2`, `deepseek-v4-pro-0813`, `kimi-k3`（需在控制台配置备选集） | [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md) |

> **注意**：文档中对 `qwen3.8-max` 的 Batch 支持描述存在矛盾——[批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md) 明确指出其“当前仅支持[多模态](../concepts/multi-modal.md)输入，暂不支持纯文本输入”，但[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)与[高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)均将其列为标准文本生成模型支持项。生产环境若需纯文本 Batch，请优先选用 `qwen3.7-plus` 或 `qwen3.6-plus` 等明确支持的型号。

## 关键参数

| 参数 | 作用 | 生效范围 | 注意事项 |
|------|------|----------|----------|
| `model` | 指定推理模型或服务标识 | 全局 | Prime 模式用 `glm-5.2-fast-preview`；吞吐预留用专属 `model-code`（如 `tpm-xxxxxx`）；智能路由固定为 `auto-model-xxxxxxxx`；Batch JSONL 中必须与 `url` 匹配（如 `/v1/chat/completions`） |
| `stream` | 控制是否启用流式响应 | Prime、实时 API | Prime 模式下流式响应会分别推送 `delta.reasoning_content` 和 `delta.content` 字段；Batch 不返回 `reasoning_content` 即使 `enable_thinking=true` |
| `enable_thinking` | 开启深度思考模式 | 多数 Qwen/GLM/DeepSeek 模型 | Batch 场景下该参数须置于 JSONL `body` 顶层（与 `model` 同级），不可嵌套于 `extra_body`；智能路由下设为 `true` 将自动排除 non-thinking 模型 |
| `thinking_budget` | 限制思考 token 长度 | 部分模型（如 Qwen3 系列） | 在[吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)中明确说明：GLM-5.2 的此参数调用时不生效 |
| `max_tokens` / `max_completion_tokens` | 控制输出长度上限 | 全局 | 智能路由下 `max_tokens` 会被自动转换为 `max_completion_tokens`，且仅路由至支持该参数的备选模型 |
| `response_format`、`enable_search`、`reasoning_effort` | 控制结构化输出、搜索增强、思考强度 | 智能路由限定 | 智能路由**不支持** `top_p`, `temperature`, `n`, `logprobs`, `stop`, `tool_choice` 等采样与工具参数，设置将导致报错 |

## 使用方式

### 1. Prime 模式（最快响应）
- **接入方式**：替换 `model` 为 Prime 专用 ID（如 `glm-5.2-fast-preview`），使用标准 `compatible-mode/v1` 域名
- **示例**：
  ```bash
  curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $API_KEY" \
    -d '{"model":"glm-5.2-fast-preview","messages":[{"role":"user","content":"你是谁"}]}'
  ```

### 2. Batch 推理（最高性价比）
- **流程**：构造 UTF-8 编码 JSONL 文件 → 调用 `/v1/batches` 创建任务 → 查询状态 → 下载结果文件
- **关键约束**：单文件 ≤ 50,000 请求 & ≤ 500 MB；每行 JSON ≤ 1 MB；`custom_id` 必填且唯一；媒体 URL 必须公网可访问

### 3. 吞吐预留 / PTU（确定性容量）
- **步骤**：控制台创建预留 → 获取专属 `model-code` → 替换 API 中 `model` 参数 → 发起请求
- **注意**：创建即计费，与实际调用量无关；建议使用右侧「TPM 容量计算器」预估输入/输出 TPM

### 4. DTU / MU 部署（物理隔离）
- **API 示例（DTU）**：
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
    -H "Authorization: Bearer $API_KEY" \
    -d '{
      "name": "my-dtu-service",
      "model_name": "qwen3.7-plus-2026-05-26",
      "plan": "dtu",
      "dtu_capacity": {"input_tpm": 2000000, "output_tpm": 250000}
    }'
  ```
- **MU 部署需指定 `deploy_spec`（如 `MU1`）与 `capacity`（副本数）**

### 5. 智能路由（零改造选模）
- **调用方式**：仅需将 `model` 替换为 `auto-model-xxxxxxxx`，其余参数与普通模型完全一致
- **验证路由**：检查响应头 `x-dashscope-resolved-model`，确认实际执行模型

## 限制和注意事项

- **地域限制**：Prime 模式、吞吐预留、智能路由均支持华北2（北京）与新加坡；Batch 推理部分模型在新加坡支持有限（如 `qwen-max` 仅支持[多模态](../concepts/multi-modal.md)输入）；DTU/MU 部署文档未明确标注地域，但控制台操作默认绑定工作空间地域。
- **模型兼容性**：
  - Batch 推理结果**不包含 `reasoning_content` 字段**，即使请求中设置了 `enable_thinking=true`；如需思考过程，请改用实时 API [深度思考](../../raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)。
  - 智能路由**不支持缓存显式控制**，`x-dashscope-cache-hit` 等缓存相关 header 可能被忽略；缓存命中率取决于实际路由到的模型及其提示词前缀重复度。
- **计费陷阱**：
  - 吞吐预留、PTU、DTU、MU 均为「创建即计费」，无论是否发起调用；[Token](../concepts/token.md) 按量部署则严格「不使用不计费」。
  - PTU/DTU 的长输入阶梯系数与缓存折扣规则因模型而异（如 `qwen3.7-flash-2026-07-15` 输入超 32K 后系数升至 3x），需结合[长输入与前缀缓存](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)文档精确估算。
- **扩缩容限制**：
  - Token 按量部署**不支持自助扩缩容**，需提交工单申请；
  - 智能路由的「8 小时时段预留」实例**不支持续费与扩容**，到期自动失效；
  - 所有部署方案的计费方式创建后均**不可变更**，切换需先下线再重建。

## 来源文档

- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)
- [高速容量（PTU）](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)


