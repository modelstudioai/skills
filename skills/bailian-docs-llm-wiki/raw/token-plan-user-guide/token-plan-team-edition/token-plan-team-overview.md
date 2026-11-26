# 团队版订阅与权益

Token Plan 团队版的套餐权益、账号权限、坐席管理、升级续费和退订规则。

> **说明**
>
> Token Plan 团队版目前仅支持**华北2（北京）**地域。如需从海外调用，请确认符合当地法律法规要求。

<a id="套餐与定价"></a>

<a id="tpt01-h-pricing"></a>

## 套餐与定价

前往 Token Plan 团队版购买页面选择坐席类型、数量和订阅周期，完成订阅。主账号和 RAM 账号均可订阅。订阅周期支持按月购买、连续包月。

<a id="token-plan-团队版"></a>

<a id="tpt01-h-seat-plans"></a>

### Token Plan 团队版

提供标准坐席、高级坐席、尊享坐席三个档位，匹配不同使用强度。

席位（坐席）是 Token Plan 团队版的最小订阅单位，代表一个团队成员的使用名额。管理员在团队管理中将席位分配给成员后，系统自动为该成员生成独立的 API Key。每个席位绑定一个成员、对应一个 API Key，不可共享。

| 坐席类型 | 价格 | 额度 | 适用场景 |
| --- | --- | --- | --- |
| 标准坐席 | **¥150/坐席/月** | 25,000 Credits/坐席/月 | 轻度使用 AI 辅助的团队成员 |
| 高级坐席 | **¥550/坐席/月** | 100,000 Credits/坐席/月 | 日常高频使用 AI 编程或办公的团队成员 |
| 尊享坐席 | **¥1,298/坐席/月** | 250,000 Credits/坐席/月 | 重度依赖 AI 的核心开发者或高强度使用者 |

每个坐席的月度 Credits 独立计量，不跨坐席共享；跨坐席的弹性额度通过共享用量包补充。团队管理员可在[**团队用量分析**](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/usage)中查看各坐席的总额度、剩余额度和成员消耗明细。

<a id="token-plan-团队版-共享用量包"></a>

<a id="tpt01-h-shared"></a>

### Token Plan 团队版 - 共享用量包

跨坐席共享的弹性用量包，当个别坐席用量超出套餐额度时，可从共享用量包中抵扣。每个共享用量包有效期为 1 个月，到期未使用的额度自动清零。所有者和管理员可按成员设置共享用量包额度上限，控制单个成员的用量，详见[团队管理](token-plan-team-management.md)。抵扣顺序见[用量与额度·抵扣顺序](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-order)。

| 档位 | 价格 | 额度 |
| --- | --- | --- |
| Token Plan 团队版 - 共享用量包 | ¥5,000/个 | 625,000 Credits/个 |

<a id="支持的模型"></a>

<a id="tpto-h-models"></a>

## 支持的模型

