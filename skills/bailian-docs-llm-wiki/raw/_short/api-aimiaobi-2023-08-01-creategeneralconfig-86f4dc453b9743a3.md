# CreateGeneralConfig - 通用配置-创建

<a id="调试"></a>

<a id="api-detail-23"></a>

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/CreateGeneralConfig)

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
    

<table><thead><tr><th>操作</th><th>访问级别</th><th>资源类型</th><th>条件关键字</th><th>关联操作</th></tr></thead><tbody><tr><td>aimiaobi:CreateGeneralConfig</td><td>create</td><td><div><div>*全部资源</div><div><code>*</code></div></div></td><td><ul>无</ul></td><td>无</td></tr></tbody></table>

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th>名称</th><th>类型</th><th>必填</th><th>描述</th><th>示例值</th></tr></thead><tbody><tr><td>WorkspaceId</td><td>string</td><td>是</td><td><div><p>百炼业务空间唯一标识：<a href="https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id">获取 workspaceId</a></p></div></td><td>llm-</td></tr><tr><td>ConfigKey</td><td>string</td><td>是</td><td><div><p>配置项唯一标识，目前支持的：</p><ul><li>妙搜-数据源-文本搜索阈值(double)：searchGenerate.searchTextMinScore</li><li>妙搜-数据源-图片搜索阈值(double)：searchGenerate.searchImageMinScore</li><li>妙搜-数据源-视频搜索阈值(double)：searchGenerate.searchVideoMinScore</li><li>妙搜-数据源-音频搜索阈值(double)：searchGenerate.searchAudioMinScore</li><li>妙搜-问答式搜索-通用-总结生成答案-纯文本 prompt 模版(string)：searchGenerate.sumQaAgentPrompt</li><li>妙搜-问答式搜索-通用-总结生成答案-文本&amp;图片 prompt 模版(string)：searchGenerate.sumQaAgentVlPrompt</li><li>妙搜-问答式搜索-深度-总结生成答案-纯文本 prompt 模版(string)：searchGenerate.sumQaEnhanceAgentPrompt</li><li>妙搜-问答式搜索-深度-总结生成答案-文本&amp;图片 prompt 模版(string)：searchGenerate.sumQaEnhanceAgentVlPrompt</li></ul></div></td><td>xxxx</td></tr><tr><td>ConfigValue</td><td>string</td><td>是</td><td><div><p>配置项值</p></div></td><td>xxx</td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | 响应结果 |  |
| Code | string | 状态码 | DataNotExists |
| HttpStatusCode | integer | http 状态码 | 200 |
| Message | string | 错误说明 | 数据不存在 |
| RequestId | string | 请求唯一标识 | 3f7045e099474ba28ceca1b4eb6d6e21 |
| Success | boolean | 是否成功：true 成功，false 失败 | false |
| Data | object | 结果 |  |
| ConfigKey | string | 配置唯一标识 | xx |
| ConfigValue | string | 配置值 | xx |
| ConfigValueType | string | 配置类型 | xx |
| ConfigDesc | string | 配置说明 | xx |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```text
{
  "Code": "DataNotExists",
  "HttpStatusCode": 200,
  "Message": "数据不存在",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": false,
  "Data": {
    "ConfigKey": "xx",
    "ConfigValue": "xx",
    "ConfigValueType": "xx",
    "ConfigDesc": "xx"
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

| 变更时间 | 变更内容概要 | 操作 |
| --- | --- | --- |
| 2025-11-12 | 新增 OpenAPI | [查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/CreateGeneralConfig?updateTime=2025-11-12#workbench-doc-change-demo) |
