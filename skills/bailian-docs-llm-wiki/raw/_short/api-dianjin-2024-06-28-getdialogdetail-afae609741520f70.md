# GetDialogDetail

获取会话详情信息。

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
| dianjin:GetDialogDetail | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
GET /{workspaceId}/api/virtualHuman/dialog/detail HTTP/1.1
```

<a id="路径参数"></a>

<a id="api-doc-request-path-parameters"></a>

## 路径参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| workspaceId | string | 是 | 业务空间 Id | llm-xxxx |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| sessionId | string | 是 | 会话 ID | 1906623923815534xxx |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>ResultCode</p></div></td><td></td></tr><tr><td>success</td><td><p>boolean</p></td><td><div><p>是否成功</p></div></td><td><p>true</p></td></tr><tr><td>dataType</td><td><p>string</p></td><td><div><p>数据类型</p></div></td><td><p>null</p></td></tr><tr><td>time</td><td><p>string</p></td><td><div><p>时间戳</p></div></td><td><p>2024-04-24 11:54:34</p></td></tr><tr><td>errCode</td><td><p>string</p></td><td><div><p>错误码</p></div></td><td><p>0</p></td></tr><tr><td>message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>ok</p></td></tr><tr><td>data</td><td><p>object</p></td><td><div><p>响应数据</p></div></td><td></td></tr><tr><td>totalDialogTurns</td><td><p>integer</p></td><td><div><p>总对话轮次。总交互轮次按 AI 与客户的对话次数计算，AI 或客户的连续多句算作一轮。最后一句若由 AI 说出且非挂机，则整体轮次减 1。</p></div></td><td><p>10</p></td></tr><tr><td>validDialogTurns</td><td><p>integer</p></td><td><div><p>有效对话轮次。 AI、客户一问一答算一轮的，有效交互轮次指一问一答算一次，不同于总轮次的统计方式。</p></div></td><td><p>5</p></td></tr><tr><td>dialogueList</td><td><p>array&lt;object&gt;</p></td><td><div><p>对话明细列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>对话明细</p></div></td><td></td></tr><tr><td>role</td><td><p>string</p></td><td><div><p>角色：</p><ul><li><p>0：客户</p></li><li><p>1：坐席</p></li></ul></div></td><td><p>0</p></td></tr><tr><td>customerServiceType</td><td><p>string</p></td><td><div><p>坐席类型：</p><ul><li><p>0: 机器人</p></li><li><p>1: 人工</p></li></ul></div></td><td><p>0</p></td></tr><tr><td>customerServiceId</td><td><p>string</p></td><td><div><p>客服 ID</p></div></td><td><p>BOT</p></td></tr><tr><td>customerId</td><td><p>string</p></td><td><div><p>客户 ID</p></div></td><td><p>123761283</p></td></tr><tr><td>content</td><td><p>string</p></td><td><div><p>对话的具体内容</p></div></td><td><p>请问具体怎么操作呢？</p></td></tr><tr><td>type</td><td><p>string</p></td><td><div><p>对话内容的类型：text（文本）；audio（语音）；image（图片）。目前仅支持文本类型。</p></div></td><td><p>text</p></td></tr><tr><td>id</td><td><p>integer</p></td><td><div><p>本句话的唯一标识,内部赋值。可能为空，建议使用 recordId。</p></div></td><td><p>1742869659849</p></td></tr><tr><td>recordId</td><td><p>string</p></td><td><div><p>本句话的唯一标识,内部赋值，String 类型。</p></div></td><td><p>19387872364736xdhcb</p></td></tr><tr><td>intentCode</td><td><p>string</p></td><td><div><p>意图 code</p></div></td><td><p>193874634xxx</p></td></tr><tr><td>intentName</td><td><p>string</p></td><td><div><p>意图名称</p></div></td><td><p>客户询问如何操作</p></td></tr><tr><td>hangUpDialog</td><td><p>boolean</p></td><td><div><p>是否挂断：当句是否挂断会话标识</p></div></td><td><p>true</p></td></tr><tr><td>status</td><td><p>string</p></td><td><div><p>会话状态</p></div></td><td><p>COMPLETED</p></td></tr><tr><td>gmtCreate</td><td><p>string</p></td><td><div><p>会话时间</p></div></td><td><p>2024-09-27 11:23:20</p></td></tr><tr><td>requestId</td><td><p>string</p></td><td><div><p>请求 id</p></div></td><td><p>5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658</p></td></tr><tr><td>cost</td><td><p>integer</p></td><td><div><p>耗时</p></div></td><td><p>null</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "success": true,
  "dataType": "null",
  "time": "2024-04-24 11:54:34",
  "errCode": "0",
  "message": "ok",
  "data": {
    "totalDialogTurns": 10,
    "validDialogTurns": 5,
    "dialogueList": [
      {
        "role": "0",
        "customerServiceType": "0",
        "customerServiceId": "BOT",
        "customerId": "123761283",
        "content": "请问具体怎么操作呢？",
        "type": "text",
        "id": 1742869659849,
        "recordId": "19387872364736xdhcb",
        "intentCode": "193874634xxx",
        "intentName": "客户询问如何操作",
        "hangUpDialog": true
      }
    ],
    "status": "COMPLETED",
    "gmtCreate": "2024-09-27 11:23:20"
  },
  "requestId": "5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658",
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

更多信息，参考[变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/GetDialogDetail#workbench-doc-change-demo)。
