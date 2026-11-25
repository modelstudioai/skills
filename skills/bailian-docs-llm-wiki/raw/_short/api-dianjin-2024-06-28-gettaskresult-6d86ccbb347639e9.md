# GetTaskResult - 获取结果

获取异步任务结果。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetTaskResult)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetTaskResult</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/api/task/result HTTP/1.1
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

<table><thead><tr><th><p>名称</p></th><th><p>类型</p></th><th><p>描述</p></th><th><p>示例值</p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><p>ResultCode</p></td><td></td></tr><tr><td><p>cost</p></td><td><p>long</p></td><td><p>耗时</p></td><td><p>null</p></td></tr><tr><td><p>data</p></td><td><p>object</p></td><td><p>异步任务的执行结果。</p><h2>pdf 翻译任务</h2><p>返回结果 file_url 是一个可下载的文件地址。</p><a id="code-block-2"></a><pre class="language-text"><code>{
  &quot;file_url&quot;: &quot;https://finllmworks.oss-cn-zhangjiakou.aliyuncs.com/render_pdf/5336180997111160501.pdf&quot;
}
</code></pre></td><td><p>{ &quot;file_url&quot;: &quot;<a href="https://finllmworks.oss-cn-zhangjiakou.aliyuncs.com/render_pdf/5336180997111160501.pdf"></a><a href="https://finllmworks.oss-cn-zhangjiakou.aliyuncs.com/render_pdf/5336180997111160501.pdf">https://finllmworks.oss-cn-zhangjiakou.aliyuncs.com/render_pdf/5336180997111160501.pdf</a>&quot; }</p></td></tr><tr><td><p>dataType</p></td><td><p>string</p></td><td><p>数据类型</p></td><td><p>null</p></td></tr><tr><td><p>errCode</p></td><td><p>string</p></td><td><p>错误码</p></td><td><p>0</p></td></tr><tr><td><p>message</p></td><td><p>string</p></td><td><p>错误信息</p></td><td><p>ok</p></td></tr><tr><td><p>requestId</p></td><td><p>string</p></td><td><p>请求 id</p></td><td><p>9D5D6BB5-BEAE-53C8-A70A-7275CC1F856C</p></td></tr><tr><td><p>success</p></td><td><p>boolean</p></td><td><p>是否成功</p></td><td><p>true</p></td></tr><tr><td><p>time</p></td><td><p>string</p></td><td><p>时间戳</p></td><td><p>2024-04-24 11:54:34</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```text
{
  "cost": 0,
  "data": {
    "file_url": "https://finllmworks.oss-cn-zhangjiakou.aliyuncs.com/render_pdf/5336180997111160501.pdf"
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "9D5D6BB5-BEAE-53C8-A70A-7275CC1F856C",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