> **重要**
>
> -   **qwen4-max-preview 已下线**：原模型 ID 仍可正常调用，请求自动路由至 qwen4-max，Credits 抵扣和用量统计均按 qwen4-max 计算；预览期的限时折扣不再适用，调用按 qwen4-max 标准价格计费，费用可能高于预览期。建议将配置中的模型 ID 更新为 qwen4-max。详情参见[《模型升级通知》](https://www.aliyun.com/notice/118887)。
> -   **限时夜间五折**：每晚 22:00 - 次日 08:00 调用 deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash、deepseek-v4.1-flash-1017，Credits 消耗享 5 折优惠。
>
> 阿里云百炼有权根据运营情况对活动进行变更或调整，包括不限于活动内容和有效期等，请以页面最新内容或阿里云通知为准。

<a id="sec-tabs"></a>

<a id="千问"></a>

<a id="千问-h4"></a>

#### 千问

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| auto | 推理模型、文本生成<br><br>平台提供的智能模型，按请求内容自动匹配底层模型，兼顾效果与成本。 |
| qwen4-max | 推理模型、视觉理解、文本生成 |
| qwen3.8-max | 推理模型、视觉理解、文本生成 |
| qwen3.8-flash | 推理模型、视觉理解、文本生成 |
| qwen3.7-max | 推理模型、文本生成 |
| qwen3.7-plus | 推理模型、视觉理解、文本生成 |
| qwen3.6-plus | 推理模型、视觉理解、文本生成 |
| qwen3.6-flash | 推理模型、视觉理解、文本生成 |
| qwen-image-2.0 | 图片生成 |
| qwen-image-2.0-pro | 图片生成 |
| qwen-image-3.0-pro | 图片生成 |
| qwen-audio-3.0-tts-plus | 语音合成 |
| qwen-audio-3.0-realtime-plus | 实时语音对话 |
| qwen-audio-3.0-asr-flash | 语音识别 |

<a id="万相"></a>

<a id="万相-h4"></a>

#### 万相

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| wan2.7-image | 图片生成 |
| wan2.7-image-pro | 图片生成 |
| wan3.0-video | 视频生成 |

<a id="deepseek"></a>

<a id="deepseek-h4"></a>

#### DeepSeek

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| deepseek-v4.1-flash | 推理模型、视觉理解、文本生成 |
| deepseek-v4.1-flash-1017 | 推理模型、视觉理解、文本生成 |
| deepseek-v4-pro | 推理模型、文本生成 |
| deepseek-v4-pro-0813 | 推理模型、文本生成 |
| deepseek-v4-flash-0731 | 推理模型、文本生成 |

<a id="月之暗面"></a>

<a id="月之暗面-h4"></a>

#### 月之暗面

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| kimi-k2.7-code | 推理模型、视觉理解、文本生成 |
| kimi-k2.6 | 推理模型、视觉理解、文本生成 |
| kimi-k2.5 | 推理模型、视觉理解、文本生成 |

<a id="智谱-ai"></a>

<a id="智谱-ai-h4"></a>

#### 智谱 AI

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| glm-5.3 | 推理模型、文本生成 |
| glm-5.2 | 推理模型、文本生成 |
| glm-5.1 | 推理模型、文本生成 |
| glm-5 | 推理模型、文本生成 |

<a id="minimax"></a>

<a id="minimax-h4"></a>

#### MiniMax

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| MiniMax-M2.5 | 推理模型、文本生成 |

<a id="happyhorse"></a>

<a id="happyhorse-h4"></a>

#### HappyHorse

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| happyhorse-1.1-i2v | 视频生成 |
| happyhorse-1.1-t2v | 视频生成 |
| happyhorse-1.1-r2v | 视频生成 |

> `auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。

<a id="支持的模型内置工具"></a>

<a id="tpt01-h-builtin"></a>

## 支持的模型内置工具

模型内置工具是模型自带能力，通过 Responses API 调用模型时自动触发，按 Credits 抵扣，无需单独接入。

| 工具能力 | 工具名称 |
| --- | --- |
| 联网搜索 | web\_search |
| 文搜图 | web\_search\_image |
| 图搜图 | image\_search |
| 网页抓取 | web\_extractor |
| 代码解释器 | code\_interpreter |

<a id="订阅管理"></a>

<a id="tpt01-h-sub-mgmt"></a>

## 订阅管理

<a id="加购坐席"></a>

<a id="tpt01-h-add-seat"></a>

### 加购坐席

在 Token Plan 控制台的**我的订阅**页面，点击**加购坐席**，选择坐席档位和数量后提交订单。新加坐席与现有订阅统一到期，费用和 Credits 额度均按剩余时长折算。

<a id="升级坐席"></a>

<a id="tpt01-h-upgrade-seat"></a>

### 升级坐席

在**订阅明细**中找到目标坐席，点击**升级**，选择更高档位后提交订单。需要批量操作时，勾选多个坐席后点击**批量升级**。升级按剩余时长补缴差价，升级新增的 Credits 额度同步按剩余时长折算后发放。补差金额和新增额度的折算见[用量与额度·升级额度计算](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-upgrade)，实际可用额度以控制台展示为准。

<a id="续费"></a>

<a id="tpt01-h-renew"></a>

### 续费

-   点击**续费**按钮，续费周期与订阅时一致，到期前完成可避免服务中断。
-   **自动续费**：点击**开启自动续费**，确认后次日生效，到期前 3 天系统按订阅周期自动扣款续费。如需关闭，点击**关闭自动续费**并确认。

<a id="退订坐席"></a>

<a id="tpt01-h-refund"></a>

### 退订坐席

在**订阅明细**中点击坐席的**退订**，按坐席维度退订；已有用量消耗的坐席不可退订。也可勾选多个坐席后点击**批量退订**。退款原路退回支付账户，预计 1-3 个工作日到账。

<a id="加购共享用量包"></a>

<a id="tpt01-h-shared-buy"></a>

### 加购共享用量包

在**共享用量包**区域点击**前往购买**。价格和额度见上方“共享用量包”，抵扣顺序见[用量与额度·抵扣顺序](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-order)。

<a id="注意事项"></a>

<a id="tpt01-h-sub-notice"></a>

### 注意事项

-   退订后 API Key 变为不可用；重新购买成功后，原 API Key 恢复可用，无需在工具中重新配置。如需更换成员的 API Key，可[重置 API Key](token-plan-team-management.md#tpt03-h-reset-key)。
-   续费不增加当前订阅周期的额度，规则见[用量与额度·额度规则](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-reset)。
-   团队版不支持降配，如需使用更低坐席类型，可在当前订阅到期后重新订阅。
-   团队版与个人版可同时持有，各自独立计费。
