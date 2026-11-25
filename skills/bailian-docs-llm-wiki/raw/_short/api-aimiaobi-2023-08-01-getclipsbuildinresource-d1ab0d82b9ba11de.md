# GetClipsBuildInResource

获得智能混剪内置资源

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
POST  HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 否 | 百炼业务空间 Id | llm-az2gglkjauwnnhpq |
| ResourceType | integer | 否 | 资源类型。 | 0 - 音色 1- 背景音 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | Id of the request | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| Code | string | 错误码 | successful |
| Data | object | 业务数据 |  |
| ResourceType | integer | 资源类型。 | 0 - 音色 1- 背景音 |
| ResourceList | array | 资源列表 |  |
|  | string | 资源列表 | 轻快 |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 返回结果消息 | successful |
| Success | boolean | 是否成功：true 成功，false 失败 | true |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "successful",
  "Data": {
    "ResourceType": 0,
    "ResourceList": [
      "轻快"
    ]
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 403 | NoPermission | You are not authorized to perform this action. | 请检查workspaceId的赋值 |

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/GetClipsBuildInResource#workbench-doc-change-demo)。
