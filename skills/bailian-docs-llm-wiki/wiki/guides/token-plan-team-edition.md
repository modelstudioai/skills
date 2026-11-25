# token plan team edition

[Token](../concepts/token.md) Plan 团队版是面向企业团队的 API 调用配额订阅服务，以“坐席”为最小单位提供独立 API Key、按月分配 Credits 额度，并支持共享用量包弹性扩容。所有坐席必须部署在华北2（北京）地域，且仅限主账号或已授权 RAM 子账号管理。该方案适用于需统一管控成员权限、用量和成本的开发团队。

## 支持的模型与内置工具

团队版支持调用百炼平台全部公开模型，包括千问（Qwen）、万相、DeepSeek、月之暗面、智谱 AI、MiniMax 和 HappyHorse 系列，覆盖文本生成、视觉理解、图片/视频生成、语音合成与识别等能力。其中 `auto` 模型可自动路由至最优底层模型，但**不支持** `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数 [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

> **注意**：文档 1 明确指出 `qwen4-max-preview` 已下线，请求将自动路由至 `qwen4-max` 并按其标准价格计费；而文档 2 未提及该变更，因此以文档 1 的说明为准。

模型内置工具（如 `web_search`、`image_search`、`code_interpreter` 等）通过 Responses API 自动触发，无需额外接入，按实际消耗 Credits 抵扣 [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 关键参数

- **坐席类型**：标准（¥150/月，25,000 Credits）、高级（¥550/月，100,000 Credits）、尊享（¥1,298/月，250,000 Credits），额度按坐席独立计量，不可跨席共享。
- **共享用量包**：¥5,000/个，含 625,000 Credits，有效期 1 个月，到期未用清零；抵扣顺序优先于坐席月度额度 [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **成员共享用量包上限**：管理员可为单个成员设置共享用量包使用上限（单位：Credits），启用后实际可用额度取“设置上限”与“组织剩余共享包余量”的较小值；每 24 小时仅可设置一次 [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)。

## 使用方式

1. **订阅开通**：主账号或 RAM 子账号在控制台「我的订阅」页面完成坐席购买（支持按月/连续包月），加购或升级坐席均按剩余订阅周期折算费用与额度。
2. **成员管理**：通过控制台「成员管理」手动添加成员（填用户名+角色）或配置 SSO/钉钉接入；SSO 需提前完成 SAML 2.0 配置（含 IdP Entity ID、SSO URL、证书），钉钉接入需创建企业内部应用并授权通讯录读取权限 [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)。
3. **席位分配**：为成员分配坐席后，系统自动生成专属 API Key 与 Base URL；成员凭此即可调用模型（Base URL 固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`）。
4. **用量监控**：所有者/管理员可在控制台「我的订阅」→「用量分析」查看各坐席额度、消耗趋势及成员明细；成员无权查看团队用量数据。

## 限制和注意事项

- **地域限制**：[Token](../concepts/token.md) Plan 团队版仅支持华北2（北京）地域，海外调用需自行确保合规性 [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。
- **退订与移出**：已产生用量的坐席不可退订；成员被移出组织后，若其坐席已消耗 Credits，则该席位不会返回资源池，无法再分配 [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)。
- **权限隔离**：所有者/管理员权限仅限本团队组织内，不涉及跨阿里云账号操作；RAM 子账号使用前须由主账号完成策略授权。
- **不支持降配**：团队版不支持将已购坐席降级为低档位，需等待当前订阅到期后重新购买。
- **API Key 生命周期**：重置 API Key 后原密钥立即失效；退订坐席会导致 API Key 不可用，续订成功后自动恢复（无需重新配置）。

## 来源文档

- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)
- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)


