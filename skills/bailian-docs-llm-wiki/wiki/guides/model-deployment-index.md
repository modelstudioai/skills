# model deployment index

百炼平台提供多种模型部署方式，以满足不同场景下的性能、成本与灵活性需求。本文档系统梳理专属部署的核心能力，涵盖支持的模型类型、关键配置参数、标准化使用流程，以及各方案的适用边界与约束条件，帮助开发者快速选型并落地生产服务。

## 支持的模型/功能

百炼支持三类主流部署模式：**PTU（预置吞吐）**、**DTU/MU（独占算力）** 和 **Token 按量**，每种模式支持的模型范围不同：

- **PTU 部署**：主要面向千问（Qwen）、DeepSeek、GLM、千问VL 等预置大模型，支持长输入（最高 1M token）与前缀缓存优化，适用于高并发、低延迟的稳定流量场景 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **DTU/MU 部署**：覆盖更广的模型谱系，包括千问全系列（3.8-Max、3.7-Plus、3.5-397B-A17B 等）、GLM-5.x、DeepSeek-v4、千问VL 多模态模型及 Omni、CosyVoice 语音模型；同时支持 LoRA 微调模型与用户从 OSS 导入的自定义模型 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token 按量部署**：**仅限 LoRA 微调模型**，不支持基础模型或全参微调模型，适用于效果验证与低成本轻量级调用 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。

此外，**智能路由**作为高级调度能力，支持基于内容动态匹配备选模型集（如 `qwen3.8-max`、`deepseek-v4-flash-0731`、`glm-5.2` 等），但仅限文本 Chat Completions 接口且必须使用 `maas.aliyuncs.com` 域名 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

> **注意**：文档 7 与文档 8 均明确指出“当前版本支持导入 LoRA 模型，**不支持导入全参微调模型**”，而文档 7 中“支持的模型”表格下方又标注“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”。该表述存在矛盾——实际生产环境应以文档 8 的明确限制为准：**全参微调模型暂不可通过 OSS 导入**，白名单属例外通道，非标准能力。

## 关键参数

不同部署模式的关键配置参数差异显著，开发者需按需设置：

| 参数类别 | PTU 模式 | DTU/MU 模式 | Token 按量模式 |
|----------|-----------|--------------|------------------|
| **核心计量单位** | 输入/输出 TPM（每分钟 Token 数） | DTU：输入/输出 TPM；MU：模型单元（MU）数量 | 输入/输出 Token 数 |
| **必填容量参数** | `input_tpm`, `output_tpm`（整数倍基准值） | DTU：`input_tpm`, `output_tpm`；MU：`deploy_spec`, `capacity`（副本数） | `capacity`（必须填写，但实际无效） |
| **推理控制** | 不可调（平台预置） | 可配置 `enable_thinking`, `max_context_length`, `rpm_limit`, `tpm_limit` | 不可调（平台预置） |
| **缓存支持** | 支持长输入阶梯系数与前缀缓存折扣（如 `glm-5.1` 缓存命中部分按 20% 折算） | MU 模式支持 PD 分离计算模式以降低首 Token 延迟 | 不支持显式缓存，仅依赖底层模型隐式缓存 |

所有模式均需指定 `model_name`（模型代码）与 `name`（服务名称）。API 部署时，`plan` 字段必须为 `ptu` / `mu` / `lora` 之一，详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 使用方式

部署可通过控制台或 API 两种方式完成，推荐优先使用控制台进行首次配置与调试：

1. **控制台流程**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy) → **模型推理 > 专属部署** → **部署新模型** → 选择部署模式（PTU/DTU/MU/Token/智能路由）→ 填写服务名称、模型、计费方式及对应容量参数 → 确认创建。
2. **API 流程**：调用 `/api/v1/deployments` 接口，按 `plan` 类型提交结构化 JSON：
   - PTU：传入 `"plan": "ptu"`, `"ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}`
   - MU：传入 `"plan": "mu"`, `"deploy_spec": "MU1"`, `"capacity": 4`
   - Token：传入 `"plan": "lora"`，`"capacity"` 任意值（如 `1`）[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)

部署成功后，服务状态变为 `RUNNING`，其唯一标识 `deployed_model`（即模型 code）可用于后续推理调用。调用时需确保 API Key 所属业务空间已开通该模型的部署权限，否则将报错 `Workspace xxx does not have deployment privilege for model xxxx` [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。

## 限制和注意事项

- **计费不可变**：所有部署方式在创建后**无法更改计费模式**，切换必须先下线旧服务再新建 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **模型权限隔离**：调优后的模型仅能被其所在业务空间的 API Key 调用，且目前**不支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用**，仅限 DashScope SDK 或原生协议 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)。
- **OSS 导入强约束**：LoRA 模型导入要求严格——必需文件（`adapter_model.safetensors`, `adapter_config.json`, `config.json`）、rank 值（8/16/32/64）、词汇表与 chat_template 必须与基础模型完全一致；视觉模型必须冻结 VIT [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **智能路由限制**：仅支持 OpenAI Chat Completions 协议、`maas.aliyuncs.com` 域名、文本输入；不支持 `logprobs`, `top_p`, `temperature` 等采样参数；上下文上限取备选集中最小窗口值 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自动释放策略**：Token 按量部署若**连续一个月未使用将自动释放**，而 PTU/DTU/MU 无此策略，需手动下线或删除以停止计费 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


