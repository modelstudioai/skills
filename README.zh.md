<div align="center">

<img src="https://img.alicdn.com/imgextra/i4/O1CN01VWH9Nq1SfXnTTVTCw_!!6000000002274-2-tps-1915-821.png" alt="Aliyun Model Studio AI Skills"  />

**阿里云百炼 (DashScope) AI 平台官方 Agent 技能集**

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-brightgreen.svg)](https://agentskills.io)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

[阿里云百炼 CLI 官方主页](https://bailian.console.aliyun.com/cli?source_channel=cli_github&) · [English](./README.md) · [API 文档](https://help.aliyun.com/zh/model-studio/) · [获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?source_channel=key_github&tab=app#/api-key)

---

_官方一方技能：核心 `bailian-cli` 技能在 [`modelstudioai/cli`](https://github.com/modelstudioai/cli) 仓库；本仓库提供可选扩展。配合 `bl` 接入百炼全模态能力，_
_精选三方技能覆盖创作、开发、设计、文档、测试 — 按需挑选，即装即用。_

_为 AI Agent 赋能，由阿里云百炼团队精选并验证的 Skill 集合。_

</div>

ModelStudio Skills 是阿里云百炼（ModelStudio）推出的官方 AI Agent 技能仓库，包含两类：

- **官方一方技能** — 由百炼团队开发。先从 [`modelstudioai/cli`](https://github.com/modelstudioai/cli) 安装核心 **`bailian-cli` 技能**（`npx skills add modelstudioai/cli --all -g`），再从本仓库安装可选扩展。配合 [`bailian-cli`](https://www.npmjs.com/package/bailian-cli) npm 包（命令别名 `bl`，安装见 [bailian.aliyun.com/cli/install.md](https://bailian.aliyun.com/cli/install.md)）使用，覆盖对话、多模态、图像/视频、语音、视觉、应用、记忆、RAG、联网搜索等百炼平台核心能力。
- **精选三方技能** — 持续追踪 GitHub、Anthropic、Vercel、Google Labs 等社区的优质 Claude Code / Agent Skills，经百炼团队真实场景验证，仅收录结论为「可用」的项目，按使用场景分组沉淀，方便开发者直接调用。

每个技能都是独立的、可组合的工作流单元，三方部分覆盖**技能管理、代码开发、设计创意、文档写作、影视创作、测试质量**六大场景。

---

## 快速开始

### 前置条件

运行调用 `bl` 命令的技能需要一个**阿里云百炼 API Key**。

👉 [免费获取 API Key](https://bailian.console.aliyun.com/cn-beijing/?source_channel=key_github&tab=app#/api-key)

### 手动安装

```bash
npx skills add modelstudioai/skills
```

提示时选择想要安装的技能，回车确认。

### 使用 Agent 安装（推荐）

将下面内容粘贴给你的 AI Agent：

```
请帮我安装百炼 AI Skills：
1. 检查 Node.js 是否已安装（需要 ≥ 18），没有则帮我安装
2. 执行：npx skills add modelstudioai/skills
3. 安装完成后先说「Bailian Skills 已安装」，再列出已安装的技能及我能做什么
```

---

## 本仓库一方技能

以下技能随本仓库发布，由百炼团队维护。安装 `modelstudioai/skills` 后，Agent 按需自动激活（与下方**社区精选**不同）。

| 技能 | 说明 |
|------|------|
| [`bailian-docs-llm-wiki`](./skills/bailian-docs-llm-wiki/) | 引导 Agent 查阅仓库内置的**百炼文档库**：模型规格与定价、API/错误码、智能体/RAG/知识库、SDK 与多模态、计费等。从 `models/index.md` 和 `wiki/index.md` 开始逐层查阅。 |
| [`bailian-model-recommend`](./skills/bailian-model-recommend/) | **模型选型与推荐**：根据场景或功能需求，从百炼模型库中推荐最合适的模型并附可直接运行的示例代码。命中"推荐 / 选哪个 / 对比"等意图时激活，内部读取 `bailian-docs-llm-wiki` 的 `models/` 数据。 |
| [`financial-expert`](./skills/financial-expert/) | **金融数据分析**：基于 `bl mcp`（`market-cmapi00073529`），覆盖 A 股、港股、基金、债券与指数，支持股票 / 基金 / 基金经理筛选、财务估值、全球宏观与行业时序、券商研报、公司及基金公告、财经新闻和企业风险查询。实时工具包括 `NewsDataQuery` 与 `IcEnterpriseDataQuery`。 |
| [`happyhorse-prompt-studio`](./skills/happyhorse-prompt-studio/) | **HappyHorse 1.0 视频提示词工作室**：用生动示例引导用户发现场景，再组装出 日/中/英 三语的成片级 Prompt。覆盖漫剧、角色 PV、漫画运动、虚拟偶像 MV 及自由创作场景。 |
| [`spark-video`](./skills/spark-video/) | **端到端短片制作**：编剧 ↔ 导演（逐场景）→ 并行渲染 DAG → 逐 clip 审片 → 拼接。适合"帮我做一集短剧/产品广告"一句话出片。入口技能注册为 **`spark-video-episode`**（见 [`SKILL.md`](./skills/spark-video/SKILL.md)）。 |
| [`novel-game`](./skills/novel-game/) | **小说改编互动小说网页游戏（React SPA）**：分支剧情引擎 + AI 生成角色立绘/过场（视频或图片）+ 可选 TTS 旁白 + 程序化 Web Audio 音频 + localStorage 存档 + 多种 UI 风格（像素 / 赛博朋克 / 水墨 / 简约）。命中"互动小说 / 文字冒险 / 视觉小说 / 小说改编游戏"时激活，全程通过 `bl video / image / speech` 离线生成素材后本地运行。 |
| [`vox-video-director`](./skills/vox-video-director/) | **端到端 Vox 风格纸质拼贴视频制作**：主题、口播视频或单张锚定照片 → beat map → 内容驱动的 5–10 秒片段 → 拼贴关键帧 → 动效 → 旁白 → 字幕与本地 ffmpeg 合成。使用 `bl image / video / speech`，并在计费生成前停在审批点。 |

---

## 阿里云百炼精选技能

下表为百炼团队验证的**社区精选**项目索引。可直接对 Agent 说示例话术，或用安装命令单独引入。上方章节列出的是**本仓库内置的一方技能**。

> 详细说明与分组介绍见 [`AWESOME_SKILLS.md`](./AWESOME_SKILLS.md)。

| 分类 | 技能 | 一句话调用示例 | 来源 |
|------|------|----------------|------|
| 🛠️ 技能管理 | [skill-creator](./AWESOME_SKILLS.md#skill-creator) | 帮我写一个分析小红书萌宠类视频热度排行原因的 Claude Code skill | [anthropics/skills](https://github.com/anthropics/skills) |
| 🛠️ 技能管理 | [find-skills](./AWESOME_SKILLS.md#find-skills) | 帮我找一个可以做 ppt 的 skill | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| 🛠️ 技能管理 | [skills-mcp](./AWESOME_SKILLS.md#skills-mcp) | 帮我查找最新的 AI 技能 | [skills-mcp/skills-mcp](https://github.com/skills-mcp/skills-mcp) |
| 🛠️ 技能管理 | [skill-atlas](./AWESOME_SKILLS.md#skill-atlas) | 帮我做 iPhone 和小米手机的竞品分析 | [GPTtang/skill-atlas](https://github.com/GPTtang/skill-atlas) |
| 🛠️ 技能管理 | [skills_repository](./AWESOME_SKILLS.md#skills_repository) | 帮我查找有没有能做项目规划的 skill | [diao10/skills_repository](https://github.com/diao10/skills_repository) |
| 🛠️ 技能管理 | [ai-toolkit](./AWESOME_SKILLS.md#ai-toolkit) | 帮我创建一篇关于 cocos creator 开发的飞书学习文档 | [mwpgxl/ai-toolkit](https://github.com/mwpgxl/ai-toolkit) |
| 🛠️ 技能管理 | [shaoqi-marketplace](./AWESOME_SKILLS.md#shaoqi-marketplace) | 帮我做人体工学椅相关的市场分析和定价策略 | [ceoniuer/shaoqi-marketplace](https://github.com/ceoniuer/shaoqi-marketplace) |
| 🛠️ 技能管理 | [servasyy_skills](./AWESOME_SKILLS.md#servasyy_skills) | 帮我写一篇关于校庆的公众号文章并排版 | [huangserva/servasyy_skills](https://github.com/huangserva/servasyy_skills) |
| 🛠️ 技能管理 | [AI-Vibe-Writing-Skills](./AWESOME_SKILLS.md#ai-vibe-writing-skills) | 帮我为这段文案消除 AI 味 | [donghuixin/AI-Vibe-Writing-Skills](https://github.com/donghuixin/AI-Vibe-Writing-Skills) |
| 🛠️ 技能管理 | [marketing-writer](./AWESOME_SKILLS.md#marketing-writer) | 帮我给莱芬吹风机写一篇营销文案 | [gushuaialan1/marketing-writer](https://github.com/gushuaialan1/marketing-writer) |
| 🛠️ 技能管理 | [social-media-skills](./AWESOME_SKILLS.md#social-media-skills) | 帮我规划社交媒体内容策略 | [blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills) |
| 🛠️ 技能管理 | [multi-agent-content](./AWESOME_SKILLS.md#multi-agent-content) | 帮我用多代理协作写一篇关于「思念家乡」的长文 | [gonelake/multi-agent](https://github.com/gonelake/multi-agent) |
| 🛠️ 技能管理 | [finance-skills](./AWESOME_SKILLS.md#finance-skills) | 帮我写一篇近期基金涨幅话题的财经爆款 | [digoal/blog](https://github.com/digoal/blog/tree/master/skills) |
| 🛠️ 技能管理 | [gptzero-mcp](./AWESOME_SKILLS.md#gptzero-mcp) | 帮我检测这段文字是不是 AI 生成的 | [louis030195/gptzero-mcp](https://github.com/louis030195/gptzero-mcp) |
| 💻 代码开发 | [mcp-builder](./AWESOME_SKILLS.md#mcp-builder) | 帮我写一个 MCP Server，让 Claude 能调用天气相关服务 | [anthropics/skills](https://github.com/anthropics/skills) |
| 💻 代码开发 | [goframe-v2](./AWESOME_SKILLS.md#goframe-v2) | 帮我用 GoFrame v2 写一个登录的 API 接口 | [gogf/skills](https://github.com/gogf/skills) |
| 🎨 设计创意 | [shadcn-ui](./AWESOME_SKILLS.md#shadcn-ui) | 帮我用 shadcn-ui 组件库搭建聊天室页面 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) |
| 🎨 设计创意 | [ui-ux-pro-max](./AWESOME_SKILLS.md#ui-ux-pro-max) | 帮我设计个人博客的网站 UI，要 50 种风格之一 | [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) |
| 🎨 设计创意 | [canvas-design](./AWESOME_SKILLS.md#canvas-design) | 帮我设计一幅自由与蝴蝶为主题的视觉海报 | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎨 设计创意 | [frontend-design](./AWESOME_SKILLS.md#frontend-design) | 帮我做一个小米手机的宣传页面，要有高设计品质 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [internal-comms](./AWESOME_SKILLS.md#internal-comms) | 帮我写个 2026 年 5 月份第一周的团队周报 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [xlsx/docx/pdf/pptx](./AWESOME_SKILLS.md#office-suite-xlsx--docx--pdf--pptx) | 帮我做个 2025 年一整年国产自研化妆品销量的 PPT | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [doc-coauthoring](./AWESOME_SKILLS.md#doc-coauthoring) | 帮我写一份技术方案：结构化文档，经三阶段产出 | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎬 影视创作 | [spark-video](./AWESOME_SKILLS.md#spark-video) | 帮我做一个产品广告视频，产品图在这里，卖点用一句话描述 | [JohnKeating1997/spark-video](https://github.com/JohnKeating1997/spark-video) |
| 🎬 影视创作 | [shanyin-screenwriting-master](./AWESOME_SKILLS.md#shanyin-screenwriting-master) | 帮我做一个真人版的小红帽的故事视频 | [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) |
| 🧪 测试质量 | [e2e-testing](./AWESOME_SKILLS.md#e2e-testing) | 帮我写 e2e 测试，覆盖用户注册→登录→浏览→购物车→下单的完整流程 | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) |

---

## 许可证

本仓库代码以 [Apache-2.0](./LICENSE) 协议发布。

## 📖 完整教程

从注册到实战、Skill 加载、跨 AI Agent 框架使用，完整的中文教程在文档站：

**[modelstudioai.github.io/guide/](https://modelstudioai.github.io/guide/)**

---

> **免责声明** — 本仓库技能会指导 Agent 通过 `bl` 代你调用 DashScope / 百炼 API，费用由你的阿里云账号承担。生成内容可能不准确，使用前请自行核对。请妥善保管 API Key。本项目按「现状」提供，不作任何担保。

*由阿里云百炼团队精心维护。我们尊重每个 Skill 上游作者的版权与授权，所有引用均保留原始 License 与 Attribution。如发现内容侵权或表达不当，请提交 Issue 与我们联系。*
