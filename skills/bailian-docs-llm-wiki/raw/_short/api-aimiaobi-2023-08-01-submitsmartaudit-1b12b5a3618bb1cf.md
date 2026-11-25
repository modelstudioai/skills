# SubmitSmartAudit

提交智能审核

<a id="接口说明"></a>

<a id="api-detail-51"></a>

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](iframe-embedding-scheme-6f73b86f9f7bdf41.md)

<a id="支持的审核类型"></a>

## 支持的审核类型

<a id="审校大类概览"></a>

## 审校大类概览

| 审校大类 | 说明 |
| --- | --- |
| 内容准确性 | 音/形相似差错；标点符号错误；的地得错误；用词不当/语法错误；人名错误；地名错误；引用错误；专有名称/术语错误 |
| 格式规范问题 | 大小写不规范；数字错误；计量单位不规范；繁体字 |
| 内容结构问题 | 文字冗余；片段重复；逻辑矛盾；占位符未填充 |
| 政治性问题 | 敏感和内容导向风险；姓名或排序差错；固有表述差错；机构名称不规范；重要讲话引用差错；落马官员；姓名职务搭配错误；职务表述错误 |
| 安全合规问题 | 暴恐；色情；违禁；侮辱；劣迹艺人；个人隐私；报道规范 |
| 法律错误 | 法律法规引用；法律条文错误 |
| 其他专业知识错误 | 违反广告法；金融类信息；科技名词 |
| 事实性检查 | 事实性审核正确项/错误项 |
| 图片审核 | 图片内容审核 |
| 自定义词库 | 自定义词库审核 |
| 规则库审核 | 规则库审核 |
| 英文审校 | 术语标准化；动词时态准确性；标点与引号；拼写与语言变体；句子结构与清晰度；数字与百分比格式；规范用语 |

* * *

<a id="子审核编码取值列表"></a>

## 子审核编码取值列表

<a id="1-内容准确性"></a>

### 1\. 内容准确性

| 描述 | code |
| --- | --- |
| 音/形相似差错 | PhoneticSimilarError |
| 标点符号错误 | PunctuationError |
| 的地得错误 | ParticleUsageError |
| 用词不当/语法错误 | WordError |
| 人名错误 | PersonNameError |
| 地名错误 | LocationError |
| 引用错误 | ReferenceError |
| 专有名称/术语错误 | NounItemError |

<a id="2-格式规范问题"></a>

### 2\. 格式规范问题

| 描述 | code |
| --- | --- |
| 大小写不规范 | CapitalizationError |
| 数字错误 | NumberError |
| 计量单位不规范 | UnitError |
| 繁体字 | TraditionalChineseError |

<a id="3-内容结构问题"></a>

### 3\. 内容结构问题

| 描述 | code |
| --- | --- |
| 文字冗余 | WordRedundancy |
| 片段重复 | DuplicateError |
| 逻辑矛盾 | LogicContradiction |
| 占位符未填充 | PlaceholderNotFilled |

<a id="4-政治性问题"></a>

### 4\. 政治性问题

| 描述 | code |
| --- | --- |
| 敏感和内容导向风险 | SensitiveContentRisk |
| 姓名或排序差错 | NameOrderError |
| 固有表述差错 | ConventionalExpressionError |
| 机构名称不规范 | DepartmentNameError |
| 重要讲话引用差错 | ImportantSpeechError |
| 落马官员 | FallenOfficialError |
| 姓名职务搭配错误 | LeaderTitleMatchError |
| 职务表述错误 | TitleError |

<a id="5-安全合规问题"></a>

### 5\. 安全合规问题

| 描述 | code |
| --- | --- |
| 暴恐 | ViolenceTerrorismError |
| 色情 | PornographyError |
| 违禁 | ProhibitedContentError |
| 侮辱 | InsultError |
| 劣迹艺人 | DisgracedArtistError |
| 个人隐私 | PersonalPrivacyError |
| 报道规范 | ReportingStandardError |

<a id="6-法律错误"></a>

### 6\. 法律错误

| 描述 | code |
| --- | --- |
| 法律法规引用 | LegalReferenceError |
| 法律条文错误 | LegalProvisionsError |

