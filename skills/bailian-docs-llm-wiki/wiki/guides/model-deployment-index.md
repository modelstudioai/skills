# model deployment index

百炼平台提供多种模型部署方式，以满足不同场景下的性能、成本与灵活性需求。本文档系统梳理了专属部署的核心能力，涵盖支持的模型类型、关键配置参数、标准使用流程，以及各部署模式的限制与注意事项，帮助开发者快速选型并落地生产服务。

## 支持的模型/功能

百炼支持三类主流部署模式：**PTU（预置吞吐）**、**DTU/MU（独占算力）** 和 **[Token](../concepts/token.md) 按量**，分别面向高并发低延迟、资源隔离强保障、低成本验证等典型场景。所有模式均支持平台预置模型及用户调优模型，但具体支持范围存在差异：

- **PTU 部署**：支持部分预置模型（如 `qwen3.8-max`、`deepseek-v4-flash`）及所有 LoRA 调优后模型，特别强化长输入（最高 1M token）与前缀缓存能力，详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **DTU/MU 部署**：DTU 面向新发布模型（按输入/输出 TPM 计费），MU 面向已有模型（按模型单元数量计费），两者均支持基础模型、LoRA 及全参微调模型，并提供 PD 分离计算等高级推理模式，详见 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：**仅支持 LoRA 微调模型**，不使用不计费，适用于效果验证阶段；不支持自定义性能参数，吞吐与延迟由平台统一预置，详见 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。

此外，平台还提供 **智能路由** 功能，通过 `auto-model-xxxx` 统一入口，动态匹配备选模型集（如 `qwen3.8-max`、`deepseek-v4-flash-0731` 等）中的最优模型，实现效果与成本的自动平衡，但仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，详见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

> **注意**：文档 1 中称“[Token](../concepts/token.md) 按量部署支持部分经过 LoRA 调优后的模型”，而文档 4 明确限定为“仅支持 LoRA 微调模型”，且文档 6 与 8 均强调“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”。因此，Token 按量部署**不支持全参微调模型**，该限制为权威口径。

## 关键参数

不同部署模式的关键配置参数差异显著，开发者需按需选择：

| 参数类别         | PTU 模式                          | DTU/MU 模式                                      | Token 按量模式               |
|------------------|-------------------------------------|--------------------------------------------------|------------------------------|
| **核心计量单位** | 输入/输出 TPM（每分钟 Token 数）     | DTU：输入/输出 TPM；MU：模型单元（MU）数量        | 输入/输出 Token 数           |
| **必填容量参数** | `input_tpm`, `output_tpm`（整数倍） | DTU：`input_tpm`, `output_tpm`；MU：`deploy_spec`, `capacity` | `capacity`（必须填写但无效）   |
| **性能控制**     | 不可调（平台预置）                  | MU 模式可调：`max_context_length`, `rpm_limit`, `tpm_limit` | 不可调（平台预置）           |
| **推理模式**     | 不支持显式配置                      | MU 模式支持：`enable_thinking`, `reasoning_effort` | MU 模式支持，PTU/Token 不支持 |

所有模式均支持设置服务名称、付费类型（预付费/后付费）、自动续费等通用参数。DTU/MU 还支持部署模版、副本数等底层资源编排选项，详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 中的参数说明。

## 使用方式

部署可通过控制台或 API 两种方式完成，推荐流程如下：

1. **前置准备**：确保业务空间已开通对应模型的部署权限；若需导入自有 LoRA 模型，须先完成 OSS 授权并上传合规文件，详见 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)；
2. **创建部署**：
   - **控制台**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，点击“部署新模型”，选择模型、计费方式及对应参数后确认；
   - **API**：使用 `curl` 或 `dashscope CLI` 调用 `/api/v1/deployments` 接口，`plan` 字段指定 `ptu`/`mu`/`lora`，并传入对应参数（如 `ptu_capacity` 或 `deploy_spec`），详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)；
3. **验证与调用**：部署状态变为 `RUNNING` 后，使用返回的 `model_code`（如 `qwen3.8-max`）通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)发起推理请求；
4. **扩缩容**：PTU/DTU/MU 支持自助扩缩容（控制台或 API），Token 按量部署需提交人工审核申请。

## 限制和注意事项

- **计费不可变**：所有部署的计费方式在创建后无法更改，切换需下线旧服务并新建，详见 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)；
- **地域与协议限制**：智能路由仅支持北京与新加坡地域，且**仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`maas.aliyuncs.com` 域名）**，不支持 DashScope 协议与 Anthropic 协议；
- **模型兼容性**：Token 按量部署明确不支持全参微调模型；DTU/MU 部署中，PD 分离模式仅对特定模型生效；视觉语言模型（VL）导入时必须冻结 VIT，否则校验失败；
- **权限与配额**：部署失败常见原因为业务空间缺少模型调用权限或账号 RPM/TPM 配额不足，需提前在[业务空间管理](https://bailian.console.aliyun.com/settings/workspace)中授权并提升额度；
- **生命周期管理**：Token 按量部署若一个月内无调用将自动释放；所有部署服务下线后即停止计费，但删除操作不可恢复，需谨慎执行。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


