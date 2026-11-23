# 智能路由与加速

智能路由与加速是百炼平台面向生产级 AI 服务提供的统一性能优化范式，通过动态策略调度（智能路由）与底层资源保障（加速能力）双轨协同，在不修改业务代码的前提下，自动实现效果、延迟、成本三者的最优平衡。

## 在百炼平台的不同场景中，这个概念如何使用

智能路由与加速并非单一功能，而是贯穿模型调用全链路的横切能力集合，按使用方式分为两类：

- **智能路由（Model Routing）**：作为“决策层”，在请求入口处基于内容特征（如输入长度、语义复杂度、领域关键词）和预设策略（`EFFECT_FIRST` 或 `COST_FIRST`），从一组已配置的候选模型（如 `qwen3.8-flash`、`glm-5.2`、`deepseek-v4-pro-0813`）中实时选择最优模型执行推理。它完全透明——开发者仅需调用一个 `auto-model-xxxxxxxx` 模型 ID，无需感知后端模型切换逻辑。当前仅支持文本输入，且仅在华北2（北京）与新加坡地域可用，强制后付费。

- **加速能力（Acceleration Paths）**：作为“执行层”，提供三种正交的性能强化路径，均通过替换 `model` 参数启用，无需变更 API 协议或 SDK：
  - **Prime 模式**：轻量级提速，适用于对首字延迟敏感的实时对话场景。使用专用 model ID（如 `glm-5.3-prime`），TPS 提升 1.5–2 倍，能力与原模型完全一致，按 token 计费。
  - **吞吐预留（TPM Reservation）**：容量保障型加速，适用于高并发、低抖动要求的 Agent 多步推理或批量评测。需预购 kTPM 额度，创建专属 `tpu-xxxxx` model code，高速模式同样提供 1.5–2 倍 TPS。
  - **独占吞吐（DTU）**：物理隔离型加速，适用于 SLA 要求严苛的核心业务（如金融客服）。部署后获得 `qwen3-8b-ft-xxx` 类 deployed_model code，性能指标（首字延迟、每 token 延迟）明确可承诺。

三者可组合使用：例如，智能路由可将请求分发至多个已开启吞吐预留的 Prime 模型实例，实现策略驱动 + 容量保障的双重优化。

## 关键参数和配置

- **核心调用参数**：
  - `model`: 必填。决定所用路径：
    - 智能路由：固定为 `auto-model-xxxxxxxx`（由控制台创建生成）；
    - Prime：如 `glm-5.2-fast-preview`；
    - 吞吐预留：如 `tpu-xxxxx`；
    - DTU：如 `qwen3-8b-ft-xxx`。
  - `routing_config`（仅智能路由创建时需配置）：JSON 对象，必须包含：
    - `strategy`: `"EFFECT_FIRST"`（优先选效果最优）或 `"COST_FIRST"`（优先选单价最低）；
    - `candidate_models`: 字符串数组，列出至少 2 个同模态、同地域的备选模型 ID（如 `["qwen3.8-flash", "glm-5.2"]`）；
    - `route_model_version`: 路由引擎版本号（如 `"model-router-20260908"`），由平台维护，创建时自动填充。

- **关键响应字段（用于可观测性）**：
  - `service_tier`: 字符串。标识本次请求实际使用的资源层级：`ptu_fast`（命中高速预留）、`ptu_default`（命中标准预留）、`null`（走按量计费）。
  - `provisioned_tokens`: 整数。本次请求**实际消耗的折算后预留容量（token）**，已应用长输入阶梯系数与前缀缓存折扣，是判断容量是否充足的唯一准确依据。
  - `cached_tokens`: 整数。本次请求中命中前缀缓存的输入 token 数，用于评估缓存收益。

> ⚠️ 注意：所有加速路径（含智能路由）均**必须使用 `compatible-mode/v1` 或 `/apps/anthropic/v1/messages` 等兼容协议路径**；若误用 `/v1/responses` 协议，将绕过预留容量，按量计费。

## 面向开发者，简洁实用

- ✅ **快速上手**：  
  想提速？直接换 `model`：  
  - 要简单快 → 用 `glm-5.3-prime`；  
  - 要稳又快 → 在控制台买吞吐预留，用 `tpu-xxxxx`；  
  - 要绝对可控 → 部署 DTU，用 `deployed_model` code；  
  - 要自动择优 → 创建智能路由，用 `auto-model-xxxxxxxx`。

- ✅ **调试验证**：  
  查看响应头或 JSON body 中的 `service_tier` 和 `provisioned_tokens`：  
  - 若 `service_tier` 为 `ptu_fast` 且 `provisioned_tokens > 0`，说明成功命中高速预留；  
  - 若 `service_tier` 为 `null` 但 `provisioned_tokens` 为 0，则走按量计费，需检查 model code 是否正确、协议路径是否合规。

- ✅ **避坑指南**：  
  - 智能路由不支持图像、语音等多模态输入，仅限纯文本；  
  - 所有加速路径均不改变模型能力边界（如 function calling、tool choice 行为），仅影响性能与计费；  
  - DTU 和吞吐预留必须使用业务空间专属域名（如 `ws-xxx.cn-beijing.maas.aliyuncs.com`），不可用 `dashscope.aliyuncs.com`；  
  - 智能路由强制后付费，不支持预付费模式。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model production](../api/model-production.md)
- [model experience](../guides/model-experience.md)
- [capabilities](../guides/capabilities.md)
- [more about models](../api/more-about-models.md)
- [test 1](../guides/test-1.md)


