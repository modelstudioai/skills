# CancelDeepWriteTask - 取消深度写作任务

取消深度写作任务。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CancelDeepWriteTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:CancelDeepWriteTask</td><td>update</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 否 | [业务空间 ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | llm-xxxxx |
| TaskId | string | 否 | 任务 ID | xbabac91-fdad-44d6-95ce-\*\*\*\*\*\* |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td>string</td><td><div><p>Id of the request</p></div></td><td>xxxxx</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>此次请求是否成功</p></div></td><td>true</td></tr><tr><td>Code</td><td>string</td><td><div><p>错误码</p></div></td><td>DataNotExists</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误消息</p></div></td><td>错误消息</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 错误码</p></div></td><td>400</td></tr><tr><td>Data</td><td>object</td><td><div><p>任务响应对象</p></div></td><td></td></tr><tr><td>TaskId</td><td>string</td><td><div><p>任务 ID</p></div></td><td>xbabac91-fdad-44d6-95ce-******</td></tr><tr><td>Input</td><td>string</td><td><div><p>用户的问题</p></div></td><td>北京2025年新能源汽车发展趋势</td></tr><tr><td>Status</td><td>string</td><td><div><p>任务状态</p></div><div><div>枚举值：</div><ul><li>in_progress：运行中。</li><li>queued：排队中。</li><li>cancelled：已取消。</li><li>completed：已完成。</li><li>failed：失败。</li></ul></div></td><td>cancelled</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "TaskId": "xbabac91-fdad-44d6-95ce-******",
    "Input": "北京2025年新能源汽车发展趋势",
    "Status": "cancelled"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
