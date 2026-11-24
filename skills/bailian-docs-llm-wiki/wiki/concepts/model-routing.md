# 模型路由

模型路由（Model Routing）是百炼平台提供的智能流量分发能力，允许开发者将单次推理请求动态分发至多个候选模型中的最优一个，依据预设策略（如效果优先或成本优先）自动决策，无需应用层硬编码模型选择逻辑。

## 在百炼平台的不同场景中，这个概念如何使用

- **生产环境模型灰度与AB测试**：通过创建路由规则，将 10% 流量导向新微调模型（如 `qwen3.8-flash-ft-v2`），90% 留给基线模型（如 `qwen3.7-plus`），支持按版本、权重、标签等维度灵活配置。
- **效果与成本平衡调度**：在 `plan=mr` 的部署中启用路由，当请求携带 `strategy=EFFECT_FIRST` 时，平台自动选择历史 SLO（如 P95 延迟 ≤800ms、准确率 ≥92%）表现最优的模型；设为 `COST_FIRST` 则优先选择单位 token 成本最低且满足基础可用性（如成功率 >99.5%）的模型。
- **CLI 快速管理**：使用 `bl deploy router create` 命令一键创建路由实例，并通过 `bl deploy router update` 动态调整候选模型列表或策略，适用于 CI/CD 流水线中的模型迭代发布。
- **地域与计费约束**：当前仅支持华北2（北京）与新加坡地域，且**必须使用后付费模式**（`charge_type="post_paid"`）；不支持与 DTU（吞吐预留）或预付费资源绑定。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plan` | string | 是 | 固定值 `"mr"`，标识该部署类型为模型路由 |
| `strategy` | string | 是 | 路由策略，取值为 `"EFFECT_FIRST"`（效果优先）或 `"COST_FIRST"`（成本优先） |
| `candidates` | array of string | 是 | 候选模型 ID 列表，如 `["qwen3.8-max", "qwen3.8-plus", "qwen3.7-plus"]`；最多支持 5 个模型，需均已部署并处于 `RUNNING` 状态 |
| `weights` | array of number | 否 | 显式指定各候选模型的静态权重（如 `[30, 50, 20]`），若提供则忽略 `strategy`，启用加权轮询；未提供时按策略动态决策 |
| `name` | string | 是 | 路由实例唯一名称，符合 DNS 子域名规范（小写字母、数字、连字符，长度 1–63 字符） |

> ✅ 提示：路由本身不消耗独立算力资源，其开销由所选目标模型承担；调用时使用路由的 `deployment_id`（而非具体模型名）作为 `model` 参数，例如：  
> ```python
> client.chat.completions.create(model="my-router-deployment-id", messages=[...])
> ```

## 面向开发者，简洁实用

- 创建即生效：路由部署后，所有指向该 `deployment_id` 的请求立即按策略分发，无冷启动延迟。
- 无侵入集成：应用代码无需修改，只需将原模型名替换为路由部署 ID 即可接入。
- 可观测性强：控制台与 API 均提供实时路由分布统计（各模型调用量、平均延迟、错误率），支持按小时粒度导出分析。
- 安全隔离：路由实例归属业务空间，仅本空间内 API Key 可调用；删除路由不影响底层候选模型状态。
- 注意事项：路由不支持流式响应的细粒度中断控制（如中途切换模型），全程绑定首次选定的模型执行到底；如需强一致性，请避免在单次请求中混用路由与直连模型。

## 关联主题页

- [model production](../api/model-production.md)
- [changelog group](../guides/changelog-group.md)
- [preparations](../api/preparations.md)
- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)


