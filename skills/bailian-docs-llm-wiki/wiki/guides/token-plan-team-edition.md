# token plan team edition

[Token](../concepts/token.md) Plan Team Edition 是面向企业团队的 AI 资源订阅服务，提供按席位（seat）计量的 Credits 额度、集中式成员与权限管理、SSO/钉钉身份集成，以及跨坐席共享用量包等能力。所有 API 调用均通过独立生成的 API Key 和 Base URL 进行，模型调用按实际消耗 Credits 结算。该服务当前仅支持华北2（北京）地域，详见[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

## 支持的模型与功能

- **支持模型**：覆盖千问（qwen4-max、qwen3.8-flash 等）、万相（wan2.7-image、wan3.0-video）、DeepSeek（deepseek-v4.1-flash、deepseek-v4-pro-0813）、月之暗面（kimi-k2.7-code）、智谱 AI（glm-5.3）、MiniMax（MiniMax-M2.5）、HappyHorse（happyhorse-1.1-t2v）等主流厂商模型；`auto` 模型支持自动路由，但不支持 `tool_choice`、`thinking.budget_tokens` 和 `thinking_budget` 参数。  
- **内置工具**：所有支持模型均可直接调用 `web_search`、`web_search_image`、`image_search`、`web_extractor`、`code_interpreter` 等内置工具，按实际调用消耗 Credits，无需额外接入。  
- **特殊规则**：`qwen4-max-preview` 已下线，请求自动路由至 `qwen4-max` 并按其标准价格计费；`deepseek-v4-pro-0813` 等指定模型在 22:00–08:00 享 Credits 5 折优惠，具体以[团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)中“支持的模型”章节为准。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `API Key` | 每个分配席位的成员独享，由系统自动生成，用于鉴权；可随时重置，旧 Key 立即失效 | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |
| `Base URL` | 成员调用模型时必需的 endpoint，格式为 `https://dashscope.aliyuncs.com/api/v1/`（或控制台指定地址），需与 API Key 配对使用 | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |
| `Credits` | 计量单位，不同模型/操作消耗不同；坐席额度按月独立发放，共享用量包额度按购买个数叠加，有效期均为 1 个月 | [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md) |
| `共享用量包额度上限` | 管理员可为单个成员设置上限（单位：Credits），启用后实际可用额度 = min(设置上限, 组织剩余共享包)；每 24 小时仅可设置一次 | [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md) |

> **注意**：文档 1 中“移出成员”条款指出：“若该成员已使用 Credits，移出后席位不会回到资源池”；而文档 2 的“退订坐席”明确“已有用量消耗的坐席不可退订”。二者逻辑一致，但表述角度不同——前者描述席位回收行为，后者约束订阅级退订操作。开发者应理解：**席位一旦产生用量，即锁定不可转移或退还**。

## 使用方式

1. **管理员配置**：主账号或已授权 RAM 用户登录 [Token](../concepts/token.md) Plan 控制台 → **我的订阅** → **团队版**卡片 → **设置**，完成组织名称、SSO/钉钉接入、管理平台地址配置；  
2. **添加成员**：  
   - 手动添加：在**成员管理**页点击**添加成员**，填用户名并分配席位，系统自动生成 API Key 与 Base URL；  
   - SSO/钉钉加入：成员访问管理员提供的**管理平台地址**，通过对应入口登录即自动入组；  
3. **成员调用**：使用分配的 API Key 与 Base URL，按标准 OpenAI 或 DashScope SDK 格式发起请求（如 `POST /chat/completions`），模型 ID 直接传入（如 `"model": "qwen4-max"`）；  
4. **用量监控**：所有者/管理员访问 [团队用量分析](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/usage) 查看坐席额度、共享包余量及成员明细。

## 限制和注意事项

- **地域限制**：仅支持华北2（北京）地域，海外调用需自行确保合规性；  
- **席位绑定**：每个席位严格绑定一名成员与一个 API Key，不可共享、转让或拆分；  
- **权限隔离**：所有者/管理员权限仅限本组织内，无法跨阿里云账号管理；成员无法查看团队订阅状态或共享包余量；  
- **SSO 配置约束**：组织内存在成员时，**无法编辑 SSO 配置**（包括 SP Entity ID、ACS URL 等），必须先清空全部成员；  
- **API Key 生命周期**：重置后旧 Key 立即失效；退订坐席将使对应 API Key 不可用，续费后恢复可用（无需重新配置）；  
- **升级与加购**：加购/升级坐席费用及 Credits 均按剩余订阅时长折算，不支持降配，需到期后重新订阅低档位。

## 来源文档

- [团队管理](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-management.md)
- [团队版订阅与权益](../../raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)


