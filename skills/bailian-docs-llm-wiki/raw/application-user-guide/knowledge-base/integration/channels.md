# 服务渠道

API / MCP / CLI / Skill 等多种接入方式

知识检索和问答服务发布后，可以通过多种渠道接入到你的应用中。在控制台 [**应用集成 → 服务渠道**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面，可以查看各渠道的接入信息和示例代码。

## 接入方式对比

渠道

类型

适用场景

说明

**REST API**

REST / SSE

自有后端服务

DashScope HTTP 接口，配套多语言 SDK（Python / Java）

**MCP Server**

MCP 协议

AI Agent 框架

支持 Qoder / Claude Code / Codex 等客户端

**CLI**

命令行

本地调试 / 脚本

`bailian-cli`，终端中直接检索和问答

**Agent Skill**

技能包

Qoder / Claude Code

以技能包形式接入，AI 编码工具自动加载

**阿里云百炼 Agent**

Web

快速验证 / 低代码

阿里云百炼智能体应用，支持 Agent 绑定和 Workflow 绑定

## REST API

所有检索与问答能力通过 DashScope API 提供，服务地址为 `https://{workspaceId}.cn-beijing.maas.aliyuncs.com`。

**鉴权方式：**

```
Authorization: Bearer <API-Key>
```

API Key 在[控制台 API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)创建，系统根据 API Key 自动路由到对应业务空间。

**主要接口：**

接口

方法

路径

说明

知识搜索

POST

`/api/v1/indices/knowledge/search`

应用级联合检索，由知识检索服务配置驱动，调用方仅需传入 `query` 和 `agent_id`

知识问答

POST

`/api/v2/apps/knowledge/chat`

流式问答，返回 SSE 事件

底层检索

POST

`/api/v1/indices/rag/index/retrieve`

单知识库底层检索，直接返回向量 + 关键词召回结果，不在此层做重排

**知识搜索接口示例**（控制台服务渠道页面提供的示例）：

```
curl -X POST 'https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/knowledge/search' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer $DASHSCOPE_API_KEY' \
  -d '{
    "query": "${YOUR_QUERY}",
    "agent_id": "${YOUR_APP_ID}"
  }'
```

检索范围和策略（多库权重、路由、混排等）由 `agent_id` 对应的知识检索服务配置驱动，调用方无需在请求中重复传入检索参数。

**底层检索接口示例**（直接指定知识库 ID）：

```
curl -X POST https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/index/retrieve \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "index_id": "<知识库ID>",
    "query": "如何配置切片策略？",
    "top_k": 5
  }'
```

**说明**单知识库底层检索接口直接返回向量 + 关键词召回结果，不在此层做重排。如需 Rerank 精排，在创建检索服务时配置混排模型，通过知识搜索接口（`agent_id`）调用。

完整接口列表见 [API 参考](raw/application-api-reference/rag-api/rag-api-overview.md)。

## MCP Server

MCP（Model Context Protocol）是一种开放协议，让 AI 编码助手和 Agent 框架直接调用外部工具。接入 RAG MCP Server 后，你的 AI 助手可以在对话中检索知识库内容。

### 前置条件

-   已创建至少一个知识库，且包含已解析完成的文档
-   已获取 [API Key](raw/application-api-reference/rag-api/rag-api-authentication.md)
-   已安装支持 MCP 协议的客户端（Qoder、Claude Code、Codex 等）

### 接入步骤

1.  **获取 API Key**
    
    在[控制台 API Key 页](https://bailian.console.aliyun.com/?tab=model#/api-key)创建 API Key。建议将 API Key 存为环境变量：
    
    ```
    export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
    ```
    
2.  **在客户端中添加 MCP Server**
    
    根据你使用的客户端，选择对应的配置方式：
    
    #### Qoder / QoderWork
    
    打开 MCP 配置文件，添加以下内容：
    
    ```
    {
      "mcpServers": {
        "rag_mcp": {
          "type": "streamableHttp",
          "url": "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/mcp",
          "headers": {
            "Authorization": "Bearer ${DASHSCOPE_API_KEY}"
          }
        }
      }
    }
    ```
    
    #### Claude Code
    
    在终端中执行：
    
    ```
    claude mcp add --transport http rag-mcp-server \
      https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/mcp \
      --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
    ```
    
    #### Codex
    
    在 Codex 配置文件中添加：
    
    ```
    [mcp_servers.rag_mcp_server]
    url = "https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/mcp"
    http_headers = {
        "Authorization" = "Bearer ${DASHSCOPE_API_KEY}"
    }
    ```
    
    Codex 0.120.0 及以上版本支持。
    
3.  **验证连接**
    
    配置完成后，在客户端中尝试调用知识库。例如在 Claude Code 中输入：
    
    > 帮我在知识库里搜索"如何创建知识库"
    
    如果 AI 助手成功调用了 `Retrieve` 工具并返回检索结果，说明接入成功。
    

### 连接信息

项

值

端点

`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/indices/rag/mcp`

协议版本

MCP 2024-11-05

传输方式

Streamable HTTP（POST + GET SSE）

鉴权

`Authorization: Bearer <API-Key>`

### 提供的工具（Tools）

工具名

功能

说明

`Retrieve`

检索知识库

从指定知识库检索相关切片，支持混合检索和 Rerank

`ListIndices`

查询知识库列表

分页获取当前业务空间下的知识库列表

`Retrieve` 的参数：

参数

类型

必填

默认值

说明

`IndexId`

string

是

—

知识库索引 ID

`Query`

string

是

—

查询文本，不能为空

`DenseSimilarityTopK`

integer

否

100

语义检索召回数量，范围 0–100

`SparseSimilarityTopK`

integer

否

100

关键词检索召回数量，范围 0–100

`EnableReranking`

boolean

否

true

是否启用重排序

`Rerank.ModelName`

string

否

qwen3-rerank

排序模型，可选 `qwen3-rerank` 或 `qwen3-rerank-hybrid`

**警告**`DenseSimilarityTopK` 与 `SparseSimilarityTopK` 之和必须大于 1，不支持只用其中一种方式检索（例如 Dense=1, Sparse=0 会报错）。

**说明**Rerank 对象中的 `RerankMode`、`RerankMinScore`、`RerankTopN`、`RerankInstruct` 参数当前版本暂不可用，传入会返回错误。如需控制重排序行为，使用 `EnableReranking` 和 `Rerank.ModelName` 即可。

`ListIndices` 的参数：

参数

类型

必填

默认值

说明

`pageNumber`

integer

否

1

页码，从 1 开始

`pageSize`

integer

否

10

每页数量

`indexName`

string

否

—

按知识库名称前缀过滤

**支持的客户端：**

-   Qoder / QoderWork
-   Claude Code
-   Codex（0.120.0+）
-   其他支持 MCP 协议的客户端

## CLI

`bailian-cli` 是知识库的命令行工具。无需编写代码，在终端中一条命令即可检索知识库，适合本地调试、脚本集成和 CI/CD 流程。控制台 [**服务渠道**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面提供安装命令和使用示例。

**重要**`bailian-cli` 除知识库检索外，还封装了图像 / 视频生成、语音、视觉理解、长期记忆等 10+ 项能力。完整能力与安装说明见 [使用 CLI](raw/application-user-guide/knowledge-base/integration/cli.md)。

### 前置条件

-   已安装 [Node.js](https://nodejs.org/)（14 及以上版本）
-   已创建至少一个知识库，且包含已解析完成的文档
-   已获取 [API Key](raw/application-api-reference/rag-api/rag-api-authentication.md)

### 上手步骤

1.  **设置 API Key**
    
    将 API Key 存为环境变量，后续命令会自动读取：
    
    ```
    export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
    ```
    
2.  **获取知识库 ID**
    
    在控制台 [**数据接入 → 知识管理**](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list) 页面，点击目标知识库，复制页面上的知识库 ID（如 `r0t4r2c4ig`）。
    
3.  **运行第一次检索**
    
    无需安装，通过 `npx` 直接运行：
    
    ```
    npx bailian-cli knowledge retrieve \
      --api-key "$DASHSCOPE_API_KEY" \
      --index-id "你的知识库ID" \
      --query "你的问题"
    ```
    
    命令会输出检索到的文档切片及相关性分数。
    

### 启用重排序

添加 `--rerank` 参数可以对检索结果二次排序，提高结果相关性：

```
npx bailian-cli knowledge retrieve \
  --api-key "$DASHSCOPE_API_KEY" \
  --index-id "r0t4r2c4ig" \
  --query "阿里云百炼" \
  --rerank true \
  --dense-similarity-top-k 80 \
  --sparse-similarity-top-k 20 \
  --rerank-top-n 4 \
  --rerank-model "qwen3-rerank-hybrid" \
  --rerank-mode "similar"
```

### 参数参考

参数

必填

默认值

说明

`--api-key`

是

—

DashScope API Key

`--index-id`

是

—

知识库索引 ID

`--query`

是

—

查询文本

`--dense-similarity-top-k`

否

100

语义检索召回数量，范围 0–100

`--sparse-similarity-top-k`

否

100

关键词检索召回数量，范围 0–100

`--rerank`

否

—

启用重排序

`--rerank-top-n`

否

5

重排序后返回的结果数

`--rerank-model`

否

qwen3-rerank

排序模型，可选 `qwen3-rerank-hybrid`

`--rerank-mode`

否

qa

排序模式，可选 `similar`、`custom`

运行 `npx bailian-cli knowledge retrieve --help` 可查看全部参数说明。

**说明**CLI 也支持旧的 AK/SK 认证方式（`--access-key-id` + `--access-key-secret` + `--workspace-id`），但推荐使用 `--api-key`。当两种方式同时传入时，`--api-key` 优先。

## Agent Skill

在 Qoder / Claude Code 等 AI 编码工具中，把知识库作为技能包接入。安装地址为 `https://skills.aliyun.com/skills/alibabacloud-bailian-rag-knowledgebase`，可在控制台 [**服务渠道 → Agent Skill**](https://bailian.console.aliyun.com/cn-beijing/rag/channel) 页面获取。

安装后 AI 编码工具自动识别并加载知识库检索能力，无需手动编写配置。

## 阿里云百炼 Agent

KnowledgeStudio 知识库可作为外部能力接入阿里云百炼智能体应用，支持两种绑定方式：

### 方式一：Agent 绑定（推荐）

适用于新版智能体应用（Agent 2.0）。知识库作为智能体的一项技能，由智能体自主规划何时调用，与 MCP 等其他工具统一调度。

1.  在阿里云百炼控制台创建应用 → 智能体应用 → Agent 2.0
2.  在「知识库」区域选择「外部知识库 → KnowledgeStudio」
3.  粘贴 API Key 与知识库 ID，发布后即可调用

### 方式二：Workflow 绑定

适用于阿里云百炼工作流应用。将复杂任务拆分为有序节点（大模型节点、意图分类、结束节点等），KnowledgeStudio 可作为「知识库检索节点」被工作流调用。

1.  在阿里云百炼控制台创建应用 → 工作流应用
2.  在画布拖入「知识库检索」节点，选择「KnowledgeStudio」作为检索源
3.  连接开始节点 / 大模型节点 / 结束节点，发布为应用

### 选型建议

方式

适用场景

Agent 绑定

任务不固定、需多步推理、需要智能体自主决策。例如企业智能问答、复杂研究任务

Workflow 绑定

流程固定、需严格控制执行顺序。例如报告生成、客服分流、诊断辅助

**重要**如果你的应用使用 Dify / Coze 等第三方平台构建，参考[第三方平台接入](raw/application-user-guide/knowledge-base/integration/third-party.md)获取详细的配置指南。
