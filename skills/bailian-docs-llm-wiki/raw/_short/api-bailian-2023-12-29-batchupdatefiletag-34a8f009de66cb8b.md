# BatchUpdateFileTag

该接口用于批量更新数据连接中的文档标签。

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
PUT /{WorkspaceId}/datacenter/batchupdatetag HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 业务空间 ID。在百炼的[控制台首页](https://bailian.console.aliyun.com/knowledge-base#/home)，单击页面左上角业务空间详情图标获取。 | llm-3shx2gu255oqxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>FileInfos</td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><div><p>需要更新的文档列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>是</p></td><td></td><td></td></tr><tr><td>FileId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>1. 打开<a href="https://bailian.console.aliyun.com/cn-beijing/rag/connector/list"><strong>数据集</strong></a>，在目标文件数据集上单击<strong>详情</strong>。<br>2. 单击目标文件的 <strong>ID</strong> 图标，再单击提示中的复制图标，复制文件 ID。</p></div></td><td><p>file_3d5319366e2c46309f4c11cfbeacd5fd_10045951</p></td></tr><tr><td>tags</td><td><p>array</p></td><td><p>是</p></td><td><div><ul><li><p>文件关联的标签列表。最多传入 100 个标签，所有标签字符长度总和不能超过 700。</p></li></ul></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签值，每个标签最多 32 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等），下划线_，中划线-，标签中不能包含空格。</p></div></td><td><p>TagA</p></td></tr><tr><td>UpdateMode</td><td><p>string</p></td><td><p>否</p></td><td><div><p>更新模式，仅支持 APPEND（追加）和 OVERWRITE（覆盖）</p></div></td><td><p>OVERWRITE</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码</p></div></td><td><p>Success</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口返回的业务字段。</p></div></td><td></td></tr><tr><td>UpdateFileTagResultList</td><td><p>array&lt;object&gt;</p></td><td><div><p>标签更新的结果列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td></td><td></td></tr><tr><td>FileId</td><td><p>string</p></td><td><div><p>文件 ID。</p></div></td><td><p>file_f40f2a32205d44b4a93b11617113da15_10045951</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr><tr><td>ErrorCode</td><td><p>string</p></td><td><div><p>返回错误码，仅当 Success 为 false 时返回。</p></div></td><td><p>NoPermission</p></td></tr><tr><td>ErrorMessage</td><td><p>string</p></td><td><div><p>错误描述信息，仅当 Success 为 false 时返回。</p></div></td><td><p>FileId not exists.</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>Required parameter(FileId) missing or invalid, please check the request parameters.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>Id of the request</p></div></td><td><p>17204B98-xxxx-4F9A-8464-2446A84821CA</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Code": "Success",
  "Data": {
    "UpdateFileTagResultList": [
      {
        "FileId": "file_f40f2a32205d44b4a93b11617113da15_10045951",
        "Success": true,
        "ErrorCode": "NoPermission",
        "ErrorMessage": "FileId not exists."
      }
    ]
  },
  "Message": "Required parameter(FileId) missing or invalid, please check the request parameters.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/BatchUpdateFileTag#workbench-doc-change-demo)。
