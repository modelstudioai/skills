# application [support](support.md)

`application support` 是百炼平台为应用层调用提供的基础服务支持能力，涵盖模型接入、参数配置、请求调度与错误处理等核心环节。它面向开发者提供统一的 API 接口抽象和标准化的运行时保障，适用于构建对话、文本生成、结构化提取等各类 AI 应用场景。该能力依赖平台底层模型服务与资源调度系统协同工作，需配合正确的参数与调用方式使用。

## 支持的模型/功能

- 支持调用百炼平台托管的全部大语言模型（如 Qwen 系列、Qwen2、Qwen3）及多模态模型（如 Qwen-VL），具体以 [服务支持](../../raw/application-user-guide/application-support.md) 中列出的可用模型列表为准；  
- 提供同步推理（`/v1/chat/completions`）、流式响应（`stream=true`）、[函数调用](../concepts/function-calling.md)（`tools` 参数）和 JSON Schema 输出约束等标准 OpenAI 兼容功能；  
- 支持通过 `model` 字段指定模型别名（如 `qwen-max`、`qwen-plus`），平台自动路由至对应实例，详见 [服务支持](../../raw/application-user-guide/application-support.md) 的“模型映射规则”章节。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型唯一标识符，必须为平台已开通的模型别名，不可使用原始模型路径；不支持动态切换未授权模型，参见 [服务支持](../../raw/application-user-guide/application-support.md) 中的权限说明 |
| `temperature` | number | 否 | 控制输出随机性，取值范围 `[0.0, 2.0]`，默认 `0.7`；设为 `0` 时启用确定性采样（greedy decode） |
| `max_tokens` | integer | 否 | 最大生成 token 数，上限受模型上下文窗口限制（如 `qwen-max` 为 32768） |
| `top_p` | number | 否 | 核采样阈值，范围 `[0.0, 1.0]`，默认 `1.0` |

> **注意**：原始文档中提及的 `repetition_penalty` 默认值为 `1.0`，但当前 v3.2+ 版本实际默认值为 `1.1`，以平台最新 API 文档为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`；  
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/chat/completions`；  
3. **请求体示例**：
   ```json
   {
     "model": "qwen-max",
     "messages": [{"role": "user", "content": "你好"}],
     "temperature": 0.5,
     "stream": false
   }
   ```
4. 成功响应返回 `200 OK`，含 `choices[0].message.content` 字段；流式响应按 SSE 协议分块传输。

## 限制和注意事项

- 单次请求最大 `input + output` tokens 总和不得超过所选模型的上下文长度（例如 `qwen-plus` 为 131072 tokens），超出将返回 `400 Bad Request`；  
- 免费试用额度仅限首次开通账号的前 7 天，后续需绑定支付方式并开通按量计费，详情见 [售后说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)；  
- 不支持跨区域调用（如华东地域 API Key 不可用于华北节点），且 `model` 字段不接受自定义模型路径或 HuggingFace 模型 ID；  
- 错误码 `503 Service Unavailable` 通常表示模型实例未就绪或资源配额耗尽，建议检查 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的扩容指引。

## 来源文档

- [服务支持](../../raw/application-user-guide/application-support.md)


