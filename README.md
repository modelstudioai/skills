# ModelStudio Skills / 阿里云百炼精选技能库

> 为 AI Agent 赋能，由阿里云百炼团队精选并验证的开源 Skill 集合。

**ModelStudio Skills** 是阿里云百炼（ModelStudio）推出的精选 AI Agent 技能仓库。我们持续追踪 GitHub、Anthropic、Vercel、Google Labs 等社区的优质 Claude Code / Agent Skills，对每个技能进行真实场景验证，仅收录验证结论为「可用」的项目，并按使用场景分组沉淀，方便开发者直接调用。

每个技能都是独立的、可组合的工作流单元，覆盖技能管理、代码开发、设计创意、文档写作、影视创作、测试质量六大场景。

## 安装

第一步，安装阿里云百炼 CLI（需要 Node.js 18+）。直接对你的 AI 助手说：

> 请帮我全局安装阿里云百炼 CLI 命令行工具：npm install -g bailian-cli

安装成功后，`bailian-cli` 会自动把本仓库的 Skill 目录注册到主流客户端：

- Claude Code → `~/.claude/skills/bailian-cli/`
- Qwen Code → `~/.qwen/skills/bailian-cli/`

第二步，在 [百炼控制台](https://bailian.console.aliyun.com/cli?source_channel=key_github&) 创建 API Key 并完成登录。直接对你的 AI 助手说：

> 帮我用刚才拿到的 API Key 完成阿里云百炼 CLI 的登录

第三步，**调用时直接用自然语言对话**，无需记忆任何命令——你的助手会根据上下文自动判断该触发哪个 Skill。下面"技能一览"里每行的"一句话调用示例"，复制粘贴给助手即可生效。

## 技能一览

| 分类 | 技能 | 一句话调用示例 | 来源 |
|------|------|----------------|------|
| 🛠️ 技能管理 | [skill-creator](#-skill-creator) | 帮我写一个分析小红书萌宠类视频热度排行原因的 Claude Code skill | [anthropics/skills](https://github.com/anthropics/skills) |
| 🛠️ 技能管理 | [find-skills](#-find-skills) | 帮我找一个可以做 ppt 的 skill | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| 🛠️ 技能管理 | [skills-mcp](#-skills-mcp) | 帮我查找最新的 AI 技能 | [skills-mcp/skills-mcp](https://github.com/skills-mcp/skills-mcp) |
| 🛠️ 技能管理 | [skill-atlas](#-skill-atlas) | 帮我做 iPhone 和小米手机的竞品分析 | [GPTtang/skill-atlas](https://github.com/GPTtang/skill-atlas) |
| 🛠️ 技能管理 | [skills_repository](#-skills_repository) | 帮我查找有没有能做项目规划的 skill | [diao10/skills_repository](https://github.com/diao10/skills_repository) |
| 🛠️ 技能管理 | [ai-toolkit](#-ai-toolkit) | 帮我创建一篇关于 cocos creator 开发的飞书学习文档 | [mwpgxl/ai-toolkit](https://github.com/mwpgxl/ai-toolkit) |
| 🛠️ 技能管理 | [shaoqi-marketplace](#-shaoqi-marketplace) | 帮我做人体工学椅相关的市场分析和定价策略 | [ceoniuer/shaoqi-marketplace](https://github.com/ceoniuer/shaoqi-marketplace) |
| 🛠️ 技能管理 | [servasyy_skills](#-servasyy_skills) | 帮我写一篇关于校庆的公众号文章并排版 | [huangserva/servasyy_skills](https://github.com/huangserva/servasyy_skills) |
| 🛠️ 技能管理 | [AI-Vibe-Writing-Skills](#-ai-vibe-writing-skills) | 帮我为这段文案消除 AI 味 | [donghuixin/AI-Vibe-Writing-Skills](https://github.com/donghuixin/AI-Vibe-Writing-Skills) |
| 🛠️ 技能管理 | [marketing-writer](#-marketing-writer) | 帮我给莱芬吹风机写一篇营销文案 | [gushuaialan1/marketing-writer](https://github.com/gushuaialan1/marketing-writer) |
| 🛠️ 技能管理 | [social-media-skills](#-social-media-skills) | 帮我规划社交媒体内容策略 | [blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills) |
| 🛠️ 技能管理 | [multi-agent-content](#-multi-agent-content) | 帮我用多代理协作写一篇关于"思念家乡"的长文 | [gonelake/multi-agent](https://github.com/gonelake/multi-agent) |
| 🛠️ 技能管理 | [finance-skills](#-finance-skills) | 帮我写一篇近期基金涨幅话题的财经爆款 | [digoal/blog](https://github.com/digoal/blog/tree/master/skills) |
| 🛠️ 技能管理 | [gptzero-mcp](#-gptzero-mcp) | 帮我检测这段文字是不是 AI 生成的 | [louis030195/gptzero-mcp](https://github.com/louis030195/gptzero-mcp) |
| 💻 代码开发 | [mcp-builder](#-mcp-builder) | 帮我写一个 MCP Server，让 Claude 能调用天气相关服务 | [anthropics/skills](https://github.com/anthropics/skills) |
| 💻 代码开发 | [goframe-v2](#-goframe-v2) | 帮我用 GoFrame v2 写一个登录的 API 接口 | [gogf/skills](https://github.com/gogf/skills) |
| 🎨 设计创意 | [shadcn-ui](#-shadcn-ui) | 帮我用 shadcn-ui 组件库搭建聊天室页面 | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) |
| 🎨 设计创意 | [ui-ux-pro-max](#-ui-ux-pro-max) | 帮我设计个人博客的网站 UI，要 50 种风格之一 | [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) |
| 🎨 设计创意 | [canvas-design](#-canvas-design) | 帮我设计一幅自由与蝴蝶为主题的视觉海报 | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎨 设计创意 | [frontend-design](#-frontend-design) | 帮我做一个小米手机的宣传页面，要有高设计品质 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [internal-comms](#-internal-comms) | 帮我写个 2026 年 5 月份第一周的团队周报 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [xlsx/docx/pdf/pptx](#-office-suite) | 帮我做个 2025 年一整年国产自研化妆品销量的 PPT | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 文档写作 | [doc-coauthoring](#-doc-coauthoring) | 帮我写一份技术方案：结构化文档，经三阶段产出 | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎬 影视创作 | [spark-video](#-spark-video) | 帮我做一个产品广告视频，产品图在这里，卖点用一句话描述 | [JohnKeating1997/spark-video](https://github.com/JohnKeating1997/spark-video) |
| 🎬 影视创作 | [shanyin-screenwriting-master](#-shanyin-screenwriting-master) | 帮我做一个真人版的小红帽的故事视频 | [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) |
| 🧪 测试质量 | [e2e-testing](#-e2e-testing) | 帮我写 e2e 测试，覆盖用户注册→登录→浏览→购物车→下单的完整流程 | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) |

---

## 🛠️ 技能管理（14）

技能管理类是「工具的工具」——帮助开发者发现、组合、创建并调度其它 Skill。建议任何 Agent 项目优先关注本组中的 `skill-creator`、`find-skills`、`skills-mcp` 三件套。

### 🧰 skill-creator

来源：[anthropics/skills](https://github.com/anthropics/skills)

Anthropic 官方认证的技能创建工具，通过访谈式分析帮助用户将重复工作流提炼为可复用的标准技能。支持完整的 draft → test → evaluate → improve 闭环，是把日常工作沉淀为生态资产的入口。

**怎么用：直接对你的 AI 助手说**

> 帮我写一个分析小红书萌宠类视频热度排行原因的 Claude Code skill

### 🔎 find-skills

来源：[vercel-labs/skills](https://github.com/vercel-labs/skills)

Vercel Labs 出品的技能发现与推荐工具。当用户提问时自动搜索技能库中最匹配的技能并给出详情链接，是扩展 AI 能力边界的入口。

**怎么用：直接对你的 AI 助手说**

> 帮我找一个可以做 ppt 的 skill

### 🔌 skills-mcp

来源：[skills-mcp/skills-mcp](https://github.com/skills-mcp/skills-mcp)

将 Claude 的 Skills 模式带到任何 MCP 兼容的 Agent。通过 Model Context Protocol 让任意 AI Agent 都能加载、组合、复用模块化技能。是阿里云百炼团队推荐用于跨客户端复用 Skill 的桥梁。

**怎么用：直接对你的 AI 助手说**

> 帮我查找最新的 AI 技能

### 🗺️ skill-atlas

来源：[GPTtang/skill-atlas](https://github.com/GPTtang/skill-atlas)

108 个即用 Claude Skills 集合。覆盖 AI Agent、开发、写作、研究、社交媒体等场景，包含 deep-research 深度研究、data-analysis 数据分析等高频技能。

**怎么用：直接对你的 AI 助手说**

> 帮我做 iPhone 和小米手机的竞品分析

### 📚 skills_repository

来源：[diao10/skills_repository](https://github.com/diao10/skills_repository)

收集整理好用的 AI Agent Skills，提升开发效率。包含自定义 Skills（如技术方案生成器 generate-tech-proposal）和第三方 Skills 索引。

**怎么用：直接对你的 AI 助手说**

> 帮我查找有没有能做项目规划的 skill

### 🧪 ai-toolkit

来源：[mwpgxl/ai-toolkit](https://github.com/mwpgxl/ai-toolkit)

AI 工具字典库，管理 Claude Code Skills、MCP Servers 和 AI Agent 工具的综合目录。按 GitHub Star 数和实用性排序，提供快速查询入口。

**怎么用：直接对你的 AI 助手说**

> 帮我创建一篇关于 cocos creator 开发的飞书学习文档

### 🛒 shaoqi-marketplace

来源：[ceoniuer/shaoqi-marketplace](https://github.com/ceoniuer/shaoqi-marketplace)

WorkBuddy 技能市场合集。23 个精选技能覆盖内容创作、自媒体运营、情感关系分析等领域，包含 blog-writer 博客写作、brand-voice-profiler 品牌调性分析等。

**怎么用：直接对你的 AI 助手说**

> 帮我做人体工学椅相关的市场分析和定价策略

### 🎞️ servasyy_skills

来源：[huangserva/servasyy_skills](https://github.com/huangserva/servasyy_skills)

AI 驱动多媒体内容生产平台。14 个集成技能：document-writer（5 种写作风格）、illustration-generator（20 种配图风格）、ppt-builder 等。

**怎么用：直接对你的 AI 助手说**

> 帮我写一篇关于校庆的公众号文章并排版

### ✍️ AI-Vibe-Writing-Skills

来源：[donghuixin/AI-Vibe-Writing-Skills](https://github.com/donghuixin/AI-Vibe-Writing-Skills)

具备风格迁移和错误记忆功能的 AI 写作助手。提供 Spec-Driven Writing 规范驱动写作方法，支持 Context Compactor 上下文压缩、Error Memory 错误记忆等高级特性。

**怎么用：直接对你的 AI 助手说**

> 帮我为这段文案消除 AI 味：……

### 📣 marketing-writer

来源：[gushuaialan1/marketing-writer](https://github.com/gushuaialan1/marketing-writer)

多 Agent 营销文案写作系统。支持 Emotional Engineering 情感工程（5 阶段情感曲线：Hook → Small Win → Cognitive Shift → Resonance → Action）。

**怎么用：直接对你的 AI 助手说**

> 帮我给莱芬吹风机写一篇营销文案

### 📱 social-media-skills

来源：[blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills)

社交媒体内容策略 AI Agent Skills 集合。覆盖 text-first 和 visual-first 平台，包含 content-strategy-calendar 内容日历、平台适配等。

**怎么用：直接对你的 AI 助手说**

> 帮我规划社交媒体内容策略

### 🤝 multi-agent-content

来源：[gonelake/multi-agent](https://github.com/gonelake/multi-agent)

Agent 协同驱动的自主内容生成工具。三个专业 AI 智能体协同工作：ResearcherAgent 热点抓取、WriterAgent 文章撰写、ReviewerAgent 审核。

**怎么用：直接对你的 AI 助手说**

> 帮我用多代理协作写一篇关于"思念家乡"的长文

### 💰 finance-skills

来源：[digoal/blog/skills](https://github.com/digoal/blog/tree/master/skills)

财经内容创作 Skills 集合。包含 daily-finance 每日财经日报、finance-core-analysis 深度财经分析、finance-explosive 财经爆款写作等。

**怎么用：直接对你的 AI 助手说**

> 帮我写一篇近期基金涨幅话题的财经爆款

### 🕵️ gptzero-mcp

来源：[louis030195/gptzero-mcp](https://github.com/louis030195/gptzero-mcp)

GPTZero AI 检测 API 的 MCP 服务器。让 Claude、Qwen 等支持 MCP 的 LLM 能直接检测 AI 生成文本，支持批量检测、置信度评分、文档级分析。

**怎么用：直接对你的 AI 助手说**

> 帮我检测这段文字是不是 AI 生成的：[贴入待检测文本]

---

## 💻 代码开发（2）

### 🧱 mcp-builder

来源：[anthropics/skills](https://github.com/anthropics/skills)

MCP 服务器开发指南技能，提供完整的四阶段开发流程：深度研究与规划 → 实现 → 审查测试 → 评估。内置 TypeScript 和 Python 两种实现路径的参考文档，帮助 AI 高质量产出 MCP 工具。

**怎么用：直接对你的 AI 助手说**

> 帮我写一个 MCP Server，让 Claude 能调用天气相关服务

### 🐹 goframe-v2

来源：[gogf/skills](https://github.com/gogf/skills)

GoFrame 框架专属 AI 技能，为 AI 深度理解 GoFrame 框架规范与最佳实践提供完整支持，涵盖命令行管理、配置管理、日志组件、错误处理、数据校验、数据库 ORM 等。

**怎么用：直接对你的 AI 助手说**

> 帮我用 GoFrame v2 写一个登录的 API 接口

---

## 🎨 设计创意（4）

### 🧩 shadcn-ui

来源：[google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)

Google 官方 stitch-skills 项目出品的 shadcn/ui 集成专家技能。shadcn/ui 元件源码直接复制到项目中，完全自主可改。提供组件源码获取、自定义安装、主题配置及最佳实践指导。

**怎么用：直接对你的 AI 助手说**

> 帮我用 shadcn-ui 组件库搭建聊天室页面

### 🎨 ui-ux-pro-max

来源：[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)

综合型 UI/UX 设计智能技能，内置 50+ UI 风格、97 种配色方案、57 组字体搭配、99 条 UX 规则和 25 种图表类型。覆盖 React、Next.js、Vue、Svelte 等主流前端框架。

**怎么用：直接对你的 AI 助手说**

> 帮我设计个人博客的网站 UI，要 50 种风格之一

### 🖼️ canvas-design

来源：[anthropics/skills](https://github.com/anthropics/skills)

视觉艺术设计技能，采用哲学先行的两步创作流程：先生成设计哲学宣言，再将其转化为博物馆级别的 PNG 或 PDF 设计作品。文字极少、视觉为主，强调如同大师作品般的精工细作。

**怎么用：直接对你的 AI 助手说**

> 帮我设计一幅自由与蝴蝶为主题的视觉海报

### 🪟 frontend-design

来源：[anthropics/skills](https://github.com/anthropics/skills)

Anthropic 官方前端设计技能，提供专业级 UI 设计规范和响应式布局最佳实践，帮助 AI 生成美观、可访问、适配多端的前端界面代码。

**怎么用：直接对你的 AI 助手说**

> 帮我做一个小米手机的宣传页面，要有高设计品质

---

## 📝 文档写作（3）

### 🏢 internal-comms

来源：[anthropics/skills](https://github.com/anthropics/skills)

内部沟通写作资源集，内置多种企业内部沟通格式的规范模板，包括 3P 周报（进展/计划/问题）、公司简报、FAQ 回答、状态报告、领导层更新、事故报告等。

**怎么用：直接对你的 AI 助手说**

> 帮我写个 2026 年 5 月份第一周的团队周报

### 📊 office-suite (xlsx / docx / pdf / pptx)

来源：[anthropics/skills](https://github.com/anthropics/skills)

Anthropic 官方办公文档操作技能集，分别处理 Excel、Word、PDF 和 PowerPoint 四种格式，支持 AI 自动创建、编辑和分析各类办公文件。每种格式都有独立的 SKILL.md 与脚手架。

**怎么用：直接对你的 AI 助手说**

> 帮我做个 2025 年一整年国产自研化妆品销量的 PPT

### 🤝 doc-coauthoring

来源：[anthropics/skills](https://github.com/anthropics/skills)

结构化文档协作写作工作流，全程引导用户完成三阶段流程：上下文收集 → 逐节细化精炼 → 读者视角测试。通过访谈式问答收集背景信息，逐节进行头脑风暴、筛选、起草和迭代。

**怎么用：直接对你的 AI 助手说**

> 帮我写一份技术方案：结构化文档，经三阶段产出

---

## 🎬 影视创作（2）

### 🎥 spark-video

来源：[JohnKeating1997/spark-video](https://github.com/JohnKeating1997/spark-video)

AI video production skill — premise → screenplay → storyboard → render → review。从一个想法走到成片的端到端工作流，已与阿里云百炼通义万相 / WAN 系列视频模型完成联调验证。

**怎么用：直接对你的 AI 助手说**

> 帮我做一个产品广告视频，产品图在这里，卖点用一句话描述

### 📜 shanyin-screenwriting-master

来源：[Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master)

山音超级编剧大师 — 由 @山音 设计的全格式影视编剧技能。覆盖从 1-3 分钟概念超短片到 90 分钟电影长片、多集剧集的全格式剧本创作。支持四种格式：概念超短片 / 短片 / 电影长片 / 剧集。

**怎么用：直接对你的 AI 助手说**

> 帮我做一个真人版的小红帽的故事视频

---

## 🧪 测试质量（1）

### 🎭 e2e-testing

来源：[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

端到端测试模式技能，内置 Playwright 测试框架最佳实践，涵盖 Page Object Model 设计模式、测试文件组织结构、CI/CD 集成配置、Artifact 管理等。

**怎么用：直接对你的 AI 助手说**

> 帮我写 e2e 测试，覆盖用户注册 → 登录 → 浏览商品列表 → 加入购物车 → 结算下单的完整流程，使用 Playwright

---

## 📂 Project Structure

```
skills/                                  # 仓库根（GitHub 上的 modelstudioai/skills）
├── README.md
├── README_EN.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/
│   └── verification-process.md          # 阿里云百炼对每个 Skill 的验证流程说明
├── skill-creator/
├── find-skills/
├── skills-mcp/
├── skill-atlas/
├── skills_repository/
├── ai-toolkit/
├── shaoqi-marketplace/
├── servasyy_skills/
├── ai-vibe-writing-skills/
├── marketing-writer/
├── social-media-skills/
├── multi-agent-content/
├── finance-skills/
├── gptzero-mcp/
├── mcp-builder/
├── goframe-v2/
├── shadcn-ui/
├── ui-ux-pro-max/
├── canvas-design/
├── frontend-design/
├── internal-comms/
├── xlsx-docx-pdf-pptx/
├── doc-coauthoring/
├── spark-video/
├── shanyin-screenwriting-master/
└── e2e-testing/
```

每个 `<skill-name>/` 目录下包含：

- `SKILL.md` — Skill 调用入口与提示词协议
- `UPSTREAM.md` — 上游仓库信息、版本、License、对齐策略
- `VERIFICATION.md` — 阿里云百炼团队的验证场景、输入输出、结论
- `assets/` — 该 Skill 在百炼平台的演示截图与运行产物（可选）

## 🤖 在不同客户端使用

通过 `bailian-cli` 安装后，三种主流客户端均会自动识别并调度本仓库中的 Skill。调用方式都是**直接用自然语言对话**——你只需把上面每个 Skill 的"怎么用"一句话发给助手即可。

- **Claude Code**：识别 `~/.claude/skills/bailian-cli/` 下的 Skill
- **Qwen Code**：识别 `~/.qwen/skills/bailian-cli/` 下的 Skill
- **Cursor / 其他 MCP 客户端**：通过 [skills-mcp](#-skills-mcp) 暴露为 MCP Server，再在客户端中添加 MCP 配置



## 📜 License

本仓库代码以 Apache-2.0 协议发布。每个 Skill 子目录保留其上游原 License，详见各 `UPSTREAM.md`。


---

*由阿里云百炼团队精心维护。我们尊重每个 Skill 上游作者的版权与授权，所有引用均保留原始 License 与 Attribution。如发现内容侵权或表达不当，请提交 Issue 与我们联系。*
