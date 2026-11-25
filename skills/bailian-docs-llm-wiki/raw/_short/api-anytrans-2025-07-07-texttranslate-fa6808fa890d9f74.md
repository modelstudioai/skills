# TextTranslate

通义多模态翻译文本翻译

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
| anytrans:TextTranslate | none | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求语法"></a>

<a id="api-detail-53"></a>

## 请求语法

<a id="code-block"></a>

```text
POST /anytrans/translate/text HTTP/1.1
```

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

<table><thead><tr><th><p><strong>名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>必填</strong></p></th><th><p><strong>描述</strong></p></th><th><p><strong>示例值</strong></p></th></tr></thead><tbody><tr><td>workspaceId</td><td><p>string</p></td><td><p>是</p></td><td><div><p>业务空间 Id</p></div></td><td><p>llm-kqtrcpdee4xm29xx</p></td></tr><tr><td>format</td><td><p>string</p></td><td><p>否</p></td><td><div><p>文本格式</p></div></td><td><p>text</p></td></tr><tr><td>sourceLanguage</td><td><p>string</p></td><td><p>是</p></td><td><div><p>源语种代码</p></div></td><td><p>zh</p></td></tr><tr><td>targetLanguage</td><td><p>string</p></td><td><p>是</p></td><td><div><p>目标语种代码</p></div></td><td><p>en</p></td></tr><tr><td>text</td><td><p>string</p></td><td><p>是</p></td><td><div><p>待翻译的文本</p></div></td><td><p>今天天气怎么样</p></td></tr><tr><td>scene</td><td><p>string</p></td><td><p>否</p></td><td><div><p>模型类型</p></div><div><p><strong>枚举值：</strong></p><ul><li>mt-plus :<div><p>专业版</p></div></li><li>mt-flash :<div><p>轻量版</p></div></li></ul></div></td><td><p>mt-flash</p></td></tr><tr><td>ext</td><td><p>object</p></td><td><p>否</p></td><td><div><p>控制翻译行为的扩展参数</p></div></td><td></td></tr><tr><td>examples</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>翻译示例列表</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>翻译示例</p></div></td><td></td></tr><tr><td>src</td><td><p>string</p></td><td><p>否</p></td><td><div><p>源文案</p></div></td><td><p>你好</p></td></tr><tr><td>tgt</td><td><p>string</p></td><td><p>否</p></td><td><div><p>目标文案</p></div></td><td><p>hello</p></td></tr><tr><td>domainHint</td><td><p>string</p></td><td><p>否</p></td><td><div><p>领域提示</p></div></td><td><p>technology</p></td></tr><tr><td>agent</td><td><p>string</p></td><td><p>否</p></td><td><div><p>专家 agent，使用前需添加白名单</p></div><div><p><strong>枚举值：</strong></p><ul><li>game :<div><p>游戏译者</p></div></li><li>medical :<div><p>医学翻译大师</p></div></li><li>ao3 :<div><p>AO3 译者</p></div></li><li>mixlang :<div><p>中英夹杂</p></div></li><li>twitter :<div><p>Twitter 翻译增强器</p></div></li><li>ecom :<div><p>金融翻译顾问</p></div></li><li>music :<div><p>音乐专家</p></div></li><li>dongbei :<div><p>东北话</p></div></li><li>design :<div><p>设计师</p></div></li><li>legal :<div><p>法律行业译者</p></div></li><li>reddit :<div><p>Reddit 翻译增强器</p></div></li><li>vocab :<div><p>词汇助手</p></div></li><li>wordalign :<div><p>分词对照翻译助手</p></div></li><li>academy :<div><p>学术论文翻译师</p></div></li><li>news :<div><p>新闻媒体译者</p></div></li><li>tech :<div><p>科技类翻译大师</p></div></li><li>github :<div><p>GitHub 翻译增强器</p></div></li><li>chess :<div><p>国际象棋专家</p></div></li><li>web3 :<div><p>Web3 翻译大师</p></div></li><li>bai2wen :<div><p>白话文转文言文</p></div></li><li>ebook :<div><p>电子书译者</p></div></li><li>sublearn :<div><p>潜意识学习</p></div></li><li>summarize :<div><p>段落总结专家</p></div></li><li>simplify :<div><p>英文简化大师</p></div></li><li>wen2bai :<div><p>文言文转白话文</p></div></li><li>finance :<div><p>金融翻译顾问</p></div></li><li>novel :<div><p>小说译者</p></div></li></ul></div></td><td><p>game</p></td></tr><tr><td>sensitives</td><td><p>array</p></td><td><p>否</p></td><td><div><p>敏感词列表</p></div></td><td></td></tr><tr><td></td><td><p>string</p></td><td><p>否</p></td><td><div><p>敏感词列表</p></div></td><td><p>password</p></td></tr><tr><td>terminologies</td><td><p>array&lt;object&gt;</p></td><td><p>否</p></td><td><div><p>翻译术语库</p></div></td><td></td></tr><tr><td></td><td><p>object</p></td><td><p>否</p></td><td><div><p>翻译术语库</p></div></td><td></td></tr><tr><td>src</td><td><p>string</p></td><td><p>否</p></td><td><div><p>源文案</p></div></td><td><p>机器学习</p></td></tr><tr><td>tgt</td><td><p>string</p></td><td><p>否</p></td><td><div><p>目标文案</p></div></td><td><p>ML</p></td></tr><tr><td>textTransform</td><td><p>object</p></td><td><p>否</p></td><td><div><p>译文文本转换</p></div></td><td></td></tr><tr><td>toLower</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>转小写</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>是</p></div></li><li>false :<div><p>否</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>toUpper</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>转大写</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>是</p></div></li><li>false :<div><p>否</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>toTitle</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>首字母大写</p></div><div><p><strong>枚举值：</strong></p><ul><li>true :<div><p>是</p></div></li><li>false :<div><p>否</p></div></li></ul></div></td><td><p>false</p></td></tr><tr><td>config</td><td><p>object</p></td><td><p>否</p></td><td><div><p>翻译行为控制</p></div></td><td></td></tr><tr><td>skipCsiCheck</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否跳过绿网检测（如果需要跳过绿网检测，需要先完成绿网关闭流程后再调用）</p></div><div><p><strong>枚举值：</strong></p><ul><li>ture :<div><p>是</p></div></li><li>false :<div><p>否</p></div></li></ul></div></td><td><p>fasle</p></td></tr><tr><td>prefix</td><td><p>string</p></td><td><p>否</p></td><td><div><p>前缀配置</p></div></td><td><p>Today's weather</p></td></tr><tr><td>paramMap</td><td><p>any</p></td><td><p>否</p></td><td><div><p>扩展参数配置（bizUserld：业务层面的用户 ID，用来区分不 同业务用户，做到“按用户隔离”的术语干预，互不影响。 bizType：业务场景类型/标识，用来区分不同场景，做到 “按场景隔离”的术语干预，互不影响。）</p></div><div><p><strong>枚举值：</strong></p><ul><li>bizType :<div><p>业务场景类型</p></div></li><li>bizUserId :<div><p>业务用户 id</p></div></li></ul></div></td><td><p>{&quot;bizUserld&quot;:&quot;123456&quot;,&quot;bizType&quot;:session&quot;}</p></td></tr><tr><td>langDetect</td><td><p>boolean</p></td><td><p>否</p></td><td><div><p>是否启用源语言自动检测。设置为 true 时，sourceLanguage 参数不生效。</p></div></td><td><p>false</p></td></tr></tbody></table>

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| code | string | 响应状态码 | 200 |
| message | string | 错误信息 | success |
| requestId | string | Id of the request | 299C57B2-EBB4-57E2-A6FE-723B874ACB74 |
| success | boolean | 调用是否成功 | true |
| httpStatusCode | string | http 状态码 | 200 |
| data | object | 返回数据 |  |
| translation | string | 翻译结果 | How does Mogujie solve the data annotation challenge by building a platform? |
| detectedLang | string | 自动检测到的源语言代码。 | zh |
| usage | object | token 消耗 |  |
| inputTokens | integer | 输入 token 数 | 491 |
| outputTokens | integer | 输出 Token 数量 | 400 |
| totalTokens | integer | 总 token 量 | 891 |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block-2"></a>

```json
{
  "code": "200",
  "message": "success",
  "requestId": "299C57B2-EBB4-57E2-A6FE-723B874ACB74",
  "success": true,
  "httpStatusCode": "200",
  "data": {
    "translation": "How does Mogujie solve the data annotation challenge by building a platform?",
    "detectedLang": "",
    "usage": {
      "inputTokens": 491,
      "outputTokens": 400,
      "totalTokens": 891
    }
  }
}
```

<a id="错误码"></a>

<a id="h2-url-6"></a>

## 错误码

| HTTP status code | 错误码 | 错误信息 | 描述 |
| --- | --- | --- | --- |
| 400 | IdempotentParameterMismatch | The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical. |  |

访问[错误中心](https://api.aliyun.com/document/AnyTrans/2025-07-07/errorCode)查看更多错误码。

<a id="变更历史"></a>

<a id="workbench-doc-change-demo"></a>

## 变更历史

更多信息，参考[变更详情](https://api.aliyun.com/document/AnyTrans/2025-07-07/TextTranslate#workbench-doc-change-demo)。
