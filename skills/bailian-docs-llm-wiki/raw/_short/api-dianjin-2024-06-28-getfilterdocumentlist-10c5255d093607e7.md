# GetFilterDocumentList - 按元信息过滤查询文档列表

获取文档列表（可按元信息过滤查询，也支持分页查询）。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetFilterDocumentList)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:GetFilterDocumentList</td><td>none</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/library/filterDocument HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>路径参数，业务空间 id</p></div></td><td>llm-xxxxx</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求 body。</p></div></td><td></td></tr><tr><td>and</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>and 表达式，用于筛选文档/文档块</p></div></td><td></td></tr><tr><td>and</td><td>object</td><td>否</td><td><div><p>一系列约束条件，为三元组，用“与”连接</p></div></td><td></td></tr><tr><td>boost</td><td>float</td><td>否</td><td><div><p>value 在文本召回引擎中的权重。默认是 1。</p></div></td><td>1</td></tr><tr><td>key</td><td>string</td><td>否</td><td><div><p>文档库中，元信息的 key</p></div></td><td>company</td></tr><tr><td>operator</td><td>string</td><td>否</td><td><div><p><strong>文档库元信息 key 存储的 value 和输入的 value 之间的关系</strong></p><ul><li>eq：文档库元信息 key 存储的 value = 输入的 value</li><li>contains：文档库元信息 key 存储的 value 列表 &quot;包含&quot; 您输入的 value</li></ul></div></td><td>eq</td></tr><tr><td>value</td><td>string</td><td>否</td><td><div><p>输入的元信息的值</p></div></td><td>alibaba</td></tr><tr><td>docIdList</td><td>array</td><td>否</td><td><div><p>文档 id 列表，用于筛选文档/文档块</p></div></td><td></td></tr><tr><td>docIdList</td><td>string</td><td>否</td><td><div><p>文档 id</p></div></td><td>3553835752369972270</td></tr><tr><td>libraryId</td><td>string</td><td>是</td><td><div><p>文档库 id 用于筛选文档/文档块</p></div></td><td>cjshcxxxx</td></tr><tr><td>or</td><td>array&lt;object&gt;</td><td>否</td><td><div><p>or 表达式，用于筛选文档/文档块。</p></div></td><td></td></tr><tr><td>or</td><td>object</td><td>否</td><td><div><p>一系列约束条件，为三元组，用“或”连接</p></div></td><td></td></tr><tr><td>boost</td><td>float</td><td>否</td><td><div><p>value 在文本召回引擎中的权重。默认是 1。</p></div></td><td>1</td></tr><tr><td>key</td><td>string</td><td>否</td><td><div><p>文档库中，元信息的 key</p></div></td><td>company</td></tr><tr><td>operator</td><td>string</td><td>否</td><td><div><p><strong>文档库元信息 key 存储的 value 和输入的 value 之间的关系</strong></p><ul><li>eq：文档库元信息 key 存储的 value = 输入的 value</li><li>contains：文档库元信息 key 存储的 value 列表 &quot;包含&quot; 您输入的 value</li></ul></div></td><td>contains</td></tr><tr><td>value</td><td>string</td><td>否</td><td><div><p>输入的元信息的值</p></div></td><td>alibaba</td></tr><tr><td>page</td><td>integer</td><td>否</td><td><div><p>页码，用于分页</p></div></td><td>1</td></tr><tr><td>pageSize</td><td>integer</td><td>否</td><td><div><p>每页大小，用于分页</p></div></td><td>10</td></tr><tr><td>status</td><td>array</td><td>否</td><td><div><p>文档状态列表，用于筛选文档。</p><p><strong>文档解析状态列表，</strong></p><p><em>StatusCode：WaitRefresh、InQueue、FetchingData、Embedding、Completed、FormatError、Error</em></p><ul><li>Completed：可用，文档解析完毕。</li><li>Error：不可用，文档解析错误。</li><li>FormatError：文件格式错误。例如文件加密或不完整时需要重新上传正确格式的文件。</li><li>InQueue：待处理，文档待解析。</li><li>Parsed：已解析完成。</li><li>其他状态：为系统内部状态，WaitRefresh 任务被调度，FetchingData 正在解析中，Embedding 正在构建索引。</li></ul></div></td><td></td></tr><tr><td>statu</td><td>string</td><td>否</td><td><div><p>文档状态，用于筛选文档。</p></div></td><td>Completed</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 返回数据 |  |
| cost | long | 耗时 | null |
| data | object | 响应数据 |  |
| currentPage | long | 当前页 | 1 |
| pageSize | long | 每页记录数 | 10 |
| records | array<object> | 记录 |  |
| record | object | 数据 |  |
| docId | string | 文档 id | 29368126816 |
| documentMeta | object | 文档元数据 | {"a": "1"} |
| fileType | string | 文档类型 | pdf |
| gmtCreate | string | 创建时间 | 2024-01-01 00:00:00 |
| gmtModified | string | 修改时间 | 2024-01-01 00:00:00 |
| libraryId | string | 文档所属库 id | sdfgsjdfg |
| statusCode | string | 文档状态（WaitRefresh：等待刷新，InQueue：待处理，FetchingData：数据获取中，Embedding：文档处理中，Error：错误，Completed：可用，Null：未知） | WaitRefresh |
| title | string | 文档标题 | 公司文档 |
| url | string | 文档链接 | null |
| totalPages | long | 总页数 | 10 |
| totalRecords | long | 总记录数 | 100 |
| dataType | string | 数据类型 | null |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| requestId | string | 请求 id | 7ADF010C-FD89-569D-A079-2D4D5247E943 |
| success | boolean | 是否成功 | true |
| time | string | 时间戳 | 2024-01-01 00:00:00 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": {
    "currentPage": 1,
    "pageSize": 10,
    "records": [
      {
        "docId": 29368126816,
        "documentMeta": {
          "a": 1
        },
        "fileType": "pdf",
        "gmtCreate": "2024-01-01 00:00:00",
        "gmtModified": "2024-01-01 00:00:00",
        "libraryId": "sdfgsjdfg",
        "statusCode": "WaitRefresh",
        "title": "公司文档",
        "url": null
      }
    ],
    "totalPages": 10,
    "totalRecords": 100
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "7ADF010C-FD89-569D-A079-2D4D5247E943",
  "success": true,
  "time": "2024-01-01 00:00:00"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
