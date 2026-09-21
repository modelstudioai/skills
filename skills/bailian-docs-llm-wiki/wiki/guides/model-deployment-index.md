# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐保障的预置资源到按需付费的弹性调用，覆盖生产级稳定服务、私有化推理与效果验证等典型场景。所有部署均通过统一控制台或 API 管理，底层资源由平台全托管，开发者聚焦业务集成。部署即计费，服务状态变更（如扩缩容、下线）直接影响费用结算。

## 支持的模型/功能

- **预置模型**：千问（Qwen）、DeepSeek、GLM、Kimi、CosyVoice 等系列的官方发布版本，支持 PTU、DTU、MU 及 Token 按量等多种部署模式。具体支持列表以控制台实时可选为准，详见[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **微调模型**：LoRA 微调模型全面支持 Token 按量部署（仅限 LoRA）及 DTU/MU 独占部署；全参微调模型支持 DTU/MU 部署，导入需联系客户经理开通白名单 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)。
- **自定义模型**：支持从 OSS 导入符合约束的 LoRA 模型（rank=8/16/32/64、词汇表与 chat_template 未修改、VIT 冻结等），导入后可部署为 PTU、DTU 或 MU 服务 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)。
- **智能路由**：仅支持文本 Chat Completions 接口，通过 `auto-model-xxxxxx` code 调用，动态匹配备选集内最优模型，当前支持北京与新加坡地域 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

> **注意**：文档 1 中称“Token 按量部署支持部分经过 LoRA 调优后的模型”，而文档 4 明确限定“仅支持 LoRA 微调模型”，且文档 5 和 7 均强调导入与部署 LoRA 模型的严格约束（如 rank、词汇表一致性）。因此，“部分”一词易引发歧义，应以“仅支持 LoRA 微调模型”为准。

## 关键参数

| 参数 | 说明 | 所属部署模式 | 备注 |
|------|------|--------------|------|
| `plan` | 计费方案标识 | API 部署必填 | `ptu`（预置吞吐）、`mu`（模型单元）、`lora`（Token 按量） |
| `ptu_capacity` | 输入/输出 TPM 额度 | PTU 模式 | `{"input_tpm": 10000, "output_tpm": 1000}` |
| `deploy_spec` / `model_unit_spec` | 模型单元规格 | MU/DTU 模式 | 如 `"MU1"`、`"MU2 x 8"`，决定算力基线 |
| `capacity` | 模型单元数量或冗余字段 | MU/Lora 模式 | MU 模式为实际单元数；Lora 模式必须填写但无效 |
| `enable_thinking` | 是否启用思考模式 | MU/DTU 模式 | 影响推理性能与计费（思考 token 按输出价计费） |
| `max_context_length` | 最长上下文长度 | MU 模式 | 部分模型支持自定义，超出将报错 |
| `rpm_limit` / `tpm_limit` | 请求/Token 限流阈值 | MU 模式 | 用于主动管控并发，非平台默认限流 |

## 使用方式

1. **控制台部署**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「模型推理 > 专属部署 > 部署新模型」，按向导填写服务名称、模型、计费方式及对应参数（如 PTU 的 TPM、MU 的单元规格）即可创建。权限不足时需检查业务空间模型部署权限 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
2. **API 部署**：使用 DashScope HTTP API 或 CLI，构造包含 `plan`、`model_name` 及模式特有参数（如 `ptu_capacity`）的 JSON 请求。示例见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
3. **调用方式**：部署成功后，在控制台「部署列表」获取 `model_code`（如 `qwen3-8b-xxx`），该 code 用于 API 请求的 `model` 字段。支持 DashScope、[OpenAI 兼容接口](../concepts/openai-compatible-api.md)及 Assistant SDK，详见 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
4. **智能路由**：创建后获得 `auto-model-xxxxxx` code，直接用于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，无需修改客户端逻辑 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

## 限制和注意事项

- **计费不可变**：服务创建后计费方式无法更改，切换需先下线旧服务再新建 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **地域限制**：PTU/DTU/MU 部署目前仅支持华北2（北京）；智能路由支持北京与新加坡 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **模型约束**：
  - Token 按量部署仅支持 LoRA 模型，且一个月不使用将自动释放 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
  - DTU 部署暂不支持 API 创建与管理，必须通过控制台操作 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **扩缩容差异**：
  - PTU/DTU/MU 支持自助扩缩容（控制台或 API）；
  - Token 按量部署扩容需提交人工审核申请 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **缓存行为**：PTU 部署支持前缀缓存并影响额度消耗（阶梯系数+折扣），响应中返回 `cached_tokens` 字段；智能路由不保障缓存命中率，仅依赖实际路由模型的隐式缓存 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)


