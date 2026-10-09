# model deployment index

百炼平台提供多种模型部署方式，以满足不同场景下的性能、成本与灵活性需求。本文档系统梳理了专属部署的核心能力，涵盖支持的模型类型、关键配置参数、标准使用流程，以及各部署模式的限制与注意事项，帮助开发者快速选型并落地生产服务。

## 支持的模型/功能

百炼支持三类主流部署模式：**PTU（预置吞吐）**、**DTU/MU（独占算力）** 和 **[Token](../concepts/token.md) 按量**，分别面向高并发低延迟、资源隔离强保障、低成本验证等典型场景。所有模式均支持平台预置模型及用户调优模型，但具体支持范围存在差异：

- **PTU 部署**：支持部分预置模型（如 `qwen3.8-max`、`deepseek-v4-flash`）及所有 LoRA 调优后模型，特别强化长输入（最高 1M token）与前缀缓存能力，详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **DTU/MU 部署**：DTU 面向新发布模型（按输入/输出 TPM 计费），MU 面向已有模型（按模型单元数量计费），两者均支持基础模型、LoRA 微调模型及用户从 OSS 导入的模型（需满足 rank、词汇表等约束），详见 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：**仅支持 LoRA 微调模型**，不支持全参微调或自定义框架模型，适用于效果验证阶段，详见 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。

> **注意**：文档 6 与文档 8 均描述“我的模型”导入流程，但文档 6 明确指出“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”，而文档 8 则称“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”。二者表述一致，确认全参微调模型导入为受限能力，非默认开放。

智能路由作为独立能力，支持文本 Chat Completions 场景，通过 `auto-model-xxxx` model-code 动态匹配备选集中的最优模型（如 `qwen3.8-max`、`deepseek-v4-flash-0731`），但**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用**，不支持 DashScope 或 Anthropic 协议，详见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 关键参数

各部署模式的关键配置参数如下，直接影响性能、成本与可用性：

| 参数类别 | PTU 模式 | DTU/MU 模式 | [Token](../concepts/token.md) 按量模式 |
|----------|----------|-------------|----------------|
| **核心计量单位** | 输入/输出 TPM（每分钟 Token 数） | DTU：输入/输出 TPM；MU：模型单元（MU）数量 | 输入/输出 Token 数 |
| **必填容量参数** | `input_tpm`, `output_tpm`（整数倍基准值） | DTU：`input_tpm`, `output_tpm`；MU：`deploy_spec`, `capacity`（副本数） | `capacity`（必须填写，但实际无效） |
| **性能相关参数** | 无用户可调并发/延迟，由平台预置 | MU 模式支持 `max_context_length`, `rpm_limit`, `tpm_limit`, `enable_thinking` | 无用户可调参数，吞吐/速度由平台预置 |
| **溢出策略** | 创建时选择：`自动溢出`（超量转按量）或 `仅使用 PTU 容量`（返回 429） | 无溢出概念，资源独占，流量受实际承载力限制 | 不适用（无预置容量） |

API 部署时，`plan` 字段是核心标识：`ptu`、`mu`、`lora` 分别对应三种模式，详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 使用方式

部署可通过控制台或 API 两种方式完成，推荐先在控制台验证再规模化调用：

1. **控制台部署**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，进入「模型推理 > 专属部署」，点击「部署新模型」，按向导填写服务名称、模型、计费方式及对应参数（如 PTU 的 TPM 值、MU 的规格与副本数），确认后等待状态变为「运行中」。
2. **API 部署**：使用 `curl` 或 SDK 调用 `/api/v1/deployments` 接口。例如 PTU 部署需传 `{"plan": "ptu", "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}}`；MU 部署需传 `{"plan": "mu", "deploy_spec": "MU1", "capacity": 4}`；Token 按量部署需传 `{"plan": "lora", "capacity": 1}`。完整示例见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
3. **调用已部署服务**：获取部署成功后的 `model_code`（如 `qwen3-8b-ft-xxx`），在推理请求中将其设为 `model` 参数值。注意：调用域名需与部署地域匹配（北京用 `cn-beijing.maas.aliyuncs.com`，新加坡用 `ap-southeast-1.maas.aliyuncs.com`），且智能路由**必须使用 `maas.aliyuncs.com` 域名**。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法更改计费模式，切换需先下线旧服务再重新部署新服务，详见 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **扩缩容能力差异**：
  - PTU 与 MU 支持自助扩缩容（增减 TPM 或副本数）；
  - Token 按量部署**不支持自助扩容**，需在控制台提交申请并等待人工审核。
- **模型权限与地域限制**：
  - 所有部署操作需确保业务空间已开通目标模型的调用权限，权限不足时会报错 `Workspace xxx does not have deployment privilege for model xxxx`；
  - 智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，DashScope 协议调用将失败。
- **OSS 导入约束**：从 OSS 导入 LoRA 模型时，必须满足 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 未修改、视觉模型 VIT 必须冻结等硬性要求，否则校验失败（错误码 `AvailableModelFileNotFound`），详见 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **费用起始时间**：无论是否发起推理请求，模型部署成功即开始计费，务必确认配置后再提交。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


