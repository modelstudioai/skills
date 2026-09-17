# test 1

test 1 是百炼平台面向开发者提供的基础模型服务入口，支持按调用次数与资源消耗进行细粒度计费。其核心能力覆盖模型推理、训练及部署全链路，适用于原型验证与中小规模生产场景。计费策略透明，提供新人免费额度与资源包等成本优化机制，详情见 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通义千问系列模型的同步/异步推理；
- 提供微调（Fine-tuning）与专属模型部署能力，支持 LoRA 与全参数微调两种模式；
- 内置 [Prompt 工程](../concepts/prompt-engineering.md)调试控制台与批量测试工具，便于快速验证效果。  
完整能力矩阵请参考 [产品计费](../../raw/model-user-guide/test-1.md) 中关联的子文档，例如 [模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md) 明确列出了各模型的输入/输出 token 单价。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-turbo`；必须与 [模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md) 中公示的可用模型一致 |
| `input` | string / object | 是 | 输入文本或结构化 [prompt](prompt.md)；最大长度受模型上下文窗口限制（如 `qwen-turbo` 为 8K tokens） |
| `max_tokens` | integer | 否 | 生成内容最大 token 数，默认 1024，上限 4096 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false` |

> **注意**：`temperature` 和 `top_p` 参数在 [模型调用计费](../../raw/model-user-guide/test-1/model-pricing.md) 中未作行为约束说明，但实际 API 调用中若超出平台允许范围（如 `temperature > 2.0`），将返回 `400 Bad Request` —— 此处以运行时行为为准，文档需后续同步更新。

## 使用方式

1. 通过 REST API 调用：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-turbo",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"max_tokens": 512}
         }'
   ```
2. SDK 调用（Python 示例）：  
   ```python
   from dashscope import Generation
   resp = Generation.call(model='qwen-turbo', input={'messages': [{'role': 'user', 'content': '你好'}]})
   ```
3. 控制台调试：登录百炼控制台 → 进入「模型服务」→ 选择 test 1 → 使用在线 Playground 测试。所有计费项均实时关联至主账号，账单明细可于 [账单查询与成本管理](../../raw/model-user-guide/test-1/bill-query-and-cost-management.md) 查看。

## 限制和注意事项

- 单次请求 `input` + `output` 总 token 数不得超过模型上下文长度（如 `qwen-plus` 为 32K）；
- 免费额度仅限新注册用户首次开通后 30 天内使用，具体规则详见 [新人免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)；
- 微调任务需预充值，且不享受免费额度抵扣；训练实例规格与存储配额受项目级资源限制约束；
- 所有调用均计入账号总用量，跨区域调用（如华东1调用华北2部署的模型）可能产生额外网络费用，该细节在 [产品计费](../../raw/model-user-guide/test-1.md) 的子文档中尚未明确说明，建议优先同地域部署。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


