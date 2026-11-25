# 智能路由

智能路由（Intelligent Routing）是百炼平台提供的动态模型分发能力，通过统一入口（`model` ID）将用户请求按预设策略自动调度至最优后端模型实例，实现模型版本灰度、A/B 测试、负载均衡、故障熔断与成本优化的统一管控。它不暴露具体部署细节，开发者仅需调用一个逻辑模型名，即可获得底层多模型协同服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型迭代与灰度发布**：在微调新版本模型（如 `qwen3-14b-suffix-ft-20241029`）完成部署后，通过智能路由创建路由策略，将 5% 流量导向新模型、95% 保留在旧模型，支持按请求特征（如 `user_id` 哈希、地域、Header 标签）或时间窗口平滑切流。
- **多模型能力融合**：针对 Qwen-MT-Uni 等全模态翻译模型，智能路由可自动识别输入类型（文本/图像/文档），并路由至对应专用子模型（如 `qwen-mt-text`, `qwen-mt-image`, `qwen-mt-doc`），对用户完全透明。
- **SLA 分级保障**：结合吞吐预留（TPM）与 Prime 模式，路由策略可优先将高优先级请求（如带 `X-Priority: high` Header）调度至已预留高速容量的 `mr` 实例，普通请求则 fallback 至按量计费的 `mu` 实例。
- **故障自愈与降级**：当某后端模型实例健康检查失败（如连续 3 次超时或错误率 >5%），智能路由自动将其从流量池剔除，并在恢复后平滑加回，无需人工干预或客户端重试。
- **跨地域/跨集群调度**：在北京与新加坡双地域部署相同语义模型时，路由策略可基于请求来源 IP 地理位置，就近调度至低延迟地域，降低网络 RTT。

> ✅ 提示：智能路由服务本身不直接提供模型推理能力，而是作为“模型网关”存在；所有后端模型必须已通过 `/api/v1/deployments` 完成部署（`plan="lora"`/`"mu"`/`"dtu"`），且状态为 `RUNNING`。

## 关键参数和配置

| 参数 | 作用 | 示例值 | 说明 |
|------|------|--------|------|
| `model`（调用时） | 路由服务对外暴露的唯一逻辑模型 ID | `"auto-model-abcd1234"` | 该 ID 由创建智能路由服务时平台分配，**不可自定义**；调用时填入此 ID 即可触发路由逻辑。 |
| `plan="mr"`（部署时） | 部署类型标识，启用智能路由能力 | `"mr"` | 必填，与其他部署方式（`lora`/`mu`/`dtu`）互斥；复用 `/api/v1/deployments` 接口。 |
| `route_model_version`（部署时） | 智能路由引擎版本号 | `"model-router-20260908"` | 创建 `mr` 服务前，需先调用 `/model-routing/versions` 查询可用版本；不同版本支持的策略语法与功能略有差异。 |
| `routing_rules`（策略配置） | JSON 格式的路由规则数组 | 见下方示例 | 通过 `/model-routing/policies` API 管理；每条规则含 `match`（匹配条件）、`backend_models`（目标模型列表）、`weight`（权重）、`fallback`（降级模型）等字段。 |
| `health_check_interval`（可选） | 后端模型健康检查周期（秒） | `30` | 默认 60 秒；建议设置为后端模型 P95 延迟的 2–3 倍，避免误判。 |

**典型路由规则示例（JSON）**：
```json
{
  "rules": [
    {
      "name": "high-priority-users",
      "match": { "headers": { "X-Priority": "^high$" } },
      "backend_models": ["qwen3-14b-dtu-prod", "qwen3-14b-mu-staging"],
      "weight": 100,
      "fallback": "qwen3-14b-mu-default"
    },
    {
      "name": "geo-based-fallback",
      "match": { "source_region": "cn-beijing" },
      "backend_models": ["qwen3-14b-mu-beijing"],
      "weight": 80,
      "fallback": "qwen3-14b-mu-singapore"
    }
  ]
}
```

## 面向开发者，简洁实用

- ✅ **快速上手三步走**：  
  1. 调用 `/model-routing/versions` 获取最新 `route_model_version`；  
  2. 用 `POST /api/v1/deployments` 创建 `mr` 服务（`plan="mr"`, `route_model_version=xxx`）→ 获取返回的 `model` 字段（即 `auto-model-xxxx`）；  
  3. 调用 `/model-routing/policies` 配置规则 → 即刻生效（无冷启动延迟）。  

- ⚠️ **关键限制**：  
  - 智能路由仅支持后付费（`charge_type="post_paid"`），不支持预付费；  
  - 后端模型必须与路由服务同地域（北京/新加坡），不支持跨地域路由；  
  - 单个路由服务最多关联 10 个后端模型，单条规则最多指定 3 个 `backend_models`；  
  - 路由决策发生在请求接入层，**不增加额外 [Token](token.md) 开销或响应延迟**（P99 < 5ms）。  

- 🔧 **调试建议**：  
  - 查看响应头 `X-Route-Backend: qwen3-14b-mu-staging` 可确认实际命中模型；  
  - 开启 `X-Debug-Route: true` 请求头，可在响应体中获取完整路由日志（含匹配规则、权重计算、健康状态）；  
  - 所有策略变更均记录审计日志，可通过 `/model-routing/audit-logs` 查询。

## 关联主题页

- [model production](../api/model-production.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model management](../api/model-management.md)
- [more about models](../api/more-about-models.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


