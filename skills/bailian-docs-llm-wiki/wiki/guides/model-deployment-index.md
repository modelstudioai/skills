# model deployment index

百炼平台提供多种模型部署方式，支持从轻量级按量计费到高性能独占算力的全场景覆盖。所有部署均通过统一控制台或 API 管理，服务创建后即产生费用，且计费方式不可变更。核心部署模式包括预置吞吐（PTU）、独占算力（DTU/MU）和 [Token](../concepts/token.md) 按量三种，分别面向高并发低延迟、资源隔离与性能定制、以及低成本效果验证等差异化需求。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高吞吐、长输入（最高 1M token）及前缀缓存场景，支持千问、DeepSeek、GLM、千问VL 等系列模型，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：提供物理资源隔离，DTU 按输入/输出 TPM 计费（新模型首选），MU 按模型单元数量计费（旧模型沿用），均支持基础模型、LoRA 微调模型及用户导入模型，支持 PD 分离计算模式与思考/非思考推理模式切换，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量**：仅支持 LoRA 微调模型，不使用不计费，适用于效果验证与低负载场景，不支持自助扩缩容，扩容需人工审核，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过 `auto-model-xxxx` model-code 动态路由至备选模型集（至少 2 个），仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与文本 Chat Completions，不支持 DashScope 协议、图片/视频输入、Embedding/Rerank 等，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入 LoRA 模型（rank 必须为 8/16/32/64，VIT 必须冻结，词汇表与 chat_template 不可修改），不支持全参微调模型导入（白名单功能），详见[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)与[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 7 明确声明“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”，而文档 5 提到“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”。二者存在矛盾——实际生产环境以文档 7 的明确限制为准，全参导入为受限白名单能力，非标准流程。

## 关键参数

| 参数 | 说明 | 取值约束 | 所属部署模式 |
|------|------|----------|--------------|
| `plan` | 计费方案标识 | `ptu` / `mu` / `lora` / `router` | API 部署必需（见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)） |
| `input_tpm` / `output_tpm` | DTU 购买额度 | 基准 TPM 的整数倍，各模型有固定基准值（如 qwen3.5-122b-a10b 输入基准为 7,288,000 TPM） | DTU 专属 |
| `deploy_spec` / `capacity` | MU 规格与副本数 | `MU1`~`MU9`，`capacity` 表示单副本模型单元数（如 `MU1 x 8`） | MU 专属 |
| `ptu_capacity` | PTU 容量配置 | `{ "input_tpm": 10000, "output_tpm": 1000 }` | PTU 专属 |
| `enable_thinking` | 推理模式开关 | `true`（思考模式）/ `false`（非思考模式），部分模型部署时可配 | DTU/MU/智能路由（影响路由逻辑） |
| `max_context_length` | 最长上下文 | 依模型能力而定（如 qwen3.8-max 支持 1M），PTU 模型在长输入时触发阶梯系数 | DTU/MU/PTU |
| `rpm_limit` / `tpm_limit` | 服务限流 | 仅 MU 模式支持配置，PTU/DTU 默认不限流（受实际承载力限制） | MU 专属 |

## 使用方式

- **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 配置参数（如 TPM、MU 规格、溢出策略等）→ 确认。部署状态变为「运行中」后即可调用。
- **API 部署**：使用 `curl` 或 DashScope SDK，按 `plan` 类型传入对应参数：
  - PTU：`"plan": "ptu", "ptu_capacity": {...}`
  - MU：`"plan": "mu", "deploy_spec": "MU1", "capacity": 4, "enable_thinking": true`
  - LoRA：`"plan": "lora", "capacity": 1`（`capacity` 必填但无效）
  - 智能路由：`"plan": "router"`（需在控制台创建后获取 `model-code`）
  详细示例见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **调用方式**：
  - DashScope SDK：`model` 参数填部署成功后的 `model_code`（非服务名称）。
  - [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：`base_url` 必须为 `maas.aliyuncs.com`（智能路由强制），`model` 填 `auto-model-xxxx` 或具体模型 code。
  - 注意：调优模型仅支持其所在业务空间的 API Key 调用，且目前仅 DashScope 协议支持（OpenAI 兼容暂不支持），详见[我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)。

## 限制和注意事项

- **计费不可变**：服务创建后无法更改计费方式，切换需先下线原服务再重新部署，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域限制**：智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）；API 部署指南明确标注“仅适用于华北2（北京）地域”。
- **权限要求**：控制台部署需业务空间具备「模型部署-操作」权限；API 部署需 API Key 所属账号在对应业务空间拥有模型部署权限，且业务空间已授权目标模型，详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)权限排查章节。
- **模型兼容性**：
  - [Token](../concepts/token.md) 按量部署仅支持 LoRA 模型，且一个月不使用将自动释放；
  - DTU/MU 支持 LoRA 与全参微调模型，但 MU 对部分大模型（如 qwen3.5-397b）要求 PD 分离模式；
  - 智能路由不支持 `top_p`、`temperature` 等采样参数，设置将导致报错。
- **退订规则**：预付费（DTU/MU/PTU）提前退订，已使用部分按 1.2 倍系数结算退费；后付费欠费后保留资源 24 小时，超时将停服并释放资源。
- **缓存行为**：PTU 部署的 `cached_tokens` 字段仅在 DashScope 和 OpenAI Chat 兼容响应中返回，Anthropic 兼容格式暂不支持；智能路由不保障缓存命中率，因请求可能被路由至不同模型。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)


