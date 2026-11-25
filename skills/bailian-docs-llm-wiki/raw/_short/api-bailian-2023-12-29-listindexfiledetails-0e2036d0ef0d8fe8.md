# ListIndexFileDetails - 查询知识库文件详情

获取指定知识库中的文件，以及它们的详细信息。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListIndexFiles 权限点），然后才能调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   本接口具有幂等性。

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
| sfm:ListIndexFileDetails | list | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/index/list_index_file_detail HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3z7uw7fwz0vexxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>IndexId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>知识库 ID，即 <strong>CreateIndex</strong> 接口返回的<code>Data.Id</code>。</p></div></td><td><p>79c0alxxxx</p></td></tr><tr><td>DocumentStatus</td><td><p>string</p></td><td><p>否</p></td><td><div><p>即通过文件导入状态对接口返回的文件列表进行过滤。取值范围：</p><ul><li><p>INSERT_ERROR：导入索引失败。</p></li><li><p>RUNNING：索引构建中。</p></li><li><p>DELETED：已经删除。</p></li><li><p>FINISH：索引构建成功。</p></li><li><p>PARSE_FAILED：解析失败</p></li><li><p>DOC_PARSING：解析中</p></li></ul><p>默认值为空，即不使用文件导入状态对结果进行过滤。</p></div></td><td><p>FINISH</p></td></tr><tr><td>DocumentName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>即通过文件名称对接口返回的文件详情列表进行过滤。默认值为空，即不使用文件名称对结果进行过滤。</p></div></td><td><p>翻译平台运维文档</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>指定要查询的页码。起始值为 1。默认值为 1。</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>指定分页查询时每页展示的文件数量 ，最大值 10。</p></div></td><td><p>10</p></td></tr><tr><td>EnableNameLike</td><td><p>string</p></td><td><p>否</p></td><td><div><p>是否开启文件名称的模糊匹配，与<code>DocumentName</code>参数配合使用。取值范围：</p><ul><li><p>true：根据文件名称对接口返回的文件列表进行模糊匹配。</p></li><li><p>false：默认根据文件名称进行精确匹配。</p></li></ul><p>默认值为 false。</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>开启</p></div></li><li>false :<div><p>不开启</p></div></li></ul></div></td><td><p>false</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>35A267BF-xxxx-54DB-8394-AA3B0742D833</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>InvalidParameter</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口业务数据字段。</p></div></td><td></td></tr><tr><td>Documents</td><td><p>array&lt;object&gt;</p></td><td><div><p>返回知识库中的文件列表，按文件导入时间倒序排序（与控制台一致）。</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>文件对象。</p></div></td><td></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>文件导入状态。可能值为：</p><ul><li><p>INSERT_ERROR：文件导入失败。</p></li><li><p>RUNNING：文件导入中。</p></li><li><p>DELETED：文件已删除。</p></li><li><p>FINISH：文件导入成功。</p></li></ul></div></td><td><p>RUNNING</p></td></tr><tr><td>EnableHeaders</td><td><p>string</p></td><td><div><p>Excel 文件表头是否支持拼装。</p></div></td><td><p>true</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>文件导入错误信息。</p></div></td><td><p>check fileUrlKey[file_path] / fileNameKey[null] / fileExtensionKey[file_extension] is invalid</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><div><p>文件大小，单位字节 Byte。</p></div></td><td><p>996764</p></td></tr><tr><td>SourceId</td><td><p>string</p></td><td><div><p>类目 ID。</p></div></td><td><p>cate_21a407a3372c4ba7aedc649709143f0cxxxxxxxx</p></td></tr><tr><td>DocumentType</td><td><p>string</p></td><td><div><p>文件格式类型。可能值为： pdf、docx、doc、txt、md、pptx、ppt、png、jpg、jpeg、bmp、gif、EXCEL。</p></div></td><td><p>pdf</p></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>文件 ID。</p></div></td><td><p>doc_c134aa2073204a5d936d870bf960f56axxxxxxxx</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>文件导入错误状态码。</p></div></td><td><p>110002</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>文件名称。</p></div></td><td><p>翻译平台运维文档</p></td></tr><tr><td>ChunkSize</td><td><p>string</p></td><td><div><p>分段长度，即文本切片的字符数。</p></div></td><td><p>600</p></td></tr><tr><td>OverlapSize</td><td><p>string</p></td><td><div><p>分段重叠长度。</p></div></td><td><p>100</p></td></tr><tr><td>ChunkMode</td><td><p>string</p></td><td><div><p>自定义切分。</p></div></td><td><p>DashSplitter</p></td></tr><tr><td>GmtModified</td><td><p>integer</p></td><td><div><p>文件导入知识库的时间，采用 Unix timestamp 格式。</p></div></td><td><p>1744856423000</p></td></tr><tr><td>separator</td><td><p>string</p></td><td><div><p>分句标识符。</p></div></td><td><p>&quot; &quot;</p></td></tr><tr><td>MetaExtractInfo</td><td><p>string</p></td><td><div><p>文档提取的 Meta 信息。</p></div></td><td><p>{ &quot;doc_summary&quot;: [&quot;Example 1.&quot;], &quot;health_rule&quot;: [&quot;Example 2&quot;] }</p></td></tr><tr><td>IndexId</td><td><p>string</p></td><td><div><p>知识库 ID。</p></div></td><td><p>79c0alxxxx</p></td></tr><tr><td>TotalCount</td><td><p>integer</p></td><td><div><p>返回结果的总条数。</p></div></td><td><p>2437</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><div><p>返回指定的页码。</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><div><p>返回指定的每页条数。</p></div></td><td><p>10</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
  "Code": "InvalidParameter\n",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Data": {
    "Documents": [
      {
        "Status": "RUNNING",
        "EnableHeaders": "true",
        "Message": "check fileUrlKey[file_path] / fileNameKey[null] / fileExtensionKey[file_extension] is invalid",
        "Size": 996764,
        "SourceId": "cate_21a407a3372c4ba7aedc649709143f0cxxxxxxxx\n",
        "DocumentType": "pdf",
        "Id": "doc_c134aa2073204a5d936d870bf960f56axxxxxxxx\n",
        "Code": "110002",
        "Name": "翻译平台运维文档\n",
        "ChunkSize": "600",
        "OverlapSize": "100",
        "ChunkMode": "DashSplitter",
        "GmtModified": 1744856423000,
        "separator": "\" \"",
        "MetaExtractInfo": "{\n  \"doc_summary\": [\"Example 1.\"],\n  \"health_rule\": [\"Example 2\"]\n}"
      }
    ],
    "IndexId": "79c0alxxxx",
    "TotalCount": 2437,
    "PageNumber": 1,
    "PageSize": 10
  },
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/ListIndexFileDetails#workbench-doc-change-demo)。
