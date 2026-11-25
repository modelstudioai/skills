# CreateDialogAnalysisTask - 创建会话分析任务

创建会话分析任务，创建成功后可根据会话ID使用GetDialogAnalysisResult查询结果

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateDialogAnalysisTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:CreateDialogAnalysisTask</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/virtualHuman/dialog/analysis/submit HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p>名称</p></th><th><p>类型</p></th><th><p>必填</p></th><th><p>描述</p></th><th><p>示例值</p></th></tr></thead><tbody><tr><td><p>workspaceId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>业务空间 id</p></td><td><p>llm-xxxxx</p></td></tr><tr><td><p>body</p></td><td><p>object</p></td><td><p>否</p></td><td><p>请求体。</p></td><td></td></tr><tr><td><p>metaData</p></td><td><p>object</p></td><td><p>否</p></td><td><p>元数据，用于会话分析过程中需要消费的一些业务相关的属性，由业务系统在发起会话分析任务的时候实时传入。</p><a id="code-block-2"></a><pre class="language-text"><code>{
  &quot;labels&quot;: &quot;XXX&quot;,  // 标签
  &quot;summaryConstraints&quot;: &quot;XXX&quot;,   // 摘要维度
  &quot;sopInfo&quot;: &quot;XXX&quot;  // SOP 信息
}
</code></pre></td><td><p>{ &quot;labels&quot;: &quot;XXX&quot;, &quot;summaryConstraints&quot;: &quot;XXX&quot;, &quot;sopInfo&quot;: &quot;XXX&quot; }</p></td></tr><tr><td><p>playCode</p></td><td><p>string</p></td><td><p>是</p></td><td><p>会话场景编码，关联会话分析配置</p></td><td><p>common</p></td></tr><tr><td><p>analysisNodes</p></td><td><p>array</p></td><td><p>否</p></td><td><p>分析节点列表，默认为空，表示全部节点。可传入一个或者多个。</p></td><td></td></tr><tr><td><p>analysisNode</p></td><td><p>string</p></td><td><p>否</p></td><td><p>分析节点</p><p>枚举值：</p><ul><li>DIALOG_EXECUTION_PLAN：执行计划。</li><li>DIALOG_SUMMARY：会话小结。</li><li>DIALOG_SOP：会话SOP。</li><li>DIALOG_LABEL：会话标签。</li></ul></td><td><p>DIALOG_LABEL</p></td></tr><tr><td><p>requestId</p></td><td><p>string</p></td><td><p>是</p></td><td><p>请求 ID</p></td><td><p>0FC6636E-380A-5369-AE01-D1C15BB9B254</p></td></tr><tr><td><p>conversationList</p></td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><p>会话内容，可传入多个会话。</p></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>会话内容</p></td><td></td></tr><tr><td><p>dialogueList</p></td><td><p>array&lt;object&gt;</p></td><td><p>是</p></td><td><p>对话列表</p></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><p>对话</p></td><td></td></tr><tr><td><p>content</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话的具体内容</p></td><td><p>您好，我是2001，很高兴为您服务！</p></td></tr><tr><td><p>role</p></td><td><p>string</p></td><td><p>是</p></td><td><p>角色（0: 客户；1: 坐席）</p></td><td><p>1</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | ResultCode<List<br><br>\> |  |
| success | boolean | 是否成功 | true |
| dataType | string | 数据类型 | null |
| time | string | 时间戳 | 2024-04-24 11:54:34 |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| data | array | 响应数据，返回会话 ID 列表。 |  |
| data | string | 会话 ID | 1876540295480209409 |
| requestId | string | 请求 id | EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258 |
| cost | long | 耗时 | null |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-3"></a>

```text
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": [
    1876540295480209400
  ],
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
  "cost": 0
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |

暂无变更历史
