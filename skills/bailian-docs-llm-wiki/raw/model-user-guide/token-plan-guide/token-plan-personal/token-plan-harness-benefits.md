# Harness 权益

Token Plan 个人版 Standard 与 Pro 套餐附赠 Harness 权益，覆盖 AgentStudio 工具的每月免费额度与后付费折扣，使用百炼 API Key 调用，不占用套餐 Credits。

## 权益概览

Standard 与 Pro 套餐在模型 Credits 之外，额外附赠 Harness 权益：

-   **每月免费额度**：覆盖联网搜索、图像生成、语音合成等 AgentStudio 工具，额度按月发放。
-   **后付费 88 折**：免费额度用尽后，超出部分按原目录价 88 折继续计费。
-   **不占用 Credits**：Harness 权益消耗独立计量，不从套餐 Credits 或用量包抵扣。

Lite 套餐不包含 Harness 权益；团队版不支持 Harness 权益。

## 工具与每月免费额度

下表为 Standard 与 Pro 套餐各工具的每月免费额度，未列免费额度的工具仅享 88 折后付费。

**分类**

**工具**

**Standard 每月额度**

**Pro 每月额度**

自研工具

联网搜索增强版

100 次

500 次

垂类搜索

100 次

500 次

网页解析

1,000 次

5,000 次

图像生成

20 张

50 张

语音合成

1 万字符

1 万字符

语音识别

5 小时

5 小时

视频生成

—

—

代码解释器

100 次

500 次

百炼知识库

知识库 RAG

—

—

百炼记忆库

记忆库 Memory

—

—

百炼全托管智能体

托管智能体 Managed Agent

—

—

百炼沙箱

云沙箱 Sandbox

—

—

“—”表示该工具无每月免费额度，仍享 88 折后付费。额度数值与折扣以[控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/overview)订阅页展示为准。

## 计费与抵扣

-   Harness 权益消耗独立计量，不从套餐 Credits 或用量包抵扣。
-   免费额度优先抵扣；用尽后超出部分按原目录价 88 折后付费。
-   Harness 权益与模型 Credits 抵扣相互独立，两者不混算。
-   **API Key 说明**：Harness 权益工具通过百炼 API Key（格式为 sk-xxx）调用 MCP 服务，消耗计入 Harness 权益额度与折扣；与 Token Plan 专属 API Key（格式为 sk-sp-xxx，用于模型调用、按 Credits 抵扣）不同，两者不可混用。

**重要**查看各工具的折后单价与折扣明细，在控制台 Harness 权益页签点击对应工具的“查看明细”。

### 额度升配

套餐升级后（如从 Standard 升到 Pro），Harness 权益的剩余额度按以下公式计算：

```
剩余权益额度 =（原档位总次数 − 已用次数）+（新档位总次数 − 原档位总次数）× 剩余天数 ÷ 30
```

-   原档位总次数 − 已用次数：原档位剩余次数，直接继承。 -（新档位总次数 − 原档位总次数）× 剩余天数 ÷ 30：新档位比原档位多的额度，按剩余天数折算补偿。

向上取整，具体以控制台升级页展示为准。

例如：Standard 每月 100 次、已用 20 次，Pro 每月 500 次，剩余 10 天，则剩余 = (100−20) + (500−100)×10÷30 ≈ 214 次。

## 接入方式

接入流程详见[快速开始](https://help.aliyun.com/zh/model-studio/token-plan-personal-quick-start#tpp02-h-optional-tool)或[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-personal/token-plan-harness-tool.md)。在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)我的订阅 Harness 权益页签可查看可用工具与额度。

## 注意事项

-   **权益归属**：Harness 权益为 Standard 与 Pro 套餐附赠，随订阅周期发放；续费、升配后的权益发放规则以控制台展示为准。
-   **额度刷新**：每月免费额度按订阅周期发放，未用完的额度不结转，具体刷新规则以控制台为准。
-   **退订**：个人版不支持自助退订；Harness 权益随订阅失效而终止。
-   **地域**：Token Plan 个人版目前仅支持华北2（北京）地域。

## 常见问题

### Harness 权益的抵扣顺序是什么？

先抵扣对应服务本身的免费额度（如各产品自带的试用/新用户额度），再抵扣 Token Plan 附赠的权益额度；权益额度用尽后，超出部分按对应服务的折扣价继续按量计费。

### Harness 调用使用哪个 API Key？

Harness 服务（联网搜索、图像生成、代码解释器、RAG、Memory、Managed Agent、Sandbox 等）使用百炼 API Key（以 `sk-` 开头）和百炼标准 Base URL 接入。系统自动识别账号下的 Token Plan 订阅并应用附赠权益，无需切换到 Token Plan 专属凭证。Token Plan 专属 API Key（以 `sk-sp-` 开头）仅用于模型调用抵扣 Credits，不用于 Harness 服务。

### Harness 调用会消耗套餐 Credits 吗？

不会。Harness 权益独立核算，调用只扣自身权益次数/额度，超出部分按折扣价走按量账单，不占用套餐 Credits，也不占用用量包。

### 在哪查看 Harness 权益的剩余额度？

在百炼控制台**我的订阅**页面切换到**Harness 权益**页签，查看各工具的免费额度发放状态、剩余次数与到期时间。

### 加量包能否抵扣 Harness 服务的费用？

不能。用量包仅用于补充 Token Plan 套餐的模型 Credits 额度，Harness 权益独立核算，超出权益部分按对应服务的折扣价走按量账单，不占用用量包。
