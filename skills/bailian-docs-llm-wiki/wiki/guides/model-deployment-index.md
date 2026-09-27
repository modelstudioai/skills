# model deployment index

百炼平台提供多种模型部署方式，以满足不同业务场景对性能、成本、灵活性和资源隔离的需求。核心部署模式包括预置吞吐（PTU）、独占算力（DTU/MU）和 [Token](../concepts/token.md) 按量计费，分别面向高吞吐稳定服务、独占资源高性能推理和低成本效果验证等典型用例。所有部署均通过统一 API 接口调用，并支持 OpenAI 兼容协议。

## 支持的模型与功能

百炼支持三类主流部署模式，对应不同模型能力与适用范围：

- **预置吞吐（PTU）**：适用于千问（Qwen）、DeepSeek、GLM、千问VL 等系列模型，支持长输入（最高 1M token）与前缀缓存，具备阶梯容量系数与缓存折扣机制。具体支持模型及参数详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：支持基础模型与自定义模型（含 LoRA/全参微调模型），提供物理资源隔离与可定制性能指标。DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费；两者均支持 PD 分离计算模式。详细模型列表与规格见 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调模型（如 `qwen3-8b-ft-*`），按实际输入/输出 token 数计费，“不使用不计费”。该模式不支持自定义性能参数，吞吐与延迟由平台统一预置，适用于效果验证与低并发场景，详见 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。

> **注意**：文档 1 与文档 5 对“千问3-32B”的输入单价存在矛盾——文档 1（PTU 表）未列出该模型，而文档 5（[Token](../concepts/token.md) 表）明确标注其输入价为 ¥2（非思考模式）。此差异源于计费维度不同（TPM vs. Token），属正常设计，非错误。

智能路由作为高级调度能力，仅支持文本类 Chat Completions 请求，当前备选模型集包含 `qwen3.8-max`、`deepseek-v4-flash-0731` 等 8 款模型，且必须通过 `maas.aliyuncs.com` 域名调用。其模型选择逻辑依赖路由策略（效果优先/COST_FIRST）与实时权限过滤，详情见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 关键参数

各部署模式的核心配置参数如下：

| 参数类别 | PTU 模式 | DTU/MU 模式 | Token 按量 | 智能路由 |
|----------|-----------|--------------|-------------|------------|
| **核心计量单位** | 输入/输出 TPM（每分钟 Token 数） | DTU：输入/输出 TPM；MU：模型单元数 | 输入/输出 Token 数 | 实际路由模型的 Token 用量 |
| **必需配置** | `input_tpm`, `output_tpm` | DTU：`input_tpm`, `output_tpm`；MU：`deploy_spec`, `capacity` | 无（自动按调用计费） | `model`（固定为 `auto-model-xxxx`）、`messages` |
| **可选配置** | `overflow_strategy`（`auto_overflow` 或 `ptu_only`） | `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` | 无 | `enable_thinking`, `max_tokens`（自动转为 `max_completion_tokens`） |
| **缓存控制** | `cached_tokens` 字段返回命中量，影响额度折算 | 不直接暴露缓存参数，但底层支持上下文缓存 | 不支持显式缓存 | 仅隐式缓存（依赖实际路由模型能力），不保障命中率 |

所有部署均需指定 `model_name`（模型代码，如 `qwen3.7-plus-2026-05-26`）与 `name`（服务名称）。API 创建时，`plan` 字段标识计费方式：`ptu`、`mu`、`lora` 或 `router`。

## 使用方式

### 控制台部署
1. 登录百炼控制台 → **模型推理 > 专属部署** → **部署新模型**；
2. 选择部署模式（PTU/DTU/MU/Token/智能路由）；
3. 填写服务名称、模型、计费方式及对应参数（如 PTU 的 TPM 数、DTU 的基准倍数、智能路由的备选模型集）；
4. 确认创建，状态变为 **运行中** 后即可调用。

### API 部署
使用 DashScope SDK 或 HTTP API，示例如下：
```bash
# PTU 部署
curl "https://dashscope.aliyuncs.com/api/v1/deployments" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "my_ptu_service",
    "model_name": "qwen-flash-2025-07-28",
    "plan": "ptu",
    "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}
  }'
```
完整 API 参考见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

### 调用方式
- **DashScope 协议**：`model` 参数填部署生成的 `model_code`（如 `qwen3.7-plus-2026-05-26`）；
- **OpenAI 兼容协议**：`base_url` 必须为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（智能路由强制要求）或 `https://dashscope.aliyuncs.com/compatible-mode/v1`（其他模式）；
- **智能路由**：`model` 参数填 `auto-model-xxxxxxxx`，响应头 `x-dashscope-resolved-model` 返回实际执行模型。

## 限制和注意事项

- **计费方式不可变**：部署创建后无法切换计费模式，需下线后重新部署 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域限制**：Token 按量部署与部分 MU 模型仅支持华北2（北京），智能路由仅支持北京与新加坡地域。
- **模型导入约束**：从 OSS 导入 LoRA 模型需满足 rank（8/16/32/64）、词汇表一致、chat_template 未修改、VIT 冻结等硬性条件，详见 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **扩缩容差异**：
  - PTU/DTU 支持自助扩缩容（手动或自动伸缩）；
  - MU 预付费支持自助扩容，后付费需人工审核；
  - Token 按量部署扩容必须提交申请并等待人工审核。
- **故障处理**：智能路由的故障自动切换仅在目标模型完全不可用时触发，对 429、400 等确定性错误不重试，且不重复计费。
- **缓存行为**：PTU 的 `cached_tokens` 字段明确反映前缀缓存效果；智能路由因模型动态切换，缓存命中率不可控，且不参与计费。

## 来源文档

- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)


