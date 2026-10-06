# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐、低延迟的生产级服务到低成本效果验证的全场景需求。部署方式按资源隔离程度、计费粒度和运维复杂度分为预置吞吐（PTU）、独占算力（DTU/MU）和 [Token](../concepts/token.md) 按量三种核心模式，均通过统一控制台或 API 管理，适用于平台预置模型、LoRA 微调模型及用户导入模型。所有部署服务创建后即开始计费，且计费方式不可变更。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持千问、DeepSeek、GLM、千问VL等系列的主流文本与多模态模型，覆盖输入长度最高达 1M token 的长上下文场景，并原生支持前缀缓存与长输入阶梯容量系数 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 面向新发布模型（如 `qwen3.7-plus-2026-05-26`），按输入/输出 TPM 计费；MU 面向已有模型（如 `qwen3.5-27b`），按模型单元数量计费；两者均支持基础模型、LoRA 微调模型及用户上传模型部署，并可配置 PD 分离计算模式 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量**：仅支持 LoRA 微调后的模型（如 `qwen3-8b-ft-202511132025-0260`），不使用不计费，适用于效果验证阶段 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过固定 model-code（如 `auto-model-abcd1234`）自动匹配备选模型集中的最优模型，仅支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与文本 Chat Completions 调用 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入符合约束的 LoRA 模型（需含 `adapter_model.safetensors`、`adapter_config.json`、`config.json`），不支持全参微调模型导入 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。

> **注意**：文档 6 和文档 8 均明确指出“当前版本支持导入 LoRA 模型，不支持导入全参微调模型”，但文档 6 中又提及“导入全参微调后的模型属于白名单功能，如需开通请联系客户经理”。该矛盾表明全参导入为受限白名单能力，非默认可用；开发者应以文档 8 的明确声明为准，即标准流程仅支持 LoRA。

## 关键参数

| 参数 | 说明 | 所属部署模式 | 示例值 |
|------|------|--------------|--------|
| `plan` | 部署计费方案标识 | API 创建必填 | `"ptu"` / `"mu"` / `"lora"` |
| `ptu_capacity` | PTU 模式下指定输入/输出 TPM 容量 | PTU | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `model_unit_spec` | MU 模式下指定模型单元规格 | MU | `"MU1"` / `"MU2 x 8"` |
| `enable_thinking` | 控制是否启用思考模式（影响推理行为与计费） | MU/DTU/智能路由 | `true` / `false` |
| `max_context_length` | 最长上下文长度（部分 MU 模式支持） | MU | `10000` |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值 | MU | `500` / `1000` |
| `response_format`, `enable_search`, `enable_thinking` | 智能路由下用于实时过滤备选模型的参数 | 智能路由 | `{"type": "json_object"}`, `true`, `true` |

## 使用方式

1. **控制台部署**：登录[专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 提交。LoRA 模型需先在[我的模型](https://bailian.console.aliyun.com/cn-beijing/model/custom)完成导入或调优 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
2. **API 部署**：使用 DashScope API 发送 POST 请求至 `/api/v1/deployments`，按 `plan` 类型传入对应参数（如 `ptu_capacity` 或 `deploy_spec`）。示例详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
3. **调用已部署服务**：API 请求中 `model` 字段填写部署成功后生成的 **模型 Code**（非服务名称），而非原始模型名。DashScope SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)均支持，但需确保业务空间与 API Key 匹配 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
4. **智能路由调用**：将请求 `model` 设为 `auto-model-xxxxxxxx`，其余参数与普通模型一致；响应头 `x-dashscope-resolved-model` 返回实际执行模型 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 限制和注意事项

- **计费不可变**：服务创建后计费方式无法更改，切换必须先下线旧服务再新建 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **权限要求**：控制台部署需业务空间具备对应模型的“模型部署-操作”权限；API 部署需 API Key 所属账号在业务空间拥有模型部署权限及模型调用权限 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **OSS 导入约束**：LoRA 模型文件必须存于 OSS Bucket 的子目录（非根目录），且需满足 rank 取值（8/16/32/64）、词汇表与 chat_template 未修改、视觉模型 VIT 冻结等硬性约束 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **扩缩容差异**：PTU 与 MU 支持自助扩缩容；[Token](../concepts/token.md) 按量部署扩容需人工审核，不支持自助操作 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **地域与协议限制**：智能路由仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，且仅兼容 OpenAI Chat Completions 协议，不支持 DashScope 或 Anthropic 协议 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)


