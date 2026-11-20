# 智能路由

智能路由（Model Routing）是百炼平台提供的动态模型调度能力，通过统一入口自动为每次推理请求匹配效果最优或成本最优的可用模型，无需客户端感知底层模型变更。该能力本质是“模型即服务”的抽象升级，将模型选择逻辑从应用层下沉至平台层，兼顾性能、效果与成本的实时权衡。

## 在百炼平台的不同场景中，这个概念如何使用

- **面向效果优先的生产场景**：如 AI 编程助手、高准确率问答系统，可选用 `EFFECT_FIRST` 策略，平台在 `qwen3.8-flash`、`deepseek-v4-pro-0813`、`glm-5.2` 等备选模型中，基于实时质量评估（如响应完整性、事实一致性、首字延迟）动态选择最优模型，保障用户体验。
  
- **面向成本敏感的规模化调用**：如客服对话摘要、批量内容生成等任务，可选用 `COST_FIRST` 策略，平台优先调度单位 Token 成本最低且满足基础 SLA（如 P95 首字延迟 ≤ 800ms）的模型，显著降低单位请求费用。

- **灰度发布与模型平滑迁移**：开发者上线新模型（如 `qwen3.8-flash`）后，可通过智能路由逐步导流（配合限流与监控），避免直接替换 model ID 带来的风险；旧模型下线时，路由自动剔除失效选项，业务无感。

- **地域与合规适配**：当前仅支持北京（`cn-beijing`）与新加坡（`ap-southeast-1`）地域，路由决策自动遵循业务空间所在地域的模型可用性与合规策略（如 GLM 系列在海外节点不可见）。

> ⚠️ 注意：智能路由**仅支持文本输入**（`request_modality: text`），不支持图像、音频、视频等多模态输入；且**不兼容 DashScope 原生协议**，必须使用 [OpenAI 兼容接口](openai-compatible-interface.md)（`/compatible-mode/v1/chat/completions`）调用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model`（请求时） | string | 必填。固定为 `auto-model-xxxx` 格式，由控制台创建路由服务时生成，代表一个已配置的路由实例 | `"auto-model-bj-20250715-abc123"` |
| `routing_strategy`（创建时） | string | 创建路由服务时指定，运行时不可修改。决定调度目标：`EFFECT_FIRST`（效果优先）或 `COST_FIRST`（成本优先） | `"EFFECT_FIRST"` |
| `input`（请求体） | object | 同标准 OpenAI Chat Completions，但 `messages` 中 content 必须为纯文本（不支持 base64 图片等） | `{"messages": [{"role":"user","content":"总结这段文字"}]}` |

- **创建方式**：需先调用 `/api/v1/deployments/model-routing/versions` 查询可用路由版本，再以 `plan=mr` 调用 `/api/v1/deployments` 创建服务；
- **调用域名**：必须使用业务空间专属域名：`https://{workspace_id}.{region}.maas.aliyuncs.com/compatible-mode/v1`；
- **响应字段**：成功响应中包含 `model`（实际被调用的底层模型 ID，如 `qwen3.8-flash`）与 `routing_info`（含 `strategy`、`selected_model`、`fallback_reason` 等调试信息），便于问题定位与效果归因。

## 面向开发者，简洁实用

- ✅ **开箱即用**：替换 `model` 字段即可接入，无需改代码逻辑、不依赖 SDK 特殊封装；
- ✅ **免运维选型**：平台自动维护模型健康度、延迟、成本数据，开发者无需手动轮询或配置 fallback；
- ✅ **可观测性强**：每个请求返回 `routing_info`，可快速验证策略生效、识别降级原因；
- ❌ **不支持运行时策略切换**：`routing_strategy` 在创建时锁定，如需调整，需新建路由服务并更新客户端 `model`；
- ❌ **不支持自定义候选模型集**：备选模型由平台预置并动态管理，开发者无法增删或排序；
- 🔍 **调试建议**：首次接入时，建议开启日志记录 `routing_info` 字段，并结合 `model-management` API 查询各候选模型的实时定价与性能指标，验证策略合理性。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model production](../api/model-production.md)
- [model management](../api/model-management.md)
- [use cases](../guides/use-cases.md)


