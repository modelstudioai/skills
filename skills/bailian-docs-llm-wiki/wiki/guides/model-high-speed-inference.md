# model high speed inference

百炼平台提供多种面向高吞吐、低延迟场景的推理加速能力，核心包括吞吐预留（高速模式）、Prime 模式、独占吞吐（DTU）及智能路由等。这些方案通过专属算力、硬件优化或动态调度，在保障服务质量的同时提升推理性能，适用于大促、Agent 多步推理、实时对话等关键业务场景。

## 支持的模型/功能

- **吞吐预留·高速模式**：为指定模型锁定专属推理容量，TPS 相比标准 API 提升 1.5~2 倍，支持预付费/按天与后付费/按小时两种计费方式；当前支持 `qwen3.8-max`、`qwen3.7-plus-2026-05-26`、`deepseek-v4-flash-0731`、`deepseek-v4-pro` 等数十个模型（华北2与新加坡地域支持列表不同），详见[吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)。
- **Prime 模式**：无需专属容量，直接通过模型 ID（如 `glm-5.2-fast-preview`）调用，同样实现 1.5~2 倍 TPS 提升，按 token 计费，适用于对输出速度敏感但无需容量保障的场景；支持 `kimi-k3.1-pro-prime`、`glm-5.3-prime`、`wan3.0-video-prime` 等模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)。
- **独占吞吐（DTU）**：提供物理隔离的 GPU 资源，按输入/输出 TPM 额度×时长计费，支持自定义规格（Efficient/Fast 等）与性能基准（首字延迟、每 token 延迟），适用于需严格资源隔离与可预测性能的生产环境；支持 `qwen3.8-flash`、`glm-5.3`、`deepseek-v4-pro-0813` 等新发布模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)。
- **智能路由**：以 `auto-model-xxxxxx` 为 model code，根据请求内容动态匹配备选模型集中的最优模型（效果优先或成本优先），在不牺牲质量的前提下降低单位成本；当前支持 `qwen3.8-flash`、`deepseek-v4-flash-0731`、`glm-5.2` 等十余个文本模型 [原文标题](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)。
- **批量推理**：异步处理大批量非实时请求，成本约为实时推理的 50%，适用于模型评测、数据标注等离线任务；支持 `qwen4-max`、`qwen3.8-max`、`qwen3.7-plus` 等主流文本与[多模态](../concepts/multi-modal.md)模型，但不支持思考模式下的 `reasoning_content` 字段返回。

> **注意**：文档 2 与文档 10 对 `glm-5.2` 的高速模式命名存在不一致——文档 2 列出的是 `glm-5.2`（标准/高速模式均支持），而文档 10 明确其 Prime 模式模型 ID 为 `glm-5.2-fast-preview`。实际调用应以文档 10 的 `glm-5.2-fast-preview` 为准，该 ID 是 Prime 模式的唯一有效标识。

## 关键参数

- **`model`**：必需。必须替换为专属模型 code（如吞吐预留生成的 `tpu-xxx`、DTU 部署生成的 `deployed_model`、Prime 模式的 `glm-5.2-fast-preview` 或智能路由的 `auto-model-xxxxxx`）。普通模型 ID（如 `qwen3.8-max`）无法触发高速推理。
- **`service_tier`**：响应头字段，用于验证是否命中高速容量。值为 `ptu_fast` 表示消耗吞吐预留高速模式容量；`null` 或缺失表示未命中，走按量计费。
- **`provisioned_tokens`**：响应中 `usage` 下的字段，表示本次请求已折算（含长输入阶梯、缓存折算）的预留容量消耗量（单位：token），是判断容量使用效率的核心指标。
- **`cached_tokens`**：响应中 `usage.prompt_tokens_details.cached_tokens` 字段，表示输入中命中前缀缓存的 token 数，用于评估缓存收益。
- **`enable_thinking`**：部分模型（如 `qwen3.7-plus` 系列）默认开启思考模式，显式设为 `false` 可避免额外 `reasoning_tokens` 开销；该参数仅在实时 API 中生效，批量推理结果文件中不包含思考过程。

