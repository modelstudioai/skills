# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的 RAG（[检索增强生成](../concepts/rag.md)）架构，通过百炼大模型应用 + AppFlow 低代码连接流实现，无需自行部署模型或编写后端逻辑。核心流程一致：创建百炼智能体应用 → 配置知识库 → 在 AppFlow 中对接目标渠道 → 发布并验证。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档1）、`千问-Plus`（文档2、3、4），该模型在效果、速度与成本间取得平衡；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（低延迟）或 `qwen-turbo`（文档3中用于规避微信5秒限制）。
- **RAG 能力**：所有用例均依赖百炼知识库功能，支持 PDF/DOCX/TXT/XLSX/MD/PNG/JPG 等格式（文档2明确列出支持格式及单文件≤100MB限制），向量存储可选 ADB-PG（集中管理多应用向量）或默认存储。
- **本地 RAG 变体**：文档5提供完全本地化部署方案，支持自定义文档切分、本地嵌入模型（如 GTE-Chinese-Large）及灵活参数调优，适用于对数据主权或切分策略有强定制需求的场景。

> **注意**：文档1中指定模型为 `Qwen3.5-Plus`，而文档2、3、4统一使用 `千问-Plus`。二者为同一模型的不同命名方式（Qwen3.5-Plus 即千问-Plus），无实质差异，但需注意控制台界面显示一致性。该信息已在[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)和[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)中得到印证。

## 关键参数

- **身份凭证**：百炼应用 ID 与 API Key（所有用例必需），需确保二者处于同一业务空间（文档1“常见问题”强调此点）。
- **知识库配置**：
  - 调用方式：`必定调用`（文档1、3、4）、`按需调用`（文档2提及但未强制）；
  - 文档处理：`全文引用`/`切片检索`/`自定义处理`（文档2明确列出）；
  - 相似度阈值与权重：支持 per-document 配置（文档2）。
- **本地 RAG 参数**（文档5）：
  - 模型：`qwen-max`/`qwen-plus`/`qwen3.5-flash`；
  - 温度、最大回复长度、上下文轮数；
  - RAG 专属：召回片段数、相似度阈值（0 表示不剔除）。

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用**，配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **配置知识库**（可选但推荐）：
   - 上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)（文档2路径不同，但功能一致）；
   - 在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建并关联至应用。
3. **对接渠道**：
   - **网站**：通过 AppFlow 创建 AI 助手 → Web 页面集成 → 复制悬浮挂件脚本嵌入 HTML（文档1）；
   - **微信公众号**：使用 AppFlow 模板 → 授权公众号凭证 → 配置 Webhook（区分认证/未认证账号）（文档3）；
   - **企业微信**：AppFlow 模板 → 配置企业微信凭证（含 [Token](../concepts/token.md)/EncodingAESKey/IP 白名单）→ 设置 API 接收消息（文档2）；
   - **钉钉**：AppFlow 模板 → 配置钉钉应用 Client ID/Secret → HTTP 模式 Webhook（文档4强调必须选 HTTP，非 Stream）；
   - **本地 RAG**：解压 `local_rag.zip` → 安装依赖 → 配置 API Key → 运行 `uvicorn main:app --port 7866`（文档5）。

## 限制和注意事项

- **渠道限制**：
  - 微信公众号未认证时，仅支持被动回复且响应必须 ≤5 秒（文档3），建议 Prompt 中加入“请总是给出简短的回答”或切换至 `qwen-turbo`；
  - 企业微信要求可信 IP 配置，若使用第三方服务（如 AppFlow 默认出口 IP）会报错，需启用内网代理或部署自有 Nginx（文档2“常见问题”详述）；
  - 钉钉机器人必须配置为 **HTTP 模式**，Stream 模式不兼容（文档4明确警告）。
- **调试与排障**：
  - 嵌入网站后出现 `request error`：需三查——API Key 状态、业务空间一致性、应用 ID 正确性（文档1）；
  - 公众号无响应：检查 AppFlow 运行日志、认证状态匹配性、IP 白名单（文档3）；
  - “Failed to stream content”：通常因前端请求地址硬编码为 `/chat` 未替换为真实后端地址（文档1）。
- **数据与安全**：
  - 文档2指出文件解析后存储于新加坡区域，需确认合规性；
  - 本地 RAG 方案（文档5）规避云端知识上传，适合敏感数据场景，但需自行维护 Python 环境（3.9–3.12）及 embedding 模型。

> **注意**：文档2与文档3在知识库上传路径描述不一致（文档2用 `/data-center?dataType=0`，文档1/4用 `/connector/list`），实际功能相同，均为文件导入入口，属控制台 UI 迭代导致的路径差异，不影响操作。此细节在[在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)和[10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)中均有体现。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


