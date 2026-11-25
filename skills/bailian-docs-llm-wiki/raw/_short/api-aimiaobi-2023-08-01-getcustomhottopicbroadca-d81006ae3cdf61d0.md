# GetCustomHotTopicBroadcastJob - 获取自定义播报单任务结果

获取自定义播报单任务结果。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetCustomHotTopicBroadcastJob)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:GetCustomHotTopicBroadcastJob</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md) | xxxx |
| TaskId | string | 是 | 任务唯一 ID<br><br>**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。 | 2e27abb32cb64f80a0c6e829b6c87a09 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>PlainResult</p></div></td><td></td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>NoData</td></tr><tr><td>Data</td><td>object</td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>ErrorMessage</td><td>string</td><td><div><p>错误信息</p></div></td><td>错误信息</td></tr><tr><td>HotTopicVersion</td><td>string</td><td><div><p>热点话题版本号标识</p></div></td><td>热点话题版本号标识</td></tr><tr><td>Status</td><td>string</td><td><div><p>任务状态</p><ul><li>PENDING：待执行</li><li>RUNNING：执行中</li><li>SUCCESSED：成功</li><li>SUSPENDED：暂停</li><li>FAILED：失败</li><li>CANCELED：取消</li></ul></div></td><td>RUNNING</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 状态码</p></div></td><td>200</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误说明</p></div></td><td>success</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>1813ceee-7fe5-41b4-87e5-982a4d18cca5</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td>true</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "NoData",
  "Data": {
    "ErrorMessage": "错误信息",
    "HotTopicVersion": "热点话题版本号标识",
    "Status": "RUNNING"
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
