# model deployment index

百炼平台提供多种模型部署方式，支持从低成本验证到高并发生产环境的全场景需求。核心部署模式包括预置吞吐（PTU）、独占算力（DTU/MU）、Token按量计费及智能路由，各模式在资源隔离性、性能确定性、计费粒度和适用场景上存在显著差异。开发者应根据业务对延迟、吞吐、成本敏感度及模型定制化程度的要求选择合适方案。

## 支持的模型/功能

- **预置吞吐（PTU）**：适用于高吞吐、低延迟生产场景，支持千问3.8-Max、DeepSeek-v4-Pro等主流大模型，具备长输入阶梯容量系数与前缀缓存折扣能力，详见[PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU面向新发布模型（按TPM×时长计费），MU面向已有模型（按模型单元数量×时长计费），均提供物理资源隔离与PD分离计算模式支持，支持全参/LoRA微调模型及部分多模态模型，详见[DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token按量计费**：仅支持LoRA微调模型（如`qwen3-8b-ft-202511132025-0260`），不使用不计费，适用于效果验证与低成本场景，详见[Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过`auto-model-xxxxxx`统一入口，动态匹配备选模型集（如`qwen3.8-max`、`deepseek-v4-flash-0731`），支持效果优先/成本优先策略，仅限OpenAI兼容接口调用，详见[智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从OSS导入LoRA微调模型（需满足rank、词汇表、chat_template等约束），导入后可部署至PTU/DTU/MU模式，不支持全参微调模型导入，详见[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 6（我的模型）与文档 8（模型导入）对“全参微调模型导入”的描述存在矛盾。文档 6 明确说明“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”，而文档 8 则断言“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”。以文档 6 的白名单说明为准，实际开通需联系客户经理。

## 关键参数

| 参数 | 适用模式 | 说明 | 约束 |
|------|----------|------|------|
| `plan` | API部署通用 | 计费模式标识：`ptu`、`mu`、`lora` | 必填，决定后续参数结构 |
| `ptu_capacity` | PTU | `{ "input_tpm": 10000, "output_tpm": 1000 }` | 后付费必填；预付费按天计费 |
| `deploy_spec` / `model_unit_spec` | MU | 如 `"MU1"`、`"MU2 x 8"` | 决定单副本算力规格，影响总模型单元数 |
| `capacity` | MU / Token | 副本数（MU）或占位值（Token） | Token模式下`capacity`无效但必须填写，详见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `enable_thinking` | MU / DTU | 控制推理模式（`true`/`false`） | 部分模型支持，影响首Token延迟与计费 |
| `max_context_length` | MU / DTU | 最长上下文长度（token） | 依模型能力而定，如`qwen3.7-plus-2026-05-26`支持256K |
| `rpm_limit` / `tpm_limit` | MU | 服务级限流阈值 | 仅MU模式支持配置 |

## 使用方式

- **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 选择模型 → 指定计费方式（PTU/DTU/MU/Token/智能路由）→ 填写参数 → 确认。部署状态变为「运行中」即成功。
- **API部署**：使用`curl`或`dashscope CLI`调用`/api/v1/deployments`接口。示例：
  - PTU：`"plan": "ptu", "ptu_capacity": {"input_tpm": 10000, "output_tpm": 1000}`
  - MU：`"plan": "mu", "deploy_spec": "MU1", "capacity": 4`
  - Token：`"plan": "lora", "capacity": 1`（`capacity`为占位符）
  完整示例见[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **智能路由调用**：将请求中的`model`参数设为生成的`auto-model-xxxxxx`，域名必须为`maas.aliyuncs.com`（非`dashscope.aliyuncs.com`），仅支持OpenAI Chat Completions协议。

## 限制和注意事项

- **计费方式不可变**：服务创建后无法切换计费模式，必须下线原服务并重新部署，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域与协议限制**：
  - 智能路由仅支持北京（`cn-beijing`）和新加坡（`ap-southeast-1`）地域，且**仅限OpenAI兼容接口**，不支持DashScope或Anthropic协议。
  - DTU部署暂不支持API创建与管理，必须通过控制台操作。
- **模型与权限约束**：
  - Token按量部署仅支持LoRA微调模型，且一个月不使用将自动释放。
  - 导入LoRA模型需严格满足`rank`（8/16/32/64）、词汇表一致性、`chat_template`未修改、VIT冻结等约束，校验失败报错`AvailableModelFileNotFound`。
- **扩缩容能力差异**：
  - PTU/MU：支持自助增减吞吐量或模型单元数量。
  - Token按量：扩容需提交人工审核申请，不支持自助操作。
- **缓存与路由特殊行为**：
  - PTU的`cached_tokens`字段反映前缀缓存命中量，但智能路由不保障缓存命中率，因其可能路由至不同模型。
  - 智能路由不支持`top_p`、`temperature`等采样参数，设置将导致运行报错。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


