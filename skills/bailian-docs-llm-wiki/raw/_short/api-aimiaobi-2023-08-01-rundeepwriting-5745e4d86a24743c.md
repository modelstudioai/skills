# RunDeepWriting - 查询深度写作事件

查询深度写作事件。 系统以SSE事件的形式下发任务执行过程中的详细信息。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunDeepWriting)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:RunDeepWriting</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /pop/deepWrite/runDeepWriting HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | llm-ir8zkqry2fncaxwq |
| TaskId | string | 否 | 任务 ID | 95c2fbe6-5a20-4fc2-8a93-376ed05fbe13 |
| Cursor | integer | 否 | 游标。流式事件的序号 | 10 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Header</td><td>object</td><td><div><p>响应头</p></div></td><td></td></tr><tr><td>ErrorCode</td><td>string</td><td><div><p>错误码</p></div></td><td>403</td></tr><tr><td>ErrorMessage</td><td>string</td><td><div><p>错误信息。</p></div></td><td>错误消息</td></tr><tr><td>Event</td><td>string</td><td><div><p>SSE 事件。</p></div><div><div>枚举值：</div><ul><li>response.sub_task.created：子任务已创建。</li><li>response.output_item.done：中间结果输出完成。</li><li>response.completed：任务完成。</li><li>response.created：任务已创建。</li></ul></div></td><td>response.output_item.done</td></tr><tr><td>SessionId</td><td>string</td><td><div><p>会话 ID</p></div></td><td>c2e2e991-f96a-4fcc-9ff7-d0df46c6d232</td></tr><tr><td>StatusCode</td><td>integer</td><td><div><p>http 响应码</p></div></td><td>200</td></tr><tr><td>TaskId</td><td>string</td><td><div><p>任务 ID</p></div></td><td>b84d31a5-44b2-4a35-9c6d-878d459c93d0</td></tr><tr><td>TraceId</td><td>string</td><td><div><p>全链路 ID</p></div></td><td>FAB10D42-F081-557B-8DCB-D6FB7AAF100B</td></tr><tr><td>Payload</td><td>object</td><td><div><p>响应体</p></div></td><td></td></tr><tr><td>Output</td><td>object</td><td><div><p>输出</p></div></td><td></td></tr><tr><td>Type</td><td>string</td><td><div><p>类型</p></div></td><td>同上级Event</td></tr><tr><td>SequenceNumber</td><td>string</td><td><div><p>流式事件的序号</p></div></td><td>1</td></tr><tr><td>OutputIndex</td><td>integer</td><td><div><p>本次事件新加的输出 item 的序号</p></div></td><td>1</td></tr><tr><td>Response</td><td>object</td><td><div><p>响应体</p></div></td><td></td></tr><tr><td>Id</td><td>string</td><td><div><p>本次任务的唯一标识</p></div></td><td>b2dc224b38694e0b668020159a7c5732</td></tr><tr><td>Status</td><td>string</td><td><div><p>本次任务的执行状态</p></div><div><div>枚举值：</div><ul><li>in_progress：处理中。</li><li>completed：已完成。</li></ul></div></td><td>in_progress</td></tr><tr><td>Item</td><td>object</td><td><div><p>本次事件新加的输出 item</p></div></td><td></td></tr><tr><td>Id</td><td>string</td><td><div><p>item 的唯一标识</p></div></td><td>88f6ed9e85c4f9377378da23e6a370d1</td></tr><tr><td>Status</td><td>string</td><td><div><p>item 的状态</p></div><div><div>枚举值：</div><ul><li>in_progress：in_progress。</li><li>completed：completed。</li></ul></div></td><td>completed</td></tr><tr><td>Type</td><td>string</td><td><div><p>item 的类型</p></div><div><div>枚举值：</div><ul><li>function_call：function_call。</li><li>message：message。</li></ul></div></td><td>function_call</td></tr><tr><td>Arguments</td><td>string</td><td><div><p>参数</p></div></td><td>item类型为function_call时，此字段有值，为调用函数的入参</td></tr><tr><td>Name</td><td>string</td><td><div><p>参数名称</p></div></td><td>item类型为function_call时，此字段有值，为调用的函数名字</td></tr><tr><td>Result</td><td>string</td><td><div><p>item 的结果</p></div></td><td>item类型为function_call时，此字段有值，为调用的函数的输出</td></tr><tr><td>Agent</td><td>string</td><td><div><p>输出此 item 的 agent 名字</p></div></td><td>ProjectManager</td></tr><tr><td>Content</td><td>array&lt;object&gt;</td><td><div><p>item 类型为 message 时，此字段有值，是输出 content 的列表</p></div></td><td></td></tr><tr><td>content</td><td>object</td><td><div><p>文本内容</p></div></td><td></td></tr><tr><td>Type</td><td>string</td><td><div><p>item 类型为 message 时，此字段的值是 output_text</p></div></td><td>output_text</td></tr><tr><td>Text</td><td>string</td><td><div><p>item 类型为 message 时, 输出的文本内容</p></div></td><td>&lt;TASK_DONE&gt;</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>唯一请求 ID</p></div></td><td>31AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3</td></tr><tr><td>HttpStatusCode</td><td>string</td><td><div><p>Http 状态码</p></div></td><td>200</td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>successful</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误信息。</p></div></td><td>success</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>此次请求是否成功</p></div></td><td>true</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "Header": {
    "ErrorCode": 403,
    "ErrorMessage": "错误消息",
    "Event": "response.output_item.done",
    "SessionId": "c2e2e991-f96a-4fcc-9ff7-d0df46c6d232",
    "StatusCode": 200,
    "TaskId": "b84d31a5-44b2-4a35-9c6d-878d459c93d0",
    "TraceId": "FAB10D42-F081-557B-8DCB-D6FB7AAF100B"
  },
  "Payload": {
    "Output": {
      "Type": "同上级Event",
      "SequenceNumber": 1,
      "OutputIndex": 1,
      "Response": {
        "Id": "b2dc224b38694e0b668020159a7c5732",
        "Status": "in_progress"
      },
      "Item": {
        "Id": "88f6ed9e85c4f9377378da23e6a370d1",
        "Status": "completed",
        "Type": "function_call",
        "Arguments": "item类型为function_call时，此字段有值，为调用函数的入参",
        "Name": "item类型为function_call时，此字段有值，为调用的函数名字",
        "Result": "item类型为function_call时，此字段有值，为调用的函数的输出",
        "Agent": "ProjectManager",
        "Content": [
          {
            "Type": "output_text",
            "Text": "<TASK_DONE>"
          }
        ]
      }
    }
  },
  "RequestId": "31AC01F1-88FB-5C4D-B6F5-E8BB136CD5A3",
  "HttpStatusCode": 200,
  "Code": "successful",
  "Message": "success",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
