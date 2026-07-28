# 限流

限流是百炼平台对模型 API 调用施加的流量控制机制：按**主账号 + 模型**维度限制请求速率与 Token 吞吐，超限请求返回 429 错误。理解限流规则并做好应对，是保障线上业务稳定性的基础工程能力。

## 三类限流规则

| 类型 | 含义 | 超限错误码 |
| --- | --- | --- |
| RPM / TPM | 分钟级配额：每分钟请求数（Requests Per Minute）与 Token 数（Tokens Per Minute） | `Throttling.RateQuota`（RPM）/ `Throttling.AllocationQuota`（TPM） |
| RPS / TPS | 瞬时频率：每秒请求数与 Token 数 | `Throttling.RateQuota`（RPS）/ `Throttling.AllocationQuota`（TPS） |
| Traffic Burst | 增速限制：短时间内流量拉升过快 | `Throttling.BurstRate` |

注意维度差异：TPM 按账号维度限流，而 TPS 限流按请求维度（TPS ≈ 1 ÷ 非首包时长均值），排查时不要混淆。

## 平台各场景中的限流表现

- **接入域名**：不同域名限流待遇不同。[业务空间](workspace.md)专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）面向生产环境，支持高并发与流量隔离（SLA 99.9%）；试用域名 RPM 固定为 1000，仅适合快速验证，无 SLA。
- **免费额度**：开启「免费额度用完即停」后，额度用尽返回 403 错误 `AllocationQuota.FreeTierOnly`，属于配额停用而非速率限流，需注意区分。
- **TPM 预留**：预付费锁定专属推理容量，不与其他用户共享、不受公共限流影响。溢出策略二选一：自动溢出至按量计费（默认，业务不中断），或仅使用预留容量（超出请求直接返回 429）。
- **快速模式（Fast mode）**：采用特殊限流策略——超出 TPM 额度不立即拒绝，请求进入排队队列。
- **模型监控**：监控详情页的「错误」类指标含限流错误次数（429），可按 API-KEY、时间范围筛选，用于定位限流发生的时段与来源。

## 限流应对三层方案

按改动成本从低到高：

1. **平台配置**：
   - 服务端排队等待：请求头 `X-DashScope-Wait-Timeout`（建议 3~120 秒），仅对 `Throttling.BurstRate` 生效；同时需上调客户端超时（非流式：原超时 + Wait-Timeout 值）。
   - 申请提升限流额度、购买 PTU 专属部署，或将离线任务迁移到 Batch API。
2. **客户端流控**：从基础重试（指数退避）、令牌桶 / 并发信号量，到双重令牌桶 / 平滑限速器、自适应拥塞控制，按工程复杂度递进选择。
3. **架构兜底**：模型降级（Fallback 到备用模型）与基于消息队列的削峰填谷。

## 容量类方案选型

- 流量可预估、不能接受限流 → **TPM 预留**（按 kTPM 预付费、按天计费，创建后用专属模型 code 替换 `model` 参数即可）。
- 追求更高吞吐与性能确定性 → **PTU 专属部署**。
- 流量波动大或短期使用 → 维持按量付费，叠加客户端流控与重试；可用资源包 / 节省计划优化费用。

> 提示：即使使用 TPM 预留，短时间内请求量快速拉升时系统仍需短暂预热，预热期间部分请求可能出现延迟波动，建议保留请求排队或重试机制。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [use cases](../guides/use-cases.md)
- [model monitoring](../guides/model-monitoring.md)


