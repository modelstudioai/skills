# token plan team edition

Token Plan 团队版是面向中小研发团队的 API 调用配额订阅服务，以“坐席”为最小计费与用量单元，提供分档额度、跨坐席共享用量包及精细化成员管理能力。所有坐席绑定独立 API Key，地域限定为华北2（北京），不支持跨地域调用。详细权益与运营规则参见 [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 支持的模型与功能

- **模型覆盖**：支持千问（qwen4-max、qwen4-max-preview、qwen3.8-flash 等）、万相（wan2.7-image、wan3.0-video）、DeepSeek（deepseek-v4.1-flash、deepseek-v4-pro-0813 等）、月之暗面（kimi-k2.7-code）、智谱 AI（glm-5.3）、MiniMax（M2.5）、HappyHorse（t2v/r2v/i2v）等多厂商模型。
- **特殊权益**：
  - `qwen4-max-preview` 为限时预览模型（2026-11-11 10:00 至 11-25 24:00 UTC+8），账单统一显示为 `qwen4.0-max-preview`，且预览期内 Credits 消耗低至 2 折；
  - `deepseek-v4-pro-0813` 等 4 款 DeepSeek 模型在每日 22:00–08:00 享 5 折 Credits 抵扣。
- **内置工具**：`web_search`、`web_search_image`、`image_search`、`web_extractor`、`code_interpreter` 等工具通过 Responses API 自动触发，按实际调用消耗 Credits，无需额外接入。
- **限制说明**：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。

> **注意**：文档 1 中列出 `qwen4-max-preview` 预览期截止时间为 2026 年 11 月 25 日，但该时间明显为占位符或过期模板；实际有效期请以控制台实时展示或阿里云官方通知为准。开发者应主动校验模型可用性，避免硬编码依赖已下线 ID。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `seat_type` | 坐席类型：`standard` / `advanced` / `premium`，对应标准/高级/尊享坐席 | [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md) |
| `credits_per_seat` | 月度额度：25,000 / 100,000 / 250,000 Credits/坐席/月，独立计量，不跨坐席共享 | [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md) |
| `shared_package` | 共享用量包：625,000 Credits/个，有效期 1 个月，到期清零；抵扣顺序优先于坐席额度 | [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md) |
| `seat_quota_limit` | 成员级共享用量包上限：由管理员在[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)中为单个成员设置，每 24 小时仅可修改一次 |

## 使用方式

1. **订阅与分配**：主账号或 RAM 账号在控制台「我的订阅」完成坐席购买；管理员在「成员管理」中手动添加成员或通过 SSO/钉钉接入，并为其分配坐席，系统自动生成专属 API Key 与 Base URL。
2. **API 调用**：成员使用分配的 API Key 和 Base URL（如 `https://dashscope.aliyuncs.com/api/v1`）调用模型，请求头需包含 `Authorization: Bearer <API_KEY>`。
3. **用量控制**：
   - 管理员可在「成员管理」中为成员设置共享用量包额度上限；
   - 所有者/管理员可查看各成员、各模型的用量趋势与明细，入口为[控制台我的订阅](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)；
   - 成员自身无法查看组织级用量，需联系管理员获取。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域调用，海外调用需自行确保合规性。
- **坐席绑定**：每个坐席严格绑定一名成员与一个 API Key，不可共享；移出成员时，若其已消耗 Credits，则坐席不可回收至资源池。
- **退订与重置**：退订坐席后 API Key 立即失效；重置 API Key 后原密钥立即作废，新密钥需重新分发。
- **升级与续费**：
  - 升级坐席按剩余周期折算差价与新增额度，不支持降配；
  - 续费不重置当期额度，额度按自然月周期刷新（非按订阅起始日滚动）。
- **权限隔离**：所有者与管理员权限限于本团队组织内，无法跨阿里云账号操作；RAM 子账号需主账号预先授权，详见 [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) 中的权限说明。
- **SSO/钉钉前提**：配置 SAML 或钉钉前，必须清空组织内所有成员；否则配置入口被禁用。

## 来源文档

- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)


