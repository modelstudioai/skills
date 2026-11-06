# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业通讯与网站场景下的 AI 应用快速落地，核心模式为“大模型应用 + RAG 知识增强 + 低代码集成”。开发者可基于百炼创建智能体应用，通过 AppFlow 与微信公众号、企业微信、钉钉、网站等渠道无缝对接，无需编写后端服务即可实现 7×24 小时智能客服能力。所有方案均默认复用百炼的模型推理、知识库与 API Key 体系，具备统一的权限、计费与可观测性管理。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 均采用），该模型在效果、速度与成本间取得平衡，适用于通用问答、客服响应等任务；也可选用 `qwen-max`（高精度）、`qwen3.5-flash`（高吞吐）等变体，具体见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 的模型参数说明。
- **核心能力**：
  - 智能体（Agent）应用：支持 Prompt 角色设定（如“你叫小助，帮助解答产品选购问题”）、多轮对话管理；
  - RAG 知识增强：支持上传 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`, `.md`, `.pptx`, `.png`, `.jpg` 等格式文件（文档 3 明确列出全部支持类型），自动解析并构建向量知识库；
  - 多源集成：原生支持网站悬浮窗、微信公众号（订阅号）、企业微信（自建应用）、钉钉机器人四类渠道，均由 AppFlow 提供零代码连接流模板。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2–4 统一写作 `千问-Plus`。二者实为同一模型（`qwen-plus`），命名差异属历史版本表述不一致，以控制台实际下拉选项为准。建议开发者在创建应用时直接选择控制台中显示的 `qwen-plus`。

## 关键参数

| 参数类别 | 参数名 | 说明 | 取值建议 | 来源依据 |
|----------|--------|------|-----------|-----------|
| **模型配置** | `temperature` | 控制生成随机性 | 0.1–0.6（客服场景建议偏低） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `max_tokens` | 最大输出长度 | 512–2048（长文档摘要可调高） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| **RAG 配置** | `retrieval_top_k` | 召回片段数 | 3–5（平衡精度与噪声） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `similarity_threshold` | 相似度阈值 | 0.3–0.7（0 表示不限制） | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |
| | `knowledge_call_mode` | 知识调用方式 | `必定调用`（强依赖私有知识时）或 `按需调用` | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |

## 使用方式

1. **创建百炼应用**：进入[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择**智能体应用** → 设置模型（`qwen-plus`）与 Prompt → **发布**；
2. **获取凭证**：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页复制 **App ID**；在[API Key](https://bailian.console.aliyun.com/?tab=app#/api-key)页创建并保存 **API Key**；
3. **配置知识库（可选但推荐）**：
   - 上传文件至[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)或[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)页签；
   - 进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)创建标准版知识库；
   - 在应用配置中启用知识库，设置调用方式（如 `必定调用`）；
4. **集成到目标渠道**：
   - **网站**：在 AppFlow 创建 AI 助手 → 配置 Web 页面集成 → 复制悬浮挂件脚本嵌入 HTML；
   - **微信公众号**：在 AppFlow 使用预置模板 → 授权公众号 → 绑定百炼应用 ID 与 API Key；
   - **企业微信/钉钉**：先在对应平台创建自建应用 → 获取 `CorpID`/`AgentId`/`Secret` 或 `Client ID`/`Client Secret` → 在 AppFlow 模板中填入凭证与百炼参数；
5. **验证与日志**：通过渠道端直接对话测试；如需分析，可在 AppFlow 连接流中添加 **SLS 日志云服务** 步骤记录对话（文档 2、3、4 均提供详细步骤）。

## 限制和注意事项

- **免费额度覆盖范围**：新用户免费额度可覆盖百炼模型调用消耗（文档 1、3、4 均强调），但 AppFlow、函数计算 FC、ADB-PG 向量存储等依赖服务单独计费；
- **文件限制**：
  - 单文件最大 100 MB 或 1000 页（文档 3 明确）；
  - 图片单张最大 20 MB（文档 3）；
  - 上传总数上限 200 个文件（文档 3）；
- **渠道特异性限制**：
  - 微信公众号未认证时，消息响应必须 ≤5 秒，否则失败；建议完成认证或改用 `qwen-turbo` 加速（文档 2 常见问题）；
  - 钉钉机器人**必须**配置为 HTTP 模式，Stream 模式不兼容（文档 4 强调）；
  - 企业微信配置 API 接收时，若遇“域名主体校验未通过”，需配置自有备案二级域名或使用 Nginx 代理（文档 3 详述）；
- **安全与权限**：
  - 百炼应用与 API Key 必须处于**同一业务空间**，否则鉴权失败（文档 1 常见问题）；
  - 企业微信/钉钉凭证中的 `IP 白名单` 必须准确配置，否则接口调用被拒（文档 3、4 均要求）；
- **调试建议**：遇到 `Failed to stream content` 或无响应时，优先检查浏览器控制台网络请求、AppFlow 执行日志（文档 1、2 均提供排查路径）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


