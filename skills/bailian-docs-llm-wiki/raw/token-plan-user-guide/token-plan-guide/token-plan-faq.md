# Token Plan 常见问题

Token Plan 的版本选择、购买订阅、退订退款、使用限制和接入问题。

## 产品与版本

### 个人版和团队版有什么区别？

个人版面向个人开发者，按套餐档位订阅；团队版面向团队和企业，按坐席订阅，提供坐席管理、成员用量分析和 SSO 接入。两者在额度机制、数据安全和高峰期性能上也有差异，完整对比见[个人版订阅与权益](raw/token-plan-user-guide/token-plan-personal/token-plan-personal-overview.md)和[团队版订阅与权益](raw/token-plan-user-guide/token-plan-team-edition/token-plan-team-overview.md)。

### 个人版和团队版能同时买吗？额度是分开算的还是共享的？

可以同时购买。同一阿里云账号可以同时持有个人版和团队版，各自独立计费，额度不共享。

### 个人版可以升级或更换为团队版坐席吗？

不可以。个人版和团队版是独立产品，额度不共享，不支持将个人版直接升级或更换为团队版坐席。如需使用团队版，请单独订阅团队版。个人版暂不支持退订，可在订阅到期后不再续费。

### 团队版的 API Key 能用在个人版上吗？

不能。个人版和团队版各自生成独立的 API Key，不可混用。系统会根据 API Key 自动识别对应的套餐。

### 已有个人版，再买团队版会冲突吗？

不冲突。两者可以同时持有，各自独立计费。使用时根据 API Key 自动匹配对应套餐。

### Token Plan 支持哪些模型？

