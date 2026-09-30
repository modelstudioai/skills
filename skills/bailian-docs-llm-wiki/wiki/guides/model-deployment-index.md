# model deployment index

百炼平台提供多种模型部署方式，支持从轻量级效果验证到高并发、低延迟生产环境的全场景需求。部署方式按计费与资源隔离维度分为预置吞吐（PTU）、独占算力（DTU/MU）和 Token 按量三类，均通过统一控制台或 API 管理，服务创建后即产生费用。所有部署均需先完成模型调优或导入，再选择适配的计费模式。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高吞吐、低延迟稳定负载场景，支持千问、DeepSeek、GLM、千问VL等系列模型，含长输入阶梯系数与前缀缓存折扣能力，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：提供物理资源隔离，DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费；支持基础模型、LoRA/全参微调模型及用户上传模型，支持 PD 分离计算模式，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token 按量**：仅支持 LoRA 微调模型，不使用不计费，适用于效果验证与低成本试用场景，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：动态匹配备选模型集，支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用，按实际路由模型计费，不额外收费，但仅限文本 Chat Completions 场景，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入 LoRA 模型（全参微调需白名单），需满足 rank、词汇表、chat_template 及 VIT 冻结等约束，详见[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)与[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 1 中称“部分经过 LoRA 调优后的模型”支持 Token 按量，而文档 6 明确限定为“仅支持 LoRA 微调模型”，且文档 8 强调“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”。因此，Token 按量部署**不支持全参微调模型**，该限制以文档 6 和文档 8 为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值约束 |
|----------|--------|------|-----------|
| **通用** | `model_name` | 模型标识符（如 `qwen3.7-plus-2026-05-26`） | 必填，需与控制台或 API 可选列表一致 |
| **PTU** | `input_tpm`, `output_tpm` | 预置吞吐额度（单位：TPM） | 必须为基准 TPM 的整数倍；溢出策略可选「自动溢出」或「仅使用 PTU 容量」 |
| **DTU/MU** | `input_tpm`, `output_tpm` (DTU) / `deploy_spec`, `capacity` (MU) | DTU 按 TPM 购买；MU 按模型单元规格（如 `MU1`）与副本数配置 | DTU：至少购买基准输入/输出各 1 倍；MU：`capacity` 表示副本数，总单元数 = `capacity` × 单副本单元数 |
| **通用部署** | `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` | 推理模式、上下文长度、RPM/TPM 限流 | 仅部分模型在 MU 模式下支持；`enable_thinking` 默认关闭，开启后按思考 token 计费 |
| **Token 按量** | `plan: "lora"` | 计费方式标识 | 必填；`capacity` 参数必须填写但无效，扩缩容需人工审核 |

## 使用方式

- **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 提交。权限不足时需参考[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)排查。
- **API 部署**：使用 `POST /api/v1/deployments` 接口，`plan` 字段指定计费方式（`ptu`/`mu`/`lora`），请求体携带对应参数（如 `ptu_capacity` 或 `deploy_spec`）。完整示例见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **调用方式**：部署成功后获取 `model_code`（如 `qwen3-8b-ft-xxxx`），通过 DashScope SDK、[OpenAI 兼容接口](../concepts/openai-compatibility.md)或 Assistant SDK 发起推理请求，`model` 参数填入该 code。
- **智能路由调用**：使用 `auto-model-xxxxxxxx` 作为 `model` 参数，仅支持 `maas.aliyuncs.com` 域名与 OpenAI Chat Completions 协议，响应头 `x-dashscope-resolved-model` 返回实际执行模型。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费方式，必须下线原服务并重新部署，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **模型兼容性限制**：
  - Token 按量仅支持 LoRA 微调模型，不支持全参微调（文档 6 与文档 8 一致）；
  - 智能路由仅支持文本输入、OpenAI 兼容协议，不支持图片/视频、Batch、Embedding/Rerank 等接口；
  - DTU 部署暂不支持 API 创建与管理，必须通过控制台操作（文档 3 明确说明）。
- **资源与生命周期**：
  - Token 按量部署若一个月内无调用将自动释放；
  - PTU 预付费订单提前终止，已使用部分按 1.2 倍系数退费；
  - MU/DTU 预付费同样适用 1.2 倍退费规则，且首月退订日单价按此系数计算（文档 1、3、6 均确认该规则）。
- **权限与授权**：从 OSS 导入模型需主账号或子账号完成服务关联角色授权，并为目标 Bucket 添加 `bailian-datahub-access=read` 标签，否则 Bucket 不可选（文档 4 与文档 8 一致强调此流程）。
- **缓存行为**：PTU 部署支持前缀缓存，`cached_tokens` 字段返回命中量；智能路由不保障缓存命中率，因请求可能路由至不同模型（文档 2 与文档 5 明确说明）。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


