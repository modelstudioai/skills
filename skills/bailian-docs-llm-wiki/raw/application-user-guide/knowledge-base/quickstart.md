# 快速开始

5 步创建知识库，完成一次检索与问答

**重要**首次登录控制台时自动开通 RAG 知识库服务，并发放 720 小时免费额度。

## 前置条件

-   [阿里云账号](https://account.aliyun.com)
-   API Key（在[控制台 API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，以 `sk-` 开头）

## 操作步骤

1.  **创建知识库并上传文档**：进入控制台 [**知识管理**](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)，点击 **创建知识库**。
    
    1.  填写名称和描述，知识库类型选择 **文档搜索**，使用场景选择 **基础文档问答**，点击 **下一步**。
    2.  数据来源选择 **上传文件**，拖拽或点击上传一份 PDF / Word / Markdown 文件。
    3.  索引设置保持默认，点击 **创建知识库**。
    
    系统自动完成解析、切片、向量化与索引构建。知识库状态变为 **已就绪** 即可检索。
    
    **重要**知识库类型、使用场景、切片策略等完整配置说明见[创建知识库](raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
    
2.  **在 Playground 中试问答**：点击左侧 **Playground**，选择刚创建的知识库，在顶部切换到 **知识问答**，输入一个问题。
    
    系统先检索相关切片，再调用大模型生成带引用的回答。可切换不同模型（Qwen / DeepSeek）对比效果。
    
3.  **通过 API 接入应用**：先将 API Key 配置到环境变量：
    
    ```
    export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
    ```
    
    再发起一次检索请求：
    
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
    
    `index_id` 在知识管理页面点击对应知识库即可复制。返回的 `nodes` 数组包含命中切片，按相关性分数倒序排列。
    
    **重要**也可通过阿里云百炼 CLI 快速检索：`bl knowledge retrieve --index-id <知识库ID> --query "查询内容" --top-k 5`。详见[使用 CLI](raw/application-user-guide/knowledge-base/integration/cli.md)。
    

## 下一步

-   了解 RAG 工作原理：[核心概念](raw/application-user-guide/knowledge-base/concepts.md)
-   接入外部数据源：[数据集](raw/application-user-guide/knowledge-base/data-connection-overview/data-connection.md)
-   创建检索服务实现多库联合检索：[知识检索](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)
-   创建问答服务获得流式回答：[知识问答](raw/application-user-guide/knowledge-base/service/rag-knowledge-qa.md)
-   查看完整 API：[API 参考](raw/application-api-reference/rag-api/rag-api-overview.md)
