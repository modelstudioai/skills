# model deployment index

百炼平台提供多种模型部署方式，支持从轻量级按量计费到高性能独占资源的全场景覆盖。本文档系统梳理部署能力矩阵，明确各模式适用边界、关键参数约束与操作路径，帮助开发者快速选型并落地生产服务。所有部署均通过统一控制台或 API 管理，计费方式一旦创建不可变更。

## 支持的模型/功能

- **预置吞吐（PTU）**：面向高并发、低延迟场景，支持千问3.x系列（如 `qwen3.8-max`、`qwen3.7-flash-2026-07-15`）、DeepSeek-v4系列（如 `deepseek-v4-flash`）、GLM-5.2 等主流文本模型，以及千问VL系列多模态模型；支持长输入（最高1M token）与前缀缓存，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费，两者均支持基础模型与自定义模型（含 LoRA/全参微调模型）。DTU 为新发布模型首选，MU 适用于已有模型；支持 PD 分离计算模式、自定义推理模式（Instruct/Thinking）及最长上下文配置，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调模型（如 `qwen3-8b-ft-202511132025-0260`），不使用不计费，适用于效果验证与低成本试用场景，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过 `auto-model-xxxxxx` 统一入口自动匹配最优模型，当前支持北京与新加坡地域，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，备选集包含 `qwen3.8-max`、`deepseek-v4-flash-0731` 等 8 款模型，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从阿里云 OSS 导入 LoRA 模型（如 `qwen3-32B`、`qwen2.5-vl-72b-instruct`），需满足 rank 取值（8/16/32/64）、词汇表一致、VIT 冻结等约束，详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 7 中称“支持导入全参微调模型（白名单）”，但文档 4 明确指出“当前版本仅支持导入 LoRA 模型，全参微调模型不可导入”。实际以文档 4 为准，全参模型导入需联系客户经理开通白名单。

## 关键参数

| 参数 | 说明 | 取值约束 | 文档依据 |
|------|------|----------|----------|
| `plan` | API 部署计费模式标识 | `ptu`（PTU）、`mu`（模型单元）、`lora`（[Token](../concepts/token.md) 按量） | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 吞吐额度 | `{"input_tpm": 10000, "output_tpm": 1000}`，单位为 TPM | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `deploy_spec` / `model_unit_spec` | MU 规格标识 | 如 `MU1`、`MU2 x 8`，不同模型对应不同规格 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `capacity` | MU 容量或 LoRA 部署占位符 | MU 模式下为副本数；LoRA 模式下必须填写但无效 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `enable_thinking` | 推理模式开关 | `true`/`false`，部分模型支持，影响 token 计费逻辑 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `max_context_length` | 最长上下文长度 | 仅 MU 模式支持设置，值需在模型能力范围内 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |

## 使用方式

- **控制台部署**：登录[百炼专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称 → 选择模型与计费方式 → 配置参数（如 PTU 容量、MU 规格、路由策略等）→ 确认。详细步骤见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **API 部署**：使用 DashScope HTTP API 或 CLI，按 `plan` 类型传入对应参数。PTU 需 `ptu_capacity`，MU 需 `deploy_spec` 和 `capacity`，LoRA 需 `plan: "lora"`。示例见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **模型导入**：先完成 OSS 授权（添加 `bailian-datahub-access=read` 标签），再在「我的模型」页面上传 LoRA 文件（`adapter_model.safetensors`、`adapter_config.json`、`config.json`），校验通过后即可部署，详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **智能路由调用**：将请求中 `model` 参数设为 `auto-model-xxxxxx`，使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)发送至 `maas.aliyuncs.com` 域名，响应头 `x-dashscope-resolved-model` 返回实际执行模型，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费模式，需下线旧服务并新建，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)**，不支持 DashScope 协议；[Token](../concepts/token.md) 按量部署仅支持 LoRA 模型，一个月不使用将自动释放。
- **权限与配额**：API 部署需确保业务空间已授权目标模型，且账号拥有模型部署权限；智能路由备选模型需账号具备调用权限，否则会被实时过滤；DTU 部署暂不支持 API 创建，仅限控制台操作。
- **模型兼容性**：LoRA 导入模型须满足 rank、词汇表、chat_template 等硬性约束，视觉模型必须冻结 VIT；PTU 长输入超过模型上限（如千问128K）时自动转为按量计费；智能路由不支持 `top_p`、`temperature` 等采样参数，设置将导致报错。
- **扩缩容差异**：PTU 与 DTU/MU 支持自助扩缩容；Token 按量部署需提交人工审核申请扩容；智能路由故障自动切换不重复计费，但 429 错误不触发切换。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)


