# application [use cases](use-cases.md)

阿里云百炼平台支持多种主流企业通讯与网站场景下的 AI 应用快速落地，核心模式为“大模型推理 + RAG 知识增强”，无需编码即可在 10 分钟内完成部署。所有方案均基于统一的百炼应用（智能体）作为后端推理服务，并通过 AppFlow 实现与前端渠道（网站、微信公众号、企业微信、钉钉）的低代码集成。知识库配置、Prompt 调优与效果评测等治理能力贯穿各场景，确保生产可用性。

## 支持的模型/功能

- **基础模型**：推荐使用 `Qwen3.5-Plus`（文档 1 中明确指定）或 `千问-Plus`（文档 2、3、4 均采用），该模型在效果、速度与成本间取得平衡，适用于客服问答类任务；也可选 `qwen-max`（高精度）、`qwen3.5-flash`（高吞吐）等变体，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。
- **核心功能**：
  - 网站悬浮式 AI 助手（含拖拽、预置问题、主题定制）；
  - 微信公众号智能客服（支持认证/未认证两种流，响应时效敏感）；
  - 企业微信自建应用机器人（需配置可信 IP 与域名主体校验）；
  - 钉钉群机器人（仅支持 HTTP 模式，需开通 `Card.Streaming.Write` 权限）；
  - 本地化 RAG 应用（知识检索在本地执行，生成调用百炼 API）[基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

> **注意**：文档 1 中模型名称写作 `Qwen3.5-Plus`，而文档 2–4 统一写作 `千问-Plus`。二者实为同一模型（`qwen-plus`），命名差异属历史文档不一致，开发时请以控制台实际可选模型 ID（如 `qwen-plus`）为准，避免硬编码别名。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `AppID`（百炼应用 ID） | 百炼控制台「应用管理」中创建的智能体唯一标识，用于绑定模型与知识库 | 必填，需与 API Key 同属一个业务空间（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题） |
| `API Key` | 百炼控制台「密钥管理」生成的凭证，用于鉴权调用 | 必填，有效期默认永久，但建议定期轮换；需与 AppID 在同一业务空间 |
| `AgentKey`（业务空间标识） | 用于校验 API Key 与智能体归属关系，非公开参数，由 AppFlow 自动注入 | 若出现 `request error`，需检查此项是否一致（见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 常见问题） |
| `WebhookUrl` | AppFlow 生成的回调地址，供微信/企业微信/钉钉转发用户消息 | 仅企业微信、钉钉、微信公众号（认证版）需配置；企业微信还需同步配置 `Token` 与 `EncodingAESKey`（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)） |
| `召回片段数` / `相似度阈值` | 控制 RAG 检索阶段返回的上下文质量与数量 | 本地 RAG 场景可精细调节（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)），云端标准知识库仅支持 `必定调用`/`按需调用` 两级开关 |

## 使用方式

1. **统一后端准备**：  
   所有场景均需先在百炼控制台创建「智能体应用」，选择模型（如 `qwen-plus`），配置 Prompt（如 `你叫小助，可以帮助用户解答产品选购、使用等方面的问题。`），并发布应用；随后获取 `AppID` 与 `API Key`。

2. **渠道侧集成**：  
   - **网站**：在 AppFlow 创建「AI助手」→ 导入百炼应用 → 配置 Web 集成 → 复制悬浮挂件脚本插入 HTML。  
   - **微信公众号**：在 AppFlow 使用预置模板 → 授权公众号（主管理员扫码）→ 绑定百炼应用 → 发布。注意未认证号受 5 秒响应限制，需优化 Prompt 或换用 `qwen-turbo`。  
   - **企业微信**：创建企业微信自建应用 → 获取 `CorpID`/`AgentId`/`Secret` → AppFlow 模板授权 → 配置 API 接收消息（填 `WebhookUrl`+`Token`+`EncodingAESKey`）→ 配置可信 IP。  
   - **钉钉**：创建钉钉应用 → 开通 `Card.Streaming.Write` 权限 → AppFlow 模板绑定 → 配置 HTTP 机器人 → 发布应用版本。  

3. **知识增强（RAG）**：  
   - 上传文件至百炼「数据连接」或「文件」页签；  
   - 在「知识库」页面创建标准版知识库，关联上传文件；  
   - 在智能体应用配置中启用「知识库」开关，选择目标知识库，设置调用方式（推荐 `必定调用`）并发布。

## 限制和注意事项

- **免费额度**：新用户可使用百炼提供的[新用户免费额度](../../raw/model-user-guide/test-1/new-free-quota.md)，覆盖模型调用消耗；AppFlow、函数计算 FC、ADB-PG 等依赖服务单独计费。
- **文件限制**：百炼云端知识库单文件 ≤ 100 MB 或 1000 页，支持格式包括 `.pdf`, `.docx`, `.txt`, `.xlsx`, `.png` 等；本地 RAG 应用暂不支持图片解析（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）。
- **响应时效**：微信未认证号、企业微信部分接口存在 5 秒超时限制，超时将导致回复失败。解决方案包括：① 完成微信认证；② Prompt 中强制要求简短回答；③ 切换至响应更快的模型（如 `qwen-turbo`）。
- **安全配置**：  
  - 企业微信需解决「域名主体校验未通过」问题，必须配置自有备案域名或通过 Nginx 代理转发（见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）；  
  - 钉钉机器人**必须**选择 HTTP 模式，Stream 模式不兼容（见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）；  
  - 所有渠道均需确保 AppFlow 凭证（API Key、公众号 AppID、企业微信 CorpID 等）与对应服务端配置完全一致，空格、大小写错误均会导致鉴权失败。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


