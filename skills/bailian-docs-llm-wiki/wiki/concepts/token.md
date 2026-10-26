# Token

Token 是百炼平台中用于计量模型调用资源消耗的最小计费与限流单位，代表模型处理的文本、图像、音频等输入/输出内容经编码后产生的基本语义单元。一个 Token 通常对应一个子词（subword）、标点、空格或特殊控制符；具体数量由模型所用分词器（Tokenizer）决定，与原始字符数无固定换算关系。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：每次 API 请求（同步 `/v1/chat/completions`、异步 `/v1/async-tasks`、批量 `/v1/batch`、流式 `stream=true`）均按实际消耗的 `input_tokens`（提示词 + 历史上下文）和 `output_tokens`（生成结果）分别计费与限流。系统在响应头（如 `X-Input-Tokens`, `X-Output-Tokens`）及响应体中返回精确数值，可用于用量分析与账单核对。

- **Token Plan 配额管理**：Token 是 Token Plan 的核心计量维度。购买的 Plan（如 Standard/Pro/Enterprise）以「千 Token」为单位授予配额，该配额在绑定的项目或 API Key 下统一扣减，支持跨模型（Qwen 系列、Qwen-VL、Qwen-Audio 等）和跨调用方式复用。Coding Plan 则独立计费，专用于代码生成类模型（如 Qwen2.5-Coder）。

- **模型训练与部署**：训练任务按训练过程中模型前向/反向计算涉及的总 Token 数（如 `n_epochs × N × (max_pixels / 压缩率) × GPU系数`）计费；部署服务（如 PTU 吞吐预留）也以 Token/分钟（TPM）为单位报价，并应用长输入阶梯系数（如 >32K 输入部分×3）和缓存折算系数（如 0.25）进行容量换算。

- **知识库（RAG）与工具调用**：Embedding 模型调用、Rerank 排序、Function Calling 中的工具描述解析等环节，其输入/输出同样按 Token 计量，纳入 `test 1` 统一计费体系，可被 AI 通用型节省计划抵扣。

- **免费额度与预算控制**：新人赠送的免费额度（如 100 万 Token）按输入+输出 Token 总和统一抵扣（仅限实时推理），不区分类型；预算管理、用量预警（≤5% 剩余配额触发通知）均基于 Token 消耗量实时统计。

## 关键参数和配置

- `input_tokens` / `output_tokens`：只读字段，由平台自动统计并返回，不可手动设置。开发者应通过 `/v1/usage` 接口或控制台「用量明细」页定期校验，避免因分词差异导致预估偏差。

- `max_tokens`：可选请求参数，用于限制生成长度。超出该值时输出将被截断，**不额外计费**；但若设为过小值导致业务异常，需自行承担重试带来的重复计费风险。

- `model`：必填参数，指定模型 ID（如 `qwen-max`）。Token 计费规则与模型强绑定——不同模型的上下文窗口、分词策略、单价均不同，直接影响 Token 消耗量与费用。

- **地域与隔离性**：Token 配额、免费额度、节省计划、吞吐预留均严格按地域（Region）隔离，华东 1 购买的资源无法在华北 2 使用；API Key 亦不可跨地域复用。

- **单次请求硬限制**：`input_tokens + output_tokens` 总和不得超过模型上下文窗口的 90%（例如 qwen-max 上下文 32768，则单次上限为 29491），超限将直接返回 `400 Bad Request`。

## 面向开发者，简洁实用

- ✅ **务必校验实际 Token 消耗**：使用 [Tokenizer 工具](https://help.aliyun.com/token-calculator) 或 SDK 的 `count_tokens()` 方法预估输入长度，避免因 prompt 过长触发截断或报错。

- ✅ **优先使用 Token Plan 绑定 Key**：相比通用 API Key，绑定 Token Plan 的 Key 具备明确配额、统一结算、团队权限继承等优势，适合生产环境。

- ✅ **流式响应仍按完整输出计费**：即使客户端提前中断 SSE 流，只要模型已生成并推送了 token，即计入 `output_tokens`。

- ❌ **不要依赖 `token_limit` 参数**：该旧版请求级硬限参数已于 v2024.06 废弃，实际生效的是账户/项目级 Token Plan 配额。

- ❌ **避免前端硬编码 API Key**：密钥泄露将导致 Token 配额被恶意耗尽，务必通过后端代理或短期临时凭证（如 STS Token）调用。

- ⚠️ **注意免费额度适用范围**：仅覆盖实时推理（`/v1/chat/completions` 等），不适用于 Batch 调用、模型训练、部署、PAI-DSW 或 OSS 存储。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)


