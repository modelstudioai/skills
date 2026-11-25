# RunStepByStepWriting

使用大纲+摘编的分步骤的模式进行写作。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](iframe-embedding-scheme-6f73b86f9f7bdf41.md)

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| aimiaobi:RunStepByStepWriting | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/miaobi/runStepByStepWriting HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：获取<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">业务空间 ID（Workspace ID）</a></p></div></td><td><p>xxxx</p></td></tr><tr><td>Prompt</td><td><p>string</p></td><td><p>是</p></td><td><div><p>提示词</p></div></td><td><p>提示词</p></td></tr><tr><td>TaskId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>任务 ID，多轮对话可复用同一轮任务 ID</p><div><p>TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</p></div></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>SessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>单轮对话的 ID</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>OriginSessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>重新生成时原始对话的 ID</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>WritingConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作配置</p></div></td><td></td></tr><tr><td>Domain</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作领域</p><ul><li><p>media（默认）：传媒写作</p></li><li><p>government：公文写作</p></li></ul></div></td><td><p>media</p></td></tr><tr><td>Keywords</td><td><p>array</p></td><td><p>否</p></td><td><div><p>关键词(影响文章检索)</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>关键词（string）</p></div></td><td><p>关键词</p></td></tr><tr><td>PromptTag</td><td><p>object</p></td><td><p>否</p></td><td><div><p>提示词小助手</p></div></td><td></td></tr><tr><td>NecessaryTips</td><td><p>string</p></td><td><p>否</p></td><td><div><p>必要提示</p></div></td><td><p>必要提示</p></td></tr><tr><td>Position</td><td><p>string</p></td><td><p>否</p></td><td><div><p>立场</p></div></td><td><p>立场</p></td></tr><tr><td>ReverseWords</td><td><p>string</p></td><td><p>否</p></td><td><div><p>反向词</p></div></td><td><p>反向词</p></td></tr><tr><td>Theme</td><td><p>string</p></td><td><p>否</p></td><td><div><p>主题</p></div></td><td><p>主题</p></td></tr><tr><td>Scene</td><td><p>string</p></td><td><p>否</p></td><td><div><p>分步骤写作场景</p><ul><li><p>传媒写作支持的写作场景：新闻写作（默认）、新闻评论、通用文体</p></li><li><p>公文写作支持的写作场景：通知（默认）、通告、通报、请示、决定、函、通用文体</p></li></ul></div></td><td><p>新闻写作</p></td></tr><tr><td>Step</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作步骤</p><ul><li><p>生成大纲：OutlineGenerate</p></li><li><p>生成摘编：MiniDocSummary</p></li><li><p>Writing（默认）：生成文章</p></li></ul></div></td><td><p>Writing</p></td></tr><tr><td>Tags</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>写作时的文体、篇幅、输出语言等控制参数</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>标签对象</p></div></td><td></td></tr><tr><td>Keyword</td><td><p>string</p></td><td><p>否</p></td><td><div><p>选项的值</p></div></td><td><p>10</p></td></tr><tr><td>Tag</td><td><p>string</p></td><td><p>否</p></td><td><div><p>选项的 Tag。例如 gcNumberSizeTag=10</p></div></td><td><p>gcNumberSizeTag</p></td></tr><tr><td>UseSearch</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否自动补充素材</p></div></td><td><p>true</p></td></tr><tr><td>SummaryReturnType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>摘编结果的返回类型：<br></p><ul><li><p>Structure: 表示在 payload.output.text 中返回 json 字符串。示例格式：<code>{&quot;event&quot;:&quot;{outline}&quot;,&quot;message&quot;:&quot;{message}&quot;}</code></p></li><li><p>Content: 仅在 payload.output.text 中返回纯文本的摘编内容。示例格式： <code>大纲：{outline}\n\n{message}\n\n\n 大纲：{outline}\n\n{message}</code></p></li><li><p>Event: 仅在每次大纲写完时，在 payload.output.text 中 返回大纲内容本身。一般会返回六条大纲</p></li></ul></div></td><td><p>Structure</p></td></tr><tr><td>ReferenceData</td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td>Articles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td>Author</td><td><p>string</p></td><td><p>否</p></td><td><div><p>作者</p></div></td><td><p>作者</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内容</p></div></td><td><p>文章内容</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>文档-自定义的唯一ID</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>8a20e007a6174522af4d6a2657d5526f</p></td></tr><tr><td>MediaUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>原始素材地址</p></div></td><td><p><a href="http://www.example.com">http://www.example.com</a></p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发布时间</p></div></td><td><p>2024-09-10 14:17:54</p></td></tr><tr><td>Source</td><td><p>string</p></td><td><p>否</p></td><td><div><p>来源</p></div></td><td><p>央视网</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章摘要</p></div></td><td><p>文章摘要</p></td></tr><tr><td>Tag</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td><p>文章标签</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标题</p></div></td><td><p>文章标题</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章 URL</p></div></td><td><p><a href="https://www.example.com/aaa.docx">https://www.example.com/aaa.docx</a></p></td></tr><tr><td>MiniDoc</td><td><p>array</p></td><td><p>否</p></td><td><div><p>排序 Rank 后的文章片段（用于后续模型生成）</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章片段</p></div></td><td><p>文章片段</p></td></tr><tr><td>Outlines</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>大纲（可以指定数据源生成大纲）</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>大纲</p></div></td><td></td></tr><tr><td>Articles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>指定大纲数据源</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>文章对象</p></div></td><td></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章内容</p></div></td><td><p>文章内容</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章标题</p></div></td><td><p>文章标题</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章链接</p></div></td><td><p>文章链接</p></td></tr><tr><td>Outline</td><td><p>string</p></td><td><p>否</p></td><td><div><p>大纲</p></div></td><td><p>大纲</p></td></tr><tr><td>Summarization</td><td><p>array</p></td><td><p>否</p></td><td><div><p>大模型摘编总结结果</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>摘编结果（模型上下文）</p></div></td><td><p>摘编结果（模型上下文）</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | BaseLlmResponse |  |
| Header | object | 响应头 |  |
| ErrorCode | string | 错误码 | 错误码 |
| ErrorMessage | string | 错误信息 | 错误信息 |
| Event | string | SSE 事件。task-started:开始，task-finished:结束，task-failed:失败 | task-started |
| OriginSessionId | string | 父会话 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| SessionId | string | 会话 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TaskId | string | 任务 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TraceId | string | 全链路 ID | 全链路ID |
| Payload | object | 响应体 |  |
| Output | object | 输出 |  |
| Articles | array<object> | 参照文章 |  |
|  | object | 参照文章 |  |
| Author | string | 作者 | 作者 |
| Content | string | 内容 | 文章内容 |
| DocId | string | 文档-自定义的唯一 ID | 文档-自定义的唯一ID |
| DocUuid | string | 内部文档唯一标识 | f1da53894e784759946d22e2cb2b522a |
| MediaUrl | string | 原始素材地址 | [http://www.example.com](http://www.example.com) |
| PubTime | string | 发布时间 | 2024-09-10 14:17:53 |
| Source | string | 来源 | 央视网 |
| Summary | string | 文章摘要 | 文章摘要 |
| Tag | string | 标签 | 文章标签 |
| Title | string | 标题 | 文章标题 |
| Url | string | 文章 URL | [https://www.example.com/aaa.docx](https://www.example.com/aaa.docx) |
| ExtraOutput | object | 额外输出字段 |  |
| summarization | array | 摘编列表（分步骤生成摘编时，会返回该字段） |  |
|  | string | 摘编字段 | 摘编 |
| MiniDoc | array | 文章精排之后的片段列表 | 文章精排之后的片段 |
|  | string | 文章精排之后的片段 \* | 文章精排之后的片段 |
| SearchQuery | string | query 改写结果 | 大模型改变世界 |
| Text | string | 文本生成结果 | 文本生成结果 |
| Usage | object | Token 用量信息 |  |
| InputTokens | integer | 输入 Token 数 | 65 |
| OutputTokens | integer | 输出 Token 数 | 80 |
| TotalTokens | integer | 总 Token 数 | 32 |
| RequestId | string | 唯一请求 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Articles": [
        {
          "Author": "作者",
          "Content": "文章内容",
          "DocId": "文档-自定义的唯一ID",
          "DocUuid": "f1da53894e784759946d22e2cb2b522a",
          "MediaUrl": "http://www.example.com",
          "PubTime": "2024-09-10 14:17:53",
          "Source": "央视网",
          "Summary": "文章摘要",
          "Tag": "文章标签",
          "Title": "文章标题",
          "Url": "https://www.example.com/aaa.docx"
        }
      ],
      "ExtraOutput": {
        "summarization": [
          "摘编"
        ]
      },
      "MiniDoc": [
        "文章精排之后的片段"
      ],
      "SearchQuery": "大模型改变世界",
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 65,
      "OutputTokens": 80,
      "TotalTokens": 32
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunStepByStepWriting#workbench-doc-change-demo)。
