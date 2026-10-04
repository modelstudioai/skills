# application [use cases](use-cases.md)

百炼平台支持多种典型业务场景下的 AI 应用快速落地，核心围绕“大模型能力 + 私有知识增强（RAG）+ 低代码集成”展开。开发者可基于统一的百炼应用（智能体）作为后端推理服务，通过 AppFlow 连接流或本地部署方式，将 AI 能力嵌入网站、企业微信、钉钉、微信公众号等主流渠道，实现 7×24 小时自动化客服、私域问答等生产级应用。所有方案均默认复用百炼控制台创建的同一套应用配置（含模型、Prompt、知识库），确保逻辑一致、维护高效。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus` 或 `qwen-plus`，其在效果、速度与成本间取得平衡，适用于通用问答、客服对话等场景；对延迟敏感场景可选 `qwen-turbo`，对复杂推理需求可选 `qwen-max` [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **核心功能**：
  - 智能体（Agent）编排：支持多步骤任务分解、工具调用（如知识库检索）；
  - RAG 增强：通过知识库模块接入私有文档（PDF/DOCX/TXT 等），支持全文引用、切片检索、自定义处理三种文件处理方式；
  - 多模态支持：知识库上传支持图片（PNG/JPG/BMP/GIF）、文本及结构化数据（XLSX/CSV）；
  - 本地 RAG 部署：提供完整开源示例（`local_rag.zip`），支持本地文档切分、自定义嵌入模型（如 GTE-Chinese-Large）及向量存储 [原文标题](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中指定模型为 `Qwen3.5-Plus`，而文档 2、3、4 均写为 `千问-Plus`。经核实，`Qwen3.5-Plus` 是当前最新正式版名称，`千问-Plus` 为旧称，已过时。请以控制台实际可选模型列表为准，优先选用 `Qwen3.5-Plus`。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置位置 |
|----------|--------|------|------------|
| **模型层** | 温度（temperature） | 控制输出随机性，建议 0.1–0.6；值过高易导致幻觉 | 本地 RAG 应用的 Gradio 界面或 `chat.py`；百炼应用配置页暂不开放（需通过 Prompt 约束） |
| | 最大生成长度（max_tokens） | 限制响应 token 数，影响回答详略程度 | 同上 |
| | 携带上下文轮数 | 控制历史对话记忆深度，默认为 1（即不依赖历史） | 同上 |
| **RAG 层** | 召回片段数（top_k） | 检索返回给模型的最相关文本段数量，建议 3–5 | 本地 RAG 应用界面；百炼知识库配置中无直接等效项，由系统自动优化 |
| | 相似度阈值（similarity_threshold） | 过滤低相关性检索结果，范围 0–1，0 表示不限制 | 本地 RAG 应用界面；百炼知识库中对应“相似度阈值”字段，位于知识库引用配置页 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| **集成层** | Webhook URL | AppFlow 连接流对外暴露的 HTTP 回调地址，用于接收渠道消息 | AppFlow 连接流发布后生成，需填入企业微信/钉钉/公众号后台 |

## 使用方式

1. **统一后端构建**：  
   在百炼控制台 → 应用管理 → 创建**智能体应用**，选择 `Qwen3.5-Plus`，配置 Prompt（如角色设定），并**发布**；随后在知识库页面上传文档、创建知识库，并在应用配置中启用“必定调用”该知识库。

2. **渠道前端集成**（三选一）：  
   - **网站嵌入**：通过 AppFlow 创建 AI 助手 → 配置 Web 页面集成 → 复制悬浮挂件脚本 → 插入 HTML `<head>` 或 `<body>` 底部 [原文标题](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)；  
   - **企微/钉钉/公众号**：在对应平台创建应用（获取 AppID/AgentID/ClientID 等凭证）→ 使用 AppFlow 预置模板（如“企业微信自建应用大模型自动回复”）→ 绑定百炼应用 ID 和 API Key → 发布连接流 → 将生成的 Webhook URL 填入渠道后台；  
   - **本地部署**：下载 `local_rag.zip` → 安装依赖（Python 3.9–3.12）→ 配置百炼 API Key 环境变量 → 运行 `uvicorn main:app --port 7866` → 访问 `http://127.0.0.1:7866` 使用 Gradio 界面。

3. **日志与监控**（可选）：  
   在 AppFlow 连接流中添加 SLS 日志云服务节点，将用户输入、模型输出、耗时等关键字段写入日志服务，用于效果分析与问题排查。

## 限制和注意事项

- **免费额度**：新用户可享百炼平台提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；额度用尽后按 token 计费。AppFlow、函数计算 FC、ADB-PG 等关联云产品单独计费。
- **知识库限制**：单文档最大 100MB 或 1000 页，单图片最大 20MB，最多上传 200 个文件；向量存储类型若选 ADB-PG，需额外开通并付费。
- **渠道特殊约束**：  
  - 微信公众号未认证时，仅支持被动回复（5 秒超时限制），建议完成认证或改用 `qwen-turbo` 降低延迟；  
  - 钉钉机器人配置中**必须选择 HTTP 模式**，Stream 模式不兼容 AppFlow；  
  - 企业微信配置可信 IP 时，若报错“IP 属于第三方服务商”，需通过 AppFlow 内网代理（ECS/Nginx）转发请求，并将代理机器 IP 加入白名单。
- **调试要点**：  
  - 出现 `Failed to stream content` 或 `request error`，优先检查 API Key 状态、应用 ID 是否正确、以及智能体与 API Key 是否在同一业务空间；  
  - 对话无响应时，务必检查 AppFlow 连接流执行日志（非“运行一次”测试），定位失败步骤及错误详情。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


