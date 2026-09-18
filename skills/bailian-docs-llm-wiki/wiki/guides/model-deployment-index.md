# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐、低延迟的生产级专属服务到低成本效果验证的按量计费模式。所有部署均通过统一控制台或 API 管理，底层资源由平台全托管，开发者无需运维 GPU。部署前需完成模型调优或导入，并确保业务空间具备对应模型的调用权限。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、低延迟场景，支持长输入（最高 1M token）与前缀缓存折扣，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：提供物理隔离的 GPU 资源，支持基础模型、LoRA/全参微调模型及用户上传模型，支持 PD 分离计算模式以降低首 Token 延迟；DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token 按量部署**：仅支持 LoRA 微调模型，不使用不计费，适用于效果验证场景；不支持自助扩缩容，扩容需人工审核，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：动态匹配请求内容至备选模型集（至少 2 个），支持效果优先与成本优先策略，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从阿里云 OSS 导入 LoRA 模型（rank 必须为 8/16/32/64，VIT 必须冻结），不支持全参微调模型直接导入（白名单功能），详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持 PTU，但文档 3 的价格表明确限定 PTU 仅支持特定千问、DeepSeek、GLM 和千问VL系列模型（如 `qwen3.7-plus-2026-05-26`），且未列出任何全参微调模型。实际支持范围以控制台可选列表为准，建议部署前在[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)确认目标模型是否可用。

## 关键参数

| 参数 | 说明 | 取值约束 | 文档依据 |
|------|------|----------|----------|
| `plan` | 计费模式标识 | `ptu` / `mu` / `lora` / `auto`（智能路由） | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 吞吐额度 | `input_tpm` 和 `output_tpm` 必须为基准 TPM 的整数倍 | [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md) |
| `deploy_spec` / `model_unit_spec` | MU/DTU 规格 | 如 `MU1`, `MU2`, `MU9`；DTU 无此参数，由输入/输出 TPM 决定 | [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) |
| `enable_thinking` | 推理模式 | `true`（思考模式）或 `false`（非思考模式），影响 token 计费与性能 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `max_context_length` | 最长上下文 | 仅 MU 部署模式支持配置，值取决于模型能力（如 `qwen3.7-plus` 支持 1M） | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |

## 使用方式

1. **控制台部署**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy) → **模型推理 > 专属部署** → **部署新模型** → 选择服务名称、模型、计费方式（PTU/DTU/MU/Token/智能路由）及对应参数 → 确认创建。
2. **API 部署**：使用 DashScope HTTP API 或 SDK，按 `plan` 类型传入对应参数（如 `ptu_capacity` 或 `deploy_spec`），详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
3. **模型准备**：
   - 预置模型：直接从下拉列表选择；
   - 微调模型：需先在[模型调优](https://bailian.console.aliyun.com/cn-beijing/model/tuning)完成训练，再部署；
   - 自定义 LoRA 模型：需通过[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)流程从 OSS 导入。
4. **调用方式**：部署成功后，在控制台「部署列表」获取 `model_code`（如 `qwen3-8b-xxx` 或 `auto-model-abcd1234`），通过 DashScope、[OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 Assistant SDK 发起推理请求。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费模式，必须下线原服务并重新部署，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域限制**：API 部署默认仅支持华北2（北京），智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`），且必须使用 `maas.aliyuncs.com` 域名。
- **权限要求**：控制台部署需业务空间具备「模型部署-操作」权限；API 部署需 API Key 所属业务空间已开通目标模型的调用权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx`。
- **Token 按量部署限制**：一个月内不使用将自动释放；不支持自助扩缩容，扩容需人工审核；仅支持 LoRA 模型，全参微调模型不可用。
- **智能路由限制**：仅支持文本 Chat Completions，不支持图片/视频输入、Embedding/Rerank、Batch 接口；不支持 `temperature`、`top_p` 等采样参数，设置将导致报错。
- **OSS 导入约束**：Bucket 必须添加 `bailian-datahub-access=read` 标签；不支持访问根目录，必须指定子目录；模型文件必须包含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`，且 rank、词汇表、chat_template 须严格符合约束。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)


