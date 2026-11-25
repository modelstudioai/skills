# AddDatasetDocument

添加文档到数据源。

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
| aimiaobi:AddDatasetDocument | create | \*全部资源<br><br>`*` | 无 | 无 |

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

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td><p>llm-xx</p></td></tr><tr><td>DatasetId</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>数据集唯一标识</p></div></td><td><p>1</p></td></tr><tr><td>DatasetName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据集名称</p></div></td><td><p>数据集名称</p></td></tr><tr><td>Document</td><td><p>object</p></td><td><p>是</p></td><td><div><p>文档</p></div></td><td></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档系统唯一 ID：自动生成，不建议传入</p></div></td><td><p>xxxx</p></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章 URL：公网可访问地址</p></div></td><td><p>http://xxx</p></td></tr><tr><td>Content</td><td><p>string</p></td><td><p>否</p></td><td><div><p>内容</p></div></td><td><p>正文</p></td></tr><tr><td>Summary</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文章摘要</p></div></td><td><p>文章摘要</p></td></tr><tr><td>Title</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档标题</p></div></td><td><p>标题</p></td></tr><tr><td>PubTime</td><td><p>string</p></td><td><p>否</p></td><td><div><p>发布时间</p></div></td><td><p>2024-12-09 13:35:40</p></td></tr><tr><td>SourceFrom</td><td><p>string</p></td><td><p>否</p></td><td><div><p>来源</p></div></td><td><p>xxx媒体</p></td></tr><tr><td>MultimodalIndexName</td><td><p>string</p></td><td><p>否</p></td><td><div><p>废弃：不可用</p></div></td><td><p>xxxx</p></td></tr><tr><td>DisableHandleMultimodalMedia</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>当前记录多模态数据（图片、视频）是否落索引库，默认 true</p></div></td><td><p>false</p></td></tr><tr><td>MultimodalMedias</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>文档中多模态数据列表：</p><ul><li><p>仅富文本等文档中存在多模态数据（图片、视频）时，可以通过这个字段传入，进而可以在搜索接口召回对应数据。</p></li><li><p>文档本身为多模态数据时，此字段为空，通过 docType+url 指定数据即可。</p></li></ul></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>多模态数据</p></div></td><td></td></tr><tr><td>MediaId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>多模态数据唯一标识：不建议传入，系统会自动生成</p></div></td><td><p>xxxx</p></td></tr><tr><td>MediaType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>多模态数据类型：</p><ul><li><p>image：图片</p></li><li><p>video：视频</p></li></ul></div></td><td><p>image</p></td></tr><tr><td>FileUrl</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文件地址：公网可访问</p></div></td><td><p>http://xxx</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档业务侧唯一 ID</p></div></td><td><p>xx</p></td></tr><tr><td>DocType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文档类型：</p><ul><li><p>plainText：纯文本，content 必选</p></li><li><p>richText：富文本：html，content 必选</p></li><li><p>text：文本文件，url 必选</p></li><li><p>pdf：url 必选</p></li><li><p>word：url 必选</p></li><li><p>image：图片，url 必选，支持 gif、png、jpg、jpeg 等大多数常见图片格式</p></li><li><p>video：视频，url 必选，支持 MP4、AVI、WMV、MOV 等大多数常见视频格式</p></li></ul></div></td><td><p>image</p></td></tr><tr><td>Extend1</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 1</p></div></td><td><p>xxx</p></td></tr><tr><td>Extend2</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 2</p></div></td><td><p>xxxx</p></td></tr><tr><td>Extend3</td><td><p>string</p></td><td><p>否</p></td><td><div><p>扩展字段 3</p></div></td><td><p>xxx</p></td></tr><tr><td>Metadata</td><td><p>object</p></td><td><p>否</p></td><td><div><p>meta 信息</p></div></td><td></td></tr><tr><td>VideoShots</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>分镜信息</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>分镜信息</p></div></td><td></td></tr><tr><td>StartTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>开始时间；毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>EndTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>结束时间：毫秒</p></div></td><td><p>2000</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><p>否</p></td><td><div><p>分镜分析文本信息</p></div></td><td><p>xxx</p></td></tr><tr><td>AsrSentences</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>语音或者字幕信息</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>语音或者字幕信息</p></div></td><td></td></tr><tr><td>StartTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>开始时间：毫秒</p></div></td><td><p>1000</p></td></tr><tr><td>EndTime</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>技术时间：毫秒</p></div></td><td><p>2000</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><p>否</p></td><td><div><p>语音或者字幕信息</p></div></td><td><p>xxx</p></td></tr><tr><td>Text</td><td><p>string</p></td><td><p>否</p></td><td><div><p>meta 描述信息：废弃字段</p></div></td><td><p>xxx</p></td></tr><tr><td>KeyValues</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>keyValue 结构 metadata</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>keyValue 结构 metadata</p></div></td><td></td></tr><tr><td>Key</td><td><p>string</p></td><td><p>否</p></td><td><div><p>名称</p></div></td><td><p>xx</p></td></tr><tr><td>Value</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数值</p></div></td><td><p>xx</p></td></tr><tr><td>CategoryUuid</td><td><p>string</p></td><td><p>否</p></td><td><div><p>类目唯一标识</p></div></td><td><p>xx</p></td></tr><tr><td>Tags</td><td><p>array</p></td><td><p>否</p></td><td><div><p>标签名称</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>标签名称</p></div></td><td><p>xx</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>响应结果</p></div></td><td></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>业务数据</p></div></td><td></td></tr><tr><td>DocUuid</td><td><p>string</p></td><td><div><p>文档系统唯一标识</p></div></td><td><p>8df2d69d63a247b6b52ff455b2d426b6</p></td></tr><tr><td>DocId</td><td><p>string</p></td><td><div><p>文档业务侧唯一标识</p></div></td><td><p>xxx</p></td></tr><tr><td>Status</td><td><p>integer</p></td><td><div><p>状态：</p><ul><li><p>1：创建完成</p></li><li><p>2：文本索引构建完成</p></li><li><p>3：多模态索引构建完成</p></li><li><p>100：全量构建完成</p></li><li><p>0：失败</p></li></ul></div></td><td><p>1</p></td></tr><tr><td>ErrorCode</td><td><p>string</p></td><td><div><p>异常错误码</p></div></td><td><p>Success</p></td></tr><tr><td>ErrorMessage</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>错误信息</p></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求唯一标识</p></div></td><td><p>1813ceee-7fe5-41b4-87e5-982a4d18cca5</p></td></tr><tr><td>Success</td><td><p>boolean</p></td><td><div><p>是否成功：true 成功，false 失败</p></div></td><td><p>true</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>状态码</p></div></td><td><p>NoData</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误说明</p></div></td><td><p>success</p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "Data": {
    "DocUuid": "8df2d69d63a247b6b52ff455b2d426b6",
    "DocId": "xxx",
    "Status": 1,
    "ErrorCode": "Success",
    "ErrorMessage": "错误信息"
  },
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/AddDatasetDocument#workbench-doc-change-demo)。
