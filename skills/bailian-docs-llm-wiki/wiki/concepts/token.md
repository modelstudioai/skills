# Token

Token 是百炼平台对模型输入与输出内容进行细粒度计量和计费的基本单位，表示模型在处理文本（或结构化内容）时实际消耗的语言单元。一个 Token 通常对应一个词、子词（subword）或标点符号；具体切分方式由模型自身的 tokenizer 决定，开发者无需手动分词，但需理解其对配额、限流和费用的影响。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用计量**：每次请求的 `input.messages`（含 system/user/assistant 角色内容）和响应中的 `output.text` 或流式 `delta.content` 均按实际生成的 Token 数精确统计。例如调用 `qwen-max` 模型处理一段 500 字中文+300 字英文的 prompt，再生成 200 字回答，总消耗 ≈ 输入 Token + 输出 Token（具体数值可通过响应头 `X-DashScope-Usage` 或 `/v1/token-plans/{id}/usage` 接口实时查询）。

- **配额与限流控制**：  
  - **TPM（Tokens Per Minute）**：用于吞吐预留（PTU）和动态限流，限制每分钟最大 token 处理量；  
  - **Token Plan**：以「总 token 配额 + 重置周期」形式实现团队/项目级用量管控，超限请求将返回 `429 Too Many Requests`；  
  - **单次请求上限**：各模型有硬性输入 token 上限（如 `qwen-max`: 32,768；`qwen-turbo`: 8,192），超出直接返回 `400 Bad Request`。

- **计费核心依据**：  
  - 所有模型服务（推理、Batch、训练、部署）均以「输入 Token + 输出 Token」为计费基础；  
  - 长文本、缓存命中、特殊模式（如 `flash` 系列）会应用阶梯系数（如 3×）或折算系数（如缓存 0.25×），详见计费文档；  
  - 免费额度、资源包、节省计划均按 token 消耗量逐笔抵扣。

- **开发调试关键指标**：  
  - 流式响应中每个 `delta.content` 的 token 数累加即为本次响应总输出 token；  
  - 响应头 `X-DashScope-Usage: {"input_tokens":123,"output_tokens":45}` 提供即时用量反馈，建议日志中采集该字段用于成本归因。

## 关键参数和配置

- **无显式 Token 参数**：开发者不直接设置 token 数，但必须关注以下关联参数：
  - `input.messages` 内容长度：直接影响输入 token 消耗，长 prompt 易触发限流或超限；
  - `max_output_tokens`（可选）：显式限制模型最大生成长度，避免意外高 token 输出；
  - `stream: true`：启用流式后，token 计费仍以最终完整输出为准，**不预占、不估算**；
  - `token_plan_id`（请求头或模型实例绑定）：指定 token 消耗归属的配额计划，决定是否受控于 daily/weekly quota。

- **配额类配置（通过 Token Plan API 管理）**：
  | 字段 | 说明 |
  |------|------|
  | `quota` | 整数，每日/每周/每月总 token 配额（最小 1000） |
  | `reset_cycle` | `"daily"`（默认）、`"weekly"` 或 `"monthly"`，按自然日（UTC+8）重置 |
  | `model_ids` | 绑定的模型 ID 列表（如 `["qwen-plus", "qwen-vl"]`），空则绑定账号下所有授权模型 |

## 面向开发者，简洁实用

- ✅ **必查**：调用前用 [模型规格页](https://help.aliyun.com/zh/model-studio/model-list) 确认目标模型的 `max_input_tokens` 和计费系数；  
- ✅ **必监**：生产环境务必开启 Token Plan 并配置 `enable_alert`，避免突发流量导致超限中断；  
- ✅ **必验**：本地调试时，在响应头解析 `X-DashScope-Usage`，验证实际 token 消耗是否符合预期；  
- ❌ **勿硬编码**：Token Plan ID 和 API Key 同属敏感配置，须通过环境变量或密钥管理服务注入；  
- ⚠️ **注意边界**：`qwen3.8-max-prime` 等带 `-prime` 后缀的模型不享受新人免费额度，token 消耗将直接计费。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [preparations](../api/preparations.md)


