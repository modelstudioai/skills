# model deployment index

百炼平台提供多种模型部署方式，支持从轻量级效果验证到高并发、低延迟生产环境的全场景需求。核心部署模式包括预置吞吐（PTU）、独占算力（DTU/MU）和 [Token](../concepts/token.md) 按量计费，分别面向性能确定性、资源隔离性与成本敏感型场景。所有部署均通过统一控制台或 API 管理，服务创建后即时计费，且计费方式不可变。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持千问、DeepSeek、GLM、千问VL 等主流文本与[多模态](../concepts/multi-modal.md)模型，覆盖输入上限至 1M token；支持长输入阶梯容量系数与前缀缓存折扣，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 面向新发布模型（按输入/输出 TPM 计费），MU 面向已有模型（按模型单元数量计费）。两者均支持基础模型、LoRA 微调模型及用户导入模型，并提供 PD 分离计算模式等高级配置 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调后的模型（如 `qwen3-8b-ft-*`），不使用不计费，适用于效果验证与低负载场景 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：动态匹配备选模型集（如 `qwen3.8-max`, `deepseek-v4-flash-0731`），仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与文本 Chat Completions 调用，不支持 DashScope 协议 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入 LoRA 模型（需满足 rank、词汇表、chat_template 等约束），不支持全参微调模型直接导入（白名单功能） [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 1 中称“部分预置模型与所有调优后模型”支持 PTU，但文档 2 明确列出 PTU 仅支持特定千问、DeepSeek、GLM 等型号（如 `qwen3.7-flash-2026-07-15`），且未提及所有调优模型；文档 6 和文档 1 均强调 [Token](../concepts/token.md) 按量部署**仅支持 LoRA 微调模型**，而文档 1 表格中“支持模型”列写为“部分经过 LoRA 调优后的模型”，二者一致，但文档 1 正文“支持模型”行存在歧义（“部分预置模型与所有调优后模型” vs 表格“部分经过 LoRA 调优后的模型”），应以表格及文档 6 的明确限定为准。

## 关键参数

| 参数 | 说明 | 取值约束 | 文档依据 |
|------|------|----------|----------|
| `plan` | 计费模式标识 | `ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 按量） | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 吞吐额度 | `{"input_tpm": N, "output_tpm": M}`，N/M 为整数倍基准值 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `deploy_spec` / `model_unit_spec` | MU 规格标识 | 如 `MU1`, `MU2 x 8`，不同模型对应不同规格 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)、[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) |
| `enable_thinking` | 推理模式开关 | `true`/`false`，影响思考 token 计费与模型行为 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)、[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) |
| `max_context_length` | 最长上下文 | 部分模型在 MU 模式下可配置，受模型能力限制 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `rpm_limit` / `tpm_limit` | 服务限流 | MU 模式下可设置，PTU/TOKEN 模式由平台预置 | [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |

## 使用方式

- **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 确认创建。部署状态变为「运行中」即成功 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **API 部署**：使用 `curl` 或 SDK 调用 `/api/v1/deployments` 接口，按 `plan` 参数指定模式并传入对应参数（如 `ptu_capacity` 或 `deploy_spec`）。部署成功后返回 `deployed_model`（即模型 code），用于后续推理调用 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **智能路由部署**：在专属部署页选择「智能路由」模式，配置路由策略（效果优先/COST_FIRST）、备选模型集（≥2 个）及路由版本，系统生成 `auto-model-xxxxxx` code [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **模型导入**：先完成 OSS 授权（添加 `bailian-datahub-access=read` 标签），再将合规 LoRA 文件（`adapter_model.safetensors`, `adapter_config.json`, `config.json`）上传至 OSS 子目录，最后在「我的模型」页提交导入 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

## 限制和注意事项

- **计费方式不可变更**：服务创建后无法切换计费模式，必须下线旧服务、新建新服务 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **扩缩容能力差异**：
  - PTU：支持自助增减吞吐量、配置自动伸缩策略；
  - MU：支持自助增减模型单元数量；
  - Token 按量：需在控制台提交扩容申请，等待人工审核 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：
  - 智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，不支持 DashScope 或 Anthropic 协议 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **模型兼容性约束**：
  - LoRA 导入要求严格：`rank` 必须为 8/16/32/64；词汇表与 `chat_template` 不可修改；视觉模型必须冻结 VIT [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **权限与配额**：
  - API 部署需确保 API Key 所属业务空间已开通目标模型部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
  - 智能路由备选模型需账号具备调用权限，且各模型 RPM/TPM 配额充足，否则可能因限流导致路由失败 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)


