# RunWriting

直接写作

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

该接口已过时，请参考： [RunWritingV2](api-aimiaobi-2023-08-01-runwritingv2-c908f14d478d0459.md)

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
| aimiaobi:RunWriting | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/aimiaobi/runWriting HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：获取<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">业务空间 ID（Workspace ID）</a></p></div></td><td><p>xxxx</p></td></tr><tr><td>Prompt</td><td><p>string</p></td><td><p>是</p></td><td><div><p>提示词</p></div></td><td><p>提示词</p></td></tr><tr><td>TaskId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>任务 ID，多轮对话可复用同一轮任务 ID</p><div><p>TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。</p></div></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>SessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>单轮对话的 ID</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>OriginSessionId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>重新生成时原始对话的 ID</p></div></td><td><p>3f7045e099474ba28ceca1b4eb6d6e21</p></td></tr><tr><td>WritingConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作配置</p></div></td><td></td></tr><tr><td>Domain</td><td><p>string</p></td><td><p>否</p></td><td><div><p>写作领域</p><ul><li><p>media:传媒</p></li><li><p>government:政务</p></li><li><p>market:营销</p></li></ul></div></td><td><p>media</p></td></tr><tr><td>PromptTag</td><td><p>object</p></td><td><p>否</p></td><td><div><p>提示词小助手</p></div></td><td></td></tr><tr><td>NecessaryTips</td><td><p>string</p></td><td><p>否</p></td><td><div><p>必要提示</p></div></td><td><p>必要提示</p></td></tr><tr><td>Position</td><td><p>string</p></td><td><p>否</p></td><td><div><p>立场</p></div></td><td><p>立场</p></td></tr><tr><td>ReverseWords</td><td><p>string</p></td><td><p>否</p></td><td><div><p>反向词</p></div></td><td><p>反向词</p></td></tr><tr><td>Theme</td><td><p>string</p></td><td><p>否</p></td><td><div><p>主题</p></div></td><td><p>主题</p></td></tr><tr><td>Tags</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>写作时的文体、篇幅、输出语言等控制参数</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作时的文体、篇幅、输出语言等控制参数</p></div></td><td></td></tr><tr><td>Keyword</td><td><p>string</p></td><td><p>否</p></td><td><div><p>选项的值</p></div></td><td><p>10</p></td></tr><tr><td>Tag</td><td><p>string</p></td><td><p>否</p></td><td><div><p>选项的 Tag。例如 gcNumberSizeTag=10</p></div></td><td><p>gcNumberSizeTag</p></td></tr><tr><td>UseSearch</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否自动补充素材</p></div></td><td><p>true</p></td></tr><tr><td>ReferenceData</td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td>Articles</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>写作时的参考文章数据</p></div></td><td></td></tr><tr><td>Author</td><td><p>string</p></td><td><p>否</p></td><td><div><p>作者</p></div></td><td><p>作者</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内容</p></div></td><td><p>文章内容</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档-自定义的唯一 ID</p></div></td><td><p>文档-自定义的唯一ID</p></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内部文档唯一标识</p></div></td><td><p>2124ca4d48a542d788aa86151e1a8c8b</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发布时间</p></div></td><td><p>2024-08-28 11:38:28</p></td></tr><tr><td>Source</td><td><p>string</p></td><td><p>否</p></td><td><div><p>来源</p></div></td><td><p>央视网</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章摘要</p></div></td><td><p>文章摘要</p></td></tr><tr><td>Tag</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td><p>文章标签</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标题</p></div></td><td><p>文章标题</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章 URL</p></div></td><td><p><a href="https://www.example.com/aaa.docx">https://www.example.com/aaa.docx</a></p></td></tr></tbody></table>

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
| StatusCode | integer | http 响应码 | 400 |
| TaskId | string | 任务 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TraceId | string | 全链路 ID | 全链路ID |
| Payload | object | 响应体 |  |
| Output | object | 输出 |  |
| Articles | array<object> | 参照文章 |  |
|  | object | 参照文章 |  |
| Author | string | 作者 | 作者 |
| Content | string | 内容 | 文章内容 |
| DocId | string | 文档-自定义的唯一 ID | 文档-自定义的唯一ID |
| DocUuid | string | 内部文档唯一标识 | 98229f6001cf4deeb1668191d4eccc75 |
| PubTime | string | 发布时间 | 2024-08-28 11:38:28 |
| Source | string | 来源 | 央视网 |
| Summary | string | 文章摘要 | 文章摘要 |
| Tag | string | 标签 | 文章标签 |
| Title | string | 标题 | 文章标题 |
| Url | string | 文章 URL | [https://www.example.com/aaa.docx](https://www.example.com/aaa.docx) |
| MiniDoc | array | 文章精排之后的片段列表 | 文章精排之后的片段 |
|  | string | 文章精排之后的片段 \* | 文章精排之后的片段 |
| SearchQuery | string | query 改写结果 | 大模型改变世界 |
| Text | string | 文本生成结果 | 文本生成结果 |
| Usage | object | token 消耗 |  |
| InputTokens | integer | 输入使用的 Token 数量 | 1 |
| OutputTokens | integer | 输出使用的 Token 数量 | 1 |
| TokenMap | object | token 消耗明细 |  |
|  | integer | token 消耗明细 | 44 |
| TotalTokens | integer | 本次调用使用的所有 Token 数总和 | 2 |
| RequestId | string | 请求 ID | 3f7045e099474ba28ceca1b4eb6d6e21 |
| End | boolean | 此次请求是否结束 | true |

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
    "StatusCode": 400,
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
          "DocUuid": "98229f6001cf4deeb1668191d4eccc75",
          "PubTime": "2024-08-28 11:38:28",
          "Source": "央视网",
          "Summary": "文章摘要",
          "Tag": "文章标签",
          "Title": "文章标题",
          "Url": "https://www.example.com/aaa.docx"
        }
      ],
      "MiniDoc": [
        "文章精排之后的片段"
      ],
      "SearchQuery": "大模型改变世界",
      "Text": "文本生成结果"
    },
    "Usage": {
      "InputTokens": 1,
      "OutputTokens": 1,
      "TokenMap": {
        "key": 44
      },
      "TotalTokens": 2
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunWriting#workbench-doc-change-demo)。
