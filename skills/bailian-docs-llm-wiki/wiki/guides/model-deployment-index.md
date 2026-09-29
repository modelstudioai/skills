# model deployment index

模型部署是百炼平台为用户提供模型服务化的核心能力，支持多种部署模式以适配不同业务场景下的性能、成本与隔离性需求。本文档系统梳理了当前平台支持的部署方式、关键配置参数、调用方法及使用约束，便于开发者快速选型与集成。所有部署方案均通过统一 API 接口调用，但底层资源模型与计费逻辑存在显著差异。

## 支持的模型与功能

百炼平台当前支持以下部署类型：
- **专属部署**：为单个模型实例分配独立计算资源，适用于对延迟、稳定性或数据隔离有强要求的生产场景；详情见 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。
- **PTU 预置吞吐部署**：基于预购 PTU（Processing Token Unit）保障长上下文与缓存命中率，适合高并发、中低延迟推理；参考 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。
- **DTU 独占算力部署**：按 GPU 卡粒度独占物理资源，支持自定义镜像与 CUDA 版本，适用于需深度定制或兼容特定框架的模型；详见 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md)。
- **Token 按量部署**：无预付费、按实际 token 数计费，适合流量波动大或验证阶段的轻量应用；参见 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。
- **智能路由**：自动将请求分发至最优可用模型实例（含多版本、多部署策略），支持灰度发布与故障熔断；说明见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md)。

> **注意**：`模型导入`（[模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md)）文档中提及的“支持 Hugging Face 格式本地上传”功能，已于 v2.3.0 版本起仅限 DTU 部署场景使用；专属部署与 PTU 部署暂不支持直接导入第三方模型权重，需先通过百炼官方模型中心申请接入。

## 关键参数

| 参数名 | 说明 | 取值范围/示例 | 是否必需 |
|--------|------|----------------|----------|
| `model_id` | 百炼平台内唯一模型标识符（如 `qwen-max-20240610`） | 字符串，由平台分配 | 是 |
| `deployment_type` | 部署策略类型 | `dedicated` / `ptu` / `dtu` / `token` / `routing` | 是 |
| `ptu_count` | PTU 预置数量（仅 `ptu` 类型生效） | 正整数，如 `100` | 否（`ptu` 类型下必需） |
| `gpu_count` | GPU 卡数（仅 `dtu` 类型生效） | `1`, `2`, `4`, `8` | 否（`dtu` 类型下必需） |
| `routing_policy` | 路由策略（仅 `routing` 类型生效） | `latency_optimized`, `cost_optimized`, `version_weighted` | 否 |

## 使用方式

1. **创建部署实例**：通过控制台「模型部署」页或 OpenAPI `POST /v1/deployments` 提交配置；
2. **获取 endpoint**：部署成功后，返回 `endpoint_url`（格式为 `https://<region>.api.bailian.aliyuncs.com/v1/models/<model_id>:predict`）；
3. **调用 API**：向 endpoint 发送标准 OpenAI 兼容请求（`POST` + `application/json`），需携带 `Authorization: Bearer <api_key>`；
4. **管理生命周期**：支持通过控制台或 `DELETE /v1/deployments/{deployment_id}` 下线实例；[API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 提供完整 cURL 示例与错误码说明。

## 限制和注意事项

- 所有部署类型均**不支持跨地域访问**，endpoint 仅在创建时指定的 Region 内可达；
- `token` 类型部署最大请求长度为 32k tokens，`ptu` 和 `dtu` 类型默认支持 128k，但需模型本身具备长上下文能力；
- 专属部署与 DTU 部署实例启动耗时约 5–15 分钟，PTU 与 Token 类型为秒级就绪；
- 已部署的模型不可变更 `deployment_type`，如需切换，须先删除原实例再新建；
- [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 页面中显示的“已部署状态”可能有最多 30 秒延迟，建议以 API 查询 `GET /v1/deployments/{id}` 返回的 `status` 字段为准。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-index.md)


