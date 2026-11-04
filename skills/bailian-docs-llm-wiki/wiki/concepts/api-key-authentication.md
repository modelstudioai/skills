# API Key 鉴权

API Key 鉴权是百炼平台统一采用的轻量级身份认证机制，通过在 HTTP 请求头中携带 `Authorization: Bearer <API-Key>`，验证调用方是否具备对应[业务空间（Workspace）](workspace.md)下的合法访问权限。该机制不依赖会话状态，适用于所有面向开发者的 RESTful 和 SDK 调用场景。

## 在百炼平台的不同场景中如何使用

API Key 是百炼所有**面向应用层调用接口**的唯一认证凭证，覆盖以下核心能力域：

- **模型服务调用（Preparations）**：文本生成、多模态对话、向量嵌入等基础模型 API 均需在请求头中传入 `Authorization: Bearer <your-api-key>`；SDK 初始化时也需显式传入 `api_key` 参数（如 `Client(api_key=...)`）。
- **RAG 知识库服务（RAG API）**：知识库管理、文档导入、语义检索与问答等全部接口均强制要求 `Authorization` 头，且必须与请求 Endpoint 中的 `workspace_id` 所属空间一致。
- **智能体与工作流调用（Flow Agent API）**：所有 DashScope 网关类接口（如 `/apps/{app_id}/completion`）均使用 API Key 鉴权；注意：组件管理类接口（如 Prompt 模板、[长期记忆](long-term-memory.md)）使用 AccessKey 签名，**不可混用**。
- **沙箱环境管理（Sandbox API）**：沙箱实例创建、模版构建、连接等操作均依赖 `Authorization: Bearer <API-Key>`，并需与 `workspace_id` 绑定的专属域名配合使用。
- **安全防护数据查询（Security API）**：防护总览、策略配置、告警列表等接口均通过 `Authorization` 头完成鉴权，且严格限定地域为 `cn-beijing`。

> ⚠️ 关键约束：API Key 与地域、业务空间强绑定。跨地域使用（如北京 Key 调用新加坡 Endpoint）或 Key 与 Workspace ID 不匹配，将直接返回 `401 Unauthorized` 或 `404 Not Found`。

## 关键参数和配置

- **Header 字段**：`Authorization: Bearer <your-api-key>`  
  - `<your-api-key>` 为控制台生成的 32 位十六进制字符串（以 `sk-` 开头），**不可泄露或硬编码**。
- **环境变量推荐配置**：`DASHSCOPE_API_KEY`（SDK 自动读取）  
- **SDK 初始化示例（Python）**：
  ```python
  from dashscope import Client
  client = Client(
      api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      workspace="llm-xxxxxxxxxxxx",  # 业务空间 ID
      region="cn-beijing"             # 必须与 Key 所属地域一致
  )
  ```
- **Endpoint 构造规则**：所有生产环境请求必须使用业务空间专属域名，格式为：  
  `https://{workspace_id}.{region}.maas.aliyuncs.com/...`  
  例如：`https://llm-abc123.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search`

## 面向开发者的重要实践建议

- ✅ **安全第一**：永远将 API Key 存储在环境变量、密钥管理服务（如阿里云 KMS）或受控配置中心中；禁止提交至 Git、前端代码或日志。
- ✅ **按需申请**：在百炼控制台「API Key」页面按业务空间粒度创建 Key，最小化权限范围；试用 Key 仅限开发测试，生产环境请使用独立 Key。
- ✅ **错误快速定位**：
  - `401 Unauthorized` → 检查 Key 是否过期、拼写错误，或是否误用了 DashScope 全局域名（`dashscope.aliyuncs.com`）；
  - `403 Forbidden` → 检查当前账号是否拥有该 Workspace 的访问权限；
  - `404 Not Found` → 核对 `workspace_id` 是否正确、Endpoint 地域是否匹配、API 路径是否拼写准确。
- ❌ **禁止行为**：不要在客户端（如浏览器、移动端）直接使用长期 API Key；不要复用其他阿里云产品（如 OSS、OSS）的 AccessKey；不要在公开文档或示例中暴露真实 Key。

API Key 是你接入百炼能力的第一道门——配得准、用得稳、管得严，才能高效、安全地释放大模型价值。

## 关联主题页

- [preparations](../api/preparations.md)
- [rag api](../api/rag-api.md)
- [flow agent api](../api/flow-agent-api.md)
- [sandbox api](../api/sandbox-api.md)
- [security api guide](../api/security-api-guide.md)


