# UpdateIndex - 更新知识库

更新指定知识库的部分配置。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](../model-user-guide/security-and-compliance/permission-management-overview.md)（需要`AliyunBailianDataFullAccess`），并加入一个业务空间后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID `Id` 有效）。
-   本接口具有幂等性。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/bailian/2023-12-29/UpdateIndex)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>sfm:UpdateIndex</td><td>update</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{WorkspaceId}/index/update HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p>业务空间 ID</p></div></td><td>llm-3shx2gu255oqxxxx</td></tr><tr><td>Id</td><td>string</td><td>是</td><td><div><p>知识库 ID</p></div></td><td>79c0alxxxx</td></tr><tr><td>Name</td><td>string</td><td>否</td><td><div><p>知识库名称</p></div></td><td>企业帮助文档库</td></tr><tr><td>Description</td><td>string</td><td>否</td><td><div><p>知识库描述</p></div></td><td>企业知识库</td></tr><tr><td>RerankMinScore</td><td>string</td><td>否</td><td><div><p>排序最低分数，取值范围[0-1]</p></div></td><td>0.01</td></tr><tr><td>DenseSimilarityTopK</td><td>integer</td><td>否</td><td><div><p>向量检索 Top K，通过生成输入文本的向量并在知识库中检索与其向量表示最相似的 K 个文本切片。K 的取值范围[0-100]。 <code>DenseSimilarityTopK</code>和<code>SparseSimilarityTopK</code>二者之和小于等于 200。</p><p>默认值为 100。</p></div></td><td>100</td></tr><tr><td>SparseSimilarityTopK</td><td>integer</td><td>否</td><td><div><p>关键词检索 TopK，即在知识库中查找与输入文本的关键词精确匹配的切片。它可以帮助您过滤掉无关的文本切片，提供更准确的结果。 取值范围[0-100]。 <code>DenseSimilarityTopK</code>和<code>SparseSimilarityTopK</code>二者之和小于等于 200。</p><p>默认值为：100。</p></div></td><td>100</td></tr><tr><td>PipelineCommercialType</td><td>string</td><td>否</td><td><div><p>知识库的规格类型。取值范围：</p><ul><li><p>standard：标准版</p></li><li><p>enterprise：旗舰版</p></li></ul></div></td><td>standard</td></tr><tr><td>PipelineCommercialCu</td><td>integer</td><td>否</td><td><div><p>指定旗舰版知识库的 RCU 数量，即仅当 pipelineCommercialType 指定 enterprise 时才需要传入。</p><p>取值范围：[1-200]。</p></div></td><td>3</td></tr></tbody></table>

参数 Name，Description，RerankMinScore ，至少填写一项，不能同时为空。

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | 请求 ID | 17204B98-7734-4F9A-8464-xxx |
| Data | object | 接口业务数据字段 |  |
| Id | string | 知识库 ID | 79c0alxxxx |
| Status | string | 接口返回的状态码 | 200 |
| Success | boolean | 接口调用是否成功，可能值为：<br><br>true：成功<br><br>false：失败 | true |
| Message | string | 错误信息 | Required parameter(%s) missing or invalid, please check the request parameters. |
| Code | string | 状态码 | Success |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "RequestId": "17204B98-7734-4F9A-8464-xxx",
  "Data": {
    "Id": "79c0alxxxx"
  },
  "Status": 200,
  "Success": true,
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Code": "Success"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |
| 2026-01-19 | 新增 OpenAPI | [查看变更详情](https://api.aliyun.com/document/bailian/2023-12-29/UpdateIndex?updateTime=2026-01-19#workbench-doc-change-demo) |
