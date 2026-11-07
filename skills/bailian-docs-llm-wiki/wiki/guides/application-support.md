# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的通用服务支持能力，涵盖模型接入、参数配置、请求调度与基础运维保障。它不直接提供模型推理能力，而是作为上层应用与底层模型服务之间的协调层，确保调用链路的稳定性与可配置性。开发者需结合具体模型文档和业务场景合理使用该支持机制。

## 支持的模型/功能

`application support` 本身不绑定特定模型，但当前兼容所有已接入百炼平台的 [通义千问系列模型](../../raw/application-user-guide/application-support.md)（如 qwen-max、qwen-plus、qwen-turbo）及部分第三方模型（需通过白名单开通）。其核心功能包括：请求路由分发、多模型负载均衡、基础鉴权透传、调用日志聚合与错误码标准化。注意：对 [Qwen2-VL 等多模态模型](../../raw/application-user-guide/application-support.md) 的图像输入支持仍处于灰度阶段，详见对应模型文档。

## 关键参数

调用时需在 `X-Application-Context` 请求头中传递以下必需字段（JSON 格式）：

- `app_id`: 应用唯一标识（由控制台生成）
- `env`: 环境标识（`prod` / `staging` / `dev`）
- `timeout_ms`: 全局超时（单位毫秒，建议 30000–120000）

此外，`application support` 会自动注入 `x-bailian-trace-id` 和 `x-bailian-app-version`，用于链路追踪与版本治理。详细参数说明见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md) 中的“调用上下文规范”章节。

## 使用方式

1. 在应用控制台开通 `application support` 服务并获取 `app_id`
2. 构造 HTTP POST 请求至 `/v1/application/invoke` 端点
3. 设置 `Content-Type: application/json` 与 `X-Application-Context` 头部
4. 请求体结构与目标模型原生 API 保持一致（例如调用 qwen-max 时，body 格式同 [qwen-max 接口文档](../../raw/application-user-guide/application-support.md)）

> **注意**：原始文档中提到的 `/v1/app/invoke` 路径已废弃，当前仅支持 `/v1/application/invoke`；请以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的最新接口清单为准。

## 限制和注意事项

- 单次请求最大 payload 为 8MB（含 base64 图像等二进制内容）
- 每 `app_id` 默认 QPS 限流为 50，可通过工单提报扩容
- 不支持跨 region 调用（例如 `app_id` 在 cn-shanghai 注册，不可调用 us-west-1 的模型实例）
- 错误响应中 `error.code` 字段遵循统一标准，但部分旧模型返回的 `error.type` 与 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 中定义存在偏差，建议以 `error.code` 为主进行重试判断

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


