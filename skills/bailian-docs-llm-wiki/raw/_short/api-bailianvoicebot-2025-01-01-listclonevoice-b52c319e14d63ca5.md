# ListCloneVoice

获取实例详情

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
| bailianvoicebot:ListCloneVoice | list | \*全部资源<br><br>`*` | 无 | 无 |

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

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>BusinessUnitId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>百炼业务空间 ID</p></div></td><td><p>llm-3pptowd2olrctsvc</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><p>否</p></td><td><div><p>状态</p></div><div><p><strong>枚举值：</strong></p><ul><li>Draft :<div><p>Draft</p></div></li><li>Published :<div><p>Published</p></div></li></ul></div></td><td><p>Published</p></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>页号</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><p>否</p></td><td><div><p>每页条数</p></div></td><td><p>10</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td></td><td><p>object</p></td><td><div><p>Schema of Response</p></div></td><td></td></tr><tr><td>RequestId</td><td><p>string</p></td><td><div><p>请求 ID</p></div></td><td><p>D771A1B6-3D5F-174A-BEE1-98CE1000D337</p></td></tr><tr><td>Code</td><td><p>string</p></td><td><div><p>内部错误码</p></div></td><td><p>OK</p></td></tr><tr><td>HttpStatusCode</td><td><p>integer</p></td><td><div><p>http 状态码</p></div></td><td><p>200</p></td></tr><tr><td>Message</td><td><p>string</p></td><td><div><p>错误信息</p></div></td><td><p>Instance llm-xdne77rxe14ziszr does not exist.</p></td></tr><tr><td>Data</td><td><p>object</p></td><td><div><p>克隆音列表分页数据</p></div></td><td></td></tr><tr><td>PageNumber</td><td><p>integer</p></td><td><div><p>页号</p></div></td><td><p>1</p></td></tr><tr><td>PageSize</td><td><p>integer</p></td><td><div><p>每页条数</p></div></td><td><p>10</p></td></tr><tr><td>TotalCount</td><td><p>integer</p></td><td><div><p>总数量</p></div></td><td><p>100</p></td></tr><tr><td>CloneVoices</td><td><p>array&lt;object&gt;</p></td><td><div><p>克隆音列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><div><p>克隆音对象</p></div></td><td></td></tr><tr><td>CloneVoiceId</td><td><p>string</p></td><td><div><p>克隆音 ID</p></div></td><td><p>8ee1160a-6999-478f-8df6-f33ef21f27d5</p></td></tr><tr><td>CreatedTime</td><td><p>integer</p></td><td><div><p>创建时间</p></div></td><td><p>1760494691000</p></td></tr><tr><td>UpdatedTime</td><td><p>integer</p></td><td><div><p>更新时间</p></div></td><td><p>1760494691000</p></td></tr><tr><td>InstanceId</td><td><p>string</p></td><td><div><p>业务空间 ID</p></div></td><td><p>llm-xdne77rxe14ziszr</p></td></tr><tr><td>TenantId</td><td><p>string</p></td><td><div><p>租户 ID</p></div></td><td><p>1655449505171</p></td></tr><tr><td>Voice</td><td><p>string</p></td><td><div><p>发音人</p></div></td><td><p>cosyvoice-v3-plus-voicebot2-3666e4bbb2b94832ac4f4107b5804c34</p></td></tr><tr><td>Name</td><td><p>string</p></td><td><div><p>克隆音名称</p></div></td><td><p>测试克隆音</p></td></tr><tr><td>NlsEngine</td><td><p>string</p></td><td><div><p>TTS 引擎</p></div></td><td><p>BAILIAN</p></td></tr><tr><td>Status</td><td><p>string</p></td><td><div><p>状态</p></div><div><p><strong>枚举值：</strong></p><ul><li>Draft :<div><p>Draft</p></div></li><li>Published :<div><p>Published</p></div></li></ul></div></td><td><p>Published</p></td></tr><tr><td>Model</td><td><p>string</p></td><td><div><p>克隆模型</p></div><div><p><strong>枚举值：</strong></p><ul><li>CosyVoice :<div><p>CosyVoice</p></div></li><li>QwenVc :<div><p>QwenVc</p></div></li></ul></div></td><td><p>CosyVoice</p></td></tr></tbody></table>

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-xdne77rxe14ziszr\n does not exist.",
  "Data": {
    "PageNumber": 1,
    "PageSize": 10,
    "TotalCount": 100,
    "CloneVoices": [
      {
        "CloneVoiceId": "8ee1160a-6999-478f-8df6-f33ef21f27d5\n",
        "CreatedTime": 1760494691000,
        "UpdatedTime": 1760494691000,
        "InstanceId": "llm-xdne77rxe14ziszr",
        "TenantId": "1655449505171",
        "Voice": "cosyvoice-v3-plus-voicebot2-3666e4bbb2b94832ac4f4107b5804c34",
        "Name": "测试克隆音",
        "NlsEngine": "BAILIAN",
        "Status": "Published",
        "Model": "CosyVoice"
      }
    ]
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/ListCloneVoice#workbench-doc-change-demo)。
