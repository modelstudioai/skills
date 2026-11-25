# 通义多模态翻译

提供基于通义翻译大模型的编排和调试，在支持文本、图片、网页等内容多语言翻译的基础上，提供术语自适应干预、敏感词定义、译文格式转换等定制能力，让译文更符合不同业务场景的具体需求。

<a id="产品介绍"></a>

<a id="82009604074vi"></a>

## 产品介绍

<table><thead><tr><th><p><strong>产品</strong></p></th><th><p><strong>功能介绍</strong></p></th><th><p><strong>模型选项</strong></p></th><th><p><strong>核心优势</strong></p></th></tr></thead><tbody><tr><td><p><strong>文本翻译API</strong></p></td><td><p><strong>根据输入类型分为以下四个接口：</strong></p><ul><li><p>文本单次翻译</p></li><li><p>文本批量翻译</p></li><li><p>html翻译：异步单次接口，能较好地保持住网页内容里的标签信息</p></li><li><p>长文本翻译：异步单次接口，无窗口长度限制</p></li></ul></td><td><p><strong>每个接口均提供轻量版（flash）和专业版（plus）两个选项：</strong></p><ul><li><p>轻量版（flash）：性能好、响应快</p></li><li><p>专业版（plus）：多语言效果均衡，能更好地理解复杂的内容</p></li></ul></td><td><ul><li><p><strong>强可控性</strong>：提供术语自适应干预、敏感词表定义、领域风格提示、译文格式转换、自定义分隔符功能，让译文精准贴合领域特定需求</p></li><li><p><strong>多场景适配：</strong>针对HTML等格式类输入和长篇章内容增强翻译效果，提升结构化数据的翻译还原度和全文术语一致性</p></li><li><p><strong>高可用保障：</strong>在极端情况下自动启用高稳定性的兜底服务，确保翻译质量和稳定性</p></li></ul></td></tr><tr><td><p><strong>图片翻译API</strong></p></td><td><p><strong>输入图片后能获得图片上文字坐标信息和多语言译文</strong></p></td><td><p><strong>提供轻量版（flash）和通用版（general）两个选项，建议优先使用通用版：</strong></p><ul><li><p>轻量版（flash）：耗时低、适用于实时场景，仅支持中英互译</p></li><li><p>通用版（general）：高精度，保证结构复杂图片的翻译效果</p></li></ul></td><td><ul><li><p><strong>多语种能力：</strong>支持中、英、日、韩、法、西、葡等11个语种图片文字的提取和翻译</p></li><li><p><strong>多语言批量翻译：</strong>支持单次调用获取多种语言的翻译结果，提升高并发下的调用效率，适用于跨境电商、本地化运营等场景</p></li></ul></td></tr><tr><td><p><strong>网页翻译SDK</strong></p></td><td><p><strong>网页翻译插件，支持网页全文内容实时翻译</strong></p></td><td><p>暂时不提供模型选项</p></td><td><ul><li><p><strong>实现质量&amp;耗时平衡：</strong>通过网页智能解析、内容动态适应、可视区域智能加载、智能段落划分等策略，让上下文保持连贯的同时弱化延迟体感</p></li><li><p><strong>简单易用：</strong>无需做网页内容处理和解析，接入后“即插即用”，高效实现网页内容的国际化</p></li></ul></td></tr><tr><td><p><strong>文档翻译API</strong></p></td><td><p><strong>支持将DOCX、DOC、TXT、XLSX、PPTX、PDF、DITA、MARKDOWN等多格式的文件翻译到目标语言，高度还原文档格式，支持PDF文档内图片翻译</strong></p></td><td><p><strong>提供轻量版（flash）和专业版（plus）两个选项：</strong></p><ul><li><p>轻量版（flash）：高性价比、响应速度快</p></li><li><p>专业版（plus）：多语言综合效果好，结构复杂的文本理解更精准</p></li></ul></td><td><ul><li><p><strong>文档格式还原：</strong>译后文档格式高度还原，效率、体验大幅提升</p></li><li><p><strong>强可控性：</strong>提供术语自适应干预、领域风格提示等功能，让译文精准贴合领域特定需求</p></li></ul></td></tr></tbody></table>

<a id="使用方式"></a>

<a id="5f0a400f007w1"></a>

## 使用方式