<a id="7-其他专业知识错误"></a>

### 7\. 其他专业知识错误

| 描述 | code |
| --- | --- |
| 违反广告法 | AdvertisingProhibitedWordsError |
| 金融类信息 | FinancialInformationError |
| 科技名词 | TechnicalTermError |

<a id="8-事实性检查"></a>

### 8\. 事实性检查

| 描述 | code |
| --- | --- |
| 事实性审核-正确项 | CorrectFact |
| 事实性审核-错误项 | WrongFactError |

<a id="9-图片审核"></a>

### 9\. 图片审核

| 描述 | code |
| --- | --- |
| 图片审核 | ImageAudit |

<a id="10-自定义词库"></a>

### 10\. 自定义词库

| 描述 | code |
| --- | --- |
| 自定义词库 | WordLibrary |

<a id="11-规则库审核"></a>

### 11\. 规则库审核

| 描述 | code |
| --- | --- |
| 规则库审核 | WrongQuestionBook |

<a id="12-英文审校"></a>

### 12\. 英文审校

| 描述 | code |
| --- | --- |
| 术语标准化 | TerminologyNormalisation |
| 动词时态准确性 | VerbTenseAccuracy |
| 标点与引号 | PunctuationAndQuotationMarks |
| 拼写与语言变体 | SpellingAndLanguageVariety |
| 句子结构与清晰度 | SentenceStructureAndClarity |
| 数字与百分比格式 | NumericAndPercentageStyle |
| 其他规范用语 | Others |

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
| aimiaobi:SubmitSmartAudit | create | \*全部资源<br><br>`*` | 无 | 无 |

<a id="请求参数"></a>

<a id="api-detail-36"></a>

## 请求参数

| 名称 | 类型 | 必填 | 描述 | 示例值 |
| --- | --- | --- | --- | --- |
| WorkspaceId | string | 否 | [业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id) | xxxx |
| Text | string | 否 | 待审核的内容 | “你好呀” |
| SubCodes | array | 否 | 子审核编码列表 |  |
|  | string | 否 | 子审核编码，子审核编码详见接口 [ListAuditContentErrorTypes](api-aimiaobi-2023-08-01-listauditcontenterrortyp-dc8a1e855346739b.md) 或下述参数补充说明 | PunctuationError |
| imageUrls | array<object> | 否 | 图片审核时传递的参数（已弃用，请使用 ImageUrlList） |  |
|  | object | 否 | 图片审核时传递的参数 |  |
| url | string | 否 | Url 可能是链接，可能是 base64 | [https://www.example.com/xxx.jpg](https://www.example.com/xxx.jpg) |
| id | string | 否 | 图片唯一标识 ID | 3HAZTv62M0vkyz5B |
| ImageUrlList | array<object> | 否 | 图片审核时传递的参数 |  |
|  | object | 否 |  |  |
| Url | string | 否 | Url 可能是链接，可能是 base64 | [http://www.example.com/xxx.png](http://www.example.com/xxx.png) |
| Id | string | 否 | 图片唯一标识 ID | xxxx |
| NoteId | string | 否 | 基于规则库审校的规则库 ID（默认 Default） | note\_1\_486 |
| TermsName | string | 否 | 基于词库审校的词库名称（默认 Default） | Default |

<a id="返回参数"></a>

<a id="api-detail-41"></a>

## 返回参数

| 名称 | 类型 | 描述 | 示例值 |
| --- | --- | --- | --- |
|  | object | Schema of Response |  |
| RequestId | string | Id of the request | xxxxx |
| Success | boolean | 此次请求是否成功 | true |
| Code | string | 错误码 | DataNotExists |
| Message | string | 错误消息 | 错误消息 |
| HttpStatusCode | integer | http 错误码 | 400 |
| Data | object | 任务响应对象 |  |
| TaskId | string | 任务 ID | xxxx |

<a id="示例"></a>

<a id="api-detail-1"></a>

## 示例

正常返回示例

`JSON`格式

<a id="code-block"></a>

```json
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "TaskId": "xxxx"
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/SubmitSmartAudit#workbench-doc-change-demo)。
