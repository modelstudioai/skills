# token plan best practice

[Token](../concepts/token.md) Plan 是百炼平台用于精细化控制模型调用资源消耗的核心机制，适用于多模态模型接入与混合推理场景。合理配置 [Token](../concepts/token.md) Plan 可避免意外超限、提升成本可控性，并保障服务稳定性。本文汇总关键实践要点，覆盖模型支持范围、参数含义、调用方式及常见约束。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持以下模型类型及其对应能力：
- 文本生成类：Qwen 系列（含 Qwen1.5、Qwen2、Qwen2.5）、Baichuan、GLM 等主流大语言模型  
- 多模态理解类：Qwen-VL、Qwen2-VL（需配合 `add-vision-skill.md` 中定义的视觉解析流程）  
- 生成类：图像生成（Stable Diffusion 兼容接口）、视频生成（SVD）、语音合成（TTS）、语音识别（ASR）、实时语音对话（RTVC）  
- 决策类：规则引擎增强型决策模型（参见 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice.md)）  

> **注意**：文档中列出的“接入实时语音对话模型”当前仅支持 WebSocket 长连接模式，REST API 调用不适用该 Token Plan 配置——此限制在 [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice.md) 中未明确说明，但已在 [token-plan-realtime-voice.md](../../raw/token-plan-best-practice/token-plan-realtime-voice.md) 的 v2.3 版本更新日志中确认。

## 关键参数

Token Plan 通过 JSON Schema 定义配额策略，核心字段包括：
- `max_tokens`：单次请求允许的最大输出 token 数（硬限制，超限将被截断并返回 `400`）  
- `input_token_ratio` / `output_token_ratio`：分别指定输入/输出 token 的计费权重（如 `input_token_ratio: 0.5` 表示 2 个输入 token 折算为 1 个计费 token）  
- `burst_capacity`：突发容量（单位：token），用于应对短时流量高峰，需配合 `burst_window_seconds` 使用  
- `enable_vision_parsing`：布尔值，启用后触发视觉预处理（仅对支持多模态输入的模型生效；详见 [添加视觉理解能力](../../raw/token-plan-best-practice/add-vision-skill.md)）

## 使用方式

1. 在模型部署时，通过 `POST /v1/models/{model_id}/token-plan` 接口提交配置（需 `admin` 或 `deployer` 权限）  
2. 调用模型时，在请求 Header 中携带 `X-Token-Plan-ID: <plan_id>` 即可激活对应策略  
3. 支持动态切换：同一模型可绑定多个 Token Plan，按业务场景 ID 区分（例如 `plan_id: "chat-prod"` vs `"chat-sandbox"`）  
4. 验证配置是否生效：检查响应 Header 中的 `X-Used-Tokens` 和 `X-Remaining-Tokens` 字段  

## 限制和注意事项

- 单个 Token Plan 最多关联 10 个模型实例；超出需创建新 Plan  
- `burst_capacity` 不可超过账户级 `total_burst_quota`（可通过 `/v1/account/quota` 查询）  
- 图像/视频类模型的 `max_tokens` 实际约束的是 base64 编码后 payload 大小等效 token，非原始像素数——具体换算逻辑见 [接入图像生成模型](../../raw/token-plan-best-practice/token-plan-image-generation.md)  
- 修改 Token Plan 后，已建立的长连接（如 RTVC）不会自动继承新策略，需主动重连或调用 `PATCH /v1/connections/{conn_id}/refresh-plan`  
- 所有参数均为强类型校验，`null` 或空字符串将导致配置失败（错误码 `422 Unprocessable Entity`）

## 来源文档

- [接入其他模型](../../raw/token-plan-user-guide/token-plan-best-practice.md)


