# 快速开始

3 步创建知识库，完成一次检索与问答

**重要**首次登录控制台时自动开通 RAG 知识库服务，并发放 720 小时免费额度。

## 前置条件

-   [阿里云账号](https://account.aliyun.com)
-   API Key（在[控制台 API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，以 `sk-` 开头）
-   准备一份 PDF / Word / Markdown 文件，以及一个能从该文件中找到答案的问题。

## 操作步骤

[

**1\. 创建并上传**

创建文档搜索知识库，等待索引就绪。

](#h-ragqs-create)[

**2\. 试问答**

在 Playground 获取带引用的回答。

](#h-ragqs-playground)[

**3\. API 检索**

获取相关切片供应用使用。

](#h-ragqs-retrieve)

### 1\. 创建知识库并上传文档

进入控制台 [**知识管理**](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，点击 **创建** 并选择 **标准版**。

1.  填写名称和描述，知识库类型选择 **文档搜索**，使用场景选择 **基础文档问答**，点击 **下一步**。
2.  数据来源选择 **上传文件**，拖拽或点击上传一份 PDF / Word / Markdown 文件。
3.  索引设置保持默认，点击 **完成**。

系统自动完成解析、切片、向量化与索引构建。知识库状态变为 **已就绪** 即可检索。

**重要**知识库类型、使用场景、切片策略等完整配置说明见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

### 2\. 在 Playground 中试问答

点击左侧 **Playground**，选择刚创建的知识库，在顶部切换到 **知识问答**，输入准备好的问题。

系统先检索相关切片，再调用大模型生成带引用的回答。可切换不同模型（如 qwen3.6-plus / qwen3.7-plus）对比效果。对照原文核对回答与引用。

### 3\. 通过 API 接入应用

先按 [API 服务地址](https://help.aliyun.com/zh/model-studio/rag-api-overview#h-ragapi-overview-endpoint) 在控制台**业务空间管理**中获取实际 `workspace_id`，替换下方地址中的 `{workspace_id}`。API Key 和知识库应属于这个业务空间，知识库状态应为**已就绪**。

将 API Key 配置到环境变量，替换占位值后执行：

```
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

`index_id` 在知识管理页面点击对应知识库即可复制。将 `<知识库ID>` 替换为此 ID，`<查询内容>` 替换为准备好的问题，再发起一次检索请求：

```
curl -X POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "index_id": "<知识库ID>",
    "query": "<查询内容>",
    "top_k": 5
  }'
```

**说明**返回的 `nodes` 数组包含命中切片，按相关性分数倒序排列。检查切片是否对应问题和原文；API 检索返回的是相关内容，不是大模型生成的回答。带引用的回答在第 2 步的控制台知识问答中查看。

**重要**也可通过阿里云百炼 CLI 检索：`bl knowledge search --agent-id <检索服务ID> --query "查询内容"`。检索服务需在[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)页面创建并发布；CLI 2.5.0 起不再提供按知识库 ID 直接检索的 `bl knowledge retrieve`。详见[使用 CLI](raw/application-user-guide/knowledge-base/integration/cli.md)。

## 下一步

[

**接入外部数据源**

用数据集连接业务文档。

](raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)[

**创建检索与问答服务**

从多库联合检索扩展到流式问答服务。

](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)[

**接入完整 API**

查看 API 参考与调用约定。

](raw/application-api-reference/rag-api/rag-api-overview.md)

创建问答服务获得流式回答：[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)。了解 RAG 工作原理：[核心概念](raw/application-user-guide/knowledge-base/rag-start-using/concepts.md)。