支持千问、万相、DeepSeek、月之暗面、智谱 AI、MiniMax、HappyHorse 等模型，个人版和团队版的模型范围不同。完整列表见[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的模型。

### 支持 Cursor、Claude Code、Cline 等第三方工具吗？

支持。Token Plan 兼容 OpenAI 和 Anthropic 协议，任何支持自定义 Base URL 和 API Key 的工具均可接入。配置方法见[快速开始](raw/token-plan-user-guide/token-plan-guide/token-plan-overview.md)。

### 模型内置工具是什么？

模型内置工具是模型自带的扩展能力，包括联网搜索、文搜图、图搜图、网页抓取和代码解释器。通过 Responses API 调用模型时自动触发，按 Credits 抵扣。个人版和团队版均支持。

Harness 权益中的同名工具通过 `sk-` 开头的百炼 API Key 调用，计入 Harness 权益额度，不占用 Credits。详见 [Harness 权益](raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。

### Harness 权益会占用 Credits 吗？

不会。Harness 权益是个人版 Standard、Pro 套餐附赠的 AgentStudio 工具免费额度与折扣，独立计量，不占用套餐 Credits 或用量包。Harness 服务使用百炼 API Key（`sk-` 开头），Token Plan 专属 API Key（`sk-sp-` 开头）仅用于模型调用。详见[Harness 权益](raw/token-plan-user-guide/token-plan-personal/token-plan-harness-benefits.md)。

### Token Plan 是否提供免费试用额度或赠送 Token？

Token Plan 套餐本身不提供试用额度，也不包含免费赠送的 Token 额度。百炼平台针对部分模型提供独立的免费额度，可以在控制台查询可用免费额度的模型列表。

## 购买与订阅

### RAM 子账号可以使用 Token Plan 吗？

可以。RAM 子账号需要主账号授予 Token Plan 权限和费用中心权限：个人版费用中心策略为 `AliyunBSSReadOnlyAccess`，团队版为 `AliyunBSSFullAccess`。完整授权步骤和权限对照见[权限与使用规范·账号与权限](https://help.aliyun.com/zh/model-studio/token-plan-permissions-and-usage#tppu-h-access)。

**说明**RAM 授权与坐席分配是两个独立概念：RAM 授权决定谁可以管理订阅；坐席分配决定谁可以使用模型。团队版成员仍需在团队管理中分配坐席后才能获得 API Key。

### 可以升配吗？升配后额度怎么算？

支持从低档位升级到更高档位。升级不重置当前订阅周期：按剩余天数补缴差价，并按新档位与原档位的月额度差折算发放当前周期新增 Credits，自下一个订阅月起按新档位额度计量。

折算公式和示例见[用量与额度·升级额度计算](https://help.aliyun.com/zh/model-studio/token-plan-usage-quota#tpuq-h-upgrade)。

### 可以降配吗？

不支持降配。如需更换为更低档位或坐席类型，可在订阅到期后重新购买或重新订阅。详见[个人版·其他](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-notice)和[团队版·注意事项](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-sub-notice)。

### 自动续费怎么取消？

-   个人版：登录[百炼控制台 Token Plan](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan) 页面，在订阅管理中关闭自动续费。
-   团队版：登录[费用中心 > 续费管理](https://usercenter2.aliyun.com/finance/renew-manage)，找到 Token Plan 团队版订单，关闭自动续费。

### 续费后需要重新配置 API Key 吗？

不需要。续费、订阅到期后重新购买、退订坐席后重新购买均不会变更已分配坐席的 API Key；订阅到期或退订期间 API Key 暂时不可用，续费或重新购买成功后即恢复可用。

### 如何查看套餐的生效时间和剩余天数？

-   **生效时间**：登录[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan)的 **Token Plan** 页面查看。
-   **剩余天数**：控制台显示的剩余天数为向下取整后的完整 24 小时周期数。例如剩余 22 天 20 小时会显示为 22 天，实际有效期以结束时间为准。

### 是否支持学生代金券购买？

不支持。学生代金券仅适用于活动界面指定的产品，不能用于购买 Token Plan。

### 从未购买过 Token Plan 个人版，为什么无法享受新用户限时价？

新用户限时价按同一用户判定，不按单个阿里云账号判定。同一用户拥有的多个阿里云账号互为关联账号（同人账号）；阿里云根据注册、登录、使用中的关联信息（如手机号、邮箱、证件）判断多个账号是否属于同一用户。同一用户下任一关联账号购买过 Token Plan 个人版后，其他账号不能再享受该优惠；同一用户仅可享受一次。

### 限时优惠的计费规则是什么？

限时优惠适用于新购、续费、自动续费、加购坐席和升级坐席。

加购坐席或升级坐席时，按剩余时长折算费用，实际收费取折算金额与限时价中的较低值。

**示例**：标准坐席原价 ¥198/月，限时价 ¥150/月。

-   加购时按剩余时长折算为 ¥99，低于限时价，实际收取 ¥99。
-   加购时按剩余时长折算为 ¥165，高于限时价，实际收取 ¥150。

## 退订与退款

### 个人版可以退订吗？

个人版暂不支持退订。可在订阅到期后不再续费。

### 团队版可以退订坐席吗？

可以按坐席维度退订，已有用量消耗的坐席不可退订。退款原路退回支付账户，预计 1-3 个工作日到账。操作见[团队版·退订坐席](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-refund)。

## 使用限制

### "禁止 API 生产自动化调用"具体是什么意思？

Token Plan 个人版仅供个人通过官方指定工具（如 Cursor、Claude Code 等）进行交互式开发。不允许将 API Key 用于生产环境的自动化服务、批量脚本或后台定时任务等非交互场景。

### 团队成员能查看团队用量吗？

不能。团队成员无法查看团队订阅、席位额度和共享用量包余量，需由所有者或管理员查看。详见[团队管理·角色与权限](https://help.aliyun.com/zh/model-studio/token-plan-team-management#tpt03-h-roles)。

### 数据会用于训练模型吗？

个人版在使用期间会将模型输入和生成内容用于服务改进与模型优化；团队版不会使用对话数据训练模型。详见[权限与使用规范·数据使用政策](https://help.aliyun.com/zh/model-studio/token-plan-permissions-and-usage#tppu-h-data)。

### 多人共用一个账号可以吗？

不可以。Token Plan 个人版限单人使用，不允许多人共用同一账号或 API Key。如需多人协作，请使用 Token Plan 团队版。

### 可以在多台设备上使用同一个 API Key 吗？

可以。同一个 API Key 可以配置到本人的多台设备上使用，但仅限本人使用。重置 API Key 会使旧 Key 立即失效，届时需在全部设备上更新为新 Key；建议仅在 Key 泄露时重置。

### 最多支持多少个 Agent 并发？

个人版并发能力与套餐档位相关：

档位

建议并发

Lite

1-2 个 Agent

Essential

2-3 个 Agent

Standard

3-4 个 Agent

Pro

6-8 个 Agent

### 高峰期响应会变慢吗？

个人版高峰期可能出现排队等待。如需更稳定的吞吐，可升级到更高档位或使用团队版。团队版基于多租户隔离架构，调用高峰期间不排队。

### 限流阈值（TPM/RPM）是多少？能否提升？

限流阈值会根据整体负载动态调整，以保障服务稳定性。套餐限流额度不支持提升。遇到限流时可精简上下文、降低任务复杂度，等待约 1 分钟后重试。

### 团队版有并发限制吗？

团队版存在并发限制。平台会根据整体资源负载动态调整并发上限，触发并发限制时，等待片刻后重试即可。

## 接入与报错

### 先区分四种情况

现象

原因

处理方式

429 insufficient\_quota

套餐额度或用量包额度用尽

等待重置、升级、购买用量包或共享用量包

429 Requests rate limit exceeded

短时间请求过于密集

等待约 1 分钟后重试，降低请求频率

并发限制

同时运行的 Agent 数量超过档位建议值

减少同时运行的 Agent，或升级到更高档位

401、403、404

API Key、Base URL 或模型配置错误

检查 Key 前缀、Base URL 和模型 ID

### 排查顺序

1.  确认 API Key 以 `sk-sp-` 开头，且与 Token Plan 的 Base URL 配套使用。
2.  确认模型 ID 在[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的模型中，且适用于当前版本。
3.  在控制台**我的订阅**和**用量分析**页面确认额度是否用尽。
4.  查看报错信息是 `insufficient_quota`、`Requests rate limit exceeded` 还是鉴权错误。

### 常见报错

报错信息

可能原因

解决方案

`401 InvalidApiKey: No API-key provided.`

请求头中未携带 API Key

生成 API Key 并在工具中完成配置

`401 InvalidApiKey: Invalid API-key provided.`

误用了按量计费的 API Key 或 Coding Plan 的 Key；订阅过期；Key 复制不完整

确认使用 Token Plan 套餐 API Key，确保完整且无空格

`404 model_not_found: Model not exist.`

模型名称拼写错误或不在支持列表

确认模型名称区分大小写，与套餐支持的模型 ID 一致

`404 model 'xxx' not found or not supported`

模型名称拼写错误或不在支持列表

确认模型名称区分大小写，与套餐支持的模型 ID 一致

`403 AccessDenied.Unpurchased: Access to model denied.`

调用的模型仅团队版支持，个人版不支持

改用个人版支持的模型，或使用 Token Plan 团队版

`401 invalid access token or token expired`

误用了 Coding Plan 或其他计费模式的 Base URL

使用 Token Plan 的 Base URL

`401 Incorrect API key provided`

误用了百炼通用 Base URL（`dashscope.aliyuncs.com`）

使用 Token Plan 的 Base URL

`400 Range of input length should be [1, xxx]`

输入内容超出模型最大上下文长度

新建会话清空历史，或使用工具的上下文压缩命令

`400 invalid_parameter_error: Unexpected item type in content.`

向纯文本模型传入了图像等非文本内容

改用支持该模态的模型，或确认请求内容与模型能力匹配

`400` 调用图像或视频生成模型报错

图像、视频生成模型使用独立接口，无法通过文本模型的 Base URL 直接调用

通过工具的 Skill、Slash Command 或 Agent 扩展机制接入

`429 Requests rate limit exceeded`

短时间内请求过于密集；多个 Agent 并行时也可能触发并发上限

等待约 1 分钟后重试，降低请求频率和并发数

`429 insufficient_quota: Your token-plan quota has been exhausted.`

套餐额度或用量包额度用尽

购买用量包、升级套餐，或等待下一个订阅月额度重置

`502 Bad Gateway`

服务端偶发异常

稍后重试

### 额度用尽

返回 `429 insufficient_quota` 表示额度已用尽。此时调用被阻断，不会自动转为按量计费。抵扣顺序和恢复方式见[用量与额度·额度用完了怎么办](https://help.aliyun.com/zh/model-studio/token-plan-usage-quota#tpuq-h-exhausted)。

### 限流与并发

返回 `429 Requests rate limit exceeded` 表示触发限流，不是额度用尽。限流阈值会根据整体负载动态调整，套餐限流额度不支持提升。等待约 1 分钟后重试，并精简上下文、减少并发或降低请求频率；团队版同样存在并发限制。

### 鉴权与配置

Token Plan、Coding Plan 和按量付费的 API Key 与 Base URL 相互隔离，必须配套使用：

-   **Token Plan**：`sk-sp-` 开头的 API Key + Token Plan Base URL。
-   **Coding Plan**：Coding Plan API Key + `https://coding.dashscope.aliyuncs.com/v1`。
-   **按量付费**：百炼 API Key（`sk-` 开头）+ `https://dashscope.aliyuncs.com/compatible-mode/v1`。

Base URL 见[接入AI工具·通用配置](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool#tpa-h-config)，支持的模型见[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)。

## 用量问题

额度怎么计算、何时重置、用完了怎么办、在哪里查看、为什么消耗异常，统一见：

-   [用量与额度](raw/token-plan-user-guide/token-plan-guide/token-plan-usage-quota.md)
-   [查看用量](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)
