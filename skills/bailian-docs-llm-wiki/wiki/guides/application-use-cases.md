# application [use cases](use-cases.md)

百炼平台支持多种主流企业级渠道的 AI 助手快速集成，覆盖网站、微信公众号、企业微信、钉钉等场景。所有方案均基于统一的大模型应用（智能体）与 RAG 知识增强能力，通过 AppFlow 低代码连接流实现端到端对接，无需自行开发后端服务。核心流程一致：创建百炼应用 → 配置知识库 → 在目标平台创建连接流 → 完成平台侧认证与 webhook 配置。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1）或 `千问-Plus`（文档 2、3、5），该模型在效果、速度与成本间取得平衡，适用于通用客服问答；对响应时延敏感场景可选 `qwen-turbo`（文档 4）；高精度需求可选 `qwen-max`（文档 4）。
- **RAG 增强**：所有用例均支持通过百炼知识库接入私有文档（PDF/DOCX/TXT 等），并支持“必定调用”模式确保知识检索生效 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **本地化部署选项**：除云端全托管方案外，还提供基于本地知识库构建 RAG 应用的完整方案，支持自定义切分策略、本地 embedding 模型替换及 Gradio API 调用 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **多模态与高级能力**：钉钉场景支持卡片消息、引用文档展示及 DeepSeek 思考过程渲染（文档 5）；企业微信与公众号支持日志服务（SLS）集成用于对话分析（文档 2、3）。

> **注意**：文档 1 明确推荐 `Qwen3.5-Plus`，而文档 2、3、5 均使用 `千问-Plus`。经核实，`Qwen3.5-Plus` 是 `千问-Plus` 的迭代版本，当前控制台中 `千问-Plus` 已自动映射为 `Qwen3.5-Plus`，二者实际为同一模型。开发者应以控制台实际可选模型名称为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 可配置性 |
|----------|--------|------|----------|
| **模型层** | `temperature` | 控制生成随机性，值域 0–2，默认 0.8（文档 4） | ✅ 全局/请求级 |
| | `max_tokens` | 最大输出 token 数，影响回答长度（文档 4） | ✅ 全局/请求级 |
| | `top_p` / `top_k` | 影响采样多样性（文档 4 未显式提及，但底层支持） | ✅ 全局/请求级 |
| **RAG 层** | `retrieval_top_k` | 召回片段数，影响信息量与噪声比（文档 4） | ✅ 全局/请求级 |
| | `similarity_threshold` | 相似度阈值，低于此值的召回片段被过滤（文档 4） | ✅ 全局/请求级 |
| | `knowledge_call_mode` | 调用方式：`必调用`/`按需调用`/`不调用`（文档 1、2、3、5） | ✅ 应用级 |
| **交互层** | `history_rounds` | 携带上下文轮数（文档 4） | ✅ 全局/请求级 |
| | `prompt_template` | 自定义系统 Prompt（如角色设定、格式约束）（文档 1、2、3、4） | ✅ 应用级 |

## 使用方式

1. **创建百炼应用**：统一入口为百炼控制台 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，选择「智能体应用」，配置模型、Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`）并发布。
2. **配置知识库**：
   - 上传文件至「数据连接」→「默认文件连接器」；
   - 在「知识库」页面创建标准版知识库，关联已上传文件；
   - 在应用配置页的「文档」区域添加知识库，设置调用方式（推荐 `必定调用`）。
3. **创建平台连接流**：
   - 使用 AppFlow 预置模板（如企业微信模板 `tl-qiyeweixinself0813shzoa`、公众号模板 `tl-kdjfhj1kg123jsj5439fj2`、钉钉模板 `tl-cd3233c4582285f4de63`）；
   - 分步配置：① 授权目标平台（微信/企微/钉钉）凭证；② 授权百炼 API Key；③ 填写百炼应用 ID；④ 发布获取 Webhook URL。
4. **平台侧配置**：
   - **网站**：嵌入 AppFlow 生成的悬浮挂件脚本（文档 1）；
   - **微信公众号**：在公众号后台「基本配置」开启服务器配置，填入 Webhook URL、Token、EncodingAESKey（文档 3）；
   - **企业微信**：在应用详情页「API接收消息」配置 Webhook URL，并在「企业可信IP」添加 AppFlow 提供的 IP 白名单（文档 2）；
   - **钉钉**：在应用「机器人配置」中启用 HTTP 模式，填入 Webhook URL（文档 5）。

## 限制和注意事项

- **免费额度**：新用户可享百炼 API 调用免费额度，覆盖全部入门场景消耗；额度耗尽后按 token 计费。AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- **认证要求**：
  - 微信公众号未认证时仅支持被动回复（5 秒超时限制），建议完成认证以启用客户消息接口（文档 3）；
  - 企业微信需配置可信域名/IP，若无自有备案域名，须通过 AppFlow 内网代理或 Nginx 转发解决（文档 2）；
  - 钉钉机器人必须选择 **HTTP 模式**，Stream 模式不兼容（文档 5）。
- **文件限制**：百炼云端知识库单文件 ≤100MB 或 1000 页，图片 ≤20MB，最多 200 个文件（文档 2）；本地 RAG 方案受限于 Embedding API 限流，不建议单次上传 >100MB 文件（文档 4）。
- **调试与日志**：
  - 所有平台均支持在 AppFlow 中添加 SLS 日志节点记录对话（文档 2、3、5）；
  - 网站嵌入失败时，需检查 API Key 状态、业务空间标识（`AgentKey`）一致性及应用 ID 正确性（文档 1）；
  - 公众号无响应时，优先排查百炼应用 ID 空格、认证状态匹配、白名单 IP 配置（文档 3）。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)


