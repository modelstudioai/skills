# DeleteIndexDocument - 删除知识库下的文件

永久删除指定知识库中的文件。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   本接口不支持删除数据查询/图片问答类知识库中的数据。请通过阿里云百炼控制台操作。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 API 权限（需要AliyunBailianDataFullAccess，已包括 sfm:DeleteIndexDocument 权限点），然后才能调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版阿里云百炼 SDK来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 IDIndexId有效）。
-   仅能删除知识库中状态为导入失败（INSERT\_ERROR）或导入成功（FINISH）的文件。如需查询指定知识库下的文件状态，可调用 ListIndexDocuments 接口。
-   删除操作不可逆，被删的文件内容将无法恢复，且 Retrieve 接口将无法再获取其相关信息，请谨慎操作。
-   调用本接口不会删除应用数据中已导入的文档。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/DeleteIndexDocument)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:DeleteIndexDocument</td><td>delete</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/index/delete_index_document HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3z7uw7fwz0vxxxx |
| IndexId | string | 是 | 知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。 | 79c0alxxxx |
| DocumentIds | array | 是 | 文件 ID 列表。 |  |
|  | string | 是 | 文件 ID，即 **AddFile** 接口返回的`FileId`。您也可以在[应用数据](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/data-center)\-文件页签，单击文件名称旁的 ID 图标获取。 | file\_5f03dfea56da4050ab68d61871fc4cb3\_xxxxxxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th>名称</th><th>类型</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td></td><td>object</td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td>string</td><td><div><p>请求 ID。</p></div></td><td>17204B98-xxxx-4F9A-8464-2446A84821CA</td></tr><tr><td>Code</td><td>string</td><td><div><p>错误状态码。</p></div></td><td>Index.InvalidParameter</td></tr><tr><td>Message</td><td>string</td><td><div><p>错误信息。</p></div></td><td>Required parameter(%s) missing or invalid, please check the request parameters.</td></tr><tr><td>Success</td><td>boolean</td><td><div><p>接口调用是否成功，可能值为：</p><ul><li>true：成功。</li><li>false：失败。</li></ul></div></td><td>true</td></tr><tr><td>Data</td><td>object</td><td><div><p>接口业务数据字段。</p></div></td><td></td></tr><tr><td>DeletedDocument</td><td>array</td><td><div><p>已成功删除的文件 ID 列表。</p></div></td><td></td></tr><tr><td>deleted</td><td>string</td><td><div><p>文件 ID。</p></div></td><td>file_5f03dfea56da4050ab68d61871fc4cb3_xxxxxxxx</td></tr><tr><td>Status</td><td>string</td><td><div><p>接口返回的状态码。</p></div></td><td>200</td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Data": {
    "DeletedDocument": [
      "file_5f03dfea56da4050ab68d61871fc4cb3_xxxxxxxx"
    ]
  },
  "Status": 200
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。
