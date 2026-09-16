# model deployment 1

百炼平台的 model deployment 1 是面向生产环境的模型推理服务部署能力，提供多种计费与资源隔离模式，支持预置吞吐（PTU）、独占算力（DTU/MU）和 Token 按量三种核心部署方式。开发者可根据性能要求、成本敏感度与业务稳定性需求，在控制台或通过 API 快速完成模型服务的创建、扩缩容与运维。所有部署均需先完成模型调优或导入，并在对应业务空间内具备相应权限。

## 支持的模型/功能

- **基础模型与微调模型**：支持平台预置的千问（Qwen）、GLM、DeepSeek、Kimi 等系列模型；LoRA 微调模型可通过 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md) 流程从 OSS 导入后部署；全参微调模型属白名单功能，需联系客户经理开通 [我的模型](../../raw/model-user-guide/model-deployment-1/my-model-center.md)。
- **部署模式覆盖**：
  - PTU（预置吞吐）：适用于高并发、低延迟场景，保障稳定 TPM 吞吐，支持长输入阶梯系数与前缀缓存折扣 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)；
  - DTU/MU（独占算力）：提供物理级 GPU 隔离，支持 PD 分离计算模式、自定义推理模式（Instruct/Thinking）及最长上下文配置，新模型优先采用 DTU 方案 [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)；
  - Token 按量：仅限 LoRA 微调模型，按实际输入/输出 Token 计费，“不使用不计费”，适用于效果验证与低成本轻量场景 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)；
  - 智能路由：动态匹配备选模型集，支持效果优先与成本优先策略，调用时使用 `auto-model-xxxx` code，响应头 `x-dashscope-resolved-model` 标明实际执行模型 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。

> **注意**：文档 1 中称“部分预置模型”支持 PTU，而文档 3 的价格表明确列出数十个千问、DeepSeek、GLM 等模型（如 `qwen3.7-plus-2026-05-26`、`deepseek-v4-flash`）均支持 PTU 部署，且文档 3 的“支持模型与价格”章节为最新定价依据，应以该文档为准。文档 1 的模糊表述已过时。

## 关键参数

| 参数 | 说明 | 取值约束 | 来源 |
|------|------|----------|------|
| `plan` | 计费模式标识 | `ptu` / `mu` / `lora` / `router`（智能路由） | [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 模式下的吞吐额度 | `{"input_tpm": N, "output_tpm": M}`，N/M 为基准 TPM 的整数倍 | [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md) |
| `deploy_spec` / `model_unit_spec` | MU/DTU 模式下的算力规格 | 如 `MU1`, `MU2`, `MU9`；DTU 模式下由输入/输出 TPM 倍数决定 | [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md) |
| `enable_thinking` | 推理模式开关 | `true`（启用思考模式）/ `false`（非思考模式），部分模型支持 | [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `max_context_length` | 最长上下文长度 | 依模型能力而定，如 `qwen3.7-plus` 支持 1M token | [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | 数值型，仅 MU 模式支持配置 | [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md) |

## 使用方式

- **控制台部署**：登录 [专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式（PTU/DTU/MU/Token/智能路由）→ 配置对应参数 → 确认创建。状态变为「运行中」即部署成功。
- **API 部署**：使用 DashScope API 发起 `POST /api/v1/deployments` 请求，`plan` 字段指定模式，其余参数按模式填充（如 `ptu_capacity`、`deploy_spec`、`enable_thinking`）。详见 [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。
- **调用方式**：部署成功后，获取模型 `code`（控制台列表页或 API 返回 `deployed_model`），通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，`model` 参数填入该 `code`。智能路由使用 `auto-model-xxxx` code，响应头 `x-dashscope-resolved-model` 返回实际执行模型。
- **扩缩容**：
  - PTU/MU：控制台点击「扩缩容」自助增减吞吐量或模型单元数量；
  - Token 按量：需在控制台提交扩容申请，等待人工审核；
  - 智能路由：修改备选模型集或路由策略即可生效。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法更改计费模式，切换需先下线旧服务再重新部署 [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)。
- **模型兼容性约束**：
  - LoRA 导入模型必须满足 `rank ∈ {8,16,32,64}`、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等要求，否则校验失败 [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)；
  - Token 按量部署**仅支持 LoRA 模型**，且一个月不使用将自动释放 [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)；
  - 智能路由**仅支持文本 Chat Completions**，不支持图片/视频输入、Embedding/Rerank、Batch、Anthropic 协议等 [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **地域与协议限制**：
  - PTU/DTU/MU 部署默认支持北京地域，API 调用需使用对应地域 Base URL；
  - 智能路由**仅支持 `maas.aliyuncs.com` 域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不支持 `dashscope.aliyuncs.com` [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)。
- **权限与配额**：部署前需确保业务空间已开通目标模型的调用权限，RAM 用户需被授予对应模型权限；智能路由备选模型若配额不足（RPM/TPM），可能导致请求被限流 [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 来源文档

- [专属部署](../../raw/model-user-guide/model-deployment-1/model-deployment-introduction.md)
- [独占算力部署（DTU）](../../raw/model-user-guide/model-deployment-1/dtu-model-deployment.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-1/ptu-long-input-and-cache.md)
- [模型导入](../../raw/model-user-guide/model-deployment-1/model-import.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-1/model-deployment-token.md)
- [我的模型](../../raw/model-user-guide/model-deployment-1/my-model-center.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)
- [智能路由](../../raw/model-user-guide/model-deployment-1/model-routing.md)


