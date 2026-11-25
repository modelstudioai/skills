# GetTopicById - 获取热点对象

根据ID获取热点事件信息。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetTopicById)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:GetTopicById</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| AgentKey | string | 是 | 业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey) | xxxxx\_p\_efm |
| Id | string | 是 | 数据 ID | 数据ID |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>PlainResult</p></div></td><td></td></tr><tr><td>Code</td><td>string</td><td><div><p>状态码</p></div></td><td>NoData</td></tr><tr><td>Data</td><td>object</td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>AsyncTaskId</td><td>string</td><td><div><p>异步任务 ID（自定义主题场景下使用）</p></div></td><td>异步任务ID（自定义主题场景下使用）</td></tr><tr><td>CreateUser</td><td>string</td><td><div><p>创建用户 ID（自定义主题场景下使用）</p></div></td><td>创建用户ID（自定义主题场景下使用）</td></tr><tr><td>HotValue</td><td>long</td><td><div><p>热度值</p></div></td><td>43</td></tr><tr><td>Id</td><td>string</td><td><div><p>热榜 ID</p></div></td><td>热榜ID</td></tr><tr><td>Status</td><td>string</td><td><div><p>异步任务状态（自定义事件场景下使用） (PENDING: 待执行, RUNNING: 执行中, SUCCESSED: 成功, SUSPENDED: 暂停, FAILED: 失败, CANCELED: 取消)</p></div></td><td>PENDING</td></tr><tr><td>StructureSummary</td><td>array&lt;object&gt;</td><td><div><p>结构化主题摘要列表</p></div></td><td></td></tr><tr><td>StructureSummary</td><td>object</td><td><div><p>结构化主题摘要对象</p></div></td><td></td></tr><tr><td>DocList</td><td>array&lt;object&gt;</td><td><div><p>生成该标题摘要引用的文章</p></div></td><td></td></tr><tr><td>DocList</td><td>object</td><td><div><p>文章对象</p></div></td><td></td></tr><tr><td>Source</td><td>string</td><td><div><p>文章源</p></div></td><td>头条</td></tr><tr><td>Title</td><td>string</td><td><div><p>文章标题</p></div></td><td>文章标题</td></tr><tr><td>Url</td><td>string</td><td><div><p>文章 URL</p></div></td><td><a href="http://www.example.com">http://www.example.com</a></td></tr><tr><td>Summary</td><td>string</td><td><div><p>摘要</p></div></td><td>摘要</td></tr><tr><td>Title</td><td>string</td><td><div><p>标题</p></div></td><td>标题</td></tr><tr><td>Summary</td><td>string</td><td><div><p>热榜摘要</p></div></td><td>热榜摘要</td></tr><tr><td>TaskErrorMessage</td><td>string</td><td><div><p>异步任务失败错误信息</p></div></td><td>异步任务失败错误信息</td></tr><tr><td>TaskStatus</td><td>integer</td><td><div><p>异步任务状态。0-待执行，1-执行中，2-执行成功，3-暂停（暂不使用），4-执行失败，6-任务取消（自定义事件场景下使用）。</p></div></td><td>14</td></tr><tr><td>Topic</td><td>string</td><td><div><p>主题唯一名称</p></div></td><td>主题唯一名称</td></tr><tr><td>TopicSource</td><td>string</td><td><div><p>热榜源，目前支持的热榜源：</p><ul><li><p>Toutiao：头条</p></li><li><p>Quark：夸克</p></li><li><p>Baidu：百度</p></li><li><p>Sina：新浪</p></li><li><p>Custom：自定义</p></li><li><p>Aggregation：热点话题榜</p></li></ul></div></td><td>Toutiao</td></tr><tr><td>Version</td><td>string</td><td><div><p>数据版本</p></div></td><td>数据版本</td></tr><tr><td>HttpStatusCode</td><td>integer</td><td><div><p>http 状态码</p></div></td><td>200</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误说明</p></div></td><td>success</td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求唯一标识</p></div></td><td>1813ceee-7fe5-41b4-87e5-982a4d18cca5</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td>true</td></tr></tbody></table>

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
    "AsyncTaskId": "异步任务ID（自定义主题场景下使用）",
    "CreateUser": "创建用户ID（自定义主题场景下使用）",
    "HotValue": 43,
    "Id": "热榜ID",
    "Status": "PENDING",
    "StructureSummary": [
      {
        "DocList": [
          {
            "Source": "头条",
            "Title": "文章标题",
            "Url": "http://www.example.com"
          }
        ],
        "Summary": "摘要",
        "Title": "标题"
      }
    ],
    "Summary": "热榜摘要",
    "TaskErrorMessage": "异步任务失败错误信息",
    "TaskStatus": 14,
    "Topic": "主题唯一名称",
    "TopicSource": "Toutiao",
    "Version": "数据版本"
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
