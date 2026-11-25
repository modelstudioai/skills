# ListWritingStyles - 获取写作文体列表

获取文体列表。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListWritingStyles)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:ListWritingStyles</td><td>list</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p><a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">业务空间 ID</a></p></div></td><td>llm-xxxxx</td></tr><tr><td>Scene</td><td>string</td><td>是</td><td><div><p>写作场景筛选</p></div><div><div>枚举值：</div><ul><li>market：营销写作。</li><li>government：法定公文 。</li><li>custom：自定义写作。</li><li>media：传媒类。</li><li>office：事务公文。</li></ul></div></td><td>media</td></tr><tr><td>MaxResults</td><td>integer</td><td>否</td><td><div><p>返回的最大结果数</p></div></td><td>100</td></tr><tr><td>NextToken</td><td>string</td><td>否</td><td><div><p>写一页 Token</p></div></td><td>下一页token</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | Id of the request | 1813ceee-7fe5-41b4-87e5-982a4d18cca5 |
| TotalCount | integer | 总记录数 | 58 |
| MaxResults | integer | 最大返回结果数 | 100 |
| NextToken | string | 下一个 token | 下一页token |
| Code | string | 错误码 | successful |
| Message | string | 错误消息 | 数据不存在 |
| Success | string | 此次请求是否成功 | true |
| Data | array<object> | 文体列表 |  |
| data | object | 文体对象 |  |
| StyleName | string | 文体名称 | 文体名称 |
| StyleKey | string | 文体唯一标识 KEY | 文体唯一标识 |
| StyleDescription | string | 文体描述 | 文体描述 |
| DistributeWriting | boolean | 是否支持分步骤写作 | false |
| StyleImage | string | 文体图片 | 文体图片 |
| Emoji | string | 文体小图标（字符符号表示） | 小图标 |
| TemplateDefine | WritingStyleTemplateDefine | 文体模板定义 |  |
| DistributeStepTemplateDefine | WritingStyleTemplateDefine | 分步骤模板定义 |  |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "TotalCount": 58,
  "MaxResults": 100,
  "NextToken": "下一页token",
  "Code": "successful",
  "Message": "数据不存在",
  "Success": true,
  "Data": [
    {
      "StyleName": "文体名称",
      "StyleKey": "文体唯一标识",
      "StyleDescription": "文体描述",
      "DistributeWriting": false,
      "StyleImage": "文体图片\n\n",
      "Emoji": "小图标",
      "TemplateDefine": {
        "Fields": [
          {
            "MinItemLength": 1000,
            "Max": 2000,
            "MinLength": 20,
            "MaxLength": 2000,
            "MaxItemLength": 4000,
            "Name": "字段名称",
            "BuildIn": true,
            "Enums": [
              {
                "CascadingFields": [
                  "级联字段"
                ],
                "Key": "枚举KEY",
                "Name": "枚举名称"
              }
            ],
            "Min": 1,
            "Required": false,
            "MaxItem": 10,
            "InitialValue": "初始值",
            "CascadingFields": [
              {
                "MinItemLength": 1000,
                "Max": 2000,
                "MinLength": 20,
                "MaxLength": 2000,
                "MaxItemLength": 4000,
                "Name": "字段名称",
                "BuildIn": true,
                "Enums": [
                  {
                    "CascadingFields": [
                      "级联字段"
                    ],
                    "Key": "枚举KEY",
                    "Name": "枚举名称"
                  }
                ],
                "Min": 1,
                "Required": false,
                "MaxItem": 10,
                "InitialValue": "初始值",
                "CascadingFields": [
                  {
                    "MinItemLength": 1000,
                    "Max": 2000,
                    "MinLength": 20,
                    "MaxLength": 2000,
                    "MaxItemLength": 4000,
                    "Name": "字段名称",
                    "BuildIn": true,
                    "Enums": [
                      {
                        "CascadingFields": [
                          "级联字段"
                        ],
                        "Key": "枚举KEY",
                        "Name": "枚举名称"
                      }
                    ],
                    "Min": 1,
                    "Required": false,
                    "MaxItem": 10,
                    "InitialValue": "初始值",
                    "CascadingFields": [],
                    "Style": {
                      "Placeholder": "清输入Prompt",
                      "Type": "media",
                      "ShowTime": true,
                      "Suffix": "后缀",
                      "Description": "输入框提示文案",
                      "Format": "yyyy-mm-dd"
                    },
                    "Key": "topic"
                  }
                ],
                "Style": {
                  "Placeholder": "清输入Prompt",
                  "Type": "media",
                  "ShowTime": true,
                  "Suffix": "后缀",
                  "Description": "输入框提示文案",
                  "Format": "yyyy-mm-dd"
                },
                "Key": "topic"
              }
            ],
            "Style": {
              "Placeholder": "清输入Prompt",
              "Type": "media",
              "ShowTime": true,
              "Suffix": "后缀",
              "Description": "输入框提示文案",
              "Format": "yyyy-mm-dd"
            },
            "Key": "topic"
          }
        ],
        "Example": [
          {
            "Value": 123,
            "Key": "topic"
          }
        ]
      },
      "DistributeStepTemplateDefine": {
        "Fields": [],
        "Example": [
          {
            "Value": 123,
            "Key": "topic"
          }
        ]
      }
    }
  ]
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
