# model monitoring

model monitoring 是百炼平台提供的模型调用行为与性能指标观测能力，用于追踪请求量、延迟、错误率等核心运行时指标，支持问题定位与容量规划。该功能面向已部署的 API 模型（包括通义千问系列、文本嵌入、[多模态](../concepts/multi-modal.md)等），无需额外埋点即可自动采集。监控数据默认保留 30 天，可通过控制台或 OpenAPI 查询。

## 支持的模型/功能

- 支持所有通过百炼平台 **API 部署模式**发布的模型（含 `qwen-max`、`qwen-plus`、`text-embedding-v1`、`wanx` 等），不支持直接调用公网地址的第三方模型或本地自托管模型。  
- 提供两类核心监控能力：**用量统计**（如日/小时请求数、[Token](../concepts/token.md) 消耗量）和 **性能监控**（如 P95 延迟、HTTP 状态码分布、失败原因分类）。  
- 告警能力依赖 [监控告警](https://help.aliyun.com/zh/model-studio/model-telemetry) 配置，需在控制台中为具体模型服务单独开启；相关配置说明详见 [原文标题](../../raw/model-user-guide/model-monitoring.md)。

## 关键参数

- `service_id`：必填，对应模型服务唯一标识（非模型 ID），可在服务详情页 URL 或 `GET /v1/services` 接口响应中获取。  
- `start_time` / `end_time`：时间范围查询参数，精度支持到秒，最大跨度为 7 天（单次查询）。  
- `metrics`：可选值包括 `request_count`、`token_usage`、`latency_p95`、`error_rate`；复合指标（如 `token_per_request`）需自行计算。  
- 所有指标均按 `service_id + region + timestamp` 维度聚合，不支持按用户 ID 或 request_id 下钻 —— 此限制在 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中未明确说明，但实测 API 返回无相关字段。

## 使用方式

1. **控制台查看**：进入「模型服务」→ 选择目标服务 → 「监控」页签，可切换时间粒度（1m/5m/1h）与指标类型。  
2. **OpenAPI 查询**：调用 `GET /v1/services/{service_id}/metrics`，需携带 `Authorization` 和 `X-Region-Id` 请求头；完整参数与示例见 [原文标题](../../raw/model-user-guide/model-monitoring.md)。  
3. **告警配置**：在「监控告警」页面新建规则，绑定 service_id 后设置阈值（如 `latency_p95 > 3000ms` 持续 5 分钟），支持钉钉/邮件通知。

## 限制和注意事项

- 单个 service_id 的监控数据延迟 ≤ 2 分钟，不适用于实时风控类场景。  
- [Token](../concepts/token.md) 统计仅覆盖模型输入输出文本，**不包含图像/音频等二进制载荷的编码开销**（如 base64 字符数），此细节在 [原文标题](../../raw/model-user-guide/model-monitoring.md) 中未体现，需开发者自行预估带宽成本。  
> **注意**：文档中链接指向 help.aliyun.com 的外部页面，其内容可能与百炼控制台最新 UI 不一致（例如「监控」页签位置已从左侧导航栏移至服务详情内嵌卡片），建议以控制台实际路径为准。  
- 免费版实例仅保留最近 7 天监控数据，且不支持自定义告警；升级专业版后解锁全部功能。

## 来源文档

- [用量统计与性能监控](../../raw/model-user-guide/model-monitoring.md)



