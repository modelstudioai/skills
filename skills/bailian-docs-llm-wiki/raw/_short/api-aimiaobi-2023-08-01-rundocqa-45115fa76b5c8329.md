# RunDocQa - 文档问答（文章问答/多模态文件问答）

文章问答：针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDocQa)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:RunDocQa</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /miaodu/stream/runDocQA HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p>阿里云百炼业务空间 ID。获取方式请参见<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md">如何使用业务空间</a>。</p></div></td><td>llm-dswd4003ny4gh9rw</td></tr><tr><td>SearchSource</td><td>string</td><td>是</td><td><div><p>搜索源</p></div><div><div>枚举值：</div><ul><li>fromIndexLib：基于整个文档库进行问答。</li><li>fromWeb：基于互联网搜索进行问答。</li><li>fromRefContent：基于ReferenceContent字段进行问答。</li><li>fromDoc：基于给出的文档Id进行文档问答。</li></ul></div></td><td>fromWeb</td></tr><tr><td>DocIds</td><td>array</td><td>否</td><td><div><p>多个文档 Id 数组</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>文档 Id</p></div></td><td>10022</td></tr><tr><td>Query</td><td>string</td><td>是</td><td><div><p>问题</p></div></td><td>苹果16手机什么时候发布</td></tr><tr><td>ReferenceContent</td><td>string</td><td>否</td><td><div><p>提问者主动提供的关联内容</p></div></td><td>关联内容</td></tr><tr><td>ConversationContexts</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>历史上下文内容数组</p></div></td><td></td></tr><tr><td></td><td>object</td><td>否</td><td><div><p>历史上下文</p></div></td><td></td></tr><tr><td>Content</td><td>string</td><td>否</td><td><div><p>问答内容</p></div></td><td>问答内容</td></tr><tr><td>Role</td><td>string</td><td>否</td><td><div><p>角色</p></div></td><td>user</td></tr><tr><td>SessionId</td><td>string</td><td>是</td><td><div><p>对话 ID</p></div></td><td>f486c4e2-b773-4d65-88f8-2ba540610456</td></tr><tr><td>CategoryIds</td><td>array</td><td>否</td><td><div><p>过滤目录 Id 数组，只在 SearchSource 为 fromIndexLib 时有效</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>类目 ID</p></div></td><td>default</td></tr><tr><td>ModelName</td><td>string</td><td>否</td><td><div><p>用户自定义模型名称</p></div></td><td>quanmiao-max、quanmiao-plus</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| Header | object | 响应头 |  |
| ErrorCode | string | 错误码 | success |
| ErrorMessage | string | 错误信息 | success |
| Event | string | 事件 | task-started |
| EventInfo | string | 事件描述 | 模型生成事件 |
| SessionId | string | 会话 ID | f5517ee8-dbec-4dc8-bd0a-af084b5e3db1 |
| TaskId | string | 任务 id | 3f7045e099474ba28ceca1b4eb6d6e21 |
| TraceId | string | 全链路 ID | 46e5c2b5-0877-4f09-bd91-ab0cf314e48b |
| Payload | object | 响应体 |  |
| Output | object | 输出 |  |
| Content | string | 回答内容 | 回答内容 |
| InterveneContent | string | 干预后的回答内容 | 干预后的回答内容 |
| IsReject | boolean | 是否拒识 | false |
| MediaUrlList | array<object> | 多模态资源信息列表 |  |
| mediaUrlList | object | 多模态资源对象 |  |
| ClipInfos | array<object> | 相关视频时间信息数组 |  |
| clipInfos | object | 相关视频时间信息 |  |
| From | double | 视频片段开始时间 | 0 |
| To | double | 视频片段结束时间 | 30 |
| FileUrl | string | 文件 url | [https://gw.alicdn.com/imgextra/i3/2775676850/O1CN01kdeffE20TM0E7wvpq\_!!2775676850.jpg\_q60.jpg](https://gw.alicdn.com/imgextra/i3/2775676850/O1CN01kdeffE20TM0E7wvpq_!!2775676850.jpg_q60.jpg) |
| MediaType | string | 媒资媒体类型 | video |
| Recommends | array<object> | 推荐内容数组 |  |
| recommends | object | 推荐内容 |  |
| Title | string | 推荐内容标题 | 标题内容 |
| Url | string | 推荐内容 url | 推荐内容url |
| References | array<object> | 回答内容来源数组 |  |
| references | object | 回答内容来源 |  |
| PubTime | string | 发布时间 | 2024-10-08 18:00 |
| Source | string | 来源 | 新浪新闻 |
| SourceDocId | string | 来源 docId | 123456 |
| Title | string | 关联内容标题 | 标题内容 |
| Url | string | 文章 URL | http://xxxxx |
| Usage | object | token 用量 |  |
| InputTokens | long | 输入 Token 数量 | 100 |
| OutputTokens | long | 输出使用的 Token 数量 | 100 |
| TotalTokens | long | 总 token 数量 | 200 |
| RequestId | string | 请求 Id | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "Header": {
    "ErrorCode": "success",
    "ErrorMessage": "success",
    "Event": "task-started",
    "EventInfo": "模型生成事件",
    "SessionId": "f5517ee8-dbec-4dc8-bd0a-af084b5e3db1",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "46e5c2b5-0877-4f09-bd91-ab0cf314e48b"
  },
  "Payload": {
    "Output": {
      "Content": "回答内容",
      "InterveneContent": "干预后的回答内容",
      "IsReject": false,
      "MediaUrlList": [
        {
          "ClipInfos": [
            {
              "From": 0,
              "To": 30
            }
          ],
          "FileUrl": "https://gw.alicdn.com/imgextra/i3/2775676850/O1CN01kdeffE20TM0E7wvpq_!!2775676850.jpg_q60.jpg",
          "MediaType": "video"
        }
      ],
      "Recommends": [
        {
          "Title": "标题内容",
          "Url": "推荐内容url"
        }
      ],
      "References": [
        {
          "PubTime": "2024-10-08 18:00",
          "Source": "新浪新闻",
          "SourceDocId": 123456,
          "Title": "标题内容",
          "Url": "http://xxxxx"
        }
      ]
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
