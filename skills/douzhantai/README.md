# 抖战台 · 百炼 Agent Skill

> 外滩大会 2026 · 百炼赛道参赛作品（Agent Skills 形态）
> 把抖音电商四大环节（选品 / 直播 / 投流素材 / 财务核算）收敛成「总指挥 + 4 专职 Agent」多智能体作战台。

## 这是什么
本 Skill 是「抖战台」作战内核的 **Agent Skills 形态**，符合百炼参赛专区「用阿里云百炼 Agent Skills 打造」的要求：
- 大脑 = 阿里云百炼 DashScope 大模型（qwen-plus / qwen-max，OpenAI 兼容协议）
- 形态 = 标准百炼 Skill 包（SKILL.md + scripts + references），Agent 自动激活
- 配套 = 抖战台 Web 版（零依赖可视化体验）：https://26040e8952db42ae9ef6d7ca086789ed.bj4.agentos-app.net

## 目录结构
```
douzhantai/
├── SKILL.md                      # 主文件：定位 / 触发 / 4 Agent / 工具链 / 运行方式
├── README.md                     # 本文件
├── scripts/
│   └── run_campaign.py           # 命令行运行器，调百炼 DashScope 跑完 4 步（零依赖）
└── references/
    └── agents_prompt.md          # 4 个专职 Agent 完整 systemPrompt
```

## 安装（两种）
**方式一 · 自动安装（推荐）**：把下面这段话粘进你的 AI Agent（Cursor / Qwen Code / Claude Desktop / OpenWork 等）：
```
请帮我安装阿里云百炼的 AI Skills：
1. 检查 Node.js >=18（Skill 脚本用 Python，另需 Python3）
2. 把 douzhantai 目录放到你的 skills 路径下，或 npx skills add <本仓库>
3. 安装完成后告诉我「Douzhantai Skill installed」
```

**方式二 · 手动**：克隆本仓库，将 `douzhantai/` 目录置于 Agent 的 skills 目录。

## 运行
```bash
export DASHSCOPE_API_KEY=sk-xxxx     # 阿里云百炼 API Key（新用户赠 1 亿免费 Token）
python scripts/run_campaign.py "推一款便携式迷你榨汁杯，客单价39-99，目标一二线年轻女性"
```
未配置 Key 时自动降级内置样例（便携榨汁杯全链路），零依赖可演示。

## 提交百炼赛道时填写（参考）
- **项目名称**：抖战台 · 抖音电商 AI 作战台
- **团队/作者**：（待填）
- **你做了什么**：把抖音电商选品/直播/素材/财务四大环节封装成 4 个专职 Agent + 总指挥，一句话驱动串联协同，输出完整作战方案
- **用到的能力**：阿里云百炼 DashScope（qwen-plus / qwen-max）大模型推理；Agent Skills 形态封装；可选接百炼 CLI（bailian-cli）扩展全模态
- **效果展示**：Web 版公网链接 + 1 分钟录屏 + run_campaign.py 输出
- **项目链接**：（本仓库地址，含 Skill 包 + Web 版源码）

## 安全
- API Key 仅来自环境变量，绝不进代码 / 仓库（已 .gitignore）
- 算术工具白名单校验，杜绝代码注入
- 不收集、不存储任何用户业务数据
