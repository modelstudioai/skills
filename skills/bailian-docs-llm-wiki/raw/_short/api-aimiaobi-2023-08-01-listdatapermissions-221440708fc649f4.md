# ListDataPermissions

权限-列表 - 数据集

<a id="调试"></a>

<a id="api-doc-debug"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

<a id="授权信息"></a>

<a id="api-detail-32"></a>

## 授权信息

当前API暂无授权信息透出。

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/use-workspace">获取 workspaceId</a></p></div></td><td><p>llm-xx</p></td></tr><tr><td>DataType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据类型：</p><ul><li><p>dataset：数据集</p></li></ul></div></td><td><p>dataset</p></td></tr><tr><td>DataId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据权限数据唯一标识</p><ul><li><p>dataset：SystemSearch.QuarkCommonNews</p></li></ul></div></td><td><p>SystemSearch.QuarkCommonNews</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>每页条数</p></div></td><td><p>10</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>当前页：默认 1</p></div></td><td><p>1</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>响应结果</p></div></td><td></td></tr><tr><td>Data</td><td><p>array&lt;object&gt;</p></td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>Id</td><td><p>integer</p></td><td><div><p>主键 ID</p></div></td><td><p>1</p></td></tr><tr><td>CreateUser</td><td><p>string</p></td><td><div><p>创建者</p></div></td><td><p>xxx</p></td></tr><tr><td>CreateTime</td><td><p>string</p></td><td><div><p>创建时间</p></div></td><td><p>2024-11-12 21:46:24</p></td></tr><tr><td>UserId</td><td><p>string</p></td><td><div><p>有权限用户唯一标识</p></div></td><td><p>CustomSemanticSearch</p></td></tr><tr><td>Username</td><td><p>string</p></td><td><div><p>有权限用户名称</p></div></td><td><p>xxx</p></td></tr><tr><td>DataType</td><td><p>string</p></td><td><div><p>数据类型：</p><ul><li><p>dataset：数据集</p></li></ul></div></td><td><p>xxx</p></td></tr><tr><td>DataId</td><td><p>string</p></td><td><div><p>数据权限数据唯一标识</p><ul><li><p>dataset：SystemSearch.QuarkCommonNews</p></li></ul></div></td><td><p>SystemSearch.QuarkCommonNews</p></td></tr><tr><td>Permission</td><td><p>string</p></td><td><div><p>权限定义：默认只读 read</p></div></td><td><p>read</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><div><p>当前页码</p></div></td><td><p>1</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求唯一标识</p></div></td><td><p>1813ceee-7fe5-41b4-87e5-982a4d18cca5</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td><p>true</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>状态码</p></div></td><td><p>NoData</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误说明</p></div></td><td><p>success</p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr><tr><td>TotalCount</td><td><p>integer</p></td><td><div><p>总条数</p></div></td><td><p>100</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><div><p>每页条数</p></div></td><td><p>10</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```json
{
  "Data": [
    {
      "Id": 1,
      "CreateUser": "xxx",
      "CreateTime": "2024-11-12 21:46:24",
      "UserId": "CustomSemanticSearch",
      "Username": "xxx",
      "DataType": "xxx",
      "DataId": "SystemSearch.QuarkCommonNews\n",
      "Permission": "read"
    }
  ],
  "PageNumber": 1,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "TotalCount": 100,
  "PageSize": 10
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListDataPermissions#workbench-doc-change-demo)。
