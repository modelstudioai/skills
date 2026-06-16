# 常见问题

Token Plan 团队版常见问题汇总，涵盖购买、使用、计量和性能相关的问题解答。

## **Token Plan 团队版和 Coding Plan 有什么区别？**

**Token Plan 团队版**

**Coding Plan**

适用场景

一人公司/团队/企业日常办公

个人开发场景

支持的模型

文本生成、图像生成模型

文本生成模型

计费方式

按 Token 消耗抵扣 Credits

按模型调用次数

使用频次

无每 5 小时/每周限额

每 5 小时/每周限额

API Key 和 Base URL

在[管理后台](https://tokenplan-enterprise.bailian.console.aliyun.com)生成专属 API Key，Base URL 详见[快速开始](https://help.aliyun.com/zh/model-studio/token-plan-quickstart)

在[Coding Plan 页面](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/coding-plan)获取专属 API Key 和专属 Base URL

高峰期性能

多租户隔离

高峰期间可能排队

数据安全

承诺不使用数据训练模型

用户数据授权

## **接入与调用**

### **如何在编程工具中使用图像生成模型？**

图像生成模型使用独立的接口，无法通过文本模型的 Base URL 直接调用。需要通过工具的 Skill 或扩展机制接入，具体配置方法请参见各工具的[接入文档](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/)中的接入图像生成模型章节。

### **常见报错及解决方案**

**报错信息**

**可能原因**

**解决方案**

**401 InvalidApiKey: No API-key provided.**

请求头中未携带 API Key（`Authorization: Bearer` 或 `x-api-key` 均未传）。

在管理后台生成 API Key，并在工具中完成配置。

**401 InvalidApiKey: Invalid API-key provided.**

1.  误用了百炼通用 API Key（sk-xxx 格式）或 Coding Plan 的 API Key
    
2.  Token Plan 团队版订阅过期
    
3.  API Key 复制不完整或包含空格
    

1.  确认使用的是 Token Plan 专属 API Key，确保完整且无空格。
    
2.  确认订阅是否过期。
    
3.  如仍报错，重置 API Key，重置后使用新 Key 配置。
    

**404 model 'xxx' not found or not supported**

**400 Model not exist.**

1.  模型名称拼写错误或大小写错误
    
2.  模型 ID 不在套餐支持列表中
    

1.  确认模型名称区分大小写，与套餐支持的模型 ID 一致。
    
2.  检查所选套餐是否包含该模型。
    

**401 invalid access token or token expired**

误用了 Coding Plan 或其他套餐的 Base URL

Anthropic 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

OpenAI 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

**401 Incorrect API key provided**

误用了百炼通用 Base URL（dashscope.aliyuncs.com）

Anthropic 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`

OpenAI 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

**400 InvalidParameter: Range of input length should be \[1, xxx\]**

输入内容（含对话历史、代码上下文等）超出模型的最大上下文长度

新建会话清空历史，或使用工具自带的上下文压缩命令（如 Claude Code 的 `/compact`、Qwen Code 的 `/clear`）。也可切换上下文窗口更大的模型。

**400 InvalidParameter: url error, please check url！**

Base URL 路径与协议不匹配。例如把 OpenAI 兼容路径配在 Anthropic 端点上，或反之。

按工具实际使用的协议选择对应的端点：

-   Anthropic 兼容协议（Claude Code 等）：以 `/apps/anthropic` 结尾。
    
-   OpenAI 兼容协议（Cursor、Qwen Code 等）：以 `/compatible-mode/v1` 结尾。
    

**400 InvalidParameter: Range of max\_tokens should be \[1, xxxx\]**

请求中的 `max_tokens`（或工具配置中的最大输出长度）超出当前模型支持的最大输出 Token 数。

将 `max_tokens` 调整为不超过报错信息中提示的上限值。

**400 invalid\_parameter\_error: The thinking\_budget parameter must be a positive integer and not greater than xxxxx**

工具配置中的思维链长度（如 `thinking_budget`、`budgetTokens`）超过当前模型支持的上限。各模型上限不同，以报错中的数值为准。

将思维链长度调整为不超过报错提示的上限值，或在不支持思考模式的模型上移除该配置项。

**400 data\_inspection\_failed: Input text data may contain inappropriate content.**

输入或输出命中平台内容安全策略。

修改输入内容后重新提交。如多次触发，调整提示词避免敏感话题。

**429 API-Key Requests rate limit exceeded, please try again later.**

短时间内请求过于密集，触发模型调用限流。

等待一分钟后重试；如频繁触发请降低请求频率，并确认 API Key 未被他人共享使用。

**429 Throttling.AllocationQuota: Allocated quota exceeded, please increase your quota limit.**

**insufficient\_quota: You exceeded your current quota, please check your plan and billing details.**

套餐 Token 已用完，坐席额度和共享用量包均已耗尽。

可加购坐席（加购后需将新坐席分配给成员后再使用）、加购共享用量包，或等待下一计费周期额度自动重置。

**Connection error**

Base URL 域名拼写错误或网络连接异常

检查 Base URL 域名拼写及网络连接。

## **产品功能相关**

### **Token Plan 团队版的 API Key 能与其他套餐或普通 API 混用吗？**

不能。Token Plan 团队版、Coding Plan 和百炼按量计费三者的 API Key 和 Base URL 互不相通，请勿混用。误用其他 API Key 不会抵扣 Token Plan 团队版的套餐额度。

### **能在多个工具中使用同一订阅吗？**

可以。同一 API Key 可在全部兼容的 AI 编程和智能体工具中使用，额度共享消耗。每个成员持有独立的 API Key，不可共享给其他成员。

### **有哪些使用限制？**

仅限在兼容的 AI 编程和智能体工具中交互式使用，不可用于自动化脚本或应用后端。违规使用可能导致订阅暂停或 API Key 封禁。

### **团队管理入口在哪里？**

阿里云主账号或 RAM 用户登录[Token Plan 控制台](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/token-plan)后，在左侧菜单使用**我的订阅**、**成员**、**设置**等功能；也可点击**进入管理平台**跳转独立管理平台。通过 SSO 或钉钉加入的成员，通过管理员分发的**管理平台地址**登录管理平台。详见[访问入口](https://help.aliyun.com/zh/model-studio/token-plan-team#tp05-enter)。

### **成员如何获取 API Key？**

管理员在管理后台创建成员账号并分配席位后，为成员生成 API Key。成员无法自行生成，需联系管理员获取。详见[团队管理](https://help.aliyun.com/zh/model-studio/token-plan-team)。

## **购买相关**

### **可以同时购买多个套餐吗？**

每个阿里云账号限购一个订阅，同一订阅下每种坐席类型均可购买多个。共享用量包可叠加购买，单次最多 1000 个。

### **可以单独购买共享用量包吗？**

不可以。共享用量包是 Token Plan 团队版的附加商品，需先订阅 Token Plan 团队版坐席套餐后，才能购买共享用量包。

### **套餐是否支持退订？**

支持按席位退订。在控制台**我的订阅**页面点击席位的**退订**，已有用量消耗的席位不可退订。退款原路退回支付账户，预计 1-3 个工作日到账。详见[订阅管理](https://help.aliyun.com/zh/model-studio/token-plan-overview#tp01-sub-mgmt)。

### **阿里云账号欠费是否影响 Token Plan 团队版的使用？**

Token Plan 团队版为预付费订阅产品，只要套餐额度未用尽且订阅仍在有效期内，阿里云账号欠费不影响 Token Plan 团队版的正常使用。

## **计量相关**

### **Credits 抵扣规则是什么？**

Token Plan 团队版实际消耗取决于每次请求中输入 Token、缓存 Token 和输出 Token 的组合。优先从坐席额度抵扣，坐席额度用尽后从共享用量包抵扣，全部用尽后服务暂停至下一计费周期或购买共享用量包补充额度。

### **如何查看用量？**

在[Token Plan 团队版页面](https://bailian.console.aliyun.com/?tab=plan#/efm/subscription/overview)可查看套餐和共享用量包的用量详情。管理员还可在[管理后台](https://tokenplan-enterprise.bailian.console.aliyun.com)的用量分析页面查看全部成员的消耗明细。

### **用量如何重置？**

坐席额度在每个订阅月到期时重置，未用完的额度不累积到下月。共享用量包的额度同样按月重置。

### **超出限额之后怎么办？**

坐席额度用尽后自动从共享用量包抵扣；全部额度用尽后服务暂停。可通过以下方式恢复：

-   购买共享用量包补充额度。
    
-   等待下一计费周期额度自动重置。
    

### **续费后为什么 Credits 没有增加？**

Token Plan 团队版的坐席额度在每个订阅月到期时自动重置，续费仅延长订阅有效期，不会立即增加当月额度。若当前月额度已用尽，可通过以下方式补充：

-   购买共享用量包补充额度。
    
-   升级至更高规格的坐席。
    
-   等待下一计费周期额度自动重置。
    

## **数据安全**

### **数据安全如何保障？**

Token Plan 团队版承诺不使用对话数据训练模型，传输过程采用 HTTPS 加密，并基于多租户隔离架构保障企业级数据隔离。
