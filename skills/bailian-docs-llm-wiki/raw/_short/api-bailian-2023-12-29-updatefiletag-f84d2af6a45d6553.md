# UpdateFileTag

更新指定文件标签。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:UpdateFileTag 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。

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
| sfm:UpdateFileTag | update | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
PUT /{WorkspaceId}/datacenter/file/{FileId} HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 文件所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3z7uw7fwz0vxxxx |
| FileId | string | 是 | 数据中心的文件 ID，您可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)页面，单击文件名称旁的 ID 图标获取。 | file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>Tags</td><td><p>array</p></td><td><p>是</p></td><td><div><ul><li><p>文件关联的标签列表。最多传入 100 个标签，所有标签字符长度总和不能超过 700。</p></li></ul></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签值，每个标签最多 32 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等），下划线_，中划线-，标签中不能包含空格。</p></div></td><td><p>标签A</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码</p></div></td><td><p>Success</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>返回内容</p></div></td><td></td></tr><tr><td>FileId</td><td><p>string</p></td><td><div><p>文件 ID</p></div></td><td><p>file_9a65732555b54d5ea10796ca5742ba22_xxxxxxxx</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>Requests throttling triggered.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>35A267BF-xxxx-54DB-8394-AA3B0742D833</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr></tbody></table>

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
    "FileId": "file_9a65732555b54d5ea10796ca5742ba22_xxxxxxxx"
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/UpdateFileTag#workbench-doc-change-demo)。
