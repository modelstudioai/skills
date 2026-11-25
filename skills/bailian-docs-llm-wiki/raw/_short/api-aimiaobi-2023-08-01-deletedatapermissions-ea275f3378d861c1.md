# DeleteDataPermissions

权限-批量删除： - 数据集权限

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

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/use-workspace) | llm-xxx |
| Ids | array | 是 | 权限 id |  |
|  | integer | 否 | 权限 id | 1 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 响应结果 |  |
| RequestId | string | 请求唯一标识 | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |
| Code | string | 状态码 | NoData |
| Message | string | 错误说明 | success |
| HttpStatusCode | integer | http 状态码 | 200 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```json
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/DeleteDataPermissions#workbench-doc-change-demo)。
