# token plan team edition

Token Plan Team Edition 是面向企业团队的 API 调用配额管理方案，以“席位（坐席）”为最小订阅单位，提供分层 Credits 额度、跨席位共享用量包、细粒度成员权限控制及 SSO/钉钉统一身份接入能力。所有席位和共享用量包均按月计量，额度在订阅周期内独立或弹性使用，适用于需集中管控 AI 资源调用的开发团队。

## 支持的模型与功能

- **支持模型**：覆盖千问（qwen4-max、qwen3.8-flash、qwen-image-3.0-pro 等）、DeepSeek（deepseek-v4.1-flash、deepseek-v4-pro-0813 等）、Kimi、GLM、MiniMax、HappyHorse 及万相系列，详见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)中的完整模型 ID 列表。
- **预览与限时权益**：`qwen4-max-preview` 为预览模型（有效期至 2026-11-25 24:00 UTC+8），预览期 Credits 消耗低至 2 折；`deepseek-v4-pro-0813` 等 4 款 DeepSeek 模型在每日 22:00–08:00 享 5 折调用优惠。
- **内置工具**：`web_search`、`web_search_image`、`image_search`、`web_extractor`、`code_interpreter` 等工具通过 Responses API 自动触发，按实际消耗 Credits 计费，无需额外配置。
- **特殊说明**：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。

> **注意**：文档 2 中明确指出团队版“目前仅支持华北2（北京）地域”，但文档 1 的团队管理流程未提及地域限制。实际部署前请确认调用请求必须经由 `cn-beijing` 地域的 endpoint 发起，否则可能因地域不匹配导致鉴权失败或额度不可见。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `seat_type` | 席位类型：`standard`（标准）、`advanced`（高级）、`premium`（尊享），对应不同月度 Credits 额度（25k / 100k / 250k） | [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md) |
| `shared_quota_package` | 共享用量包：单个包含 625,000 Credits，有效期 1 个月，到期清零；可为成员设置个人额度上限（每 24 小时限设一次） | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |
| `api_key` | 每个已分配席位的成员独有，由系统自动生成；重置后原 key 立即失效 | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |
| `base_url` | 成员调用模型必需的 endpoint，格式为 `https://dashscope.aliyuncs.com/api/v1/`（华北2 区域） | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |

## 使用方式

1. **订阅与初始化**  
   主账号或已授权 RAM 用户登录 Token Plan 控制台 → 进入**我的订阅** → 订购团队版（选择席位档位、数量、周期）→ 完成支付。

2. **成员与席位管理**  
   - 在**团队版卡片 → 设置**中配置 SSO（SAML 2.0）或钉钉接入，获取**管理平台地址**并分发给成员。  
   - 在**成员管理**页手动添加成员（填用户名+角色）或通过 SSO/钉钉自动加入。  
   - 为成员**分配席位**后，系统生成专属 `api_key` 和 `base_url`，成员即可调用模型。

3. **API 调用示例（OpenAI 兼容模式）**  
   ```bash
   curl https://dashscope.aliyuncs.com/api/v1/chat/completions \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen4-max",
           "messages": [{"role": "user", "content": "Hello"}]
         }'
   ```

4. **用量控制（可选）**  
   管理员可在成员管理页点击**共享用量包额度 → 设置**，为指定成员启用 Credits 上限（如 `50000`），实际可用额度取该上限与组织剩余共享包余量的较小值。

## 限制和注意事项

- **地域限制**：团队版服务仅部署于华北2（北京），所有 API 请求必须指向该 region 的 endpoint，海外调用需自行确保合规性。  
- **席位绑定**：每个席位严格绑定一名成员与一个 `api_key`，不可复用或转让；移出成员时，若其已消耗 Credits，则对应席位**不会回收至资源池**，无法重新分配。  
- **共享用量包**：仅已分配席位的成员可被设置个人额度上限；额度每 24 小时仅可修改一次；包内 Credits 不跨周期结转。  
- **退订与续费**：已产生用量的席位不可退订；续费仅延长周期，**不增加当期额度**；团队版不支持降配（如需降低档位，须等待当前订阅到期后重新购买）。  
- **权限隔离**：所有者/管理员权限仅限本团队组织内，无法跨阿里云账号操作；成员无法查看团队订阅详情或用量余量，需联系管理员获取信息。

## 来源文档

- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)
- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)


