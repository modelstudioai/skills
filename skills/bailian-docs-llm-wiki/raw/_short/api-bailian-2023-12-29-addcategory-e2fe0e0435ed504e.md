# AddCategory

在指定的业务空间中创建一个类目，用于分类和管理文件。每个业务空间最多创建500个类目。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   不支持通过 API 新增数据表，请通过控制台的[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)操作。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:AddCategory 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口不具备幂等性。

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
| sfm:AddCategory | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/datacenter/category/ HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 业务空间 ID，即在该业务空间中新增类目。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。 | llm-3z7uw7fwz0vxxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>CategoryName</td><td><p>string</p></td><td><p>是</p></td><td><div><p>类目名称。长度为 1~20 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等）。可以包含半角冒号（:）、下划线（_）、半角句号（.）或者短划线（-）。</p></div></td><td><p>产品清单</p></td></tr><tr><td>CategoryType</td><td><p>string</p></td><td><p>是</p></td><td><div><p>类目类型。取值范围：</p><ul><li><p>UNSTRUCTURED：类目。</p></li></ul></div></td><td><p>UNSTRUCTURED</p></td></tr><tr><td>ParentCategoryId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>父类目的类目 ID。在此父类目下创建新类目，此值为空时创建一级类目。</p></div></td><td><p>cate_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx</p></td></tr><tr><td>ConnectorId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>所属数据连接（Connector）的实例 id，请到百炼控制台获取。</p></div></td><td><p>conn_xxxx</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码。</p></div></td><td><p>success</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>接口业务数据字段。</p></div></td><td></td></tr><tr><td>CategoryId</td><td><p>string</p></td><td><div><p>类目 ID。请妥善保管该值，它将用于后续所有与此类目相关的 API 操作。</p></div></td><td><p>cate_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx</p></td></tr><tr><td>CategoryName</td><td><p>string</p></td><td><div><p>类目名称。</p></div></td><td><p>类目名称</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息。</p></div></td><td><p>Requests throttling triggered.</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID。</p></div></td><td><p>778C0B3B-xxxx-5FC1-A947-36EDD13606AB</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码。</p></div></td><td><p>200</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功，可能值为：</p><ul><li><p>true：成功。</p></li><li><p>false：失败。</p></li></ul></div></td><td><p>true</p></td></tr></tbody></table>

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
    "CategoryId": "cate_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx",
    "CategoryName": "类目名称"
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddCategory#workbench-doc-change-demo)。
