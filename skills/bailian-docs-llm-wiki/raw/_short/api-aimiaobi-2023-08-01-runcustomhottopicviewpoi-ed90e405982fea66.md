# RunCustomHotTopicViewPointAnalysis - 自定义选题视角分析

自定义选题视角分析。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunCustomHotTopicViewPointAnalysis)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:RunCustomHotTopicViewPointAnalysis</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /quanmiao/miaoce/runCustomHotTopicViewPointAnalysis HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | xxxx |
| AskUser | string | 否 | 模型反问 | 模型反问 |
| UserBack | string | 否 | 用户反馈 | 用户反馈 |
| SearchQuery | string | 否 | 改写后的 Query | 改写后的Query |
| Prompt | string | 是 | 自定义选题视角的 Prompt | 自定义选题视角的Prompt |
| SkipAskUser | boolean | 否 | 是否跳过反问 | true |
| TopicId | string | 否 | 热点主题 ID | 热点主题ID |
| Topic | string | 否 | 热点主题 | 热点主题 |
| TopicVersion | string | 否 | 热点主题版本 | 热点主题版本 |
| TopicSource | string | 否 | 热点主题来源 | 热点主题来源 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>CustomHoTTopicBaseLlmResponse</p></div></td><td></td></tr><tr><td>Header</td><td>object</td><td><div><p>响应头</p></div></td><td></td></tr><tr><td>ErrorCode</td><td>string</td><td><div><p>错误码</p></div></td><td>错误码</td></tr><tr><td>ErrorMessage</td><td>string</td><td><div><p>错误信息</p></div></td><td>错误信息</td></tr><tr><td>Event</td><td>string</td><td><div><p>SSE 事件。task-started:开始，task-finished:结束，task-failed:失败</p></div></td><td>task-started</td></tr><tr><td>OriginSessionId</td><td>string</td><td><div><p>父会话 ID</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr><tr><td>SessionId</td><td>string</td><td><div><p>会话 ID</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr><tr><td>TaskId</td><td>string</td><td><div><p>任务 ID</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr><tr><td>TraceId</td><td>string</td><td><div><p>全链路 ID</p></div></td><td>全链路ID</td></tr><tr><td>Payload</td><td>object</td><td><div><p>响应体</p></div></td><td></td></tr><tr><td>Output</td><td>object</td><td><div><p>输出</p></div></td><td></td></tr><tr><td>AskUser</td><td>array</td><td><div><p>反问列表</p></div></td><td></td></tr><tr><td>AskUser</td><td>string</td><td><div><p>模型反问</p></div></td><td>xxxxxxx</td></tr><tr><td>AsyncTaskId</td><td>string</td><td><div><p>异步任务 ID</p></div></td><td>异步任务ID</td></tr><tr><td>Attitude</td><td>string</td><td><div><p>模型生成的自定义选题视角的观点</p></div></td><td>模型生成的自定义选题视角的观点</td></tr><tr><td>CustomViewPointId</td><td>string</td><td><div><p>自定义视角 ID</p></div></td><td>xxxxxx</td></tr><tr><td>Text</td><td>string</td><td><div><p>文本生成结果</p></div></td><td>文本生成结果</td></tr><tr><td>TopicId</td><td>string</td><td><div><p>话题 ID</p></div></td><td>话题ID</td></tr><tr><td>Articles</td><td>array&lt;object&gt;</td><td><div><p>参考文章列表</p></div></td><td></td></tr><tr><td>Articles</td><td>object</td><td><div><p>参考文章对象</p></div></td><td></td></tr><tr><td>Author</td><td>string</td><td><div><p>作者</p></div></td><td>作者</td></tr><tr><td>Title</td><td>string</td><td><div><p>标题</p></div></td><td>文章标题</td></tr><tr><td>Content</td><td>string</td><td><div><p>内容</p></div></td><td>文章内容</td></tr><tr><td>PubTime</td><td>string</td><td><div><p>发布时间</p></div></td><td>2024-09-10 14:17:53</td></tr><tr><td>Source</td><td>string</td><td><div><p>来源</p></div></td><td>央视网</td></tr><tr><td>Url</td><td>string</td><td><div><p>URL 标题</p></div></td><td><a href="https://www.example.com/aaa.docx">https://www.example.com/aaa.docx</a></td></tr><tr><td>Summary</td><td>string</td><td><div><p>摘要</p></div></td><td>文章摘要</td></tr><tr><td>Usage</td><td>object</td><td><div><p>镜像是否已经运行在 ECS 实例中。取值范围：</p><ul><li>instance：镜像处于运行状态，有 ECS 实例使用。</li><li>none：镜像处于闲置状态，暂无 ECS 实例使用。</li></ul></div></td><td></td></tr><tr><td>InputTokens</td><td>long</td><td><div><p>输入 Token 数量</p></div></td><td>51</td></tr><tr><td>OutputTokens</td><td>long</td><td><div><p>输出 Token 数量</p></div></td><td>79</td></tr><tr><td>TotalTokens</td><td>long</td><td><div><p>总 Token 数量</p></div></td><td>130</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求 ID</p></div></td><td>3f7045e099474ba28ceca1b4eb6d6e21</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
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
      "AskUser": [
        "xxxxxxx"
      ],
      "AsyncTaskId": "异步任务ID",
      "Attitude": "模型生成的自定义选题视角的观点",
      "CustomViewPointId": "xxxxxx",
      "Text": "文本生成结果",
      "TopicId": "话题ID",
      "Articles": [
        {
          "Author": "作者\n\n",
          "Title": "文章标题",
          "Content": "文章内容",
          "PubTime": "2024-09-10 14:17:53",
          "Source": "央视网",
          "Url": "https://www.example.com/aaa.docx",
          "Summary": "文章摘要"
        }
      ]
    },
    "Usage": {
      "InputTokens": 51,
      "OutputTokens": 79,
      "TotalTokens": 130
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
