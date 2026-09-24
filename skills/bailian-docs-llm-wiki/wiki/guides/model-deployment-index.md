# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐保障的预置资源到低成本按量计费的灵活方案，满足生产环境稳定性、性能隔离性与验证阶段成本敏感性的差异化需求。所有部署均通过统一控制台或 API 管理，服务创建后即开始计费，且计费方式不可变更。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高并发、低延迟场景，支持千问3.8-Max、qwen3.7-flash-2026-07-15、deepseek-v4-flash、glm-5.2 等主流模型，具备长输入阶梯容量系数与前缀缓存折扣能力，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 按输入/输出 TPM 计费，MU 按模型单元数量计费，均提供物理资源隔离。支持基础模型（如 qwen3.7-plus-2026-05-26、glm-5.1）及 LoRA/全参微调模型，支持 PD 分离计算模式，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量部署**：仅支持 LoRA 微调模型（如 `qwen3-8b-ft-202511132025-0260`），不使用不计费，适用于效果验证；不支持自助扩缩容，扩容需人工审核，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过 `auto-model-xxxxxx` 统一入口自动匹配备选模型集（如 `qwen3.8-max`、`deepseek-v4-flash-0731`），支持效果优先/成本优先策略，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与文本 Chat Completions，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型**：支持从 OSS 导入 LoRA 模型（需满足 rank、词汇表、chat_template 等约束），以及百炼平台调优生成的模型，导入后可部署为 PTU、DTU 或 [Token](../concepts/token.md) 按量服务，详见[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)与[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 7 与文档 8 均描述 OSS 导入流程，但文档 8 明确声明“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”，而文档 7 中“支持的模型”部分提及“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”。二者存在矛盾。实际生产中应以文档 8 的明确限制为准——标准流程仅支持 LoRA；全参微调导入为受限白名单能力，非默认可用。

## 关键参数

| 参数 | 说明 | 适用部署方式 | 示例值 |
|------|------|--------------|--------|
| `plan` | 计费方案标识 | 所有 API 部署 | `"ptu"` / `"mu"` / `"lora"` |
| `ptu_capacity` | PTU 吞吐额度配置 | PTU | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `model_unit_spec` | 模型单元规格 | MU/DTU | `"MU1"` / `"MU2 x 8"` |
| `capacity` | 模型单元数量（MU）或占位符（LoRA） | MU / LoRA | `4`（MU）；`1`（LoRA，必填但无效） |
| `enable_thinking` | 是否启用思考模式 | MU / DTU / OpenAI 接口 | `true` / `false` |
| `max_context_length` | 最长上下文长度 | MU/DTU（部分模型） | `10000` |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | MU/DTU（部分模型） | `500`, `1000` |

## 使用方式

1. **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 选择模型 → 指定计费方式（PTU/DTU/MU/[Token](../concepts/token.md) 按量/智能路由）→ 填写参数 → 确认。权限不足时需检查业务空间模型部署权限及 RAM 用户角色，详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)中的权限排查章节。
2. **API 部署**：使用 `curl` 或 `dashscope` CLI 调用 `/api/v1/deployments` 接口。PTU 需传 `ptu_capacity`，MU 需传 `deploy_spec` 和 `capacity`，LoRA 需设 `plan: "lora"` 并填占位 `capacity`。部署成功后返回 `deployed_model` 字段作为后续调用的 `model` 参数，详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
3. **调用已部署服务**：使用 DashScope SDK、[OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 Assistant SDK，将 `model` 参数设为部署生成的 `model_code`（如 `qwen3-14b-xxx`）或智能路由 `model-code`（如 `auto-model-abcd1234`）。注意：调优模型仅支持 DashScope 协议调用，不支持 OpenAI 兼容方式，详见[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费方式，必须下线旧服务并新建，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **模型支持范围差异**：
  - PTU 与 DTU 支持模型列表不同，新模型优先采用 DTU 方案；
  - Token 按量仅支持 LoRA 微调模型，且一个月不使用将自动释放；
  - 智能路由仅支持文本 Chat Completions，不支持图片、Embedding、Rerank 等接口。
- **扩缩容能力**：
  - PTU/DTU/MU 支持自助扩缩容（手动或自动伸缩）；
  - Token 按量扩容需在控制台提交申请并等待人工审核；
  - 智能路由不支持扩缩容，其容量由备选模型自身配额决定。
- **地域与协议限制**：
  - 智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且仅限 `maas.aliyuncs.com` 域名与 OpenAI 兼容协议；
  - DTU 部署暂不支持 API 创建与管理，必须通过控制台操作。
- **缓存行为**：PTU 部署的 `cached_tokens` 字段反映前缀缓存命中量，但智能路由因模型动态切换，不保障缓存命中率，详见[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


