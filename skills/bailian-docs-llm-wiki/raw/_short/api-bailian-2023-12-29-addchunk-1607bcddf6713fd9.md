# AddChunk - 新增切片

使用此API可为文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库添加切片。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

-   对于文档搜索类（document）、数据查询类（table）、图片问答类（image）知识库，本接口可向指定知识库中添加切片内容；目前尚不支持对音视频搜索类（multimedia）知识库进行相关操作。仅当数据源为表格连接器(excel)时，对数据查询与图片问答类型知识库的操作方可生效。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ChunkList 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
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
POST /{WorkspaceId}/chunk/create HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 是 | 工作区标识 | llm-19hxxxxx7htdf9lh |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>PipelineId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>知识库 id</p></div></td><td><p>79c0alxxxx</p></td></tr><tr><td>dataId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文件 id</p></div></td><td><p>doc_xxx</p></td></tr><tr><td>field</td><td><p>object</p></td><td><p>否</p></td><td><div><p>插入的切片内容信息，以键值对形式传入。文档搜索类知识库使用固定 key 列表：</p><ul><li><p>content（<strong>String</strong>）：<strong>必填</strong>，切片正文内容</p></li><li><p>title（<strong>String</strong>）<strong>选填</strong>，切片标题</p></li><li><p>image_urls（<strong>Array</strong>）：<strong>选填</strong>，切片包含的图片链接，最多 10 张</p></li></ul><p>数据查询类、图片问答类知识库 key 不固定，由该知识库的数据源表格决定：key 为 Excel 列标题，value 为对应列的值。</p></div></td><td><p>{ &quot;content&quot;: &quot;The Bailian platform supports parsing multiple document formats including PDF, Word, and PPT.&quot;, &quot;title&quot;: &quot;Document Parsing and Chunking&quot;, &quot;image_urls&quot;: [ &quot;<a href="https://example.com/images/chunk-flow.png">https://example.com/images/chunk-flow.png</a>&quot;, &quot;<a href="https://example.com/images/parsing-result.png">https://example.com/images/parsing-result.png</a>&quot; ] }</p></td></tr><tr><td></td><td><p>any</p></td><td><p>否</p></td><td><div><p>插入切片的表头字段信息，仅数据查询类与图片问答类知识库支持。需要参与检索或参与回复的表头为必填。各类型取值要求：</p><ul><li><p><strong>String 类型</strong> ：最大长度 6000</p></li><li><p><strong>时间 类型</strong>：13 位时间戳（毫秒）</p></li><li><p><strong>Long 类型</strong>：整数，最大 2147483647</p></li><li><p><strong>Double 类型</strong>：支持小数</p></li><li><p><strong>image_url 类型</strong>：最多 5 张，多张用英文逗号拼接为一个字符串</p></li></ul></div></td><td><p>{&quot;Product Name&quot;: &quot;Wireless Bluetooth Headphones&quot;, &quot;Publish Time&quot;: 1752624000000, &quot;Stock Quantity&quot;: 1580, &quot;Unit Price&quot;: 299.99, &quot;image_url&quot;:&quot;<a href="https://example.com/images/headphones-front.jpg,https://example.com/images/headphones-side.jpg,https://example.com/images/headphones-package.jpg">https://example.com/images/headphones-front.jpg,https://example.com/images/headphones-side.jpg,https://example.com/images/headphones-package.jpg</a>&quot; }</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 id</p></div></td><td><p>35A267BF-xxxx-54DB-8394-AA3B0742D833</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>错误状态码</p></div></td><td><p>Index.InvalidParameter</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>Required parameter(%s) missing or invalid, please check the request parameters.</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>接口调用是否成功</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>true</p></div></li><li>false :<div><p>false</p></div></li></ul></div></td><td><p>true</p></td></tr><tr><td>Data</td><td><p>boolean</p></td><td><div><p>请求成功返回的业务数据</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>true</p></div></li><li>false :<div><p>false</p></div></li></ul></div></td><td><p>true</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>接口返回的状态码</p></div></td><td><p>200</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Data": true,
  "Status": "200"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/AddChunk#workbench-doc-change-demo)。
