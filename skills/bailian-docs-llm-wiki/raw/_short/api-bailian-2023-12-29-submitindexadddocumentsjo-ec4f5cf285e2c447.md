# SubmitIndexAddDocumentsJob - 提交知识库文件追加任务

向指定知识库中追加导入已解析的文件。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   本接口不支持数据查询/图片问答类知识库。关于如何更新数据查询/图片问答类知识库，请参见[知识库](../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)一文中关于更新知识库的说明。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:SubmitIndexAddDocumentsJob 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   调用该接口前，请先调用 **AddFile** 接口将您需要追加导入的文件上传至阿里云百炼。
-   调用本接口后，任务需一定时间执行，高峰期可能耗时数小时。任务完成前请勿重复发起请求。如果需要查询任务的执行状态，可调用 **GetIndexJobStatus** 接口查询。此接口返回的文件列表`Documents`为您本次追加（由您提供的`job_id`唯一确定）全部文件，您可以查看每个文件是否导入（解析）成功。注意频繁调用 GetIndexJobStatus 接口会被限流，频率请勿高于 20 次/分钟。
-   本接口调用成功后，将执行一段时间，请求返回前请勿重复发起请求。本接口不具备幂等性。

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
| sfm:SubmitIndexAddDocumentsJob | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/index/add_documents_to_index HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3shx2gu255oqxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>IndexId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>知识库 ID，即 <strong>CreateIndex</strong> 接口返回的<code>Data.Id</code>。</p></div></td><td><p>79c0alxxxx</p></td></tr><tr><td>SourceType</td><td><p>string</p></td><td><p>是</p></td><td><div><p>数据来源类型。取值范围：</p><ul><li><p>DATA_CENTER_CATEGORY：类目类型，即导入<a href="https://bailian.console.aliyun.com/?tab=app#/data-center">应用数据</a>中指定类目下的所有文档，支持导入多个类目。</p></li><li><p>DATA_CENTER_FILE：文档类型，即导入<a href="https://bailian.console.aliyun.com/?tab=app#/data-center">应用数据</a>下的指定文件，支持导入多个文件。</p></li></ul><div><p>如果本参数传入 DATA_CENTER_CATEGORY，则必须指定<code>CategoryIds</code>参数；如果本参数传入 DATA_CENTER_FILE，则必须指定<code>DocumentIds</code>参数。</p></div></div><div><p><strong>枚举值：</strong></p><ul><li>DATA_CENTER_CATEGORY :<div><p>类目类型</p></div></li><li>DATA_CENTER_FILE :<div><p>文档类型</p></div></li></ul></div></td><td><p>DATA_CENTER_FILE</p></td></tr><tr><td>DocumentIds</td><td><p>array</p></td><td><p>否</p></td><td><div><p>文件 ID 列表。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>文件 ID，即 <strong>AddFile</strong> 接口返回的<code>FileId</code>。您也可以在<a href="https://bailian.console.aliyun.com/?tab=app#/data-center">应用数据</a>页面，单击文件名称旁的 ID 图标获取。</p></div></td><td><p>doc_ea4a504d9ce545508d8aa6d90371bf54xxxxxxxx</p></td></tr><tr><td>CategoryIds</td><td><p>array</p></td><td><p>否</p></td><td><div><p>类目 ID 列表。</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>类目 ID，即 <strong>AddCategory</strong> 接口返回的<code>CategoryId</code>。您也可以在<a href="https://bailian.console.aliyun.com/?tab=app#/data-center">应用数据</a>-文件页签，单击类目旁的 ID 图标获取。</p></div></td><td><p>cate_21a407a3372c4ba7aedc649709143f0cxxxxxxxx</p></td></tr><tr><td>ChunkMode</td><td><p>string</p></td><td><p>否</p></td><td><div><div><p>启用自定义切分（仅对您本次追加的文件生效）。更多信息，请参见<a href="../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md">知识库</a>。可能取值（不支持同时传入多个值）：</p><ul><li><p><strong>length</strong>：按长度切分。严格按照您指定的<code>ChunkSize</code>和<code>OverlapSize</code>切分。 若您未传入这两个参数，系统将采用默认值（<code>ChunkSize</code>为 500，<code>OverlapSize</code>为 100）。按长度切分不支持<code>Separator</code>（即使传入也不生效）。</p></li><li><p><strong>page</strong>：按页切分。如果指定了<code>ChunkSize</code>，切分时将一并考虑（未传入时，将使用默认值 500）。按页切分不支持<code>OverlapSize</code>和<code>Separator</code>（即使传入也不生效）。</p></li><li><p><strong>h1</strong>~<strong>h5</strong>：按照对应层级的标题切分（<code>h1</code>为一级标题，依此类推，最深支持到<code>h5</code>五级标题）。如果指定了<code>ChunkSize</code>，切分时将一并考虑（未传入时，将使用默认值 500）。按标题切分不支持<code>OverlapSize</code>和<code>Separator</code>（即使传入也不生效）。</p></li><li><p><strong>regex</strong>：按照正则切分，此时必须指定<code>Separator</code>参数。如果指定了<code>ChunkSize</code>，切分时将一并考虑（未传入时，将使用默认值 500）。按正则切分不支持<code>OverlapSize</code>（即使传入也不生效）。</p></li></ul><p>默认值为空，采用智能切分。</p></div></div></td><td><p>length</p></td></tr><tr><td>Separator</td><td><p>string</p></td><td><p>否</p></td><td><div><div><p>分句标识符，仅在<code>chunkMode</code>=<strong>regex</strong> 时生效（否则即使传入也不生效）。可传入一个正则表达式（不支持多个），用于将文件分割为小段的文本切片。更多信息，请参见<a href="../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md">知识库</a>。</p><p>使用智能切分（未指定<code>chunkMode</code>）时，保持默认空值即可。</p></div></div></td><td><p>(?&lt;=。)</p></td></tr><tr><td>ChunkSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><div><p>分段长度，即您希望每个文本切片的字符数上限（仅对您本次追加的文件生效）。超过该长度时：</p><ul><li><p><strong>智能切分</strong>（未指定<code>chunkMode</code>）：文本很可能会被截断。</p></li><li><p><strong>自定义切分</strong>（指定了<code>chunkMode</code>）：文本将被强制切割。</p></li></ul><p>取值范围[1-6000]。如果未传入本参数，将使用默认值 500。</p><p>更多信息，请参见<a href="../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md">知识库</a>。</p><div><p>请注意，如果您指定了<code>ChunkSize</code>参数且小于 100，则必须指定<code>OverlapSize</code>参数。您也可以不指定这 2 个参数（系统将采用默认值）。</p></div></div></div></td><td><p>128</p></td></tr><tr><td>OverlapSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><div><p>分段重叠长度（仅对您本次追加的文件生效）。它表示当前文本切片与上一个文本切片的重叠字符数。更多信息，请参见<a href="../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md">知识库</a>。取值范围[0-1024]。</p><p>如果未传入本参数，将使用默认值 100。</p><div><p>请注意，<code>OverlapSize</code>的值必须小于<code>ChunkSize</code>的值，否则会导致切分异常。</p></div></div></div></td><td><p>16</p></td></tr><tr><td>EnableHeaders</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>Excel 文件表头是否支持拼装。开启后，知识库会将所有 xlsx、xls 格式文件的首行数据视为表头，并自动拼接到每个文本切片中（数据行），避免大模型误将表头视为普通数据行来处理。</p><div><p>建议仅在导入文件均为 xlsx、xls 格式且含表头时开启，否则无需开启。</p></div><p>取值范围：</p><ul><li><p>true：开启。</p></li><li><p>false：不开启。</p></li></ul><p>默认值为 false，即不开启。</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>开启</p></div></li><li>false :<div><p>不开启</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>Extra</td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>uniqueId</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>778C0B3B-xxxx-5FC1-A947-36EDD13606AB</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口返回的业务字段。</p></div></td><td></td></tr><tr><td>Id</td><td><p>string</p></td><td><div><p>任务 ID，又称<code>JobId</code>。</p></div></td><td><p>42687eb254a34802bed398357f5498ae</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>Index.InvalidParameter</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
  "Data": {
    "Id": "42687eb254a34802bed398357f5498ae"
  },
  "Status": "200",
  "Success": true,
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Code": "Index.InvalidParameter"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | IdempotentParameterMismatch | The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical. |  |

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/SubmitIndexAddDocumentsJob#workbench-doc-change-demo)。
