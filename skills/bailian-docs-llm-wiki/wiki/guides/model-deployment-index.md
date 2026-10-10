# model deployment index

百炼平台提供多种模型部署方式，以满足不同场景下的性能、成本与灵活性需求。本文档系统梳理了预置吞吐（PTU）、独占算力（DTU/MU）、[Token](../concepts/token.md)按量及智能路由四类核心部署模式，涵盖支持能力、关键参数、使用方式及约束限制，为开发者提供统一、准确的选型与实施参考。

## 支持的模型/功能

百炼当前支持四类主流部署模式，覆盖基础模型、微调模型及自定义模型：

- **预置吞吐（PTU）**：面向高吞吐、低延迟生产环境，支持千问（Qwen）、DeepSeek、GLM、千问VL等系列模型，具备长输入阶梯容量系数与前缀缓存折扣能力，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：提供物理资源隔离，DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费；支持全参与 LoRA 微调模型，以及部分视觉语言模型（如千问VL系列），详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调模型，按实际 [Token](../concepts/token.md) 输入/输出用量计费，适用于效果验证与低成本轻量场景，不支持自助扩缩容，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：动态匹配请求内容至最优备选模型，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与文本 Chat Completions 调用，当前版本 `model-router-2026-0908` 支持 `qwen3.8-max`、`deepseek-v4-flash-0731`、`glm-5.2` 等 9 款模型，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

> **注意**：文档 1 中列出的 `qwen3.7-flash-2026-07-15` 在“新加坡”区域价格表中标注“联系商务经理开通”，而文档 2 的部署概述中未提及该模型的开通限制；实际部署前请以控制台实时可选模型为准，避免依赖文档静态描述。

## 关键参数

各部署模式的关键配置参数如下：

| 部署类型 | 必填参数 | 说明 |
|----------|----------|------|
| **PTU** | `plan: "ptu"` + `ptu_capacity: {input_tpm, output_tpm}` | `input_tpm`/`output_tpm` 单位为 KTPM，需结合预置吞吐额度计算器评估长输入与缓存命中率后设定，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。 |
| **DTU** | `plan: "dtu"` + `input_tpm`, `output_tpm`（整数倍基准值） | 基准 TPM 因模型而异（如 `qwen3.7-plus-2026-05-26` 基准输入为 1,372,000 TPM），购买值必须为基准的整数倍。 |
| **MU** | `plan: "mu"` + `deploy_spec`（如 `"MU1"`）+ `capacity` | `capacity` 表示副本数，总算力 = `capacity × deploy_spec`；部分模型支持 `enable_thinking`、`max_context_length` 等推理参数。 |
| **Token 按量** | `plan: "lora"` + `capacity`（必填但无效） | `capacity` 字段必须提供（如设为 `1`），实际扩容需人工审核，不支持 API 自助调整。 |
| **智能路由** | `model: "auto-model-xxxxxxx"`（固定前缀） | 无显式容量参数；路由策略（`EFFECT_FIRST`/`COST_FIRST`）与备选模型集在控制台创建时配置，API 调用无需变更。 |

## 使用方式

- **控制台部署**：登录[百炼专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 指定部署模式 → 填写参数 → 确认。PTU、DTU、智能路由均支持控制台全流程操作；Token 按量部署仅支持 LoRA 模型，且扩容需提交工单。
- **API 部署**：通过 `POST /api/v1/deployments` 接口创建，需在请求体中明确 `plan` 字段（`"ptu"`/`"mu"`/`"lora"`）。DTU 部署暂不支持 API 创建，详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **模型来源**：除平台预置模型外，LoRA 微调模型可通过[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)导入 OSS 后部署；全参微调模型需联系客户经理白名单开通。
- **调用方式**：所有部署服务均通过 `model_code`（如 `qwen3.8-max-abc123` 或 `auto-model-abcd1234`）调用；智能路由仅支持 `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，不支持 DashScope 协议。

## 限制和注意事项

- **计费不可变**：部署创建后计费方式不可更改，切换需先下线旧服务再新建，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：
  - 智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，不支持 DashScope 或 Anthropic 协议；
  - PTU 部署的 API 响应中 `cached_tokens` 字段在 Anthropic 兼容格式下暂不返回，需通过 `provisioned_tokens` 间接判断缓存效果。
- **模型兼容性**：
  - Token 按量部署**仅支持 LoRA 模型**，不支持基础模型或全参微调模型；
  - 导入 LoRA 模型须满足严格约束：`rank` 仅限 8/16/32/64；词汇表与 `chat_template` 必须与基座模型完全一致；视觉模型必须冻结 VIT（禁止 `visual.*` 参数），详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **扩缩容差异**：
  - PTU 与 DTU 支持自助扩缩容（含自动伸缩策略）；
  - MU 支持自助增减副本数；
  - Token 按量部署扩容需人工审核，不支持 API 调整；
  - 智能路由不提供容量参数，其吞吐能力由备选模型的实际限流（RPM/TPM）决定。
- **缓存行为**：PTU 的前缀缓存折扣与长输入阶梯系数直接影响额度消耗，但智能路由因请求可能被分发至不同模型，**不保障缓存命中率**，仅依赖各备选模型自身的隐式缓存机制。

## 来源文档

- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


