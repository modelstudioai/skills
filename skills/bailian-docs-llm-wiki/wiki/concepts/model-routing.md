# 智能模型路由

智能模型路由是百炼平台提供的一种动态请求分发机制，它根据预设策略（如效果优先或成本优先），在运行时自动将用户请求调度至一组兼容的备选模型中性能与业务目标最优的一个，无需开发者手动指定具体模型 ID。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用推理调用**：开发者在 OpenAI 兼容 API 的 `model` 字段中传入形如 `auto-model-cost-optimize` 或 `auto-model-quality-first` 的路由标识符，平台即在后台维护的模型池（如 `qwen3.8-flash`、`deepseek-v4-flash-0731`、`glm-5.2`）中实时匹配并转发请求，全程对上层透明。
- **结构化输出场景**：当请求中携带 `response_format`（如 JSON Schema），智能路由会自动过滤不支持该能力的备选模型；若所有候选模型均不兼容，则直接返回 400 错误，避免无效调用。
- **多模态/高阶能力协同**：结合模型元数据中的 `features`（如 `function-calling`、`cache`、`web-search`），路由引擎可按需筛选具备对应能力的模型子集，确保功能可用性与策略目标一致。
- **成本敏感型批量任务**：在 Batch 异步批处理中，智能路由默认启用「成本优先」策略，自动选择单位 Token 成本最低且满足 SLA 的模型完成批量作业，显著降低长周期任务的综合开销。

## 关键参数和配置

- **`model`（必需）**：固定值为 `auto-model-xxxx` 格式，目前支持：
  - `auto-model-cost-optimize`：优先选择当前可用、单位 Token 成本最低的模型；
  - `auto-model-quality-first`：优先选择在标准评测集上综合得分最高、响应质量最优的模型；
  - （未来扩展）`auto-model-latency-aware`：优先选择 P95 延迟最低的模型（适用于实时交互类场景）。
- **`response_format`（可选）**：声明期望的结构化响应格式。智能路由将其作为硬性约束条件参与模型筛选，不支持该参数的模型将被排除。
- **`capabilities` / `features`（隐式）**：虽不直接出现在请求体中，但路由决策依赖模型管理 API 返回的元数据（如 `capabilities=TG`、`features=structured-outputs`）。建议在模型授权阶段确保所需能力已开启。
- **无显式开关或开关参数**：智能路由由 `model` 字段值唯一触发，不依赖额外 header 或 query 参数；禁用方式即改用具体模型 ID（如 `qwen3.8-flash`）。

> ⚠️ 注意：智能路由不支持 Prime 模式、吞吐预留（TPM）、PTU/DTU 等专属资源绑定场景——这些模式要求确定性模型实例与容量保障，与动态路由机制互斥。如需兼顾路由灵活性与资源确定性，应通过模型管理 API 预先筛选出符合容量策略的子集，再构建自定义路由逻辑。

## 关联主题页

- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [more about models](../api/more-about-models.md)
- [use cases](../guides/use-cases.md)


