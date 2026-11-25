# ListDatasetDocuments

查询数据源文档列表。

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
| aimiaobi:ListDatasetDocuments | list | \*全部资源<br><br>`*` | 无 | 无 |

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

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td><p>xxxx</p></td></tr><tr><td>Query</td><td><p>string</p></td><td><p>否</p></td><td><div><p>搜索条件</p></div></td><td><p>搜索条件</p></td></tr><tr><td>DatasetId</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>数据集唯一标识：DatasetName、DatasetId 二选一必填</p></div></td><td><p>1</p></td></tr><tr><td>DatasetName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据集名称</p></div></td><td><p>数据集名称</p></td></tr><tr><td>Status</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>文档状态：</p><ul><li><p>1：创建完成</p></li><li><p>2：文本索引构建完成</p></li><li><p>3：多模态索引构建完成</p></li><li><p>100：全量构建完成</p></li><li><p>0：失败</p></li></ul></div></td><td><p>100</p></td></tr><tr><td>DocType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档类型：</p><ul><li><p>plainText：纯文本</p></li><li><p>richText：富文本</p></li><li><p>text：文本文件</p></li><li><p>pdf：</p></li><li><p>word：</p></li><li><p>image：图片</p></li><li><p>video：视频</p></li></ul></div></td><td><p>text</p></td></tr><tr><td>DatasetDescription</td><td><p>string</p></td><td><p>否</p></td><td><div><p>废弃</p></div></td><td><p>xx</p></td></tr><tr><td>IncludeFields</td><td><p>array</p></td><td><p>否</p></td><td><div><p>包括字段</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>包括字段</p><ul><li><p>content：正文</p></li><li><p>chunks：片段</p></li></ul></div></td><td><p>content</p></td></tr><tr><td>ExcludeFields</td><td><p>array</p></td><td><p>否</p></td><td><div><p>排除字段：</p><ul><li><p>content：正文</p></li></ul></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>排除字段</p></div></td><td><p>content</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>当前页码</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>每页条数：默认 10</p></div></td><td><p>10</p></td></tr><tr><td>CategoryUuids</td><td><p>array</p></td><td><p>否</p></td><td><div><p>类目唯一标识</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签</p></div></td><td><p>xx</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><p>否</p></td><td><div><p>自定义扩展字段。</p></div></td><td><p>xx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><p>否</p></td><td><div><p>自定义扩展字段。</p></div></td><td><p>xx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><p>否</p></td><td><div><p>自定义扩展字段。</p></div></td><td><p>xx</p></td></tr><tr><td>CreateTimeStart</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>起始创建时间，时间戳形式。</p></div></td><td><p>111</p></td></tr><tr><td>CreateTimeEnd</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>截止创建时间，时间戳形式。</p></div></td><td><p>111</p></td></tr><tr><td>DocUuids</td><td><p>array</p></td><td><p>否</p></td><td><div><p>文档唯一标识</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档唯一标识</p></div></td><td><p>xxx</p></td></tr><tr><td>DocIds</td><td><p>array</p></td><td><p>否</p></td><td><div><p>文档 ID 数组</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档 ID</p></div></td><td><p>xxx</p></td></tr><tr><td>StartTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>开始时间；毫秒</p></div></td><td><p>111</p></td></tr><tr><td>EndTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>结束时间：毫秒</p></div></td><td><p>1111</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>标题</p></div></td><td><p>xxx</p></td></tr><tr><td>NextToken</td><td><p>string</p></td><td><p>否</p></td><td><div><p>下一页的唯一标识：查询第 10000 条以上数据时，必传</p></div></td><td><p>xxx</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 响应结果 |  |
| Data | array<object> | 业务数据 |  |
|  | array<object> | 业务数据 |  |
| DocUuid | string | 内部文档唯一 ID | 内部文档唯一ID |
| Url | string | url | https://xxx/xx |
| Content | string | 正文 | xx |
| Summary | string | 文章摘要 | xx |
| Title | string | 标题 | xx |
| PubTime | string | 发布时间 | 2022-01-01 00:00:00 |
| SourceFrom | string | 来源 | 来源 |
| DisableHandleMultimodalMedia | boolean | 当前记录是否落多模态索引库 | false |
| MultimodalMedias | array<object> | 多模态信息 |  |
|  | object | 多模态信息 |  |
| MediaId | string | 多模态数据唯一标识 | 多模态数据唯一标识 |
| MediaType | string | 多模态数据类型 | 多模态数据类型 |
| FileUrl | string | 图片或视频文件地址 | 图片或视频文件地址 |
| DocId | string | 用户指定的文档唯一 ID | xx |
| DocType | string | 文档类型 | text |
| Status | integer | 文档索引构建状态 | 100 |
| CategoryUuid | string | 类目唯一标识 | xx |
| Extend1 | string | 扩展字段 1 | xx |
| Extend2 | string | 扩展字段 2 | xx |
| Extend3 | string | 扩展字段 3 | xx |
| CreateTime | string | 创建时间 | 2025-04-14 19:59:53 |
| UpdateTime | string | 修改时间 | 2025-04-14 19:59:53 |
| UpdateUser | string | 更新用户 | 1 |
| CreateUser | string | 创建者 | 1 |
| Tags | array | 标签。 |  |
|  | string | 标签。 | xx |
| PageNumber | integer | 当前页码 | 1 |
| PageSize | integer | 每页记录条数 | 10 |
| TotalCount | integer | 总记录条数 | 100 |
| RequestId | string | 请求唯一标识 | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |
| Code | string | 状态码 | NoData |
| Message | string | 错误说明 | success |
| HttpStatusCode | integer | http 状态码 | 200 |
| NextToken | string | 下一页的唯一标识 | xxx |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Data": [
    {
      "DocUuid": "内部文档唯一ID",
      "Url": "https://xxx/xx",
      "Content": "xx",
      "Summary": "xx",
      "Title": "xx",
      "PubTime": "2022-01-01 00:00:00",
      "SourceFrom": "来源",
      "DisableHandleMultimodalMedia": false,
      "MultimodalMedias": [
        {
          "MediaId": "多模态数据唯一标识",
          "MediaType": "多模态数据类型",
          "FileUrl": "图片或视频文件地址"
        }
      ],
      "DocId": "xx",
      "DocType": "text",
      "Status": 100,
      "CategoryUuid": "xx",
      "Extend1": "xx",
      "Extend2": "xx",
      "Extend3": "xx",
      "CreateTime": "2025-04-14 19:59:53",
      "UpdateTime": "2025-04-14 19:59:53",
      "UpdateUser": "1",
      "CreateUser": "1",
      "Tags": [
        "xx"
      ]
    }
  ],
  "PageNumber": 1,
  "PageSize": 10,
  "TotalCount": 100,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "NextToken": "xxx"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDatasetDocuments#workbench-doc-change-demo)。
