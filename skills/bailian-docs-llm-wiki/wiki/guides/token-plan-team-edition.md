# token plan team edition

[Token](../concepts/token.md) Plan Team Edition 是面向企业团队的 AI 模型调用服务订阅方案，提供多档位坐席、共享用量包及集中式成员管理能力。所有坐席绑定独立 API Key，支持 SSO（SAML）和钉钉身份集成，适用于需统一管控模型访问权限与用量的开发团队。该服务当前仅支持华北2（北京）地域。

## 支持的模型与功能

### 支持的模型
团队版支持调用百炼平台全量商用模型，包括：
- **千问系列**：`qwen4-max`、`qwen4-max-preview`（预览期至 2026-11-25，详见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)）、`qwen3.8-flash`、`qwen-image-3.0-pro`、`qwen-audio-3.0-realtime-plus` 等；
- **万相系列**：`wan2.7-image-pro`、`wan3.0-video`；
- **DeepSeek 系列**：`deepseek-v4.1-flash-1017`、`deepseek-v4-pro-0813`（夜间 22:00–08:00 享 5 折）；
- **月之暗面、智谱 AI、MiniMax、HappyHorse** 等合作厂商模型。

> **注意**：`auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。

### 内置工具能力
所有支持模型均可直接调用以下内置工具（按 Credits 计费，无需额外接入）：
- `web_search`（联网搜索）
- `web_search_image`（文搜图）
- `image_search`（图搜图）
- `web_extractor`（网页抓取）
- `code_interpreter`（代码解释器）

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| `model` | 必填，指定模型 ID（如 `qwen4-max-preview`） | 不支持别名混用；`qwen4-max-preview` 与 `qwen4.0-max-preview` 等价，账单统一显示为后者 |
| `base_url` | 必填，由控制台分配，格式为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（或新版兼容地址） | 需与分配席位时生成的 Base URL 严格一致 |
| `api_key` | 必填，每个席位唯一，由管理员分配或成员通过 SSO/钉钉登录后自动生成 | 仅限本组织内成员使用；重置后原 Key 立即失效 |
| `shared_usage_package_quota` | 可选，通过[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)为成员设置单人共享用量包上限 | 单次设置后 24 小时内不可重复修改；启用后实际可用额度 = min(设置上限, 组织剩余共享包) |

## 使用方式

1. **订阅与初始化**  
   主账号或已授权 RAM 用户登录 [Token](../concepts/token.md) Plan 控制台 → 进入**我的订阅** → 订购团队版（标准/高级/尊享坐席 + 共享用量包）。

2. **成员与席位管理**  
   - 手动添加成员：在[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)中填写用户名（英文字母/数字/下划线），分配席位后系统自动生成 API Key 和 Base URL；  
   - SSO/钉钉接入：完成 IdP 或钉钉应用配置后，成员通过管理平台地址（见[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)“基本信息”区域）登录即自动加入。

3. **API 调用**  
   成员使用分配的 `api_key` 和 `base_url`，按 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)格式发起请求（如 `/chat/completions`），无需额外鉴权头。

## 限制和注意事项

- **地域限制**：团队版仅支持华北2（北京）地域，海外调用需自行确保合规性。
- **坐席绑定**：每个坐席严格绑定一名成员与一个 API Key，不可转让、不可共享；移出成员时，若其已消耗 Credits，则该坐席**不会回归资源池**（见[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)）。
- **共享用量包**：有效期为 1 个月，到期未用额度自动清零；抵扣顺序优先于坐席月度额度（详见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)）。
- **升级与退订**：支持加购、升级、续费；**不支持降配**（如需降低坐席档位，须等待当前订阅到期后重新订购）；已产生用量的坐席不可退订。
- **API Key 生命周期**：退订坐席会导致对应 API Key 不可用；续订成功后原 Key 自动恢复有效——如需更换，应通过[团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)执行重置操作。

## 来源文档

- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)
- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)


