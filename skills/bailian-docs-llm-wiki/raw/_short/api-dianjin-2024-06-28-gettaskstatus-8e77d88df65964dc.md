# GetTaskStatus - 获取任务状态

获取任务状态。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetTaskStatus)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetTaskStatus</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/api/task/status HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 Id | llm-xxxx |
| taskId | string | 是 | 任务 Id | 17071319 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>ResultCode</p></div></td><td></td></tr><tr><td>cost</td><td>long</td><td><div><p>耗时</p></div></td><td>null</td></tr><tr><td>data</td><td>string</td><td><div><p>响应数据，任务状态。</p><ul><li>invalid：参数/依赖的资源状态不可用。</li><li>success：成功。</li><li>evict: 被取消。</li><li>error：失败。</li><li>running：运行中。</li><li>pending：排队中。</li></ul></div></td><td>running</td></tr><tr><td>dataType</td><td>string</td><td><div><p>数据类型</p></div></td><td>null</td></tr><tr><td>errCode</td><td>string</td><td><div><p>错误码</p></div></td><td>0</td></tr><tr><td>message</td><td>string</td><td><div><p>错误信息</p></div></td><td>ok</td></tr><tr><td>requestId</td><td>string</td><td><div><p>请求 id</p></div></td><td>30F6AD44-F078-540D-B5A5-1E519C8E9E6D</td></tr><tr><td>success</td><td>boolean</td><td><div><p>是否成功</p></div></td><td>true</td></tr><tr><td>time</td><td>string</td><td><div><p>时间戳</p></div></td><td>2024-04-24 11:54:34</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": "running",
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "30F6AD44-F078-540D-B5A5-1E519C8E9E6D",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
