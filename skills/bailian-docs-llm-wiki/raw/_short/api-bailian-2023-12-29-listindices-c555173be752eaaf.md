# ListIndices - 查询知识库列表

获取指定业务空间下知识库列表。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListIndex 权限点），然后才能调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

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
| sfm:ListIndex | list | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{WorkspaceId}/index/list_indices HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3shx2gu255oq6xxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| IndexName | string | 否 | 知识库的名称。支持通过名称查找知识库。长度为 1~20 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等）。可以包含半角冒号（:）、下划线（\_）、半角句号（.）或者短划线（-）。<br><br>默认值为空，即查询指定业务空间下的所有知识库。 | idx\_status\_score |
| PageNumber | string | 否 | 指定要查询的页码。起始值为 1。默认值为 1。 | 1 |
| PageSize | string | 否 | 指定分页查询时每页展示的知识库数量。最大值不限。 默认值为 10。 | 10 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>17204B98-xxxx-4F9A-8464-2446A84821CA</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>返回数据。</p></div></td><td></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><div><p>返回指定的页码。</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><div><p>返回指定的每页条数。</p></div></td><td><p>10</p></td></tr><tr><td>TotalCount</td><td><p>integer</p></td><td><div><p>返回结果的总条数。</p></div></td><td><p>48</p></td></tr><tr><td>Indices</td><td><p>array&lt;object&gt;</p></td><td><div><p>知识库列表。</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><div><p>知识库对象。</p></div></td><td></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>知识库 ID，即 <strong>CreateIndex</strong> 接口返回的<code>Data.Id</code>。</p></div></td><td><p>lecxr5xxxx</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>知识库名称。</p></div></td><td><p>XXXX产品清单</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>知识库描述。</p></div></td><td><p>清单中产品主要面向海外客户。</p></td></tr><tr><td>StructureType</td><td><p>string</p></td><td><div><p>知识库类型。可能值：</p><ul><li><p>UNSTRUCTURED：文档搜索类。</p></li></ul></div></td><td><p>UNSTRUCTURED</p></td></tr><tr><td>ChunkSize</td><td><p>integer</p></td><td><div><p>分段预估长度。可能值范围[1-2048]。</p></div></td><td><p>5</p></td></tr><tr><td>OverlapSize</td><td><p>integer</p></td><td><div><p>分段重叠长度。可能值范围[0-1024]。</p></div></td><td><p>10</p></td></tr><tr><td>Separator</td><td><p>string</p></td><td><div><p>分句标识符。如果有多个分句标识符，则用 ｜ 分隔。可能值：</p><ul><li><p>\n：换行</p></li><li><p>，：中文逗号</p></li><li><p>,：英文逗号</p></li><li><p>。：中文句号</p></li><li><p>.：英文句号</p></li><li><p>！:中文叹号</p></li><li><p>!：英文叹号</p></li><li><p>；：中文分号</p></li><li><p>;：英文分号</p></li><li><p>？：中文问号</p></li><li><p>?：英文问号</p></li></ul></div></td><td><p>\n</p></td></tr><tr><td>EmbeddingModelName</td><td><p>string</p></td><td><div><p>Embedding 模型名称。可能值：</p><ul><li><p>text-embedding-v4：text-embedding-v4 模型。</p></li><li><p>text-embedding-v3：text-embedding-v3 模型。</p></li><li><p>text-embedding-v2：text-embedding-v2 模型。</p></li></ul></div></td><td><p>text-embedding-v2</p></td></tr><tr><td>RerankModelName</td><td><p>string</p></td><td><div><p>Rank 模型名称。可能值：</p><ul><li><p>qwen3-rerank-hybrid：qwen3-rerank(hybrid)排序。</p></li><li><p>qwen3-rerank：qwen3-rerank 排序。</p></li><li><p>gte-rerank-hybrid：gte-rerank(hybrid)排序。</p></li><li><p>gte-rerank：gte-rerank 排序。</p></li></ul></div></td><td><p>gte-rerank-hybrid</p></td></tr><tr><td>RerankMinScore</td><td><p>string</p></td><td><div><p>相似度阈值。范围[0.01-1.00]。</p></div></td><td><p>0.01</p></td></tr><tr><td>SourceType</td><td><p>string</p></td><td><div><p>阿里云百炼<a href="https://bailian.console.aliyun.com/?tab=app#/data-center">应用数据</a>的数据类型。</p><p>对于文档搜索/音视频搜索类知识库，可能值：</p><ul><li><p>DATA_CENTER_CATEGORY：类目类型。</p></li><li><p>DATA_CENTER_FILE：文件类型。</p></li></ul><p>对于数据查询/图片问答类知识库，可能值：</p><ul><li><p>DATA_CENTER_STRUCTURED_TABLE：数据表类型。</p></li></ul></div></td><td><p>DATA_CENTER_FILE</p></td></tr><tr><td>DocumentIds</td><td><p>array</p></td><td><div><p>文件 ID 列表。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><div><p>文件 ID。</p></div></td><td><p>file_8c67b438043848199ffaa903d29addd4_xxxxxxxx</p></td></tr><tr><td>SinkType</td><td><p>string</p></td><td><div><p>知识库的向量存储类型。可能值：</p><ul><li><p>ES：内置的向量数据库。</p></li><li><p>BUILT_IN：内置的向量数据库。</p></li><li><p>ADB：AnalyticDB for PostgreSQL 数据库。</p></li></ul></div></td><td><p>BUILT_IN</p></td></tr><tr><td>SinkInstanceId</td><td><p>string</p></td><td><div><p>知识库的向量存储的实例 ID。</p></div></td><td><p>gp-bp1gq62t1788yxxxx</p></td></tr><tr><td>SinkRegion</td><td><p>string</p></td><td><div><p>知识库的向量存储的实例地域。</p></div></td><td><p>cn-hangzhou</p></td></tr><tr><td>ConfgModel</td><td><p>string</p></td><td><div><p>此知识库采用的配置模式。可能值：</p><ul><li><p>recommend：推荐配置。</p></li><li><p>user-defined：自定义。</p></li></ul></div></td><td><p>recommend</p></td></tr><tr><td>EnableRewrite</td><td><p>boolean</p></td><td><div><p>此知识库是否开启了<a href="https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji">多轮对话改写</a>。可能值：</p><ul><li><p>true：已开启。</p></li><li><p>false：未开启。</p></li></ul></div></td><td><p>false</p></td></tr><tr><td>StructuredIndexConfig</td><td><p>array&lt;object&gt;</p></td><td><div><p>数据查询或图片问答类知识库中的索引配置信息</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>索引字段名称</p></div></td><td><p>name</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><div><p>索引字段类型</p></div><div><p><strong>枚举值：</strong></p><ul><li>datetime :<div><p>datetime</p></div></li><li>string :<div><p>string</p></div></li><li>double :<div><p>double</p></div></li><li>image_url :<div><p>image_url</p></div></li><li>long :<div><p>long</p></div></li></ul></div></td><td><p>string</p></td></tr><tr><td>IsSearch</td><td><p>boolean</p></td><td><div><p>是否参与知识库检索。<strong>true</strong> 表示允许知识库在此列数据中进行搜索</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>true</p></div></li><li>false :<div><p>false</p></div></li></ul></div></td><td><p>true</p></td></tr><tr><td>IsRecall</td><td><p>boolean</p></td><td><div><p>是否参与模型回复。<strong>true</strong> 表示本列的检索结果将作为大模型生成回答时的输入信息</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>true</p></div></li><li>false :<div><p>false</p></div></li></ul></div></td><td><p>true</p></td></tr><tr><td>PipelineCommercialType</td><td><p>string</p></td><td><div><p>知识库的规格类型。可能值：</p><ul><li><p>standard：标准版。</p></li><li><p>enterprise：旗舰版。</p></li></ul></div></td><td><p>standard</p></td></tr><tr><td>PipelineCommercialCu</td><td><p>integer</p></td><td><div><p>知识库的 RCU 数量，仅对旗舰版知识库有效。</p></div></td><td><p>1</p></td></tr><tr><td>PipelineStorageUsage</td><td><p>number</p></td><td><div><p>知识库的存储使用量，单位为 GB。</p></div></td><td><p>0.03</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>Index.InvalidParameter</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Data": {
    "PageNumber": 1,
    "PageSize": 10,
    "TotalCount": 48,
    "Indices": [
      {
        "Id": "lecxr5xxxx",
        "Name": "XXXX产品清单",
        "Description": "清单中产品主要面向海外客户。",
        "StructureType": "UNSTRUCTURED",
        "ChunkSize": 5,
        "OverlapSize": 10,
        "Separator": "\\n",
        "EmbeddingModelName": "text-embedding-v2",
        "RerankModelName": "gte-rerank-hybrid",
        "RerankMinScore": "0.01",
        "SourceType": "DATA_CENTER_FILE",
        "DocumentIds": [
          "file_8c67b438043848199ffaa903d29addd4_xxxxxxxx"
        ],
        "SinkType": "BUILT_IN",
        "SinkInstanceId": "gp-bp1gq62t1788yxxxx",
        "SinkRegion": "cn-hangzhou",
        "ConfgModel": "recommend",
        "EnableRewrite": false,
        "StructuredIndexConfig": [
          {
            "Name": "name",
            "Type": "string",
            "IsSearch": true,
            "IsRecall": true
          }
        ],
        "PipelineCommercialType": "standard",
        "PipelineCommercialCu": 1,
        "PipelineStorageUsage": 0.03
      }
    ]
  },
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Status": "200"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/ListIndices#workbench-doc-change-demo)。
