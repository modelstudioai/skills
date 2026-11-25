# 个人版订阅与权益

Token Plan 个人版的套餐权益、账号权限、升级续费、退订和使用规则。

> **说明**
>
> Token Plan 个人版目前仅支持**华北2（北京）**地域。

<a id="套餐档位与定价"></a>

<a id="tppo-h-pricing"></a>

## 套餐档位与定价

|  | Lite 套餐 | Essential 套餐 | Standard 套餐 | Pro 套餐 |
| --- | --- | --- | --- | --- |
| **定价** | **39 元/月**<br>[新用户限时价](#tpp01-h-new-user-promo) **19.5 元/月** | **79 元/月**<br>[新用户限时价](#tpp01-h-new-user-promo) **39.5 元/月** | **139 元/月** | **312 元/月** |
| **每月限额** | 20,000 Credits | 45,000 Credits | 80,000 Credits | 200,000 Credits |
| **并发 Agent** | 1-2 个 | 2-3 个 | 3-4 个 | 6-8 个 |
| **权益** | 文本、视觉等模型<br><br>联网搜索等内置工具<br><br>适配主流工具 | Lite 全部权益 | Lite 全部权益<br><br>赠送 Harness 权益 | Standard 全部权益<br><br>更高的并发上限<br><br>赠送 Harness 权益 |

<a id="tpp01-h-new-user-promo"></a>

> **说明**
>
> 新用户限时价有效期至 2026 年 11 月 30 日 23:59:59（UTC+8），仅同一用户下全部账号均未购买过 Token Plan 个人版时可享受；账号关联判定见[常见问题](../token-plan-guide/token-plan-faq.md#tpf-h-new-user-promo)。价格以实际页面为准。

-   **每月限额**：额度按订阅月计算。额度用尽后的处理见[用量与额度·额度用完了怎么办](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-exhausted)。
-   **用量包**：定价 100 元/个/月，每个用量包含 20,000 Credits。需先订阅有效套餐后购买，最多同时持有 5 个；不占用、不计入套餐月额度，有效期为 1 个月，到期后未使用的额度自动作废，不支持退款。抵扣顺序见[用量与额度·抵扣顺序](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-order)。
-   **额度调整**：2026 年 11 月 9 日 20:00:00（UTC+8）起，Token Plan 个人版四档套餐额度上调，Pro 套餐目录价及官网折扣价下调。存量订阅在当前订阅周期内按新额度补齐，已使用额度不变；Pro 套餐当前订阅周期价格不变，新价格于下一订阅周期生效。详情参见[《Token Plan 个人版套餐降价通知》](https://www.aliyun.com/notice/118815)。

月额度用满后可购买用量包补充额度。查看剩余额度、重置时间和消耗明细，见[控制台我的订阅](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan)。

<a id="支持的模型"></a>

<a id="tppo-h-models"></a>

## 支持的模型

> **重要**
>
> -   **qwen4-max-preview 已下线**：原模型 ID 仍可正常调用，请求自动路由至 qwen4-max，Credits 抵扣和用量统计均按 qwen4-max 计算；预览期的限时折扣不再适用，调用按 qwen4-max 标准价格计费，费用可能高于预览期。建议将配置中的模型 ID 更新为 qwen4-max。详情参见[《模型升级通知》](https://www.aliyun.com/notice/118887)。
> -   **限时夜间折扣**：每晚 22:00 - 次日 08:00 调用 qwen3.8-max、qwen3.8-flash 享 4 折，调用 deepseek-v4-pro-0813、deepseek-v4-flash-0731、deepseek-v4.1-flash、deepseek-v4.1-flash-1017 享 5 折。
> -   **decision-model-preview 限时免费**：调用不消耗 Credits。接入方法参见[接入决策模型](../token-plan-best-practice/token-plan-decision-model.md)。
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
| qwen3.6-flash | 推理模型、视觉理解、文本生成 |
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

<a id="智谱-ai"></a>

<a id="智谱-ai-h4"></a>

#### 智谱 AI

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| glm-5.3 | 推理模型、文本生成 |
| glm-5.2 | 推理模型、文本生成 |

<a id="happyhorse"></a>

<a id="happyhorse-h4"></a>

#### HappyHorse

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| happyhorse-1.1-i2v | 视频生成 |
| happyhorse-1.1-t2v | 视频生成 |
| happyhorse-1.1-r2v | 视频生成 |

<a id="领域模型"></a>

<a id="领域模型-h4"></a>

#### 领域模型

| 模型 ID（Model ID） | 模型能力 |
| --- | --- |
| decision-model-preview | 文本生成 |

> `auto` 模型不支持 `tool_choice`、`thinking.budget_tokens`（Anthropic 兼容）和 `thinking_budget`（OpenAI 兼容）参数。

<a id="支持的模型内置工具"></a>

<a id="tpp01-h-harness"></a>

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

<a id="tpp01-h-sub-mgmt"></a>

## 订阅管理

<a id="升级"></a>

<a id="tpp01-h-upgrade"></a>

### 升级

支持从低档位升级到更高档位。套餐升级不重置当前订阅周期：按当前订阅周期剩余天数补缴差价，当前周期仅按额度差折算发放新增 Credits，自下一个订阅月起按新档位月额度计量。

补差金额、新增额度的折算公式和示例见[用量与额度·升级额度计算](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-upgrade)。

升级后 Harness 权益的剩余额度计算详见[Harness 权益·升级后权益计算](token-plan-harness-benefits.md#tphb-h-upgrade)。

<a id="续费"></a>

<a id="tpp01-h-renew"></a>

### 续费

个人版支持包月、包季、包年订阅；续费支持切换续费周期，也可一次续费多个周期。

-   **手动续费**：支持选择不同续费时长，可续费多个周期。
-   **自动续费**：开启后到期前系统自动扣款续费。

续费不增加当前订阅周期的额度，规则见[用量与额度·额度规则](../token-plan-guide/token-plan-usage-quota.md#tpuq-h-reset)。

<a id="其他"></a>

<a id="tpp01-h-notice"></a>

### 其他

-   个人版暂不支持退订。
-   个人版不支持降配，如需更换为更低档位，可在订阅到期后重新购买。
-   订阅到期后 API Key 变为不可用；重新购买成功后，原 API Key 恢复可用，无需在工具中重新配置。
