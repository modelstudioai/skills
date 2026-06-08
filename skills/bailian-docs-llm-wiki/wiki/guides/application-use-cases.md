# application [use cases](use-cases.md)

本页汇总百炼平台开箱即用的若干典型应用方案，覆盖在网站、微信公众号、钉钉、企业微信等渠道上接入基于百炼 RAG 的 AI 助手/客服/机器人，以及在本地基于通义千问 API 构建 RAG 应用的方案。所有渠道接入方案均依托 AppFlow（无代码集成）+ 百炼智能体应用 + 知识库三件套实现，开发者可在 10 分钟内完成最小可用版本。

## 方案矩阵

下表整理了各场景的入口、是否需要外部凭证、典型耗时与文档链接，便于按渠道快速选型。

| 渠道 / 场景 | 集成方式 | 关键外部凭证 | 适用文档 |
| --- | --- | --- | --- |
| 网站悬浮 AI 助手 | AppFlow + Web 集成（悬浮挂件脚本） | 百炼 API Key、应用 ID | [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) |
| 微信公众号智能客服 | AppFlow + 微信公众号连接流（认证/未认证两条模板） | 百炼 API Key、应用 ID、公众号 AppID | [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) |
| 钉钉群机器人 | AppFlow + 钉钉应用（HTTP 模式 Webhook） | 百炼 API Key、应用 ID、钉钉 Client ID / Secret，并开通 `Card.Streaming.Write`、`Card.Instance.Write` | [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md) |
| 企业微信内部应用 | AppFlow + 企业微信 API 接收消息 | 百炼 API Key、应用 ID、企业 ID、AgentId、Secret，需配置可信 IP 与可信域名 | [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) |
| 本地 RAG 应用 | Python（FastAPI + Gradio + LlamaIndex），调用百炼通义千问 API 与可选 Embedding | 百炼 API Key | [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 共用前置步骤：创建大模型问答应用

四个渠道集成方案（网站、微信公众号、钉钉、企业微信）共享同一段前置步骤：

1. 进入百炼控制台**应用管理**，创建**智能体应用**。
2. 选择模型并保存其它默认参数；可选择性填写一段 system Prompt 设置角色。
3. 发布应用，前往**应用管理**复制**应用 ID**，前往**密钥管理 / API Key** 页创建并保存 **API Key**。

> **注意**：原文档中网站方案选模型为 **Qwen3.5-Plus**，而钉钉、微信公众号、企业微信方案均建议选**千问-Plus（qwen-plus）**。两者均为百炼推荐的"能力均衡"档位，没有功能差异；按当时控制台中可选的最新 Plus 档模型选择即可，不影响后续 AppFlow / Webhook 配置。

阿里云百炼对新用户提供[免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)，可覆盖以上教程消耗。

## 渠道集成方案

### 网站集成（悬浮挂件）

通过 AppFlow 创建 **AI 助手**，导入模型时选择**阿里云百炼**作为模型服务平台并新增凭证（填入 API Key + 应用 ID）；然后创建 **Web 页面集成**，自定义字体、背景、头像、预置问题。最后回到 **Web 集成 → 登录配置 → 匿名方式**，复制**悬浮挂件部署脚本**粘贴到目标网站 HTML 中即可。详见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。

如果暂时没有自有网站，可使用文档提供的[函数计算 FC 一键部署模板](https://fcnext.console.aliyun.com/applications/create?template=web-page-deploy)体验完整流程。

### 微信公众号

公众号渠道的关键决策是**是否完成微信认证**——它决定了应使用哪一份 AppFlow 模板：

- 已认证：使用[客户消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html)接口，对响应时间无 5 秒硬限制。
- 未认证：只能使用[被动回复消息](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html)接口，**5 秒超时即放弃回复**。对此场景应在百炼应用 Prompt 中强制要求简短回答（如"请总是给出简短的回答，不要讲太多"），或改用 **qwen-turbo** 以压缩首字延迟，否则极易触发限制。

授权过程必须用**公众号主管理员**微信扫码完成，普通管理员会失败。详见 [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)。

> **注意**：服务器配置一旦开启，公众号原有的**自定义菜单会因冲突自动关闭**；未认证账号无法同时启用服务器配置和自定义菜单，已认证账号可通过 `access_token` + `menu/create` 接口重新配置菜单。

### 钉钉

钉钉方案要求账号具备[开发者权限](https://open.dingtalk.com/document/orgapp/obtain-developer-permissions)，创建钉钉应用后需要**开通两项卡片消息权限**：`Card.Streaming.Write` 与 `Card.Instance.Write`。AppFlow 模板创建连接流后，会得到一个 **WebhookUrl**，将其填入钉钉应用的**机器人配置 → HTTP 模式 → 消息接收地址**即可。

> **注意**：消息接收模式**必须**选择 **HTTP 模式**，AppFlow 暂不支持 Stream 模式，选错将导致机器人不回消息。

应用配置完毕后，需进入**版本管理与发布**创建新版本并选择**应用可见范围**，才能被组织内成员搜索到。详见 [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md)。

可选增强：通过修改 AppFlow 卡片模板与 Prompt（`{{Node2.reasoning}}` / `{{Node2.text}}`），可在卡片中展示**回答引用的文档**或 **DeepSeek 深度思考过程**。

### 企业微信

企业微信方案与钉钉类似，差异点在于必须配置**企业可信 IP**与**API 接收消息**（URL = WebhookUrl，Token / EncodingAESKey 由 AppFlow 创建凭证时生成）。

- **域名校验**：企业微信要求接收消息域名与企业备案主体一致。若 WebhookUrl 主机名校验失败，需通过 AppFlow 域名管理添加二级域名（已在阿里云备案的可一键创建 CNAME），或勾选 **AppFlow 凭证 → 内网代理**，由计算巢 / 自有 Nginx / ECS 托管实例做请求转发。
- **可信 IP 唯一性**：同一个可信 IP 仅能服务一个企业，否则企业微信会判定为第三方服务商，导致通讯录、身份校验接口不可用。需通过自有 ECS 或托管实例做请求转发以隔离。

详见 [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 本地 RAG 应用（Python 方案）

如果业务需要把**知识库与检索环节保留在本地**（更灵活的切分策略 / 嵌入模型 / 避免大文件上传），可参考 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。该方案将**检索**留在本地（LlamaIndex 向量存储 + 可选嵌入模型），**生成**调用百炼通义千问 API。

环境与运行：

- Python `>= 3.8` 且 `<= 3.12`。
- 解压 [local_rag.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/odwvrb/local_rag.zip)，`pip install -r requirements.txt`。
- 配置 `DASHSCOPE_API_KEY` 到环境变量。
- `uvicorn main:app --port 7866` 启动 Gradio 界面，浏览器访问 `http://127.0.0.1:7866`。

知识库与文件管理：

- 临时上传：在 RAG 问答输入框旁直接附件上传 pdf / docx / txt / xlsx / csv，**页面刷新后失效**。
- 长期使用：通过**上传数据**+**创建知识库**入口，结构化数据落 `File/Structured`，非结构化落 `File/Unstructured`，向量数据落 `VectorStore`。
- 单文件不建议超过 100 MB（受嵌入模型 API 限流影响）。

可调参数（在 Gradio 界面中即时生效）：

- 模型：`qwen-max`（效果）/ `qwen-plus`（均衡）/ `qwen-turbo`（速度）。
- 温度：控制随机性。
- 最大回复长度：控制输出 token 上限。
- 携带上下文轮数：设为 1 表示无历史。
- 召回片段数 / 相似度阈值：检索粒度调优。
- 默认嵌入模型为百炼托管 API；如需切到本地 GTE 中文 embedding，按文档取消 `chat.py` / `create_kb.py` 中的 ModelScope 段注释并 `modelscope download` 模型。

应用同时通过 **Gradio "通过 API 使用"** 提供 API 自动文档，可直接集成进业务后端。

## 通用配置与运维要点

### 知识库（RAG）

四个渠道集成方案的"为应用增加私有知识"步骤完全一致：

1. **数据连接 / 文件上传**：在百炼控制台**数据连接 → 默认文件连接器**（或**数据中心 → 文件**）导入数据，解析通常需要 1–6 分钟。
2. **创建知识库**：选**标准版**，绑定上传的文件，向量存储类型若希望多应用共享可选 **ADB-PG**，否则保留默认。
3. **应用绑定**：回到应用配置页绑定知识库，**调用方式选"必定调用"**，测试通过后**发布**。

### 对话日志 / 链路调试

对于通过 AppFlow 接入的方案（公众号、钉钉、企业微信），可在 AppFlow 工作流中编辑版本，添加 **SLS 日志云服务** 节点并选择**写入日志**动作，将对话 Key/Value 写入指定 Project + Logstore（需开启全文索引才能查询）。出现"对话无响应"先到 AppFlow **运行日志 → 详情**排查；常见原因：

- 应用 ID 填错或前后含空格；
- 公众号未认证却用了已认证模板；
- 微信公众号未配置 AppFlow 白名单 IP；
- 模型生成超过 5 秒（仅未认证公众号场景触发）。

### 应用质量与持续优化

正式上线前建议通过百炼[人工评测 / 应用评测](https://help.aliyun.com/zh/model-studio/evaluate-application/)流程组织业务方共建测试集；不达预期时迭代 Prompt、补私有知识或调整文档切分策略。

## 来源文档

- [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)
- [10分钟让微信公众号成为智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md)
- [10分钟在钉钉上增加一个AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk-in-10-minutes.md)
- [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)
- [在企业微信中集成一个 AI 助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)




