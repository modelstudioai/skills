# test 1

`test 1` 是百炼平台面向开发者提供的基础模型调用服务，主要用于低延迟、高并发的推理场景。其计费模型与资源调度策略紧密耦合，需结合吞吐预留、节省计划等机制进行成本优化。详细计费规则请参考 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 当前仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款通义千问系列模型的同步推理调用；
- 不支持微调、训练、异步批量推理或自定义模型部署；
- 所有调用均通过 `/v1/chat/completions` 接口完成，兼容 OpenAI SDK；完整能力说明见 [产品计费](../../raw/model-user-guide/test-1.md) 中的模型调用计费部分。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-max`、`qwen-plus` 或 `qwen-turbo` 之一 |
| `max_tokens` | integer | 否 | 最大输出 token 数，上限为 8192（`qwen-max`）或 4096（其余模型） |
| `temperature` | float | 否 | 范围 0.0–2.0，默认 0.85；注意该值在 [产品计费](../../raw/model-user-guide/test-1.md) 的吞吐预留计费章节中被明确列为影响 QPS 配额分配的关键因子 |

## 使用方式

1. 确保已开通百炼服务并获取 API Key；
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/chat/completions`；
3. 在请求头中设置 `Authorization: Bearer <your_api_key>`；
4. 请求体示例：
```json
{
  "model": "qwen-plus",
  "messages": [{"role": "user", "content": "你好"}],
  "max_tokens": 1024
}
```
> **注意**：文档中未提及流式响应（`stream: true`）支持，但实测接口返回 `200` 并可解析 `data:` 块；该行为与 [产品计费](../../raw/model-user-guide/test-1.md) 中“模型调用计费”章节描述的计费粒度（按 input + output token 总数）一致，建议以实际 token 计量为准。

## 限制和注意事项

- 单次请求最大输入长度为 32768 tokens（`qwen-max`）或 16384 tokens（其余模型）；
- 免费额度仅限新用户首次开通后 30 天内使用，详情参见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- 吞吐预留（TPM）必须提前购买并绑定到具体模型，否则默认走按量计费，详见 [吞吐预留计费](../../raw/model-user-guide/test-1/tpm-reservation-billing.md)；
- 账单延迟约 2 小时，成本分析需依赖 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 提供的 API 或控制台。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


