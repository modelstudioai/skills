# 教育社群故事化群日报

文本模型把群聊素材转成 story.json，本地离线渲染成 HTML 与 PNG 长图。

**说明**

**免责声明**：本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台「用量详情」为准。

本篇以一天的群聊素材跑通全链路：先让文本模型把素材结构化为 `story.json`，再在本地离线渲染成品牌化的 HTML 与 PNG 长图日报，把社群内容沉淀成资产。

调用链：`qwen3.7-max`（群聊素材 → `story.json`，官方开源方案 [`group-daily-waytoagi-edu`](https://help.aliyun.com/zh/model-studio/token-plan-playbook-group-daily-report)）→ 本地渲染 HTML / PNG 长图（离线，不耗 Credits）。

## 实测产出

以一天的群聊素材跑通全链路，渲染出的故事化群日报长图（节选）：

![故事化群日报长图](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9e14.png)

## 步骤一：设定主编人设

用 System Prompt 固定主编人设与输出结构（节选）：

```
你是 WaytoAGI-EDU 教育社群的群日报主编。
任务：把用户提供的群聊素材整理成可被渲染的 story.json。
- 只输出一个 JSON 对象；不要编造不存在的人名、观点、链接或数据
- 风格是教育 AI 共创社群：温暖、故事化、有角色、有现场感，不写成会议纪要
- 每个 timeline 条目包含 no/time/badge/cast/theme/story/quotes/output
- footer_quote 选择最能代表当天气质的一句话
输出顶层字段：group_name, date, time_range, lead_title, opening,
timeline, highlights, sops, qas, stats, footer_quote ...
```

## 步骤二：附群聊素材生成 story.json

用 User Prompt 传入当天的群聊素材：

```
请根据以下群聊素材生成 story.json。
群名：WaytoAGI-EDU 情报局 ｜ 日期：2026-07-28 ｜ 时间范围：09:18 → 20:10
安全规则：不要输出任何手机号、邮箱、地址、账号等隐私信息。
群聊素材：
{手动整理的群聊文本，如 [09:18] 示例老师A：今天想问一个课堂问题……}
```

## 说明

-   **消耗**：本玩法只有文本生成一步耗费 Credits（`qwen3.7-max`，群聊素材转 `story.json`），后续离线渲染 HTML 与 PNG 长图不耗 Credits。
-   **成本变化**：消耗随群聊素材长度变化，素材越长越高。
