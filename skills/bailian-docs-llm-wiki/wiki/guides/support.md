# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、功能范围及基础服务策略，是开发者集成前必查的元信息入口。该接口不执行推理，仅返回结构化元数据，适用于运行时动态适配模型选型与权限校验。所有响应字段均以 JSON 格式返回，符合 OpenAPI v3 规范。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖 Qwen 系列（如 qwen-max、qwen-plus）、开源微调模型及部分第三方托管模型。
- 功能覆盖文本生成、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、多轮对话上下文管理，但**不支持图像输入、语音转写或实时音视频流处理**。
- 模型能力标识（如 `supports_streaming: true` 或 `supports_tools: true`）直接映射至 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `capabilities` 字段，开发者应以该文档为准进行能力判断。

## 关键参数

- `model`: 必填，字符串，取值必须来自 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `model_id` 字段。
- `with_capabilities`: 可选布尔值，默认 `false`；设为 `true` 时返回模型细粒度能力（如 token 限制、最大上下文长度、工具调用支持状态）。
- `region`: 可选，指定服务地域（如 `cn-beijing`），影响可用模型集合；若未指定，返回全局默认区域支持的模型。

## 使用方式

通过 HTTP GET 请求访问 `https://dashscope.aliyuncs.com/api/v1/support`，需携带有效的 `Authorization: Bearer <api_key>` 头。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model=qwen-max&with_capabilities=true" \
  -H "Authorization: Bearer sk-xxx"
```

> **注意**：原始文档中 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 提到“支持 7×24 小时工单响应”，但该描述与当前 SLA 协议（见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)）中定义的“工作日 5×8 小时响应”存在冲突；请以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 的正式条款为准。

## 限制和注意事项

- 单 IP 每分钟限频 60 次，超限返回 `429 Too Many Requests`。
- `model` 参数不校验是否存在——若传入无效 model_id，接口仍返回 200，但 `supported` 字段为 `false`，需主动检查响应体中的 `supported` 和 `error` 字段。
- 不支持跨区域批量查询；如需获取多 region 支持情况，须分别调用并合并结果。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


