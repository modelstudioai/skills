# Token

Token 是百炼平台中用于计量模型输入与输出文本长度的基本单位，也是资源配额、计费、限流与监控的核心度量基准。1 个 Token 通常对应一个子词（subword）或标点符号，具体切分由模型底层 tokenizer 决定（如 Qwen 系列使用 QwenTokenizer），而非简单按字符或字数计算。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与配额控制**：所有同步/异步模型请求（如 `/v1/chat/completions`、`/v1/coding/completions`）均按实际消耗的 **Input Tokens + Output Tokens** 总和计费与扣减配额。Token Plan（如 `personal`/`team`/`coding`）直接约束该总量，超出即触发截断（返回 `truncated: true`）或拒绝（403/429）。
  
- **API 请求参数约束**：`max_tokens` 显式限制生成长度（Output Tokens 上限）；`input.messages` 的总长度受模型上下文窗口限制（如 `qwen-plus` 最大 `max_context_length = 32768`，含 system/user/assistant 所有 tokens）；超长输入将被服务端静默截断或报错。

- **流式响应计费**：启用 `stream: true` 时，Token 按实际逐 chunk 返回的 tokens 累计计费，非预估值；首 Token 延迟（Time to First Token）和总延迟均以 token 级粒度监控。

- **用量监控与告警**：模型监控系统提供 `TotalToken` 指标（分钟级聚合），支持按 API Key、模型、时间精度筛选，可用于成本审计与异常告警（例如“1 分钟内 TotalToken > 10000”）。

- **文件多模态调用**：上传图片/音频等本地文件获取临时 URL 时，需指定 `model` 参数；该 model 必须与后续调用一致，否则因 tokenizer 不匹配导致 token 计算错误或调用失败。

- **临时凭证与子空间隔离**：临时 API Key、子业务空间调用均继承源账号的 token 配额与计费归属，Token 消耗始终绑定到发起调用的 API Key 所属主体（个人账号或组织席位）。

## 关键参数和配置

| 参数 | 作用 | 注意事项 |
|------|------|----------|
| `max_tokens` | 控制模型最多生成的 Output Tokens 数量 | 默认 1024，最大 8192；受所选 `plan` 总配额限制，超限将被截断；流式响应中实际返回数可能略低于该值 |
| `plan` | 显式声明 Token Plan 类型（必填） | 取值为 `personal` / `team` / `coding`（大小写敏感）；必须与 `model` 兼容（如 `qwen-max` 不支持 `personal`）；不共享配额，切换 plan 后历史消耗不累计 |
| `input.messages` | 包含所有角色消息的数组，其总 token 数计入 Input Tokens | 单次请求总 tokens ≤ 模型 `max_context_length`（可通过 `/models/{model_id}` 接口查询）；system [prompt](../guides/prompt.md) 也计入 token |
| `stream` | 是否启用流式响应 | `true` 时 token 按实际返回量实时计费；建议预留约 10% 余量应对服务端缓冲策略影响 |

> ⚠️ 重要提示：  
> - Token 计算以服务端 tokenizer 实际切分为准，开发者应使用百炼官方 SDK（如 `dashscope` Python SDK）的 `count_tokens()` 工具函数预估，避免自行按字符估算；  
> - 所有 token 配额按自然日 UTC+0 00:00 重置，非北京时间；  
> - 审计日志中记录的 `input_tokens` 和 `output_tokens` 字段为最终计费依据，可用于对账。

## 面向开发者，简洁实用

- ✅ **快速验证 token 消耗**：调用后检查响应头 `X-DashScope-Usage`（JSON 格式），含 `"input_tokens"` 和 `"output_tokens"` 字段；  
- ✅ **预估输入长度**：Python SDK 中 `dashscope.get_tokenizer(model='qwen-plus').count_tokens(messages)`；  
- ✅ **避免配额超限**：生产环境务必显式传入 `plan`，并监听响应中的 `truncated` 字段；  
- ✅ **排查 token 相关错误**：403（plan/model 不匹配）、429（配额耗尽）、400（missing plan）、截断响应（`truncated:true`）均与 token 管理强相关；  
- ❌ **不要假设**：不同模型 tokenizer 结果不同（如 `qwen-turbo` 与 `qwen-vl` token 数不可直接换算）；token 数 ≠ 字符数 ≠ 中文词语数。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [get started with models](../guides/get-started-with-models.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


