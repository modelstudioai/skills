# application [use cases](use-cases.md)

百炼平台围绕“[检索增强生成](../concepts/rag.md)（RAG）+ [智能体应用](../concepts/agent-application.md)”提供了多种开箱即用的应用场景，可在无需编码或少量编码的情况下，将大模型问答能力接入网站、企业微信、微信公众号、钉钉等渠道，并支持基于本地[知识库](../concepts/knowledge-base.md)构建 RAG 应用。本页汇总这些典型用法的关键流程、模型选择、参数配置与注意事项。

## 支持的接入渠道

百炼 RAG 应用可通过 AppFlow（无代码连接流）或本地部署方式接入以下渠道：

- 网站：通过 AppFlow 创建 AI 助手并生成悬浮挂件部署脚本，粘贴到网站 HTML 即可。详见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
- 企业微信：通过 AppFlow 模板“企业微信自建应用大模型自动回复”连接企业微信应用与百炼应用。详见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。
- 微信公众号（订阅号）：通过 AppFlow 模板连接公众号与百炼应用，完成认证的公众号可用客户消息接口，未认证只能被动回复且响应限制为 5 秒。详见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。
- 钉钉：创建钉钉应用并通过 AppFlow 模板连接，机器人消息接收模式必须选 HTTP 模式。详见 [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)。
- 本地[知识库](../concepts/knowledge-base.md) RAG：检索环节在本地执行，生成环节调用通义千问 API，适合需要灵活切分与嵌入模型选择的场景。详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 通用流程

各渠道方案共享相似的四到五步骨架：

1. 创建百炼[智能体应用](../concepts/agent-application.md)并获取应用 ID 与 [API Key](../concepts/api-key.md)；
2. 在目标平台（企业微信 / 公众号 / 钉钉）创建应用或机器人，获取对应凭证（企业 ID、AgentId、Secret、AppID、Client ID/Secret 等）；
3. 通过 AppFlow 模板创建连接流，填入双方凭证与应用 ID，发布并获取 WebhookUrl；
4. 在目标平台配置消息接收地址为 WebhookUrl，并配置可信 IP / 白名单；
5. 为百炼应用添加私有[知识库](../concepts/knowledge-base.md)（RAG），让回答覆盖私域问题。

网站方案略不同：第 2–3 步改为在 AppFlow 创建 AI 助手并生成 web 页面集成脚本，第 4 步将悬浮挂件脚本粘贴到网站 HTML。

## 模型选择

各教程对模型选择存在差异，需注意版本与命名：

- 网站方案原选 **Qwen3.5-Plus**，其余渠道教程多选 **千问-Plus**（qwen-plus）。
- 本地 RAG 应用可选 qwen-max、qwen-plus、qwen-turbo 三个通义千问商业模型：qwen-max 性能优秀，qwen-turbo 速度更快价格更低，qwen-plus 效果、速度、成本均衡。

> **注意**：不同文档对模型命名不一致（“Qwen3.5-Plus”与“千问-Plus”）。实际配置时以百炼控制台“更多模型”列表中可用的版本为准。未认证公众号若超 5 秒未返回，可在 [prompt](prompt.md) 中加“请总是给出简短的回答”或改用 qwen-turbo 提速，但会降低效果。

## 关键参数

百炼应用侧：

- Prompt：可设置角色人设引导回答，如“你叫小助，可以帮助用户解答产品选购、使用等方面的问题。”
- 知识库调用方式：可选**必定调用**；知识文档支持配置相似度阈值与权重。
- 文件处理：可选全文引用、切片检索或自定义处理。
- 向量存储：标准版默认即可；如需集中管理多应用向量数据可选 ADB-PG。

本地 RAG 应用侧：

- 模型参数：模型选择、温度（越高随机性越高）、最大回复长度、携带上下文轮数（设为 1 时不参考历史）。
- RAG 参数：召回片段数（越大参考越多但噪声可能增加）、相似度阈值（越大参考越少但噪声减少，为 0 不剔除）。
- 嵌入模型：默认用百炼 embedding API；可改用本地部署的 GTE 文本向量模型（如 `iic/nlp_gte_sentence-embedding_chinese-large`）。
- 文件限制：受 embedding API 限流，不建议传入超过 100 MB 的文件。

AppFlow 连接流：

- 钉钉消息接收模式必须选 **HTTP 模式**，Stream 模式会导致无法返回消息。
- 公众号需区分已认证 / 未认证两条工作流；未认证只能被动回复，5 秒超时。
- 企业微信需配置企业可信 IP；若报“域名主体校验未通过”，需配置企业自有域名或通过 ECS / 托管实例 / 计算巢 Nginx 代理转发。

## 使用方式

网站接入：在 AppFlow AI 助手 Web 集成页复制悬浮挂件部署脚本，粘贴到网站 HTML 注释下方；可选启用图标拖拽。也可用函数计算 FC 一键部署示例网站。

企业微信 / 公众号 / 钉钉：发布连接流后，在目标平台配置 API 接收消息（URL 填 WebhookUrl，[Token](../concepts/token.md) / EncodingAESKey 填 AppFlow 凭证生成的值），配置可信 IP，即在聊天中 @机器人 或直接对话使用。

本地 RAG：解压 `local_rag.zip`，Python 3.8–3.12 环境安装依赖，配置百炼 [API Key](../concepts/api-key.md) 环境变量，运行 `uvicorn main:app --port 7866`，访问 `http://127.0.0.1:7866`。支持临时性文件上传（对话框直接传 pdf/docx/txt/xlsx/csv，刷新后失效）与长期知识库创建（上传到 File/Unstructured 或 File/Structured 后在界面创建知识库存于 VectorStore）。通过 Gradio 界面下方的“通过 API 使用”可获取 API 文档集成到业务。

## 日志与扩展

AppFlow 连接流可在百炼步骤后添加 SLS 日志云服务节点，将对话写入阿里云日志服务（需创建 Project/Logstore 并开启全文索引）。钉钉还支持通过卡片平台导入模板展示回答引用的文档来源，以及展示 DeepSeek 深度思考过程（在发送 AI 卡片阶段填入 `思考过程： {{Node2.reasoning}}` 与 `推理结果： {{Node2.text}}`）。

## 限制和注意事项

- 新用户免费额度可覆盖教程资源消耗，超额后按 token 计费。
- 百炼文件导入支持 pdf、doc、docx、txt、md、pptx、ppt、png、jpg、jpeg、bmp、gif、xls、xlsx，单文档最大 100MB 或 1000 页，单图片最大 20MB，最多 200 个文件；文件存储在新加坡区域，解析通常 1–6 分钟。
- 钉钉应用需开通 `Card.Streaming.Write` 与 `Card.Instance.Write` 权限以发送卡片消息；应用供企业内其他用户使用需发布版本并设置可见范围。
- 企业微信可信 IP 一个 IP 仅能用于一个企业，多企业共用会被识别为服务商导致通讯录 / 身份校验接口不可用。
- 公众号开启服务器配置后自定义菜单会冲突关闭；未认证无法同时开启二者，已认证可通过接口重建菜单。
- 本地 RAG Windows 系统若缺少 Microsoft Visual C++ Redistributable 需另行安装；报 `DLL load failed while importing _cext:` 时运行 `pip install msvc-runtime`。
- 上线前建议组织业务人员参与应用评测，结合优化提示词、补充私有知识、调整切分策略改进效果。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)


