# ListBuildConfigs

获取系统自定义预设，用于创作文章 -> 直接生成中的内置选项。例如：写作文体、文章篇幅、输出语言、生成文章篇数等选项。

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
| aimiaobi:ListBuildConfigs | get | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>AgentKey</td><td><p>string</p></td><td><p>是</p></td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td><p>cd327c3d5d5e44159cc716e23bfa530e_p_beebot_public</p></td></tr><tr><td>Type</td><td><p>string</p></td><td><p>否</p></td><td><div><p>政务和传媒类别，media：传媒；government：政务</p></div><div><p><strong>枚举值：</strong></p><ul><li>market :<div><p>营销文稿</p></div></li><li>government :<div><p>政务文稿</p></div></li><li>media :<div><p>传媒文稿</p></div></li><li>office :<div><p>办公文稿</p></div></li></ul></div></td><td><p>media</p></td></tr><tr><td>RegionId</td><td><p>string</p></td><td><p>否</p></td><td></td><td></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PlainResult<List<br><br>\> |  |
| Code | string | 状态码 | 200 |
| Data | array<object> | 业务数据 |  |
|  | array<object> | 业务对象 |  |
| BuildIn | boolean | 是否为内置 | true |
| CreateTime | string | 创建时间 | 2023-04-11 06:14:07 |
| CreateUser | string | 创建用户 | 1 |
| Id | integer | 主键 ID | 主键ID，内置配置（buildIn=true）无该字段 |
| Keywords | array<object> | 标签可选的值列表 |  |
|  | object | 标签可选的值定义 |  |
| Description | string | 预设标签的描述 | 新闻内容 |
| Key | string | 预设标签的 KEY | 新闻内容 |
| Tag | string | 标签 key 值 | writingStyle |
| TagDescription | string | 标签描述 | 文体 |
| Type | string | 区分政务和传媒-media：传媒；government：政务 | media |
| UpdateTime | string | 更新时间 | 2023-04-11 06:14:07 |
| UpdateUser | string | 更新用户 | 1 |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误说明 | Success |
| RequestId | string | 请求唯一标识 | DA021073-17CE-5CCF-9FEB-93226C766887 |
| Success | boolean | 是否成功：true 成功，false 失败 | true |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```json
{
  "Code": "200",
  "Data": [
    {
      "BuildIn": true,
      "CreateTime": "2023-04-11 06:14:07",
      "CreateUser": "1",
      "Id": 0,
      "Keywords": [
        {
          "Description": "新闻内容",
          "Key": "新闻内容"
        }
      ],
      "Tag": "writingStyle",
      "TagDescription": "文体",
      "Type": "media",
      "UpdateTime": "2023-04-11 06:14:07\n",
      "UpdateUser": "1"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "Success",
  "RequestId": "DA021073-17CE-5CCF-9FEB-93226C766887",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListBuildConfigs#workbench-doc-change-demo)。
