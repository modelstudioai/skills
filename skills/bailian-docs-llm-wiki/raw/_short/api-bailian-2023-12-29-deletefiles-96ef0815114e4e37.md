# DeleteFiles

批量删除文件

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   不支持通过 API 删除数据表。如需删除数据表或表中特定的数据，请前往[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)操作。
-   本接口用于删除[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)中的文件，不会影响已构建好的知识库。如需删除知识库中的文件，请调用 **DeleteIndexDocument** 接口。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:DeleteFiles 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口仅能删除状态为解析失败（PARSE\_FAILED）或解析完成（PARSE\_SUCCESS）的文件。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

当前API暂无授权信息透出。

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/datacenter/file/delete HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 类目所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-mbhn96xxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| FileIds | array | 是 | 需要删除的文件 id 列表，单次删除最多支持 20 个文件 |  |
|  | string | 否 | 需要删除的文件 id | file\_xxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>DataCenter.FileTooLarge</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>返回内容</p></div></td><td></td></tr><tr><td>DeleteFileResultList</td><td><p>array&lt;object&gt;</p></td><td><div><p>删除结果</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>单个文件删除结果</p></div></td><td></td></tr><tr><td>FileId</td><td><p>string</p></td><td><div><p>文件 ID。</p></div></td><td><p>file_6b193b9b4b1546ef9eaa7340e69adfca_10052857</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>文件删除状态。状态可能值为：</p><ul><li><p>DELETED：删除成功。</p></li><li><p>FAILED：删除失败。</p></li><li><p>NOT_FOUND：未查询到文件</p></li></ul></div></td><td><p>DELETED</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>Id of the request</p></div></td><td><p>17204B98-7734-4F9A-8464-2446A84821CA</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Code": "DataCenter.FileTooLarge",
  "Data": {
    "DeleteFileResultList": [
      {
        "FileId": "file_6b193b9b4b1546ef9eaa7340e69adfca_10052857",
        "Status": "DELETED"
      }
    ]
  },
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-7734-4F9A-8464-2446A84821CA",
  "Status": "200",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/DeleteFiles#workbench-doc-change-demo)。
