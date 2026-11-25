# CreateDataset

数据源管理-创建。

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
| aimiaobi:CreateDataset | create | \*全部资源<br><br>`*` | 无 | 无 |

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

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>WorkspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>阿里云百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td><p>llm-xxx</p></td></tr><tr><td>DatasetType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据集类型：</p><ul><li><p>CustomSemanticSearch：自建语义索引（默认），用户上传文档构建数据集</p></li><li><p>ThirdSearch：三方搜索源（api），配置用户自己的搜索 api</p></li></ul></div></td><td><p>CustomSemanticSearch</p></td></tr><tr><td>DatasetName</td><td><p>string</p></td><td><p>是</p></td><td><div><p>数据集名称，全局唯一</p></div></td><td><p>businessDataset</p></td></tr><tr><td>DatasetDescription</td><td><p>string</p></td><td><p>否</p></td><td><div><p>数据集描述：控制台展示名称，建议传入业务可读的名称</p></div></td><td><p>企业知识库</p></td></tr><tr><td>SearchDatasetEnable</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>数据集搜索开关：</p><ul><li><p>0：全部关闭</p></li><li><p>1：仅妙搜可见</p></li><li><p>2：仅妙笔可见</p></li><li><p>3：妙搜&amp;妙笔均可见 （默认）</p></li></ul></div></td><td><p>3</p></td></tr><tr><td>DatasetConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>数据集搜索配置</p></div></td><td></td></tr><tr><td>SearchSourceConfigs</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>三方搜索：api 定义</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>三方搜索：api 定义</p></div></td><td></td></tr><tr><td>DemoQuery</td><td><p>string</p></td><td><p>否</p></td><td><div><p>可以搜索到的关键词，用来验证是否可用</p></div></td><td><p>可以搜索到的关键词，用来验证是否可用</p></td></tr><tr><td>Size</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>默认请求、响应数据条数限制</p></div></td><td><p>10</p></td></tr><tr><td>SearchSourceRequestConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>api 请求配置</p></div></td><td></td></tr><tr><td>Url</td><td><p>string</p></td><td><p>否</p></td><td><div><p>api 地址</p></div></td><td><p>api地址</p></td></tr><tr><td>Method</td><td><p>string</p></td><td><p>否</p></td><td><div><p>请求方式</p></div></td><td><p>请求方式</p></td></tr><tr><td>ConnectTimeout</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>连接超时时间：单位毫秒</p></div></td><td><p>3000</p></td></tr><tr><td>SocketTimeout</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>读超时时间：单位毫秒</p></div></td><td><p>3000</p></td></tr><tr><td>Headers</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>http 请求头</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>http 请求头</p></div></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数名称</p></div></td><td><p>参数名称</p></td></tr><tr><td>ValueType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数值数据类型：默认 string</p></div></td><td><p>参数值数据类型：默认string</p></td></tr><tr><td>ValueFormat</td><td><p>string</p></td><td><p>否</p></td><td><div><p>valueType = time 时有效</p></div></td><td><p>valueType = time 时有效</p></td></tr><tr><td>Value</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数值</p></div></td><td><p>参数值</p></td></tr><tr><td>Params</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>请求 path 参数</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Name</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数名称</p></div></td><td><p>参数名称</p></td></tr><tr><td>ValueType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数值数据类型：默认 string</p></div></td><td><p>参数值数据类型：默认string</p></td></tr><tr><td>ValueFormat</td><td><p>string</p></td><td><p>否</p></td><td><div><p>valueType = time 时有效</p></div></td><td><p>valueType = time 时有效</p></td></tr><tr><td>Value</td><td><p>string</p></td><td><p>否</p></td><td><div><p>参数值</p></div></td><td><p>参数值</p></td></tr><tr><td>PathParamsEnable</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否开启 pathParam</p></div></td><td><p>true</p></td></tr><tr><td>Body</td><td><p>string</p></td><td><p>否</p></td><td><div><p>请求 body</p></div></td><td><p>{}</p></td></tr><tr><td>SearchSourceResponseConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>api 响应配置</p></div></td><td></td></tr><tr><td>JqNodes</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>节点配置</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td></td><td></td></tr><tr><td>Key</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点 key</p></div></td><td><p>节点key</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点数据类型：string number list object base</p></div></td><td><p>节点数据类型：string number list object base</p></td></tr><tr><td>Path</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点路径</p></div></td><td><p>节点路径</p></td></tr><tr><td>JqNodes</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>子节点配置</p></div></td><td></td></tr><tr><td></td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>子节点配置</p></div></td><td></td></tr><tr><td>Key</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点 key</p></div></td><td><p>title</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><p>否</p></td><td><div><p>type 类型</p></div></td><td><p>string</p></td></tr><tr><td>Path</td><td><p>string</p></td><td><p>否</p></td><td><div><p>路径。</p></div></td><td><p>节点路径</p></td></tr><tr><td>JqNodes</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>子节点配置</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>子节点配置</p></div></td><td></td></tr><tr><td>Key</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点 key</p></div></td><td><p>title</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><p>否</p></td><td><div><p>type 类型</p></div></td><td><p>string</p></td></tr><tr><td>Path</td><td><p>string</p></td><td><p>否</p></td><td><div><p>节点路径</p></div></td><td><p>节点路径</p></td></tr><tr><td>SearchSourceConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>数据集配置项</p></div></td><td></td></tr><tr><td>TagSearchEnable</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>标签是否参与搜索：默认 true</p></div></td><td><p>true</p></td></tr><tr><td>TagGenerateEnable</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>标签是否参与生成：默认 true</p></div></td><td><p>true</p></td></tr><tr><td>MetadataKeyValueSearchEnable</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>metadata-keyValue 部分是否参与搜索：默认 true</p></div></td><td><p>true</p></td></tr><tr><td>MetadataKeyValueGenerateEnable</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>metadata-keyValue 部分是否参与生成：默认 true</p></div></td><td><p>true</p></td></tr><tr><td>DocumentHandleConfig</td><td><p>object</p></td><td><p>否</p></td><td><div><p>数据集索引配置</p></div></td><td></td></tr><tr><td>DisableHandleMultimodalMedia</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>禁用多媒体文件处理逻辑：</p><ul><li><p>true：禁用多模态（图片、视频）索引，仅索引和搜索文本</p></li><li><p>false：支持多模态（文本、图片、视频）索引，同时开通视频云并在系统管理中做了授权才正式生效，仅设置 false，这里识别到未授权会自动跳过图片、视频索引（默认）</p></li></ul></div></td><td><p>false</p></td></tr><tr><td>InvokeType</td><td><p>string</p></td><td><p>否</p></td><td><div><p>调用方式：目前仅支持值 portal，标识控制台调用。</p><ul><li><p>空时：当 DatasetType= ThirdSearch，datasetConfig.SearchSourceConfigs（三方 api 定义）必传。</p></li><li><p>portal 时：当 DatasetType= ThirdSearch，后台会默认初始化一个 SearchSourceConfigs（三方 apidemo）示例，供参考。</p></li></ul></div></td><td><p>portal</p></td></tr><tr><td>AccessLevel</td><td><p>string</p></td><td><p>否</p></td><td></td><td><p>private</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 响应结果 |  |
| Data | object | 业务数据 |  |
| DatasetId | integer | 数据集 ID | 1 |
| CreateUser | string | 创建者 | xxx |
| CreateTime | string | 创建时回见 | 2024-11-12 21:46:24 |
| DatasetType | string | 数据集类型 | CustomSemanticSearch |
| DatasetName | string | 数据集名称 | xxx |
| DatasetDescription | string | 数据集显示名称 | xxx |
| SearchDatasetEnable | integer | 数据集搜索开关 | 1 |
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

<a id="code-block-2"></a>

```json
{
  "Data": {
    "DatasetId": 1,
    "CreateUser": "xxx",
    "CreateTime": "2024-11-12 21:46:24",
    "DatasetType": "CustomSemanticSearch",
    "DatasetName": "xxx",
    "DatasetDescription": "xxx",
    "SearchDatasetEnable": 1
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/CreateDataset#workbench-doc-change-demo)。
