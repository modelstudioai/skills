# GetDataSourceOrderConfig - 获取信源配置权重数据

获取写作信源，通用搜索信源的配置信息。

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetDataSourceOrderConfig)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:GetDataSourceOrderConfig</td><td>get</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>AgentKey</td><td>string</td><td>是</td><td><div><p>业务空间唯一标识： <a href="https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey">AgentKey</a></p></div></td><td>d9a1f6146a37446495d9985c2e7b267e_p_outbound_public</td></tr><tr><td>ProductCode</td><td>string</td><td>是</td><td><div><p>配置类型。可选值如下：</p><ul><li><p>miaobi</p></li><li><p>miaosou</p></li></ul></div></td><td>miaobi</td></tr><tr><td>GenerateTechnology</td><td>string</td><td>否</td><td><div><p>productCode=miaosou 时，对应妙搜：生成技术</p><p>可取值如下：</p><ul><li><p>copilotPrecise</p></li><li><p>copilotReference</p></li></ul></div></td><td>copilotPrecise</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | PlainResult |  |
| Code | string | 状态码 | successful |
| Data | object | 业务数据 |  |
| UserConfigDataSourceList | array<object> | 用户配置数据源权重列表 |  |
| UserConfigDataSourceList | object |  |  |
| Code | string | code 描述 | QuarkCommonNews |
| Name | string | 显示名称 | 夸克通用搜索 |
| Number | integer | 数量 | 20 |
| Type | string | type 类型 | SystemSearch |
| Enable | boolean | 是否启用 |  |
| TotalDocSize | integer | 最大文档总数 | 1 |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误说明 | successful |
| RequestId | string | 请求唯一标识 | 428DCC0D-3C63-5306-BD1B-124396AB97BE |
| Success | boolean | 是否成功：true 成功，false 失败 | true |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "successful",
  "Data": {
    "UserConfigDataSourceList": [
      {
        "Code": "QuarkCommonNews",
        "Name": "夸克通用搜索",
        "Number": 20,
        "Type": "SystemSearch",
        "Enable": true
      }
    ],
    "TotalDocSize": 1
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "428DCC0D-3C63-5306-BD1B-124396AB97BE",
  "Success": true
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。
