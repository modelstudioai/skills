# CreateQualityCheckTask - 创建质检任务

创建质检任务。

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

[调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreateQualityCheckTask)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>dianjin:CreateQualityCheckTask</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /{workspaceId}/api/qualitycheck/task/submit HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>workspaceId</td><td>string</td><td>是</td><td><div><p>业务空间 id</p></div></td><td>llm-xxxx</td></tr><tr><td>body</td><td>object</td><td>否</td><td><div><p>请求体。</p></div></td><td></td></tr><tr><td>conversationList</td><td>object</td><td>是</td><td><div><p>会话内容，关联质检场景需要传入多个会话，否则只有一个会话</p></div></td><td></td></tr><tr><td>callType</td><td>string</td><td>否</td><td><div><p>呼叫类型:</p></div><div><div>枚举值：</div><ul><li>1：呼入。</li><li>2：呼出。</li></ul></div></td><td>1</td></tr><tr><td>customerId</td><td>string</td><td>否</td><td><div><p>客户 ID</p></div></td><td>1</td></tr><tr><td>customerName</td><td>string</td><td>否</td><td><div><p>客户名称</p></div></td><td>张三</td></tr><tr><td>customerServiceId</td><td>string</td><td>否</td><td><div><p>客服 ID</p></div></td><td>xxx</td></tr><tr><td>customerServiceName</td><td>string</td><td>否</td><td><div><p>客服名称</p></div></td><td>李四</td></tr><tr><td>dialogueList</td><td>array&lt;object&gt;</td><td>是</td><td><div><p>对话明细列表</p></div></td><td></td></tr><tr><td>dialogueList</td><td>object</td><td>否</td><td><div><p>对话明细</p></div></td><td></td></tr><tr><td>begin</td><td>integer</td><td>否</td><td><div><p>本句话的开始时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>beginTime</td><td>string</td><td>否</td><td><div><p>这句话的开始时间</p></div></td><td>2024-05-23 14:57:50</td></tr><tr><td>content</td><td>string</td><td>是</td><td><div><p>对话的具体内容</p></div></td><td>您好，我是2001，很高兴为您服务！</td></tr><tr><td>customerId</td><td>string</td><td>否</td><td><div><p>对话角色的唯一标识</p></div></td><td>2348234</td></tr><tr><td>customerServiceId</td><td>string</td><td>否</td><td><div><p>客服 ID</p></div></td><td>23874627346</td></tr><tr><td>customerServiceType</td><td>string</td><td>否</td><td><div><p>坐席类型</p></div><div><div>枚举值：</div><ul><li>0：机器人。</li><li>1：人工。</li></ul></div></td><td>0</td></tr><tr><td>end</td><td>integer</td><td>否</td><td><div><p>本句话的结束时间，相对于会话开始点的偏移时间 ms</p></div></td><td>0</td></tr><tr><td>role</td><td>string</td><td>是</td><td><div><p>角色</p></div><div><div>枚举值：</div><ul><li>0：客户。</li><li>1：坐席。</li></ul></div></td><td>1</td></tr><tr><td>type</td><td>string</td><td>是</td><td><div><p>对话内容的类型</p></div><div><div>枚举值：</div><ul><li>IMAGE：图片。</li><li>TEXT：文本。</li><li>AUDIO：语音。</li></ul></div></td><td>TEXT</td></tr><tr><td>gmtService</td><td>string</td><td>否</td><td><div><p>会话时间</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>gmtService</td><td>string</td><td>是</td><td><div><p>业务发生时间，用于系统记录提交时间，任务调度优先级决策等</p></div></td><td>2024-09-27 11:23:20</td></tr><tr><td>metaData</td><td>object</td><td>否</td><td><div><p>元数据，用于规则执行过程中需要消费的一些业务相关的属性，由业务系统在发起质检的时候实时传入。</p></div></td><td></td></tr><tr><td></td><td>string</td><td>否</td><td><div><p>元数据</p></div></td><td>{ &quot;isSpecialArchive&quot;: false, &quot;hasProcessingWorkOrder&quot;: false, &quot;primaryArchiveType&quot;: &quot;其他&quot;, &quot;businessType&quot;: &quot;预警&quot;, &quot;workOrderActionType&quot;:&quot;业务升级&quot; }</td></tr><tr><td>qualityGroup</td><td>array</td><td>否</td><td><div><p>质检规则组</p></div></td><td></td></tr><tr><td>qualityGroup</td><td>string</td><td>否</td><td><div><p>质检规则</p></div></td><td>warning_customers</td></tr><tr><td>requestId</td><td>string</td><td>是</td><td><div><p>请求 ID</p></div></td><td>0FC6636E-380A-5369-AE01-D1C15BB9B254</td></tr><tr><td>type</td><td>string</td><td>是</td><td><div><p>质检类型</p></div><div><div>枚举值：</div><ul><li>0：离线文本会话质检。</li></ul></div></td><td>0</td></tr><tr><td>sceneCode</td><td>string</td><td>否</td><td><div><p>场景编码。</p></div></td><td>o9c8u8</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | ResultCode |  |
| cost | long | 耗时 | null |
| data | object | 响应数据 |  |
| taskId | string | taskId | 172373500521 |
| dataType | string | 数据类型 | null |
| errCode | string | 错误码 | 0 |
| message | string | 错误信息 | ok |
| requestId | string | 请求 id | EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258 |
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
  "data": {
    "taskId": 172373500521
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "EF4B5C9B-3BC8-5171-A47B-4C5CF3DC3258",
  "success": true,
  "time": "2024-04-24 11:54:34"
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
| 2025-12-11 | API 内部配置变更，不影响调用 | [查看变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/CreateQualityCheckTask?updateTime=2025-12-11#workbench-doc-change-demo) |
