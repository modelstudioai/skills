# Token Plan 概述

Token Plan 是阿里云百炼推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。Token Plan 提供个人版和团队版两个版本，满足从个人开发者到企业团队的不同需求。

**说明**Token Plan 目前仅支持**华北2（北京）**地域，请在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan)左上角将地域切换至**华北2（北京）**后购买并使用。

## 产品简介

Token Plan 采用 Credits 统一抵扣机制，一份订阅即可在 Claude Code、Cursor、Qwen Code、Codex、Qoder、Qoder CN、OpenClaw 等主流 AI 编程和智能体工具中使用。支持文本生成、图像生成、视频生成、语音识别、实时语音对话等多种模型，以及联网搜索、代码解释器等 Harness 工具。

Token Plan 兼容 OpenAI 和 Anthropic 接口协议，任何支持自定义 **Base URL** 和 **API Key** 的工具均可接入，判定标准是 API 协议兼容性，而非工具的界面形态。不调用标准 API 的自研工具无法配置专属 API Key，因此不能抵扣 Token Plan 套餐额度，此类场景建议改用以 `sk-` 或 `sk-ws-` 开头的按量付费 API Key。

-   **个人版**：面向个人开发者，提供 Lite、Standard、Pro 三档套餐，设有 7 天的 Credits 限额，档位越高额度越大。
-   **团队版**：面向团队和企业，提供标准座席、高级座席、尊享座席三个档位，支持多席位管理、用量分析，承诺不使用数据训练模型。

## 个人版

**Lite 套餐**

**Standard 套餐**

**Pro 套餐**

**用量包**

**定价**

原价 60 元/月  
限时 **39 元/月**

原价 180 元/月  
限时 **139 元/月**

原价 600 元/月  
限时 **499 元/月**

100 元/个/月  
20,000 Credits/个

**每 7 天限额**

2,500 Credits

10,000 Credits

40,000 Credits

无限制

**并发 Agent**

1-2 个

3-4 个

6-8 个

\-

**购买条件**

\-

需有效订阅，最多 5 个

**模型**

支持文本生成、图像生成、视频生成、语音识别、实时语音对话等多种模型（[查看完整列表](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-models)）

**Harness 工具**

支持多种 Harness 工具，以 Credits 统一抵扣（[查看详情](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tpp01-h-harness)）

## 团队版

**标准座席 Standard**

**高级座席 Pro**

**尊享座席 Max**

**共享用量包 Extra Bundle**

**定价**

原价 198 元/座席/月  
限时 **150 元/座席/月**

原价 698 元/座席/月  
限时 **550 元/座席/月**

**1,398 元/座席/月**

5,000 元/个/月

**每月总额度**

25,000 Credits/座席/月

100,000 Credits/座席/月

250,000 Credits/座席/月

625,000 Credits/个

**7 天限额**

无限制

**模型**

支持文本生成、图像生成、视频生成、语音识别、实时语音对话等多种模型（[查看完整列表](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpt01-h-models)）

**Harness 工具**

支持多种 Harness 工具，以 Credits 统一抵扣（[查看详情](https://help.aliyun.com/zh/model-studio/token-plan-harness-tool#tpws-h-models-team)）

**团队管理**

支持多席位管理和用量分析（[团队管理](raw/model-user-guide/token-plan-guide/token-plan-team-edition/token-plan-team-management.md)）

## 套餐限额

### 个人版

个人版采用 7 天固定窗口限额，限额单位为 Credits：

-   **7 天限额**：自首次调用起开启 7 天计时窗口，窗口期内累计消耗达到限额后暂停服务，需等待满 7 天后额度重置。

限额触顶即暂停服务，可购买用量包补充额度继续使用，或等待窗口周期结束后额度重置。窗口期内未用完的额度不结转至下一周期。

### 团队版

团队版采用月度总额度制，无 7 天窗口限额。每个座席的月度额度在计费周期内可用，到期未使用的额度不结转。超出月度总额度后调用将被阻断，可购买共享用量包补充额度。计费周期按订购日起算（订阅月，非自然月）。例如 6 月 4 日订阅，则本计费周期有效期至下月 4 日。订阅后，系统按订阅月一次性发放全量月度额度，而非按天发放。续费仅延长订阅有效期，不会为当前计费周期叠加补充额度。

## 常见问题

### 个人版和团队版可以同时购买吗？

可以。同一阿里云账号可以同时持有个人版和团队版，各自独立计费。

### 关于 Coding Plan

Coding Plan 和 Token Plan 是两个独立的订阅产品，两者之间无法迁移或升级。Coding Plan Lite 已于 2026 年 3 月 20 日停止新购，2026 年 4 月 13 日停止续费和升级；Coding Plan Pro 为限量抢购，库存售罄后不再补充。推荐使用 **Token Plan**，支持更多模型和 Harness 工具。

### 为什么自研工具界面和官方工具相似，却不能用 Token Plan？

Token Plan 通过以 `sk-sp-` 开头的专属 API Key 和自定义 **Base URL** 抵扣套餐额度，工具必须支持 OpenAI 或 Anthropic 接口协议才能接入，界面相似不代表协议兼容。不调用标准 API 的自研工具请改用以 `sk-` 或 `sk-ws-` 开头的按量付费 API Key。
