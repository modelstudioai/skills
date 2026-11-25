# ListPlanningProposal - 获取选题策划列表

获取选题策划列表。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListPlanningProposal)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:ListPlanningProposal</td><td>list</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AgentKey</td><td>string</td><td>是</td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td>xxxxx_p_efm</td></tr><tr><td>ViewPointType</td><td>string</td><td>是</td><td><div><p>选题策划类型</p><ul><li><p>CustomViewPoints：自定义视角</p></li><li><p>HotViewPoints：热门视角</p></li><li><p>TimedViewPoints：时效性视角</p></li><li><p>WebReviewPoints：网友视角</p></li><li><p>FreshViewPoints：新颖视角</p></li></ul></div></td><td>CustomViewPoints</td></tr><tr><td>Titles</td><td>array</td><td>否</td><td><div><p>选题策划标题筛选，对应各个选题策划类型的视角名称</p></div></td><td></td></tr><tr><td>Title</td><td>string</td><td>否</td><td><div><p>视角筛选</p></div></td><td>标题 *</td></tr><tr><td>CustomViewPointId</td><td>string</td><td>否</td><td><div><p>自定义视角 ID（用于自定义视角选题策划场景）</p></div></td><td>e7b26a9e1211444db8f0a984361a5e0f</td></tr><tr><td>CustomViewPointIds</td><td>array</td><td>否</td><td><div><p>自定义视角 ID 列表（用于自定义视角选题策划场景）</p></div></td><td></td></tr><tr><td>CustomViewPointId</td><td>string</td><td>否</td><td><div><p>自定义视角 ID（用于自定义视角选题策划场景） *</p></div></td><td>3c67e87fc9044a8aae534f617195ab31</td></tr><tr><td>TopicSource</td><td>string</td><td>是</td><td><div><p>热榜源</p></div></td><td>热榜源</td></tr><tr><td>Topic</td><td>string</td><td>是</td><td><div><p>热榜主题</p></div></td><td>热榜主题</td></tr><tr><td>TopicVersion</td><td>string</td><td>否</td><td><div><p>热点事件数据版本</p></div></td><td>2024-09-10_08</td></tr><tr><td>NextToken</td><td>string</td><td>否</td><td><div><p>下一页的 Token</p></div></td><td>下一页的Token</td></tr><tr><td>MaxResults</td><td>integer</td><td>否</td><td><div><p>最大返回结果数</p></div></td><td>73</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PageResult2 |  |
| Code | string | 状态码 | NoData |
| Data | array<object> | 业务数据 |  |
| Data | object | 选题策划对象 |  |
| Outlines | array<object> | 大纲列表 |  |
| Outline | object | 大纲对象 |  |
| Outline | string | 大纲 | 大纲 |
| Summary | string | 大纲摘要 | 大纲摘要 |
| Summary | string | 摘要 | 摘要 |
| Title | string | 标题 | 标题 |
| HttpStatusCode | integer | http 状态码 | 200 |
| MaxResults | integer | 最大返回结果数 | 77 |
| Message | string | 错误说明 | success |
| NextToken | string | 下一页的 token | 下一页的token |
| RequestId | string | 请求唯一标识 | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |
| TotalCount | integer | 总数 | 80 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "NoData",
  "Data": [
    {
      "Outlines": [
        {
          "Outline": "大纲",
          "Summary": "大纲摘要"
        }
      ],
      "Summary": "摘要",
      "Title": "标题"
    }
  ],
  "HttpStatusCode": 200,
  "MaxResults": 77,
  "Message": "success",
  "NextToken": "下一页的token",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "TotalCount": 80
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
