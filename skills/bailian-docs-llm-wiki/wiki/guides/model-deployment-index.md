# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐、低延迟的生产级专属服务到低成本验证型按量计费模式。所有部署均通过统一控制台或 API 管理，资源由平台全托管，开发者无需运维底层 GPU。核心能力包括 PTU（预置吞吐）、DTU/MU（独占算力）和 [Token](../concepts/token.md) 按量三种计费模式，以及智能路由等高级调度能力。

## 支持的模型/功能

- **基础模型与调优模型**：支持千问（Qwen）、DeepSeek、GLM、Kimi 等主流开源模型的预置版本；LoRA 微调模型可通过 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 流程导入并部署；全参微调模型需白名单开通。
- **部署模式覆盖**：
  - PTU：面向高并发、低延迟场景，保障确定性 TPM 吞吐，支持长输入阶梯系数与前缀缓存折扣 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)；
  - DTU/MU：面向独占资源需求，DTU 按输入/输出 TPM 计费（新模型首选），MU 按模型单元数量计费（存量模型沿用），均支持 PD 分离计算模式 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)；
  - [Token](../concepts/token.md) 按量：仅限 LoRA 微调模型，不使用不计费，适用于效果验证 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)；
  - 智能路由：动态匹配请求内容至最优备选模型，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与文本 Chat Completions 调用 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义能力**：DTU/MU 支持配置推理模式（Instruct/Thinking）、最长上下文、RPM/TPM 限流；PTU 支持溢出策略（自动溢出或仅使用 PTU 容量）；智能路由支持效果优先/成本优先策略及故障自动切换。

> **注意**：文档 1 中称“DTU 是模型单元(MU)的继任方案”，但文档 3 明确说明“DTU 与 MU 按模型适用区分：新发布模型采用 DTU，已有模型沿用 MU”，二者为并存方案而非替代关系。实际选型应以控制台可选项为准。

## 关键参数

| 参数 | 说明 | 取值约束 | 关联模式 |
|------|------|----------|----------|
| `plan` | 计费方案标识 | `ptu` / `mu` / `lora` | API 部署必需 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 输入/输出 TPM 容量 | 整数倍基准值，单位 kTPM | PTU 模式 |
| `deploy_spec`, `capacity` | MU 规格与单元数量 | 如 `MU1`, `MU2`；`capacity` 为副本数 | MU 模式 |
| `enable_thinking` | 是否启用思考模式 | `true` / `false` | MU/DTU/智能路由（影响模型选型） |
| `max_context_length` | 最长上下文长度 | 依模型能力而定，如 128K、256K | MU 模式（部分模型支持） |
| `rpm_limit`, `tpm_limit` | 服务级限流阈值 | 正整数 | MU 模式（可选） |
| `response_format`, `enable_search` | 智能路由兼容性参数 | 仅路由至支持该参数的备选模型 | 智能路由 |

## 使用方式

- **控制台部署**：登录 [专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 提交。首次部署需确保已开通对应业务空间权限 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **API 部署**：使用 HTTP 或 DashScope SDK 调用 `/api/v1/deployments` 接口。示例中 `model_name` 必须为模型 ID（非显示名称），`name` 为服务别名；部署成功后返回 `deployed_model` 字段作为后续调用的 `model` 参数 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **调用已部署服务**：使用 DashScope 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，`model` 参数填入部署生成的唯一 model code（如 `qwen3-8b-ft-xxx`）。注意：调用必须与部署在同一业务空间，且 API Key 归属账号需具备该空间操作权限。
- **扩缩容**：
  - PTU/DTU/MU：控制台自助增减吞吐量或模型单元数；
  - [Token](../concepts/token.md) 按量：需在控制台提交人工审核申请 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)；
  - 智能路由：修改路由配置（备选集、策略）后几分钟内生效。

## 限制和注意事项

- **计费不可变**：服务创建后计费方式无法更改，切换需先下线原服务再重新部署 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：
  - 智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且仅限 `maas.aliyuncs.com` 域名与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)；
  - DTU 部署暂不支持 API 创建与管理，必须通过控制台操作 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **模型约束**：
  - Token 按量仅支持 LoRA 微调模型，且一个月不使用将自动释放 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)；
  - 导入 LoRA 模型需满足 rank（8/16/32/64）、词汇表一致、chat_template 未修改、VIT 冻结等硬性约束 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **费用与退订**：预付费订单提前终止时，已使用部分按 1.2 倍系数结算退费；PTU/DTU/MU 均适用此规则 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)


