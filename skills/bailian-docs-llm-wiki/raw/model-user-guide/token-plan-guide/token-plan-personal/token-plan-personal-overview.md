# 概述

Token Plan 个人版 是面向个人开发者的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态模型及模型内置工具，Standard 与 Pro 套餐附赠 Harness 权益，适配主流 AI 编程和智能体工具。

**说明**Token Plan 个人版目前仅支持**华北2（北京）**地域。

## 核心特性

-   **Credits 统一计量**：通过 Credits 统一抵扣模型调用及[模型内置工具](#tpp01-h-harness)的费用。
-   **多模态模型支持**：覆盖文本生成、推理、视觉理解、图片生成、语音合成、实时语音对话、语音识别、视频生成等能力。
-   **Harness 权益**：Standard 与 Pro 套餐附赠 AgentStudio 工具的每月免费额度与后付费折扣，不占用 Credits，详见[Harness 权益](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-benefits.md)。
-   **用量包**：超出限额后可购买用量包，不受限制继续使用。
-   **兼容多种工具**：适配 Claude Code、Cursor、Qwen Code、Qoder、Qoder CN、OpenClaw 等主流 AI 编程和智能体工具。

## 套餐档位与定价

**Lite 套餐**

**Essential 套餐**

**Standard 套餐**

**Pro 套餐**

**定价**

原价 60 元/月  
限时 **39 元/月**

原价 120 元/月  
限时 **79 元/月**

原价 180 元/月  
限时 **139 元/月**

原价 600 元/月  
限时 **499 元/月**

**每月限额**

11,500 Credits

25,500 Credits

45,000 Credits

180,000 Credits

**并发 Agent**

1-2 个

2-3 个

3-4 个

6-8 个

**权益**

文本、视觉等模型

联网搜索等内置工具

适配主流工具

Lite 全部权益

2.25x Lite 套餐用量

Lite 全部权益

4x Lite 套餐用量

赠送 Harness 权益

Standard 全部权益

16x Lite 套餐用量

更高的并发上限

赠送 Harness 权益

-   **每月限额**：自订阅当日起向后延伸 30 天作为订阅周期，订阅周期内累计消耗达到套餐额度后暂停服务，需等待下一个订阅月后额度恢复。月额度用满后，可购买用量包作为补充，或等待下一个订阅月开始后重置。
-   **用量包**：定价 100 元/个/月，每个用量包含 20,000 Credits。需先订阅有效套餐后购买，最多同时持有 5 个；套餐月额度用尽后自动抵扣用量包额度。

月额度触顶即暂停服务，可购买用量包补充额度继续使用，或等待下一个订阅月额度重置。订阅月内未用完的额度不结转至下一周期。

## Credits 计费机制

**说明**不同模型按分档抵扣系数计费，视频生成等多模态模型的单次消耗明显高于文本对话，使用时需重点关注以下两点：

-   **单次消耗高**：视频生成的 Credits 随时长和分辨率上升，可能在短时间内占用较多限额。建议首次使用时以较短时长、较低分辨率试跑，通过控制台订阅页用量详情确认单次实际消耗后，再决定后续用量。
-   **异步任务集中结算**：视频生成等异步任务的 Credits 在任务完成后统一结算，而非提交时立即扣除。短时间内提交多个异步任务时，集中结算的 Credits 可能导致限额快速触顶。

### 计费说明

单次消耗的 Credits 由模型类型、Token 用量、思考模式及工具调用等动态决定，实际消耗以[控制台订阅页](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)用量详情为准。

### 抵扣顺序

1.  每次调用优先抵扣当前订阅月的套餐额度。
2.  套餐月额度用尽后，自动抵扣用量包额度；用量包额度用尽或未持有用量包时，服务暂停，可升级至更高档位套餐，或等待下一个订阅月额度自动重置。

**重要**Harness 权益（AgentStudio 工具的免费额度与折扣）独立计量，不从 Credits 或用量包抵扣，详见 [Harness 权益](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-benefits.md)。

### 额度重置

额度按订阅月自动重置：每个订阅月开始时，套餐额度恢复为对应档位的满月额度。2026 年 9 月 22 日个人版取消周限额起，存量订阅的剩余额度已于当日一次性重置为对应套餐的满月额度，订阅周期与到期时间保持不变。

## 支持的模型

**重要**

-   **auto 模型**：平台提供的智能模型，按请求内容自动匹配底层模型，兼顾效果与成本。
-   **限时夜间四折**：每晚 22:00 - 次日 08:00 调用 qwen3.8-max、qwen3.8-flash，Credits 消耗享 4 折优惠。
-   **限时夜间五折**：每晚 22:00 - 次日 08:00 调用 deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash，Credits 消耗享 5 折优惠。
-   **qwen3.8-max-preview 已下线**：原模型 ID 仍可正常调用，请求自动路由至 qwen3.8-max，Credits 抵扣和用量统计均按 qwen3.8-max 计算，建议将配置中的模型 ID 更新为 qwen3.8-max。

阿里云百炼有权根据运营情况对活动进行变更或调整，包括不限于活动内容和有效期等，请以页面最新内容或阿里云通知为准。

**品牌**

**模型 ID（Model ID）**

**模型能力**

千问

auto

推理模型、文本生成

qwen3.8-max

推理模型、视觉理解、文本生成

qwen3.8-flash

推理模型、视觉理解、文本生成

qwen3.7-max

推理模型、文本生成

qwen3.7-plus

推理模型、视觉理解、文本生成

qwen3.6-flash

推理模型、视觉理解、文本生成

qwen-image-3.0-pro

图片生成

qwen-audio-3.0-tts-plus

语音合成

qwen-audio-3.0-realtime-plus

实时语音对话

qwen-audio-3.0-asr-flash

语音识别

万相

wan2.7-image

图片生成

wan2.7-image-pro

图片生成

DeepSeek

deepseek-v4.1-flash

推理模型、视觉理解、文本生成

deepseek-v4-pro

推理模型、文本生成

deepseek-v4-pro-0813

推理模型、文本生成

deepseek-v4-flash-0731

推理模型、文本生成

智谱 AI

glm-5.3

推理模型、文本生成

glm-5.2

推理模型、文本生成

HappyHorse

happyhorse-1.1-i2v

视频生成

happyhorse-1.1-t2v

视频生成

happyhorse-1.1-r2v

视频生成

## 支持的模型内置工具

模型内置工具是模型自带能力，通过 Responses API 调用模型时自动触发，按 Credits 抵扣，无需单独接入。

**工具能力**

**工具名称**

联网搜索

web\_search

文搜图

web\_search\_image

图搜图

image\_search

网页抓取

web\_extractor

代码解释器

code\_interpreter

## 订阅管理

### 升级

支持从低档位升级到更高档位。套餐升级不重置当前订阅周期：按当前订阅周期剩余天数补缴差价，当前周期仅按额度差折算发放新增 Credits，自下一个订阅月起按新档位月额度计量。

升级（含席位升级场景）发放的 Credits 并非新档位的全额月额度，而是按实付补差金额和当前订阅周期的实际剩余有效时长折算得出，折算公式如下。

```
升级补差金额 = (新套餐价格 − 旧套餐价格) × 剩余天数 ÷ 30
（不满一天按一天计算）

升级后当前周期新增额度 = 剩余天数 ÷ 30 × (升级后月额度 − 升级前月额度)
（不满一天按一天计算，结果向上取整）
```

例如：9 月 2 日订阅 Lite 套餐（39 元/月，月额度 11,500 Credits），9 月 12 日升级至 Essential 套餐（79 元/月，月额度 25,500 Credits），当前订阅周期剩余 20 天：补差金额为 (79 − 39) × 20 ÷ 30 ≈ 26.67 元，当前周期新增额度为 20 ÷ 30 × (25,500 − 11,500) ≈ 9,334 Credits（向上取整）。

升级后 Harness 权益的剩余额度计算详见 [Harness 权益·升级后权益计算](https://help.aliyun.com/zh/model-studio/token-plan-harness-benefits#tphb-h-upgrade)。

### 续费

续费支持切换续费周期，也可一次续费多个周期。

-   **手动续费**：支持选择不同续费时长，可续费多个周期。
-   **自动续费**：开启后到期前系统自动扣款续费。

续费仅延长订阅有效期，不会叠加补充至当前计费周期的额度。

### 其他

-   个人版暂不支持退订。
-   订阅到期后重新购买，API Key 会发生变更，需在工具中重新配置。新 API Key 可在控制台[**我的订阅**](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)页面的 API Key 区域获取。

## 订阅前须知

1.  **使用范围**：仅限在编程工具和智能体工具（如 Claude Code、Cursor、Qwen Code、Qoder、Qoder CN、OpenClaw 等）中交互式使用，不可用于自动化脚本、自定义应用程序后端或任何非交互式批量调用场景。模型通过工具的扩展机制（Skill、Slash Command 或 Agent）接入，工具内交互式发起的调用属于正常使用；将套餐 API Key 用于允许范围之外的调用将被视为违规或滥用，可能会导致订阅被暂停或 API Key 被封禁。
2.  **数据使用授权**：使用 Token Plan 个人版期间，模型输入以及模型生成的内容将用于服务改进与模型优化。停止使用 Token Plan 个人版服务可终止后续数据授权，但终止授权的范围不涵盖已授权使用的数据。详细条款请参见[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)第 5.2 条。
3.  **账号使用规范**：套餐为订阅人专享使用，禁止共享。账号共享可能导致订阅权益受限。
4.  **购买限制**：同一实名认证主体限购一份，可同时购买个人版和团队版。
5.  **设备使用说明**：Token Plan 个人版供本人在单台设备上使用。将 API Key 共享给他人使用可能被判定为违规并导致封禁。
6.  **RAM 子账号无需单独实名认证**：只要主账号已完成实名认证，并为 RAM 子账号分配了席位及 API 调用权限，该 RAM 子账号即可正常使用 Token Plan，无需单独实名认证。
