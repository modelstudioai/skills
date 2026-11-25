# ListHotTopics

获取热点话题列表。

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

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
    

| 操作 | 访问级别 | 资源类型 | 条件关键字 | 关联操作 |
| --- | --- | --- | --- | --- |
| aimiaobi:ListHotTopics | list | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST  HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| AgentKey | string | 是 | 业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey) | xxxxx\_p\_efm |
| TopicSource | string | 否 | 热榜源筛选，支持的热榜源。热榜源详见 API：ListHotSources<br><br>Aggregation：表示 聚合后的全国热点话题榜 | Quark |
| Topics | array | 否 | 热榜主题事件筛选 |  |
|  | string | 否 | 热榜主题事件名称 | xxx |
| TopicVersion | string | 否 | 数据版本筛选 | 数据版本筛选 |
| TopicQuery | string | 否 | 根据热榜主题全文检索 | 根据热榜主题全文检索 |
| TopicIds | array | 否 | 热榜主题 ID 列表 |  |
|  | string | 否 | 热榜主题 ID | xxxxxx |
| WithNews | boolean | 否 | 响应是否包含新闻 | true |
| NextToken | string | 否 | 下一页的 token | 下一页的token |
| MaxResults | integer | 否 | 最大返回结果数 | 1 |
| CustomField | string | 否 | 自定义业务字段筛选（keyword 精确匹配），长度上限 255 字符 | biz-tag-001 |
| CreateTimeStart | string | 否 | 话题创建时间筛选起点（包含），格式：yyyy-MM-dd HH:mm:ss | 2026-06-01 00:00:00 |
| CreateTimeEnd | string | 否 | 话题创建时间筛选终点（包含），格式：yyyy-MM-dd HH:mm:ss | 2026-06-04 23:59:59 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>PageResult2</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>状态码</p></div></td><td><p>NoData</p></td></tr><tr><td>Data</td><td><p>array&lt;object&gt;</p></td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>热点事件列表</p></div></td><td></td></tr><tr><td>AsyncTaskId</td><td><p>string</p></td><td><div><p>异步任务 ID（自定义主题场景下使用）</p></div></td><td><p>异步任务ID（自定义主题场景下使用）</p></td></tr><tr><td>CreateUser</td><td><p>string</p></td><td><div><p>创建用户 ID（自定义主题场景下使用）</p></div></td><td><p>创建用户ID（自定义主题场景下使用）</p></td></tr><tr><td>HotValue</td><td><p>integer</p></td><td><div><p>热度值</p></div></td><td><p>61</p></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>热榜 ID</p></div></td><td><p>热榜ID</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>异步任务状态（自定义事件场景下使用） (PENDING: 待执行, RUNNING: 执行中, SUCCESSED: 成功, SUSPENDED: 暂停, FAILED: 失败, CANCELED: 取消)</p></div></td><td><p>FAILED</p></td></tr><tr><td>StructureSummary</td><td><p>array&lt;object&gt;</p></td><td><div><p>结构化主题摘要列表</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td></td><td></td></tr><tr><td>DocList</td><td><p>array&lt;object&gt;</p></td><td><div><p>生成该标题摘要引用的文章</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Source</td><td><p>string</p></td><td><div><p>文章来源</p></div></td><td><p>夸克</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>文章标题</p></div></td><td><p>xxxxx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><div><p>文章 URL</p></div></td><td><p><a href="http://www.example.com">http://www.example.com</a></p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>摘要</p></div></td><td><p>摘要</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><div><p>标题</p></div></td><td><p>标题</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><div><p>热榜摘要</p></div></td><td><p>热榜摘要</p></td></tr><tr><td>TaskErrorMessage</td><td><p>string</p></td><td><div><p>异步任务失败错误信息</p></div></td><td><p>异步任务失败错误信息</p></td></tr><tr><td>TaskStatus</td><td><p>integer</p></td><td><div><p>异步任务状态。0-待执行，1-执行中，2-执行成功，3-暂停（暂不使用），4-执行失败，6-任务取消（自定义事件场景下使用）</p></div></td><td><p>26</p></td></tr><tr><td>Topic</td><td><p>string</p></td><td><div><p>主题唯一名称</p></div></td><td><p>主题唯一名称</p></td></tr><tr><td>TopicSource</td><td><p>string</p></td><td><div><p>热榜源，目前支持的热榜源：</p><ul><li><p>Toutiao：头条</p></li><li><p>Quark：夸克</p></li><li><p>Baidu：百度</p></li><li><p>Sina：新浪</p></li><li><p>Custom：自定义</p></li><li><p>Aggregation：热点话题榜</p></li></ul></div></td><td><p>Toutiao</p></td></tr><tr><td>Version</td><td><p>string</p></td><td><div><p>数据版本</p></div></td><td><p>数据版本</p></td></tr><tr><td>CustomField</td><td><p>string</p></td><td><div><p>自定义业务字段（keyword）</p></div></td><td><p>biz-tag-001</p></td></tr><tr><td>CreateTime</td><td><p>string</p></td><td><div><p>话题创建时间，格式：yyyy-MM-dd HH:mm:ss</p></div></td><td><p>2026-06-04 12:34:56</p></td></tr><tr><td>TopicUrl</td><td><p>string</p></td><td><div><p>话题原文链接</p></div></td><td><p><a href="https://www.example.com/topic/123">https://www.example.com/topic/123</a></p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr><tr><td>MaxResults</td><td><p>integer</p></td><td><div><p>最大返回结果数</p></div></td><td><p>94</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误说明</p></div></td><td><p>success</p></td></tr><tr><td>NextToken</td><td><p>string</p></td><td><div><p>下一页的 token</p></div></td><td><p>下一页的token</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求唯一标识</p></div></td><td><p>1813ceee-7fe5-41b4-87e5-982a4d18cca5</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td><p>true</p></td></tr><tr><td>TotalCount</td><td><p>integer</p></td><td><div><p>总数</p></div></td><td><p>23</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Code": "NoData",
  "Data": [
    {
      "AsyncTaskId": "异步任务ID（自定义主题场景下使用）",
      "CreateUser": "创建用户ID（自定义主题场景下使用）",
      "HotValue": 61,
      "Id": "热榜ID",
      "Status": "FAILED",
      "StructureSummary": [
        {
          "DocList": [
            {
              "Source": "夸克",
              "Title": "xxxxx",
              "Url": "http://www.example.com"
            }
          ],
          "Summary": "摘要",
          "Title": "标题"
        }
      ],
      "Summary": "热榜摘要",
      "TaskErrorMessage": "异步任务失败错误信息",
      "TaskStatus": 26,
      "Topic": "主题唯一名称",
      "TopicSource": "Toutiao",
      "Version": "数据版本",
      "CustomField": "biz-tag-001",
      "CreateTime": "2026-06-04 12:34:56",
      "TopicUrl": "https://www.example.com/topic/123"
    }
  ],
  "HttpStatusCode": 200,
  "MaxResults": 94,
  "Message": "success",
  "NextToken": "下一页的token",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "TotalCount": 23
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListHotTopics#workbench-doc-change-demo)。
