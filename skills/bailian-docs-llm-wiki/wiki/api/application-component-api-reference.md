# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置业务能力（如对话管理、知识检索、工作流编排等）的标准接口。该 API 以 RESTful 形式提供，支持通过 AccessKey 或 STS Token 进行身份认证，并与百炼应用实例深度绑定。开发者可通过此接口实现低代码/无代码场景下的能力复用与定制化扩展。

## 支持的模型/功能

应用组件本身不直接提供大模型推理能力，而是封装了基于百炼平台已部署应用实例的**可复用业务逻辑单元**，包括但不限于：  
- 对话状态管理（`conversation` 组件）  
- 外部知识库检索（`retrieval` 组件）  
- 条件分支与[函数调用](../concepts/function-calling.md)编排（`workflow` 组件）  
- 用户意图识别与槽位填充（`nlu` 组件）  

所有可用组件均在 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中明确定义，每个组件对应独立的 endpoint 和请求 schema。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台创建的应用唯一 ID，需与授权 RAM 角色具备访问权限，详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) |
| `component_name` | string | 是 | 组件名称（如 `retrieval`, `workflow`），必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中注册名称完全一致 |
| `input` | object | 是 | 组件特定输入结构，格式由组件类型决定；例如 `retrieval` 要求 `query: string`，`workflow` 要求 `variables: object` |
| `trace_id` | string | 否 | 用于链路追踪的唯一标识，建议在分布式调用中传入 |

> **注意**：`app_id` 的权限校验逻辑在 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中描述为“仅校验存在性”，但实际自 2024-03 起已升级为强制校验 RAM 授权策略，以匹配 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 的最新要求。

## 使用方式

1. 获取服务地址：从 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取当前 Region 对应的 endpoint（如 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/components/{component_name}`）  
2. 构造 HTTP POST 请求，Header 中包含 `Authorization: Bearer <token>`（token 可通过 STS AssumeRole 或长期 AK/SK 签名生成）  
3. Body 为 JSON 格式，包含 `input` 及可选字段（如 `trace_id`）  
4. 解析响应体中的 `output` 字段获取结果；错误时检查 `code` 与 `message` 字段  

示例请求（`curl`）：
```bash
curl -X POST \
  "https://dashscope.aliyuncs.com/api/v1/apps/app-abc123/components/retrieval" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "百炼支持哪些模型？"}, "trace_id": "trc-789"}'
```

## 限制和注意事项

- 单次请求 `input` 总大小不得超过 256 KB；`output` 返回内容上限为 1 MB  
- 每个 `app_id` 下组件调用默认 QPS 限流为 10，可通过工单申请提升  
- 组件执行超时时间为 30 秒，超时后返回 `504 Gateway Timeout`  
- 所有组件均**不支持跨 region 调用**，endpoint 必须与应用部署 region 严格一致（参见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）  
- `workflow` 组件暂不支持嵌套调用其他 `workflow` 组件，该限制将在 v2.1 版本解除（见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)）

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


