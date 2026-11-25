# CreateCloneVoice

创建克隆音

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
| bailianvoicebot:CreateCloneVoice | create | \*全部资源<br><br>`*` | 无 | 无 |

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

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>BusinessUnitId</td><td><p>string</p></td><td><p>否</p></td><td><div><p>百炼业务空间 ID</p></div></td><td><p>llm-xdne77rxe14ziszr</p></td></tr><tr><td>FileKey</td><td><p>string</p></td><td><p>否</p></td><td><div><p>上传文件路径</p></div></td><td><p>voice_clone/音色克隆单元测试.wav</p></td></tr><tr><td>Model</td><td><p>string</p></td><td><p>否</p></td><td><div><p>克隆模型</p></div><div><p><strong>枚举值：</strong></p><ul><li>CosyVoice :<div><p>CosyVoice</p></div></li><li>QwenVc :<div><p>QwenVc</p></div></li></ul></div></td><td><p>CosyVoice</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | 请求 ID | CF6D3484-19A1-5C77-863B-AC8B5754D37C |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误信息 | Instance llm-xdne77rxe14ziszr does not exist. |
| Code | string | 内部错误码 | OK |
| Data | object | 克隆音对象 |  |
| CloneVoiceId | string | 克隆音 ID | 8ee1160a-6999-478f-8df6-f33ef21f27d5 |
| Voice | string | 发音人 | cosyvoice-v3-plus-voicebot2-3666e4bbb2b94832ac4f4107b5804c34 |
| Params | array | 动态错误参数列表 |  |
|  | string | 动态错误参数 | llm-xdne77rxe14ziszr |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "RequestId": "CF6D3484-19A1-5C77-863B-AC8B5754D37C",
  "HttpStatusCode": 200,
  "Message": "Instance llm-xdne77rxe14ziszr\n does not exist.",
  "Code": "OK",
  "Data": {
    "CloneVoiceId": "8ee1160a-6999-478f-8df6-f33ef21f27d5",
    "Voice": "cosyvoice-v3-plus-voicebot2-3666e4bbb2b94832ac4f4107b5804c34"
  },
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateCloneVoice#workbench-doc-change-demo)。
