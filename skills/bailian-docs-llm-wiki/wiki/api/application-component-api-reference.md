# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、知识库检索、工作流编排等服务。该 API 采用 RESTful 设计，支持标准 HTTP 请求与 JSON 数据格式，适用于后端服务调用场景。开发者需通过 RAM 授权获取访问凭证，并使用指定服务接入点发起请求。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- 同步/异步文本生成（基于 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型）；
- 多轮对话管理（含历史消息上下文维护与 session 生命周期控制）；
- 内置知识库检索（需提前配置知识库 ID，支持语义匹配与片段高亮）；
- 工作流触发（通过 `workflow_id` 调用预设的可视化编排流程）。

> **注意**：部分文档中提及的 `qwen-vl` 视觉语言模型尚未在当前稳定版 API 中开放调用，实际可用模型请以 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中的 `model_list` 字段为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-max"`；必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 所列一致 |
| `input.messages` | array | 是 | 对话消息数组，每项含 `role`（`user`/`assistant`）和 `content`（string） |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`，范围 `[0.0, 1.0]` |
| `parameters.top_p` | number | 否 | 核采样阈值，默认 `0.95`，范围 `[0.0, 1.0]` |
| `parameters.max_tokens` | integer | 否 | 最大输出 token 数，默认 `1024`，上限 `4096` |

## 使用方式

1. 获取 RAM 授权凭证（AccessKey ID / Secret），参考 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)；
2. 构造请求 URL：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（具体接入点见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
4. 发送 JSON Body，示例：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求 `input.messages` 总长度不得超过 32768 个字符（含 role 和 content）；
- 免费调用量受应用配额限制，超出后返回 `429 Too Many Requests`，需检查 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的配额变更；
- 异步接口（如 `/v1/services/aigc/text-generation/async`) 返回 `task_id` 后，需轮询 `GET /v1/tasks/{task_id}` 获取结果，超时时间为 10 分钟；
- `input.messages` 中若包含 `assistant` 角色的历史回复，其 `content` 字段**不可为空字符串**，否则将触发 `400 Bad Request` —— 此约束未在 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中明确说明，但已在实际网关校验中强制执行。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