为确保您能顺利使用本产品，请先前往[服务开通地址](https://common-buy.aliyun.com/?commodityCode=sfm_TongyiTranslate_public_cn)或[百炼应用卡片页面](https://bailian.console.aliyun.com/?tab=app#/app/app-market/mt)完成服务开通。

> **重要**
>
> 为满足特定业务场景下对原文高保真的需求，我们提供内容滤网跳过功能（skipCsiCheck）。此功能默认关闭。出于安全合规要求，请联系技术支持团队提交开通申请。审批通过后，我们将为您单独开启。

<a id="计量计费"></a>

<a id="ec47017271a1t"></a>

## 计量计费

<table><thead><tr><th><p><strong>接口类型</strong></p></th><th><p><strong>模型选项</strong></p></th><th colspan="2"><p><strong>目录单价</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>文本翻译</p></td><td><p>轻量版（flash）</p></td><td><p>输入：0.0008元/千tokens</p></td><td><p>输出：0.0024元/千tokens</p></td></tr><tr><td><p>专业版（plus）</p></td><td><p>输入：0.012元/千tokens</p></td><td><p>输出：0.036元/千tokens</p></td></tr><tr><td rowspan="2"><p>图片翻译</p></td><td><p>轻量版（flash）</p></td><td><p>输入：0.02元/张图</p></td><td><p>-</p></td></tr><tr><td><p>通用版（general）</p></td><td><p>输入：0.0025元/张图</p></td><td><p>-</p></td></tr><tr><td><p>网页翻译</p></td><td><p>-</p></td><td><p>输入：0.0008元/千tokens</p></td><td><p>输出：0.0024元/千tokens</p></td></tr><tr><td rowspan="4"><p>文档翻译</p></td><td rowspan="2"><p>轻量版（flash）</p></td><td><p>文字输入：0.2元/页</p></td><td><p>-</p></td></tr><tr><td><p>图片输入：0.01元/页</p></td><td><p>-</p></td></tr><tr><td rowspan="2"><p>专业版（plus）</p></td><td><p>文字输入：0.3元/页</p></td><td><p>-</p></td></tr><tr><td><p>图片输入：0.01元/页</p></td><td><p>-</p></td></tr></tbody></table>

> **说明**
>
> -   付费方式：按照使用次数后付费，仅开通服务不会产生费用，费用发生以实际调用为准。
> -   调用限制：对于每个账号，限流为5RPM（每分钟不超过5次请求）。
> -   计费逻辑：无免费额度，按照“成功的请求量\*单价”进行计费。
> -   出账方式：跟百炼统一出账周期和扣费规则一致，出账周期为一小时，请预先保证账户余额充足，以免账户欠费影响您的业务。

<a id="语种列表"></a>

<a id="ede9408cb0w21"></a>

## 语种列表

发起翻译请求时，可使用**英文全拼**或**语种编码**指定源语言和目标语言。文本、图片与文档翻译均支持源语言自动检测（auto）。

<a id="文本-网页与文档翻译"></a>

<a id="5bf29eb861ojq"></a>

### 文本、网页与文档翻译

| 英文全拼 | 中文名称 | 语种编码 |
| --- | --- | --- |
| English | 英语 | en |
| Chinese | 简体中文 | zh |
| Traditional Chinese | 繁体中文 | zh\_tw |
| Russian | 俄语 | ru |
| Japanese | 日语 | ja |
| Korean | 韩语 | ko |
| Spanish | 西班牙语 | es |
| French | 法语 | fr |
| Portuguese | 葡萄牙语 | pt |
| German | 德语 | de |
| Italian | 意大利语 | it |
| Thai | 泰语 | th |
| Vietnamese | 越南语 | vi |
| Indonesian | 印度尼西亚语 | id |
| Malay | 马来语 | ms |
| Arabic | 阿拉伯语 | ar |
| Hindi | 印地语 | hi |
| Hebrew | 希伯来语 | he |
| Burmese | 缅甸语 | my |
| Tamil | 泰米尔语 | ta |
| Urdu | 乌尔都语 | ur |
| Bengali | 孟加拉语 | bn |
| Polish | 波兰语 | pl |
| Dutch | 荷兰语 | nl |
| Romanian | 罗马尼亚语 | ro |
| Turkish | 土耳其语 | tr |
| Khmer | 高棉语 | km |
| Lao | 老挝语 | lo |
| Cantonese | 粤语 | yue |
| Czech | 捷克语 | cs |
| Greek | 希腊语 | el |
| Swedish | 瑞典语 | sv |
| Hungarian | 匈牙利语 | hu |
| Danish | 丹麦语 | da |
| Finnish | 芬兰语 | fi |
| Ukrainian | 乌克兰语 | uk |
| Bulgarian | 保加利亚语 | bg |
| Serbian | 塞尔维亚语 | sr |
| Telugu | 泰卢固语 | te |
| Afrikaans | 南非荷兰语 | af |
| Armenian | 亚美尼亚语 | hy |
| Assamese | 阿萨姆语 | as |
| Asturian | 阿斯图里亚斯语 | ast |
| Basque | 巴斯克语 | eu |
| Belarusian | 白俄罗斯语 | be |
| Bosnian | 波斯尼亚语 | bs |
| Catalan | 加泰罗尼亚语 | ca |
| Cebuano | 宿务语 | ceb |
| Croatian | 克罗地亚语 | hr |
| Egyptian Arabic | 埃及阿拉伯语 | arz |
| Estonian | 爱沙尼亚语 | et |
| Galician | 加利西亚语 | gl |
| Georgian | 格鲁吉亚语 | ka |
| Gujarati | 古吉拉特语 | gu |
| Icelandic | 冰岛语 | is |
| Javanese | 爪哇语 | jv |
| Kannada | 卡纳达语 | kn |
| Kazakh | 哈萨克语 | kk |
| Latvian | 拉脱维亚语 | lv |
| Lithuanian | 立陶宛语 | lt |
| Luxembourgish | 卢森堡语 | lb |
| Macedonian | 马其顿语 | mk |
| Maithili | 迈蒂利语 | mai |
| Maltese | 马耳他语 | mt |
| Marathi | 马拉地语 | mr |
| Mesopotamian Arabic | 美索不达米亚阿拉伯语 | acm |
| Moroccan Arabic | 摩洛哥阿拉伯语 | ary |
| Najdi Arabic | 内志阿拉伯语 | ars |
| Nepali | 尼泊尔语 | ne |
| North Azerbaijani | 北阿塞拜疆语 | az |
| North Levantine Arabic | 北黎凡特阿拉伯语 | apc |
| Northern Uzbek | 北乌兹别克语 | uz |
| Norwegian Bokmål | 书面语挪威语 | nb |
| Norwegian Nynorsk | 新挪威语 | nn |
| Occitan | 奥克语 | oc |
| Odia | 奥里亚语 | or |
| Pangasinan | 邦阿西楠语 | pag |
| Sicilian | 西西里语 | scn |
| Sindhi | 信德语 | sd |
| Sinhala | 僧伽罗语 | si |
| Slovak | 斯洛伐克语 | sk |
| Slovenian | 斯洛文尼亚语 | sl |
| South Levantine Arabic | 南黎凡特阿拉伯语 | ajp |
| Swahili | 斯瓦希里语 | sw |
| Tagalog | 他加禄语 | tl |
| Ta’izzi-Adeni Arabic | 塔伊兹-亚丁阿拉伯语 | acq |
| Tosk Albanian | 托斯克阿尔巴尼亚语 | sq |
| Tunisian Arabic | 突尼斯阿拉伯语 | aeb |
| Venetian | 威尼斯语 | vec |
| Waray | 瓦来语 | war |
| Welsh | 威尔士语 | cy |
| Western Persian | 西波斯语 | fa |

<a id="图片翻译"></a>

<a id="0ccb5a70a1erz"></a>

### 图片翻译

<a id="轻量版flash"></a>

<a id="091755ad7eeqb"></a>

#### 轻量版Flash

支持将中文或英文图片翻译到日、韩、法、西等12个小语种

<table><thead><tr><th colspan="3"><p>译图语种</p></th></tr></thead><tbody><tr><td><p>英文全拼</p></td><td><p>中文名称</p></td><td><p>语种编码</p></td></tr><tr><td><p>Chinese</p></td><td><p>简体中文</p></td><td><p>zh</p></td></tr><tr><td><p>English</p></td><td><p>英语</p></td><td><p>en</p></td></tr><tr><td><p>Japanese</p></td><td><p>日语</p></td><td><p>ja</p></td></tr><tr><td><p>Korean</p></td><td><p>韩语</p></td><td><p>ko</p></td></tr><tr><td><p>French</p></td><td><p>法语</p></td><td><p>fr</p></td></tr><tr><td><p>Spanish</p></td><td><p>西语</p></td><td><p>es</p></td></tr><tr><td><p>Portuguese</p></td><td><p>葡萄牙语</p></td><td><p>pt</p></td></tr><tr><td><p>Italian</p></td><td><p>意大利语</p></td><td><p>it</p></td></tr><tr><td><p>Russian</p></td><td><p>俄语</p></td><td><p>ru</p></td></tr><tr><td><p>Thai</p></td><td><p>泰语</p></td><td><p>th</p></td></tr><tr><td><p>Vietnamese</p></td><td><p>越南语</p></td><td><p>vi</p></td></tr><tr><td><p>Malay</p></td><td><p>马来语</p></td><td><p>ms</p></td></tr><tr><td><p>Indonesian</p></td><td><p>印尼语</p></td><td><p>id</p></td></tr><tr><td><p>Arabic</p></td><td><p>阿拉伯语</p></td><td><p>ar</p></td></tr></tbody></table>

<a id="通用版general"></a>

<a id="fd374072f9tre"></a>

#### 通用版General

<table><thead><tr><th colspan="3"><p><strong>原图语种</strong></p></th><th colspan="3"><p><strong>译图语种</strong></p></th></tr></thead><tbody><tr><td><p>英文全拼</p></td><td><p>中文名称</p></td><td><p>语种编码</p></td><td><p>英文全拼</p></td><td><p>中文名称</p></td><td><p>语种编码</p></td></tr><tr><td><p>Chinese</p></td><td><p>简体中文</p></td><td><p>zh</p></td><td><p>Chinese</p></td><td><p>简体中文</p></td><td><p>zh</p></td></tr><tr><td><p>English</p></td><td><p>英语</p></td><td><p>en</p></td><td><p>English</p></td><td><p>英语</p></td><td><p>en</p></td></tr><tr><td><p>Japanese</p></td><td><p>日语</p></td><td><p>ja</p></td><td><p>Japanese</p></td><td><p>日语</p></td><td><p>ja</p></td></tr><tr><td><p>Korean</p></td><td><p>韩语</p></td><td><p>ko</p></td><td><p>Korean</p></td><td><p>韩语</p></td><td><p>ko</p></td></tr><tr><td><p>French</p></td><td><p>法语</p></td><td><p>fr</p></td><td><p>French</p></td><td><p>法语</p></td><td><p>fr</p></td></tr><tr><td><p>Spanish</p></td><td><p>西语</p></td><td><p>es</p></td><td><p>Spanish</p></td><td><p>西语</p></td><td><p>es</p></td></tr><tr><td><p>Portuguese</p></td><td><p>葡萄牙语</p></td><td><p>pt</p></td><td><p>Portuguese</p></td><td><p>葡语</p></td><td><p>pt</p></td></tr><tr><td><p>Italian</p></td><td><p>意大利语</p></td><td><p>it</p></td><td><p>Italian</p></td><td><p>意大利语</p></td><td><p>it</p></td></tr><tr><td><p>Russian</p></td><td><p>俄语</p></td><td><p>ru</p></td><td><p>Russian</p></td><td><p>俄语</p></td><td><p>ru</p></td></tr><tr><td><p>German</p></td><td><p>德语</p></td><td><p>de</p></td><td><p>Thai</p></td><td><p>泰语</p></td><td><p>th</p></td></tr><tr><td><p>Vietnamese</p></td><td><p>越南语</p></td><td><p>vi</p></td><td><p>Vietnamese</p></td><td><p>越南语</p></td><td><p>vi</p></td></tr><tr><td rowspan="3" colspan="3"></td><td><p>Malay</p></td><td><p>马来语</p></td><td><p>ms</p></td></tr><tr><td><p>Indonesian</p></td><td><p>印尼语</p></td><td><p>id</p></td></tr><tr><td><p>Arabic</p></td><td><p>阿拉伯语</p></td><td><p>ar</p></td></tr></tbody></table>
