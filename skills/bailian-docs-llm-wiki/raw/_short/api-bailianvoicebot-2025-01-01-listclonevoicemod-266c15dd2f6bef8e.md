# ListCloneVoiceModels

获取克隆音色可用模型列表

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
| bailianvoicebot:ListCloneVoiceModels | list | \*全部资源<br><br>`*` | 无 | 无 |

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

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| PageNumber | integer | 否 | 页号 | 1 |
| PageSize | integer | 否 | 每页条数 | 10 |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | Id of the request | CF6D3484-19A1-5C77-863B-AC8B5754D37C |
| Code | string | 内部错误码 | OK |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误信息 | Instance llm-zzu528i29ecnprcl does not exist. |
| Data | object | 克隆音模型分页数据 |  |
| PageNumber | integer | 页号 | 1 |
| PageSize | integer | 每页条数 | 10 |
| TotalCount | integer | 总数量 | 100 |
| CloneVoiceModels | array<object> | 克隆音模型列表 |  |
|  | object | 克隆音模型对象 |  |
| Name | string | 模型名称 | CosyVoice |
| DisplayName | string | 显示名称 | CosyVoice |
| Description | string | 描述 | 口音还原相似度高、韵律流畅 |
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
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "Instance llm-zzu528i29ecnprcl does not exist.",
  "Data": {
    "PageNumber": 1,
    "PageSize": 10,
    "TotalCount": 100,
    "CloneVoiceModels": [
      {
        "Name": "CosyVoice",
        "DisplayName": "CosyVoice",
        "Description": "口音还原相似度高、韵律流畅"
      }
    ]
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

更多信息，参考[变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/ListCloneVoiceModels#workbench-doc-change-demo)。
