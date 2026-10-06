# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、功能范围及基础服务策略，是开发者集成前必查的元信息入口。它不提供实时推理能力，仅返回静态配置与策略说明。所有响应内容均以结构化 JSON 形式返回，适用于自动化校验与文档同步。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，该文档按模型类型（如 text-generation、embedding、multimodal）和上线状态（`active` / `deprecated`）分类维护。
- 功能覆盖包括：同步调用、流式响应、批量推理、[Token](../concepts/token.md) 计费模式、私有化部署兼容性标识等，具体以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中各模型的 `capabilities` 字段为准。
- 售后支持范围（如 SLA、故障响应等级、工单通道）见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)，注意该文档明确区分了公有云与专属版的服务边界。

## 关键参数

调用 `support` 接口时需传入以下可选参数：
- `model_id`（string）：指定模型 ID，用于获取单个模型的详细支持信息；若省略，则返回全局支持概览。
- `with_capabilities`（boolean，默认 `false`）：启用后返回完整能力矩阵（含输入格式、最大上下文长度、支持的 temperature 范围等）。
- `locale`（string，默认 `"zh"`）：控制返回文案语言，当前仅支持 `"zh"` 和 `"en"`。

> **注意**：[售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中关于“2 小时内响应 P1 故障”的承诺，仅适用于已签署《企业级服务协议》的客户；标准版用户适用 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中约定的通用响应时效，二者存在差异，请务必核对签约版本。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support` 端点（鉴权方式同其他 API，需携带 `Authorization: Bearer <api_key>`）：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model_id=qwen-max&with_capabilities=true" \
  -H "Authorization: Bearer sk-xxx"
```

响应示例（精简）：
```json
{
  "model_id": "qwen-max",
  "status": "active",
  "capabilities": {
    "max_input_tokens": 32768,
    "streaming": true,
    "input_types": ["text"]
  }
}
```

## 限制和注意事项

- 单 IP 每分钟限频 60 次，超出将返回 `429 Too Many Requests`。
- `model_id` 必须为 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确标注 `status: active` 的 ID；传入已下线模型将返回 `404 Not Found`。
- 接口返回的 `capabilities` 为服务端当前生效配置，**不保证与模型实际推理行为完全一致**——例如部分 embedding 模型虽声明支持 `batch_size > 1`，但实际调用时需以 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“批量调用限制”章节为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


