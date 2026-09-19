# model deployment index

百炼平台提供多种模型部署方式，支持从高吞吐、低延迟的生产级服务到低成本效果验证的全场景需求。部署方式分为预置吞吐（PTU）、独占算力（DTU/MU）和 [Token](../concepts/token.md) 按量三种核心模式，均通过统一控制台或 API 管理，计费方式、性能保障与适用模型各不相同。所有部署服务均生成唯一 `model-code` 用于 API 调用，且创建后计费立即生效。

## 支持的模型/功能

- **预置吞吐（PTU）**：支持千问、DeepSeek、GLM、千问VL 等主流预置模型，适用于长输入（最高 1M token）、多轮对话及内容审核等高并发场景；支持前缀缓存与长输入阶梯容量系数，详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **独占算力（DTU/MU）**：DTU 面向新发布模型（按输入/输出 TPM 计费），MU 适配已有模型（按模型单元数量计费），两者均支持基础模型、LoRA 微调模型及部分全参微调模型部署，并提供 PD 分离计算模式等高级配置 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **[Token](../concepts/token.md) 按量**：仅支持 LoRA 微调后的模型，适用于效果验证与低负载场景，不使用不计费；但一个月内不使用将自动释放 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：通过 `auto-model-xxxxxx` 动态路由至备选模型集（如 `qwen3.8-max`、`deepseek-v4-flash-0731` 等），支持效果优先/成本优先策略，仅限 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与文本 Chat Completions 调用 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **自定义模型导入**：支持从 OSS 导入 LoRA 模型（需满足 rank、词汇表、chat_template 等约束），导入后可在 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 中统一管理并部署，全参微调模型需白名单开通。

> **注意**：文档 1 和文档 3 均提及“DTU 是 MU 的继任方案”，但文档 3 明确说明 DTU 与 MU 并存且按模型适用区分（新模型用 DTU，旧模型沿用 MU），并非完全替代关系；实际选型应以控制台可选项为准。

## 关键参数

| 参数 | 说明 | 取值示例 | 备注 |
|------|------|----------|------|
| `plan` | API 部署时指定计费模式 | `"ptu"` / `"mu"` / `"lora"` | 必填，决定后续参数结构 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) |
| `ptu_capacity` | PTU 模式下输入/输出 TPM 配额 | `{"input_tpm": 10000, "output_tpm": 1000}` | 单位为 token/分钟，受阶梯系数与缓存折扣影响 |
| `deploy_spec` / `capacity` | MU 模式下模型单元规格与数量 | `"MU1"` / `4` | 总算力 = 副本数 × 单副本模型单元数 |
| `enable_thinking` | 控制是否启用思考模式 | `true` / `false` | 影响推理延迟与 [Token](../concepts/token.md) 计费（思考 token 按输出价计费） |
| `max_context_length` | 最长上下文长度（仅 MU 支持） | `10000` | 需在模型支持范围内，超出将报错 |
| `rpm_limit` / `tpm_limit` | 服务级限流阈值（仅 MU 支持） | `500` / `1000` | 不设则无硬性限制，实际承载由资源决定 |

## 使用方式

- **控制台部署**：登录 [专属部署控制台](https://bailian.console.aliyun.com/cn-beijing/model/deploy)，选择「部署新模型」→ 填写服务名称、选择模型与计费方式 → 提交。首次部署需完成权限配置与 OSS 授权（如导入模型）[专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **API 部署**：使用 `POST /api/v1/deployments` 接口，按 `plan` 类型传入对应参数（如 `ptu_capacity` 或 `deploy_spec`），返回 `deployed_model` 为调用所需的 `model-code` [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **调用方式**：所有部署服务均通过 `model-code` 调用，支持 DashScope、[OpenAI 兼容接口](../concepts/openai-compatible-api.md)（需配置 `base_url`）及 Assistant SDK；智能路由必须使用 `maas.aliyuncs.com` 域名 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **扩缩容**：PTU/DIU 支持自助增减吞吐量或模型单元；Token 按量需提交人工审核申请 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。

## 限制和注意事项

- **计费不可变**：服务创建后无法切换计费方式，必须下线原服务再重新部署 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **模型兼容性**：
  - Token 按量仅支持 LoRA 模型，且必须通过百炼调优或符合 OSS 导入规范；
  - DTU 部署暂不支持 API 创建，仅限控制台操作 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)；
  - 智能路由不支持图片/视频输入、Embedding/Rerank、Batch 推理及 `top_p`、`temperature` 等采样参数 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。
- **资源与权限**：
  - OSS 导入需为主 Bucket 添加 `bailian-datahub-access=read` 标签，且模型文件须置于子目录（非根目录）；
  - API 部署失败常见原因为业务空间未授权目标模型或账号无部署权限，需在 [业务空间管理](https://bailian.console.aliyun.com/settings/workspace) 中检查 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)。
- **状态与生命周期**：
  - Token 按量部署若一个月内无调用将自动释放；
  - PTU/DIU 预付费订单退订时，已使用部分按 1.2 倍系数结算；
  - 智能路由 `model-code` 删除后不复用，需重新创建。

## 来源文档

- [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)
- [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)
- [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)
- [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)
- [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)
- [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)
- [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md)
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md)


