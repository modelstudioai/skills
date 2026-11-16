# 智能模型路由

智能模型路由（Intelligent Model Routing）是百炼平台提供的动态模型调度能力，它基于请求内容、实时负载、模型性能与成本策略，在预配置的多个候选模型间自动选择最优模型执行推理，无需客户端修改调用逻辑。该能力在保障服务质量（如延迟、准确率）的同时，实现单位 Token 成本的帕累托优化。

## 在百炼平台的不同场景中如何使用

- **效果优先场景**：适用于对生成质量敏感的业务（如客服对话摘要、法律文书生成）。路由系统根据请求语义复杂度、上下文长度、输出要求等特征，自动匹配高能力模型（如 `qwen3.8-max` 或 `kimi-k3`），并在必要时降级至次优模型以保障可用性。
- **成本敏感场景**：适用于批量处理、内部工具等对响应速度容忍度较高的任务。系统按预设成本权重，优先调度轻量高效模型（如 `qwen3.8-flash` 或 `glm-5.2`），显著降低 Token 单价，同时维持可接受的效果下限。
- **忙闲分时调度**：支持结合时段（如工作日 9:00–18:00）与地域负载状态，自动切换主备模型池。例如高峰时段启用高吞吐模型，非高峰时段切至低成本模型，实现资源弹性复用。
- **灰度发布与A/B测试**：开发者可将新微调模型或第三方模型加入路由池，通过流量比例控制曝光范围，结合效果指标（如人工评分、自动评估分数）快速验证模型迭代收益。
- **多模态任务兜底**：当前仅支持文本生成类模型（TG 能力），但可作为统一入口接入，后续将扩展至支持具备相同输入/输出 Schema 的多模态模型（如图文理解→文本生成链路）。

> ✅ 注意：智能路由仅支持后付费（`charge_type="post_paid"`），且**仅在北京（华北2）与新加坡（ap-southeast-1）地域可用**；不支持 LoRA 微调模型直连路由池，需先部署为独立服务再纳入调度。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model` | string | 是 | 路由实例唯一标识，固定格式为 `auto-model-{8位随机字符}`（由平台分配，不可自定义） | `"auto-model-7f3a9b2c"` |
| `routing_strategy` | string | 否 | 调度策略：`effectiveness_first`（默认，效果优先）或 `cost_first`（成本优先） | `"cost_first"` |
| `candidate_models` | array of string | 是 | 预设的候选模型 ID 列表，至少 2 个，须为平台已开通且支持路由的文本生成模型 | `["qwen3.8-flash", "glm-5.2", "kimi-k3"]` |
| `fallback_model` | string | 否 | 当所有候选模型不可用时的兜底模型（必须在 `candidate_models` 中） | `"qwen3.8-flash"` |
| `enable_thinking` | boolean | 否 | 是否对支持思考模式的模型启用 `reasoning_content` 输出（仅影响部分模型行为） | `true` |

- **创建方式**：通过 `/api/v1/deployments` 接口调用，`plan="mr"`，`charge_type="post_paid"`，其余参数按上表填写。
- **调用方式**：与标准 [OpenAI 兼容接口](openai-compatible-interface.md)完全一致，只需将 `model` 字段替换为路由实例 ID，其余参数（`messages`, `stream`, `temperature` 等）保持不变。
- **监控与调试**：调用响应头中返回 `X-Bailian-Routed-Model: qwen3.8-flash`，明确本次实际执行模型；可通过控制台「模型路由监控」查看各候选模型的调用量、平均延迟、成功率及路由决策分布。

## 面向开发者：简洁实用提示

- ✅ **起步最快**：在控制台「模型部署」页选择「智能路由」模板，勾选 2–4 个文本模型，点击创建，5 秒获取 `auto-model-xxxx` 实例 ID，直接用于现有 API 请求。
- ⚠️ **避坑提醒**：
  - 不要手动构造 `model` 值——`auto-model-*` 必须由平台生成，硬编码将返回 `InvalidModel` 错误；
  - 路由池中所有模型必须在同一地域开通 `inference` 权限，否则部署失败；
  - `stream=true` 下，`delta.reasoning_content` 等非标字段行为与所选实际模型一致，无需额外适配。
- 📈 **优化建议**：
  - 初始配置推荐 `effectiveness_first` + 3 个模型（1 个高性能 + 1 个均衡型 + 1 个低成本）；
  - 结合业务日志分析 `X-Bailian-Routed-Model` 分布，若某模型长期未被选中，可移出池子或调整策略权重；
  - 成本敏感场景可搭配 PTU（预置吞吐）为路由实例单独预留容量，避免公共队列排队影响 SLA。

## 关联主题页

- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [more about models](../api/more-about-models.md)
- [use cases](../guides/use-cases.md)


