# 用量与额度

Token Plan 的 Credits 计费规则、抵扣顺序、重置规则、额度用尽和用量异常排查。

<a id="凭证与计费边界"></a>

<a id="tpuq-h-boundary"></a>

## 凭证与计费边界

-   **Token Plan 专属 API Key（`sk-sp-`）**：用于 Token Plan 套餐调用，抵扣套餐额度和用量包。
    
-   **阿里云百炼通用 API Key（`sk-`）**：**仅用于抵扣个人版附赠的 Harness 权益额度**，**不能用于抵扣模型调用额度**。
    
-   **免费额度、资源包、节省计划和账户余额**：属于阿里云百炼按量计费体系，**与 Token Plan 额度相互独立**。
    

<a id="抵扣顺序"></a>

<a id="tpuq-h-order"></a>

## 抵扣顺序

1.  优先抵扣当前订阅月的套餐额度；团队版为当前坐席的月度额度。
2.  套餐额度用尽后，个人版自动抵扣用量包额度；团队版从共享用量包抵扣，持有多个共享用量包时优先抵扣最近到期的包。
3.  可用额度用尽后，消耗 Credits 的调用会被阻断，不会自动转为按量计费。可等待下一个订阅月重置、升级套餐或坐席、购买用量包或共享用量包。

Harness 权益不参与上述抵扣顺序。详见[Harness 权益](../token-plan-personal/token-plan-harness-benefits.md)。

<a id="额度规则"></a>

<a id="tpuq-h-reset"></a>

## 额度规则

<a id="重置与结转"></a>

### 重置与结转

-   额度按订阅月自动重置，每个订阅月开始时恢复为对应档位的满月额度。重置时间取决于订阅日期，不是每月 1 日。
-   订阅月内未用完的额度不结转至下一周期。

<a id="升级额度计算"></a>

<a id="tpuq-h-upgrade"></a>

### 升级额度计算

升级套餐或坐席不重置当前订阅周期：按当前订阅周期剩余天数补缴差价，当前周期仅按额度差折算发放新增 Credits，自下一个订阅月起按新档位月额度计量。

升级（含坐席升级场景）发放的 Credits 并非新档位的全额月额度，而是按实付补差金额和当前订阅周期的实际剩余有效时长折算得出，折算公式如下。

<a id="code-block"></a>

```text
升级补差金额 = (新档位价格 − 旧档位价格) × 剩余天数 ÷ 30
（不满一天按一天计算）

升级后当前周期新增额度 = 剩余天数 ÷ 30 × (升级后月额度 − 升级前月额度)
（不满一天按一天计算，结果向上取整）
```

实际补差金额以支付页面展示的价格明细为准。团队版按坐席升级，实际补差金额和可用额度以控制台展示为准。

例如：9 月 2 日订阅个人版 Lite 套餐（39 元/月，月额度 20,000 Credits），9 月 12 日升级至 Essential 套餐（79 元/月，月额度 45,000 Credits），当前订阅周期剩余 20 天：补差金额为 (79 − 39) × 20 ÷ 30 ≈ 26.67 元，当前周期新增额度为 20 ÷ 30 × (45,000 − 20,000) ≈ 16,667 Credits（向上取整）。

