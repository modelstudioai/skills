# GetConnector

获取连接器信息。当前接口仅支持获取文件连接器信息。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:GetConnector 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口具备幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

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
| sfm:GetConnector | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{WorkspaceId}/datacenter/connector HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 文件所属的业务空间 ID，获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace) | llm-3z7uw7fwz0vxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| ConnectorName | string | 否 | 查询的连接器名称，精确查询 | 连接器名称 |
| ConnectorId | string | 否 | 所属连接器 ID，请到[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/connector/list)获取 | conn\_file\_xxxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码</p></div></td><td><p>success</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口业务数据字段</p></div></td><td></td></tr><tr><td>ConnectorId</td><td><p>string</p></td><td><div><p>连接器 ID</p></div></td><td><p>conn_file_e0c9db4030b2465a9478028f7d76cd92_1234</p></td></tr><tr><td>ConnectorName</td><td><p>string</p></td><td><div><p>连接器名称</p></div></td><td><p>name</p></td></tr><tr><td>ConnectorType</td><td><p>string</p></td><td><div><p>连接器类型</p></div></td><td><p>FILE</p></td></tr><tr><td>Description</td><td><p>string</p></td><td><div><p>连接器描述</p></div></td><td><p>Description</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>Requests throttling triggered.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>Id of the request</p></div></td><td><p>7BA8ADD9-53D6-53F0-918F-A1E776AD230E</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功</p></li><li><p>false：失败</p></li></ul></div></td><td><p>True</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Code": "success",
  "Data": {
    "ConnectorId": "conn_file_e0c9db4030b2465a9478028f7d76cd92_1234",
    "ConnectorName": "name",
    "ConnectorType": "FILE",
    "Description": "Description"
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "7BA8ADD9-53D6-53F0-918F-A1E776AD230E",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/GetConnector#workbench-doc-change-demo)。
