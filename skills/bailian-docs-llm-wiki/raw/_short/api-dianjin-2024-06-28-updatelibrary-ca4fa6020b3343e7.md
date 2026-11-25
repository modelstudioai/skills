# UpdateLibrary - 更新文档库

更新文档库，可用于更新文档库的名称、描述、索引配置等信息。

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/UpdateLibrary)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:UpdateLibrary</td><td>update</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
PUT /{workspaceId}/api/library/update HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>业务空间 id</p></div></td><td>llm-xxxxx</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求体参数。</p></div></td><td></td></tr><tr><td>description</td><td>string</td><td>否</td><td><div><p>文档库描述</p></div></td><td>文档库描述</td></tr><tr><td>indexSetting</td><td>object</td><td>否</td><td><div><p>文档库索引配置</p></div></td><td></td></tr><tr><td>chunkStrategy</td><td>object</td><td>否</td><td><div><p>分块策略</p></div></td><td></td></tr><tr><td>docTreeSplit</td><td>boolean</td><td>否</td><td><div><p>版面切分</p></div></td><td>true</td></tr><tr><td>docTreeSplitSize</td><td>integer</td><td>否</td><td><div><p>版面切分大小</p></div></td><td>160</td></tr><tr><td>enhanceGraph</td><td>boolean</td><td>否</td><td><div><p>是否增强图片</p></div></td><td>true</td></tr><tr><td>enhanceTable</td><td>boolean</td><td>否</td><td><div><p>是否增强表格</p></div></td><td>true</td></tr><tr><td>overlap</td><td>integer</td><td>否</td><td><div><p>chunk 重叠长度</p></div></td><td>20</td></tr><tr><td>sentenceSplit</td><td>boolean</td><td>否</td><td><div><p>是否按照句子切分：默认为 true</p></div></td><td>true</td></tr><tr><td>sentenceSplitSize</td><td>integer</td><td>否</td><td><div><p>按照句子切分的平均长度</p></div></td><td>160</td></tr><tr><td>size</td><td>integer</td><td>否</td><td><div><p>定长切分的 chunk 长度</p></div></td><td>256</td></tr><tr><td>split</td><td>boolean</td><td>否</td><td><div><p>是否切块</p></div></td><td>true</td></tr><tr><td>modelConfig</td><td>object</td><td>否</td><td><div><p>模型配置</p></div></td><td></td></tr><tr><td>temperature</td><td>double</td><td>否</td><td><div><p>温度</p></div></td><td>0.8</td></tr><tr><td>topP</td><td>double</td><td>否</td><td><div><p>topP</p></div></td><td>0.8</td></tr><tr><td>promptRoleStyle</td><td>string</td><td>否</td><td><div><p>prompt 角色风格</p></div></td><td>你是一位文档分析专家，非常善于从给定的知识中，找到重点，像老师给学生讲课一样把问题回答清晰。你的回答富有逻辑性，遇到复杂问题，你善于一步一步思考。</td></tr><tr><td>queryEnhancer</td><td>object</td><td>否</td><td><div><p>query 增强</p></div></td><td></td></tr><tr><td>enableFollowUp</td><td>boolean</td><td>否</td><td><div><p>多轮增强</p></div></td><td>true</td></tr><tr><td>enableMultiQuery</td><td>boolean</td><td>否</td><td><div><p>是否利用大模型知识拆解问题</p></div></td><td>true</td></tr><tr><td>enableOpenQa</td><td>boolean</td><td>否</td><td><div><p>是否利用大模型知识回答问题</p></div></td><td>true</td></tr><tr><td>enableQueryRewrite</td><td>boolean</td><td>否</td><td><div><p>是否根据领域知识改写问题</p></div></td><td>true</td></tr><tr><td>enableSession</td><td>boolean</td><td>否</td><td><div><p>记录 session</p></div></td><td>true</td></tr><tr><td>localKnowledgeId</td><td>string</td><td>否</td><td><div><p>知识改写使用的文档库 id</p></div></td><td>sjdhgfc</td></tr><tr><td>withDocumentReference</td><td>boolean</td><td>否</td><td><div><p>是否带文档引用</p></div></td><td>true</td></tr><tr><td>recallStrategy</td><td>object</td><td>否</td><td><div><p>召回策略</p></div></td><td></td></tr><tr><td>documentRankType</td><td>string</td><td>否</td><td><div><p>合并&amp;排序策略</p></div><div><div>枚举值：</div><ul><li>model：使用BGE进行排序。</li><li>llm：使用大模型进行排序。</li></ul></div></td><td>model</td></tr><tr><td>limit</td><td>integer</td><td>否</td><td><div><p>两路合并总结的结果数</p></div></td><td>10</td></tr><tr><td>textIndexSetting</td><td>object</td><td>否</td><td><div><p>文本索引设置</p></div></td><td></td></tr><tr><td>category</td><td>string</td><td>否</td><td><div><p>文本索引类型</p></div></td><td>ElasticSearch</td></tr><tr><td>enable</td><td>boolean</td><td>否</td><td><div><p>文本索引是否开启</p></div></td><td>true</td></tr><tr><td>indexAnalyzer</td><td>string</td><td>否</td><td><div><p>文本索引的索引分析器: (Standard, IkMaxWord, IkSmart)</p></div></td><td>Standard</td></tr><tr><td>rankThreshold</td><td>double</td><td>否</td><td><div><p>文本索引排序阈值</p></div></td><td>0.5</td></tr><tr><td>searchAnalyzer</td><td>string</td><td>否</td><td><div><p>文本索引的搜索分析器: (Standard, IkMaxWord, IkSmart)</p></div></td><td>Standard</td></tr><tr><td>topK</td><td>integer</td><td>否</td><td><div><p>文本索引最后总结结果数</p></div></td><td>50</td></tr><tr><td>vectorIndexSetting</td><td>object</td><td>否</td><td><div><p>向量索引设置</p></div></td><td></td></tr><tr><td>category</td><td>string</td><td>否</td><td><div><p>向量索引来源：建议填写 ADB</p></div></td><td>ADB</td></tr><tr><td>embeddingType</td><td>string</td><td>否</td><td><div><p>向量索引文本 Embedding 模型</p></div></td><td>DashScope</td></tr><tr><td>enable</td><td>boolean</td><td>否</td><td><div><p>是否开启</p></div></td><td>true</td></tr><tr><td>rankThreshold</td><td>double</td><td>否</td><td><div><p>向量索引排序阈值</p></div></td><td>0.5</td></tr><tr><td>topK</td><td>integer</td><td>否</td><td><div><p>向量索引最后总结结果数</p></div></td><td>10</td></tr><tr><td>libraryId</td><td>string</td><td>是</td><td><div><p>文档库 id</p></div></td><td>dsfbashdbb</td></tr><tr><td>libraryName</td><td>string</td><td>否</td><td><div><p>文档库名称</p></div></td><td>测试文档库</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | ResultCode |  |
| cost | long | 耗时 | null |
| data | string | 响应数据 | null |
| dataType | string | 数据类型 | null |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| requestId | string | 请求 id | eb2b6139-ddf1-91a0-a47f-df7617ae9032 |
| success | boolean | 是否成功 | true |
| time | string | 时间戳 | 2024-04-24 11:54:34 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```text
{
  "cost": 0,
  "data": null,
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "eb2b6139-ddf1-91a0-a47f-df7617ae9032",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。
