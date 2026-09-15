# model deployment 1

百炼平台的 model deployment 1 是面向生产环境的模型服务化核心能力，提供多种计费与资源隔离模式，支持从效果验证到高并发低延迟场景的全栈部署需求。其核心是通过 PTU（预置吞吐）、DTU/MU（独占算力）和 [Token](../concepts/token.md) 按量三种主要模式，实现性能、成本与灵活性的平衡。所有部署均需在专属部署控制台或通过 API 完成，且计费方式创建后不可变更。

## 支持的模型/功能

- **PTU 预置吞吐**：适用于高吞吐、低延迟场景，支持千问3.8-Max、DeepSeek-v4-Pro 等主流大模型，以及长输入（最高 1M token）与前缀缓存能力 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)。
- **DTU/MU 独占算力**：提供物理级资源隔离，支持基础模型与自定义模型（含 LoRA/全参微调），并支持 PD 分离计算模式以优化首字延迟 [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调模型，用于低成本效果验证，不使用不计费 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)。
- **智能路由**：非传统部署模式，但属于 model deployment 1 生态关键组件，通过 `auto-model-xxxx` 动态路由至备选模型集，实现效果与成本的自动权衡 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **模型来源**：支持平台预置模型、百炼调优模型及从 OSS 导入的 LoRA 模型（全参微调需白名单）；导入模型需满足 rank、词汇表、chat_template 等严格约束 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

> **注意**：文档 1 中称“DTU 是模型单元(MU)的继任方案”，而文档 5 明确 DTU 与 MU 是并存的两种方案（DTU 面向新模型，MU 面向已有模型）。此处以文档 5 的权威定义为准，二者为互补关系，非替代关系。

## 关键参数

| 参数 | 说明 | 示例值 | 所属模式 |
|------|------|--------|----------|
| `plan` | API 部署必需字段，标识计费类型 | `"ptu"`, `"mu"`, `"lora"` | [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 模式下指定输入/输出 TPM 额度 | `{"input_tpm": 10000, "output_tpm": 1000}` | PTU |
| `deploy_spec` / `capacity` | MU 模式下指定模型单元规格与数量 | `"MU1"`, `4` | MU |
| `enable_thinking` | 控制是否启用思考模式（影响推理行为与计费） | `true`, `false` | PTU/MU |
| `max_context_length` | 设置最长上下文长度（部分模型支持） | `10000` | MU |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | `500`, `1000` | MU |

## 使用方式

1. **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称 → 选择模型与计费方式 → 配置参数（如 TPM、MU 规格、路由策略等）→ 确认。部署状态变为「运行中」即成功。
2. **API 部署**：使用 DashScope API 发起 HTTP 请求，需正确设置 `plan`、`model_name` 及对应容量参数。例如 PTU 部署需传 `ptu_capacity`，MU 部署需传 `deploy_spec` 和 `capacity` [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
3. **调用方式**：部署成功后，使用返回的 `model_code`（如 `qwen3-8b-ft-xxx` 或 `auto-model-abcd1234`）调用 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。注意：智能路由必须使用 `maas.aliyuncs.com` 域名，不支持 `dashscope.aliyuncs.com` [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
4. **模型导入前置**：若需部署自有 LoRA 模型，须先完成 OSS 授权（添加 `bailian-datahub-access=read` 标签）、准备合规文件（`adapter_model.safetensors` 等），再通过「我的模型」控制台导入 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 限制和注意事项

- **计费不可变**：所有部署的计费方式（PTU/MU/[Token](../concepts/token.md)）创建后无法修改，切换必须先下线旧服务再新建 [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **扩缩容差异**：
  - PTU/MU：支持自助扩缩容（手动或自动伸缩）。
  - Token 按量：扩容需提交人工审核申请，不支持自助操作 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)。
- **模型兼容性**：
  - Token 按量仅支持 LoRA 微调模型，不支持全参微调或原始预置模型。
  - 智能路由仅支持文本 Chat Completions，不支持图片、Embedding、Rerank、Batch 或 Anthropic 协议 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **权限与地域**：
  - API 部署要求 API Key 所属业务空间已开通目标模型的部署权限，否则报错 `Workspace xxx does not have deployment privilege for model xxxx` [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
  - 智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **OSS 导入限制**：不支持访问 Bucket 根目录；存储类型不支持归档/冷归档；子账号需主账号授权 `ram:CreateServiceLinkedRole` 权限方可完成首次授权 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)。

## 来源文档

- [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-1/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)


