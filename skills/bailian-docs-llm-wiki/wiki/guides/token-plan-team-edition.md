# token plan team edition

Token Plan 团队版是面向企业团队的 API 调用额度订阅服务，以“坐席”为最小单位提供独立 API Key、按月计费的 Credits 额度及跨坐席共享用量包。所有坐席绑定唯一成员，额度独立计量、不可共享，适用于需统一管理、分权控制和用量审计的开发团队。该服务当前仅支持华北2（北京）地域，详见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 支持的模型与功能

团队版支持调用百炼平台全部公开模型，包括千问（Qwen）、万相（WanXiang）、DeepSeek、月之暗面（Kimi）、智谱 AI（GLM）、MiniMax 和 HappyHorse 系列，覆盖文本生成、视觉理解、图片/视频生成、语音合成与识别等能力。关键模型 ID 包括 `qwen4-max`（替代已下线的 `qwen4-max-preview`）、`qwen3.8-flash`、`wan3.0-video`、`deepseek-v4.1-flash-1017`（享夜间五折优惠时段）、`kimi-k2.7-code`、`glm-5.3` 等。  
所有模型均支持内置工具调用（如 `web_search`、`code_interpreter`），无需额外接入，按实际消耗 Credits 计费。注意：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens` 和 `thinking_budget` 参数。详细模型列表与能力说明见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

> **注意**：文档 1 明确指出 `qwen4-max-preview` 已下线，请求将自动路由至 `qwen4-max` 并按其标准价格计费；而文档 2 未提及该变更。开发者应以文档 1 的说明为准，及时更新客户端配置中的模型 ID。

## 关键参数

- **坐席类型**：标准（¥150/月，25,000 Credits）、高级（¥550/月，100,000 Credits）、尊享（¥1,298/月，250,000 Credits）。每个坐席对应一个成员、一个独立 API Key。
- **共享用量包**：¥5,000/个，含 625,000 Credits，有效期 1 个月，到期未用清零；用于跨坐席弹性抵扣超额用量。
- **Base URL**：成员调用模型时必需，由系统在分配席位后自动生成，格式为 `https://dashscope.aliyuncs.com/api/v1`（华北2专属 endpoint）。
- **API Key**：每个坐席独有，由管理员分配或重置；成员无法自行创建或查看组织级订阅信息。

## 使用方式

1. **开通与配置**：主账号或已授权 RAM 账号登录 Token Plan 控制台 → 进入**我的订阅** → 点击**团队版**卡片的**设置**完成组织基本信息、SSO 或钉钉接入配置（详见[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)）。
2. **添加与分配成员**：
   - 手动添加：在**成员管理**中填写用户名（仅限字母/数字/下划线）并指定角色，可同步分配席位；
   - SSO/钉钉加入：成员通过管理平台地址（在**设置**→**基本信息**中获取）选择对应入口登录即自动入组。
3. **调用模型**：成员使用分配的 API Key 与 Base URL，按标准 DashScope [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（或 Anthropic 兼容接口）发起请求，例如：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "qwen4-max", "input": {"messages": [...]}}'
   ```
4. **用量监控与调整**：所有者/管理员可在控制台实时查看各成员坐席状态、剩余 Credits、共享用量包余量及消耗趋势；支持为成员单独设置共享用量包额度上限（每 24 小时限设一次）。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域调用，海外调用需自行确保合规性，参见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **坐席生命周期**：已使用 Credits 的坐席不可退订；移出成员时，若其尚未消耗 Credits，席位可回收至资源池；否则席位永久释放，不可再分配。
- **权限隔离**：成员仅能使用自身 API Key 调用模型，无法查看团队订阅详情、坐席额度或共享用量包余额；所有用量分析与管理操作必须由所有者或管理员执行。
- **升级与续费**：支持加购/升级坐席及共享用量包，费用与新增 Credits 均按剩余订阅周期折算；团队版不支持降配，需待当前周期结束后重新订阅低档位。
- **API Key 安全**：重置 API Key 后原密钥立即失效；退订坐席会导致 API Key 不可用，但续订成功后原 Key 自动恢复有效——此行为已在[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)中明确说明。

## 来源文档

- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)


