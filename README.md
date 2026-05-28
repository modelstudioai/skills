<div align="center">

<img src="https://img.alicdn.com/imgextra/i4/O1CN01VWH9Nq1SfXnTTVTCw_!!6000000002274-2-tps-1915-821.png" alt="Aliyun Model Studio AI Skills"  />

**The official Agent Skills collection for Aliyun Model Studio (DashScope) AI Platform**

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-brightgreen.svg)](https://agentskills.io)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18-brightgreen)](https://nodejs.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

[Aliyun Model Studio CLI Site](https://bailian.console.aliyun.com/cli) · [中文](./README_CN.md) · [API Documentation](https://help.aliyun.com/zh/model-studio/) · [Get API Key](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/api-key)

---

_1st-party skills pair with bailian-cli (bl) for Bailian's full-modal capabilities,_
_curated 3rd-party skills cover creation, dev, design, docs, and testing — pick and go._

_Empowering AI Agents with a Skills collection curated and verified by the Aliyun Bailian team._

</div>

ModelStudio Skills is the official AI Agent Skills repository from Aliyun Model Studio, containing two categories:

- **1st-party skills** — Developed by the Bailian team and paired with [`bailian-cli`](https://www.npmjs.com/package/bailian-cli) (`bl`, install via [bailian.aliyun.com/cli/install.md](https://bailian.aliyun.com/cli/install.md)), covering chat, multimodal, image/video, speech, vision, apps, memory, RAG, and web search on the Bailian platform.
- **Curated 3rd-party skills** — Continuously tracked from GitHub, Anthropic, Vercel, Google Labs, and other communities. Each Claude Code / Agent Skill is verified in real-world scenarios by the Bailian team; only those marked "usable" are included, grouped by use case for direct integration.

Each skill is an independent, composable workflow unit. The 3rd-party set spans **skill management, code development, design & creativity, documentation, video production, and testing** — six major scenarios.

---

## Quick Start

### Manual Install

```bash
npx skills add modelstudioai/skills
```

When prompted, press `a` to select all skills, then Enter to confirm.

### Install via Your Agent (Recommended)

Paste the following into your AI Agent:

```
Please install Bailian AI Skills for me:
1. Check if Node.js is installed (>= 18), install it if not
2. Run: npx skills add modelstudioai/skills --all -y
3. Once installed, start with "Bailian Skills installed", then list the installed skills and what I can do
```

---

## Skills

| Skill | Description |
|-------|-------------|
| [`bailian-cli`](./skills/bailian-cli/) | Guides the Agent to use `bl` commands for chat, multimodal, image/video, speech, vision, apps, memory, RAG, and web search; detailed command reference under `reference/`. Install the CLI first → [bailian.aliyun.com/cli/install.md](https://bailian.aliyun.com/cli/install.md). |
| [`bailian-docs-llm-wiki`](./skills/bailian-docs-llm-wiki/) | **Bailian Docs Library**: enable when answering Bailian questions about model specs, APIs/error codes, agents/RAG/knowledge base, SDK compatibility, multimodal, billing, etc.; check `models/` for specs and pricing, `wiki/` for concepts and guides. |

---

## Aliyun Bailian Curated Skills

The following skills come from open-source community projects, curated and verified by the Bailian team. Use the example prompts directly with your Agent, or install each one individually.

> See [`AWESOME_SKILLS.md`](./AWESOME_SKILLS.md) for detailed descriptions and category overviews.

| Category | Skill | Example Prompt | Source |
|----------|-------|----------------|--------|
| 🛠️ Skill Management | [skill-creator](./AWESOME_SKILLS.md#skill-creator) | Write me a Claude Code skill that analyzes why pet videos go viral on Xiaohongshu | [anthropics/skills](https://github.com/anthropics/skills) |
| 🛠️ Skill Management | [find-skills](./AWESOME_SKILLS.md#find-skills) | Find me a skill for making PPTs | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| 🛠️ Skill Management | [skills-mcp](./AWESOME_SKILLS.md#skills-mcp) | Find me the latest AI skills | [skills-mcp/skills-mcp](https://github.com/skills-mcp/skills-mcp) |
| 🛠️ Skill Management | [skill-atlas](./AWESOME_SKILLS.md#skill-atlas) | Run a competitive analysis between iPhone and Xiaomi phones | [GPTtang/skill-atlas](https://github.com/GPTtang/skill-atlas) |
| 🛠️ Skill Management | [skills_repository](./AWESOME_SKILLS.md#skills_repository) | Find me a skill for project planning | [diao10/skills_repository](https://github.com/diao10/skills_repository) |
| 🛠️ Skill Management | [ai-toolkit](./AWESOME_SKILLS.md#ai-toolkit) | Create a Feishu learning doc on Cocos Creator development | [mwpgxl/ai-toolkit](https://github.com/mwpgxl/ai-toolkit) |
| 🛠️ Skill Management | [shaoqi-marketplace](./AWESOME_SKILLS.md#shaoqi-marketplace) | Do market analysis and pricing strategy for ergonomic chairs | [ceoniuer/shaoqi-marketplace](https://github.com/ceoniuer/shaoqi-marketplace) |
| 🛠️ Skill Management | [servasyy_skills](./AWESOME_SKILLS.md#servasyy_skills) | Write and lay out a WeChat article for our school anniversary | [huangserva/servasyy_skills](https://github.com/huangserva/servasyy_skills) |
| 🛠️ Skill Management | [AI-Vibe-Writing-Skills](./AWESOME_SKILLS.md#ai-vibe-writing-skills) | Rewrite this copy to remove the AI feel | [donghuixin/AI-Vibe-Writing-Skills](https://github.com/donghuixin/AI-Vibe-Writing-Skills) |
| 🛠️ Skill Management | [marketing-writer](./AWESOME_SKILLS.md#marketing-writer) | Write marketing copy for the Laifen hair dryer | [gushuaialan1/marketing-writer](https://github.com/gushuaialan1/marketing-writer) |
| 🛠️ Skill Management | [social-media-skills](./AWESOME_SKILLS.md#social-media-skills) | Plan a social media content strategy | [blacktwist/social-media-skills](https://github.com/blacktwist/social-media-skills) |
| 🛠️ Skill Management | [multi-agent-content](./AWESOME_SKILLS.md#multi-agent-content) | Use multi-agent collaboration to write a long essay on "missing home" | [gonelake/multi-agent](https://github.com/gonelake/multi-agent) |
| 🛠️ Skill Management | [finance-skills](./AWESOME_SKILLS.md#finance-skills) | Write a viral finance article on recent fund gains | [digoal/blog](https://github.com/digoal/blog/tree/master/skills) |
| 🛠️ Skill Management | [gptzero-mcp](./AWESOME_SKILLS.md#gptzero-mcp) | Check whether this text is AI-generated | [louis030195/gptzero-mcp](https://github.com/louis030195/gptzero-mcp) |
| 💻 Code Development | [mcp-builder](./AWESOME_SKILLS.md#mcp-builder) | Build me an MCP Server so Claude can call weather-related services | [anthropics/skills](https://github.com/anthropics/skills) |
| 💻 Code Development | [goframe-v2](./AWESOME_SKILLS.md#goframe-v2) | Write a login API in GoFrame v2 | [gogf/skills](https://github.com/gogf/skills) |
| 🎨 Design & Creativity | [shadcn-ui](./AWESOME_SKILLS.md#shadcn-ui) | Build a chat room page with the shadcn-ui component library | [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) |
| 🎨 Design & Creativity | [ui-ux-pro-max](./AWESOME_SKILLS.md#ui-ux-pro-max) | Design a personal blog UI in one of 50 styles | [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) |
| 🎨 Design & Creativity | [canvas-design](./AWESOME_SKILLS.md#canvas-design) | Design a visual poster themed around freedom and butterflies | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎨 Design & Creativity | [frontend-design](./AWESOME_SKILLS.md#frontend-design) | Design a high-quality promotional page for a Xiaomi phone | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 Documentation | [internal-comms](./AWESOME_SKILLS.md#internal-comms) | Write a team weekly report for the first week of May 2026 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 Documentation | [xlsx/docx/pdf/pptx](./AWESOME_SKILLS.md#office-suite-xlsx--docx--pdf--pptx) | Make a PPT on domestic indie cosmetics sales for the full year 2025 | [anthropics/skills](https://github.com/anthropics/skills) |
| 📝 Documentation | [doc-coauthoring](./AWESOME_SKILLS.md#doc-coauthoring) | Write a technical design doc — structured, produced in three stages | [anthropics/skills](https://github.com/anthropics/skills) |
| 🎬 Video Production | [spark-video](./AWESOME_SKILLS.md#spark-video) | Make a product ad video — here's the product image, with the selling point in one sentence | [JohnKeating1997/spark-video](https://github.com/JohnKeating1997/spark-video) |
| 🎬 Video Production | [shanyin-screenwriting-master](./AWESOME_SKILLS.md#shanyin-screenwriting-master) | Make a live-action video of the Little Red Riding Hood story | [Shanyin-ai/shanyin-screenwriting-master](https://github.com/Shanyin-ai/shanyin-screenwriting-master) |
| 🧪 Testing & Quality | [e2e-testing](./AWESOME_SKILLS.md#e2e-testing) | Write e2e tests covering signup → login → browsing → cart → checkout | [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code) |

---

## License

This repository's code is released under the [Apache-2.0](./LICENSE) license.

---

> **Disclaimer** — These skills instruct your Agent to call DashScope / Bailian APIs via `bl` on your behalf, billed to your Alibaba Cloud account. Generated content may be inaccurate — review before use. Keep your API key secure. This project is provided as-is, without warranties.

*Maintained by the Aliyun Bailian team. We respect the copyrights and licenses of each Skill's upstream author; all references retain the original License and Attribution. If you find any content infringing or inappropriate, please file an Issue to contact us.*
