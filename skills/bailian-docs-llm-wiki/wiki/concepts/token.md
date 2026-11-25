# Token 计量与消耗

Token 计量与消耗是百炼平台统一的资源计量核心机制，指对模型调用过程中实际处理的输入文本、输出文本及上下文缓存等数据单元进行标准化计数，并据此触发额度抵扣或费用结算的过程。该机制贯穿所有按量调用场景，是成本控制、预算管理、限流策略与用量监控的数据基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用按量调用（`sk-` Key）**：以千字为单位精确计量 `input_tokens` 和 `output_tokens`，费用按模型单价 × Token 数计算；免费额度、节省计划、资源包均按此 Token 总量优先抵扣；异步任务（如生图、生视频）同样按最终完成时的实际 Token 消耗出账。

- **Token Plan（`sk-sp-` Key）**：不直接按原始 Token 计费，而是以 Credits 为统一计量单位，1 Credits 对应模型特定的“加权 Token 成本”。其消耗由输入 Token、缓存 Token（命中时按折算系数计）、输出 Token、工具调用次数及模型单价共同决定，例如 `qwen3.6-plus` 单次调用可能消耗约 3.18 Credits。

- **Agent 场景（Managed Agents / Flow Agent）**：模型调用部分严格按 `token_input` / `token_output` 实际数量计费（与通用按量一致），而会话运行时、沙箱快照、知识库 RCU、记忆库操作等则属于独立计费项，不参与 Token 计量。

- **吞吐预留（TPM）与训练任务**：TPM 消耗量受 Token 长度影响（如长输入区间按阶梯系数折算），直接影响预留容量占用；模型微调训练费用则按训练阶段总 Token 量（含 prompt + target）结算。

- **监控与告警**：`TotalToken 数` 是核心可观测指标，支持配置突增告警，用于及时发现异常调用或成本风险，但监控数据本身不用于计费——计费以 [模型用量](https://bailian.console.aliyun.com/cn-beijing/model/usage) 页面和账单为准。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 注意事项 |
|------|----------|------|----------|
| `input_tokens` / `output_tokens` | 全场景通用 | API 响应中返回的实际 Token 数（含系统提示词、用户输入、模型输出） | 异步任务需查询结果接口获取；多模态模型（如 Qwen-VL）对图像 token 有专用计量逻辑 |
| `cached_tokens` | 缓存启用模型（如 `qwen3.8-max`） | 上下文缓存命中时计入的输入 Token，按固定系数（如 0.125）折算 | 折算仅影响计费金额，**不减少免费额度消耗**；需在请求头显式启用缓存（`x-dashscope-cache-enable: true`） |
| `credits_consumed` | Token Plan | 每次调用消耗的 Credits 数量，由模型 ID、输入/输出长度、工具调用等动态计算 | 无法在请求时预知，需通过 [用量页面](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/usage) 或 `/usage/summary` API 查询历史明细 |
| `session_runtime_hours` | Managed Agents | 会话处于“运行中”状态的累计时长（秒级精度），独立于 Token 计费 | 即使未触发模型调用，只要会话活跃即产生费用 |
| `tpm_consumed` | 吞吐预留 | 实际占用的每分钟 Token 数，受输入长度阶梯折算影响 | 调用 `qwen3.7-flash` 时，32K–256K 输入区间按 3× 折算，显著提升 TPM 占用 |

## 面向开发者，简洁实用

- ✅ **务必校验响应头**：所有成功响应均包含 `x-dashscope-token-count-input` 和 `x-dashscope-token-count-output`，这是最权威的 Token 消耗依据，优于客户端估算。
- ✅ **免费额度共用规则**：新人 100 万 Token 免费额度为输入+输出总额度，不区分模型或地域（仅限华北2生效），但不同模型版本（如 `qwen3.7` 与 `qwen3.7-flash`）额度独立。
- ✅ **Token Plan 开发者须知**：必须使用 `sk-sp-` Key + 配套 Base URL；调用模型内置工具（如联网搜索）自动消耗 Credits；若需调用同名 Harness 工具（如图像生成 MCP），请改用 `sk-` Key + `dashscope.aliyuncs.com`，不扣 Credits。
- ⚠️ **避免常见误用**：
  - 不要用 `sk-` Key 调 Token Plan 模型（401 错误）；
  - 不要用 `sk-sp-` Key 调通用模型或 Harness 服务（403 错误）；
  - 不要依赖客户端 tokenizer 估算 Token 数——百炼服务端 tokenizer 可能不同（尤其含 emoji、多语言、XML 标签时）；
  - 异步任务提交时不扣费，但完成时按实际 Token 结算，请确保账户余额充足。
- 🔍 **排查建议**：若 Token 消耗异常偏高，优先检查：
  - 是否启用了冗长系统提示词（system message）；
  - 是否重复上传同一文件导致多次解析计费；
  - 是否在 Flow Agent 中误将条件分支节点设为必执行；
  - 是否未启用缓存（`x-dashscope-cache-enable`）却频繁发送相似请求。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [agent billing](../guides/agent-billing.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