升级后 Harness 权益的剩余额度计算详见[Harness 权益·升级后权益计算](../token-plan-personal/token-plan-harness-benefits.md#tphb-h-upgrade)。

<a id="续费与加购"></a>

### 续费与加购

-   续费仅延长订阅有效期，不增加当前订阅周期的额度。
-   加购坐席的费用和 Credits 按剩余时长折算，与现有订阅统一到期。

<a id="credits-消耗规则"></a>

<a id="tpuq-h-example"></a>

## Credits 消耗规则

Credits 是 Token Plan 的统一计量单位，不等于 Token。

个人版和团队版采用相同的 Credits 计费逻辑。不同模型的单价不同，单次请求的 Credits 由输入 Token、缓存 Token 和输出 Token 共同决定。以团队版 `qwen3.6-plus` 为例：

| Token 类型 | 数量 | 消耗 Credits |
| --- | --- | --- |
| 输入 Token | 8,349 | 1.67 |
| 缓存 Token | 40,794 | 0.82 |
| 输出 Token | 573 | 0.69 |
| 合计 | — | 约 3.18 Credits |

影响单次消耗的主要因素：

-   模型单价：高价模型在相同 Token 数下消耗更多 Credits。
-   上下文长度：历史消息越长，输入 Token 越多。
-   思考模式：开启思考会增加输出 Token。
-   工具调用：通过模型接口触发的内置工具、MCP 工具和子任务会增加模型调用次数，消耗 Credits；通过 `sk-` 直接调用的 Harness 权益工具不消耗 Credits。
-   缓存命中：缓存命中的 Token 单价通常低于正常输入 Token。

> **说明**
>
> 单次实际消耗以控制台**用量分析**为准；需要预估时，建议先用较短任务试跑，再查看用量分析中的消耗明细。

<a id="降低-credits-消耗"></a>

<a id="tpuq-h-save"></a>

## 降低 Credits 消耗

Credits 消耗主要受上下文长度、模型单价、思考模式、工具调用和任务类型影响。

<a id="对话与上下文"></a>

### 对话与上下文

-   压缩历史消息或新开对话，避免长上下文累积。
-   简单任务关闭思考模式，减少输出 Token。

<a id="模型与工具"></a>

### 模型与工具

-   非复杂任务改用轻量模型，例如用 `qwen3.8-flash` 替代 `qwen3.8-max`。
-   减少不必要的工具调用、MCP 调用和多 Agent 并行。
-   重复内容利用缓存，缓存命中的 Token 单价低于正常输入 Token。

<a id="视频等多模态"></a>

<a id="tpuq-h-multimodal"></a>

### 视频等多模态

视频生成等多模态模型的单次消耗高于文本对话，且随时长、分辨率上升。异步任务在完成后统一结算，集中提交可能快速触顶；首次使用建议先用较短时长、较低分辨率试跑。

<a id="夜间折扣"></a>

### 夜间折扣

个人版和团队版在每晚 22:00 - 次日 08:00 对部分模型提供 Credits 折扣，具体模型、折扣和活动有效期见[个人版支持的模型](../token-plan-personal/token-plan-personal-overview.md#tppo-h-models)和[团队版支持的模型](../token-plan-team-edition/token-plan-team-overview.md#tpto-h-models)。

<a id="用量监控"></a>

### 用量监控

个人版用户可在[**个人版用量详情**](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal/usage-detail)中查看模型消耗。

团队管理员可在[**团队用量分析**](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/usage)中按模型和成员查看消耗。

<a id="额度用尽与恢复"></a>

<a id="tpuq-h-exhausted"></a>

## 额度用尽与恢复

套餐额度和用量包（含团队版共享用量包）都用尽后，消耗 Credits 的模型调用会被阻断，不会自动按量计费。恢复方式：

-   **等待重置**：下一个订阅月开始后，套餐额度自动恢复。
-   **升级套餐或坐席**：按剩余天数折算新增额度，详见[升级额度计算](#tpuq-h-upgrade)。
-   **购买用量包或共享用量包**：个人版用量包见[个人版·套餐档位与定价](../token-plan-personal/token-plan-personal-overview.md#tppo-h-pricing)，团队版共享用量包见[团队版·共享用量包](../token-plan-team-edition/token-plan-team-overview.md#tpt01-h-shared)。

<a id="用量异常排查"></a>

<a id="tpuq-h-troubleshooting"></a>

## 用量异常排查

额度用尽、限流、并发限制和鉴权错误的区别，见[接入报错与限流](token-plan-faq.md#tpt-h-scenarios)。

如果消耗比预期快，检查上下文长度、思考模式、模型单价、工具调用和异步任务结算，详见[一次调用消耗多少 Credits](#tpuq-h-example)和[如何降低 Credits 消耗](#tpuq-h-save)。

<a id="第三方工具统计不一致"></a>

### 第三方工具统计不一致

第三方工具（如 Claude Code）显示的 Token 用量可能低于百炼控制台，常见原因：

-   **统计口径不同**：第三方工具只显示模型输入输出 Token，控制台统计包含完整消耗项。
-   **隐藏消耗**：系统提示词、工具定义（Schema）、项目约定、多轮对话历史、工具调用参数与返回结果、模型推理内容等都会计入 Credits，但不在工具中显示。
-   **模型单价不同**：相同 Token 数下，高价模型的 Credits 消耗更高。

<a id="按量扣费"></a>

### 按量扣费

常见原因：

-   **生效前调用**：开通 Token Plan 之前发生的调用属于独立计费，无法被套餐抵扣。
-   **配置错误**：未使用 Token Plan 专属 API Key（`sk-sp-` 开头）和 Base URL，例如误用百炼通用地址 `dashscope.aliyuncs.com` 或 Coding Plan 的 Key。

已产生的按量费用无法通过 Credits 事后抵扣或退款。请立即检查 API Key 和 Base URL，确保后续调用正常抵扣。

<a id="用量为-0"></a>

### 用量为 0

-   尚未产生实际消耗。
-   使用了非 Token Plan 专属 API Key。

如果用量为 0 但仍有调用，检查是否在工具中误用了阿里云百炼通用 API Key 并产生按量计费。
