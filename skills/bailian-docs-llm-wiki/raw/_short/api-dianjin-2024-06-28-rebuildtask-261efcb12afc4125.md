# RebuildTask - 重建任务

对已有任务进行重建，但在队列中或执行中的任务不可重建。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/RebuildTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:RebuildTask</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/task/rebuild HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 Id | llm-xxxxx |
| body | object | 否 | 请求体参数 |  |
| taskIds | array | 是 | 任务 ID 列表 |  |
| taskId | string | 否 | 任务 ID | 3894763764 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p>名称</p></th><th><p>类型</p></th><th><p>描述</p></th><th><p>示例值</p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><p>ResultCode&lt;List&lt;Map&lt;String, Object&gt;&gt;&gt;</p></td><td></td></tr><tr><td><p>success</p></td><td><p>boolean</p></td><td><p>是否成功</p></td><td><p>true</p></td></tr><tr><td><p>dataType</p></td><td><p>string</p></td><td><p>数据类型</p></td><td><p>null</p></td></tr><tr><td><p>time</p></td><td><p>string</p></td><td><p>时间戳</p></td><td><p>2024-04-24 11:54:34</p></td></tr><tr><td><p>errCode</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>0</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>ok</p></td></tr><tr><td><p>data</p></td><td><p>array&lt;object&gt;</p></td><td><p>响应数据</p></td><td></td></tr><tr><td><p>data</p></td><td><p>object</p></td><td><p>重建任务操作的响应结果。其中 taskId 表示任务 id，status 表示操作的状态（success 为成功，error 为失败），message 为详细信息。</p><a id="code-block-2"></a><pre class="language-text"><code>{
    &quot;message&quot;: &quot;任务正在执行中，不能重新构建&quot;,
    &quot;taskId&quot;: &quot;-253103935&quot;,
    &quot;status&quot;: &quot;error&quot;
}
</code></pre></td><td><p>{ &quot;message&quot;: &quot;任务正在执行中，不能重新构建&quot;, &quot;taskId&quot;: &quot;-253103935&quot;, &quot;status&quot;: &quot;error&quot; }</p></td></tr><tr><td><p>requestId</p></td><td><p>string</p></td><td><p>请求 id</p></td><td><p>EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258</p></td></tr><tr><td><p>cost</p></td><td><p>long</p></td><td><p>耗时</p></td><td><p>null</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```text
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": [
    {
      "message": "任务正在执行中，不能重新构建",
      "taskId": -253103935,
      "status": "error"
    }
  ],
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
  "cost": 0
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