## 使用方式

1. **创建与配置**：
   - 吞吐预留：在控制台「模型推理 > 吞吐预留」创建，选择模型、高速模式、输入/输出 kTPM 容量（起步 200/20 kTPM），获取专属 model code [原文标题](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)。
   - DTU：在「模型推理 > 专属部署」选择 DTU 计费方式，按基准 TPM 规格购买整数倍容量。
   - Prime 模式：无需创建，直接使用对应模型的 `-fast-preview` 后缀 ID 调用。
   - 智能路由：在「模型推理 > 智能路由」新建服务，勾选至少 2 个备选模型，获取 `auto-model-xxxxxx` code。

2. **API 调用**：
   - 所有高速方案均使用 OpenAI Chat Completions 兼容协议（推荐）或 Anthropic 协议。
   - Endpoint 必须使用业务空间专属域名：`https://{workspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（`{region}` 为 `cn-beijing` 或 `ap-southeast-1`），**不可使用 `dashscope.aliyuncs.com`**。
   - 请求体中仅需将 `model` 替换为对应 code，其余参数（`messages`, `stream` 等）保持不变。
   - 示例（吞吐预留高速模式）：
     ```bash
     curl -X POST https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
       -H "Authorization: Bearer $API_KEY" \
       -d '{"model": "tpu-abc123", "messages": [{"role":"user","content":"你好"}]}'
     ```

3. **验证与监控**：
   - 检查响应中的 `service_tier` 字段是否为 `ptu_fast`（吞吐预留）或 `null`（未命中）。
   - 查看 `provisioned_tokens` 和 `cached_tokens` 评估实际消耗与缓存效果。
   - 在控制台「吞吐预留」页面的「概览」页签启用「以折算容量观测」，观察真实利用率趋势。

## 限制和注意事项

- **协议与域名限制**：吞吐预留、DTU、智能路由均**不支持 `dashscope.aliyuncs.com` 域名**，必须使用 `maas.aliyuncs.com` 专属域名；Responses 协议调用吞吐预留专属 code 时**不消耗预留容量，按量计费**，需改用 Chat Completions 或 Anthropic 协议。
- **模型与地域约束**：高速模式支持模型因地域而异（如 `GLM-5.3` 在华北2支持高速模式，在新加坡仅支持标准模式），且不支持所有模型（如 `Qwen4-Max` 当前无高速模式）。务必以控制台实时下拉菜单为准。
- **长输入与缓存折算**：容量消耗非原始 token 数，而是经「长输入阶梯系数」（如 `qwen3.7-flash` 输入超 32K 部分×3）与「缓存折算系数」（如 `glm-5.2` 命中部分×0.25）双重折算后的值，需用[TPM 容量计算器](https://help.aliyun.com/zh/model-studio/tpm-reservation-long-input#tpm-long-input-calc-h2)预估并持续监控「超额降级统计」。
- **溢出策略**：吞吐预留默认为「自动溢出」（超出部分转按量计费），若需强限流保障，应设为「仅使用预留容量」（返回 429 错误）。
- **Prime 模式特殊性**：虽提升 TPS，但**不提供容量保障**，仍受账号级 RPM/TPM 限流约束；其价格与标准 API 不同（如 `glm-5.2-fast-preview` 输入单价 ¥16/百万 token），需单独核算成本。

## 来源文档

- [吞吐预留](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index.md)
- [吞吐预留概述](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)
- [创建、接入与管理](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-create.md)
- [长输入与前缀缓存](../../raw/model-user-guide/model-high-speed-inference/tpm-reservation-index/tpm-reservation-long-input.md)
- [批量推理](../../raw/model-user-guide/model-high-speed-inference/batch-inference.md)
- [模型部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index.md)
- [模型导入](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-import.md)
- [专属部署概述](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)
- [部署模式](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes.md)
- [Prime 模式](../../raw/model-user-guide/model-high-speed-inference/prime-mode.md)
- [独占吞吐（DTU）](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-modes/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-high-speed-inference/model-routing.md)


