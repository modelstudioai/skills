# 通义多模态翻译

提供基于通义翻译大模型的编排和调试，在支持文本、图片、网页等内容多语言翻译的基础上，提供术语自适应干预、敏感词定义、译文格式转换等定制能力，让译文更符合不同业务场景的具体需求。

## **产品介绍**

**产品**

**功能介绍**

**模型选项**

**核心优势**

**文本翻译API**

**根据输入类型分为以下四个接口：**

-   文本单次翻译
    
-   文本批量翻译
    
-   html翻译：异步单次接口，能较好地保持住网页内容里的标签信息
    
-   长文本翻译：异步单次接口，无窗口长度限制
    

**每个接口均提供轻量版（turbo）和专业版（plus）两个选项：**

-   轻量版（turbo）：性能好、响应快
    
-   专业版（plus）：多语言效果均衡，能更好地理解复杂的内容
    

-   **强可控性**：提供术语自适应干预、敏感词表定义、领域风格提示、译文格式转换、自定义分隔符功能，让译文精准贴合领域特定需求
    
-   **多场景适配：**针对HTML等格式类输入和长篇章内容增强翻译效果，提升结构化数据的翻译还原度和全文术语一致性
    
-   **高可用保障：**在极端情况下自动启用高稳定性的兜底服务，确保翻译质量和稳定性
    

**图片翻译API**

**输入图片后能获得图片上文字坐标信息和多语言译文**

**提供轻量版（flash）和通用版（general）两个选项，建议优先使用通用版：**

-   轻量版（flash）：耗时低、适用于实时场景，仅支持中英互译
    
-   通用版（general）：高精度，保证结构复杂图片的翻译效果
    

-   **多语种能力：**支持中、英、日、韩、法、西、葡等11个语种图片文字的提取和翻译
    
-   **多语言批量翻译：**支持单次调用获取多种语言的翻译结果，提升高并发下的调用效率，适用于跨境电商、本地化运营等场景
    

**网页翻译SDK**

**网页翻译插件，支持网页全文内容实时翻译**

暂时不提供模型选项

-   **实现质量&耗时平衡：**通过网页智能解析、内容动态适应、可视区域智能加载、智能段落划分等策略，让上下文保持连贯的同时弱化延迟体感
    
-   **简单易用：**无需做网页内容处理和解析，接入后“即插即用”，高效实现网页内容的国际化
    

**文档翻译API**

**支持将DOCX、DOC、TXT、XLSX、PPTX、PDF、DITA、MARKDOWN等多格式的文件翻译到目标语言，高度还原文档格式，支持PDF文档内图片翻译**

**提供轻量版（turbo）和专业版（plus）两个选项：**

-   轻量版（turbo）：高性价比、响应速度快
    
-   专业版（plus）：多语言综合效果好，结构复杂的文本理解更精准
    

-   **文档格式还原：**译后文档格式高度还原，效率、体验大幅提升
    
-   **强可控性：**提供术语自适应干预、领域风格提示等功能，让译文精准贴合领域特定需求
    

## **使用方式**

为确保您能顺利使用本产品，请先前往[服务开通地址](https://common-buy.aliyun.com/?commodityCode=sfm_TongyiTranslate_public_cn)或[百炼应用卡片页面](https://bailian.console.aliyun.com/?tab=app#/app/app-market/mt)完成服务开通。

**重要**

为满足特定业务场景下对原文高保真的需求，我们提供内容滤网跳过功能（skipCsiCheck）。此功能默认关闭。出于安全合规要求，请联系技术支持团队提交开通申请。审批通过后，我们将为您单独开启。

## **计量计费**

**接口类型**

**模型选项**

**目录单价**

文本翻译

轻量版（turbo）

输入：0.0008元/千tokens

输出：0.0024元/千tokens

专业版（plus）

输入：0.012元/千tokens

输出：0.036元/千tokens

图片翻译

轻量版（flash）

输入：0.02元/张图

\-

通用版（general）

输入：0.0025元/张图

\-

网页翻译

\-

输入：0.0008元/千tokens

输出：0.0024元/千tokens

文档翻译

轻量版（turbo）

文字输入：0.2元/页

\-

图片输入：0.01元/页

\-

专业版（plus）

文字输入：0.3元/页

\-

图片输入：0.01元/页

\-

**说明**

-   付费方式：按照使用次数后付费，仅开通服务不会产生费用，费用发生以实际调用为准。
    
-   调用限制：对于每个账号，限流为5RPM（每分钟不超过5次请求）。
    
-   计费逻辑：无免费额度，按照“成功的请求量\*单价”进行计费。
    
-   出账方式：跟百炼统一出账周期和扣费规则一致，出账周期为一小时，请预先保证账户余额充足，以免账户欠费影响您的业务。
    

## **语种列表**

发起翻译请求时，可使用**英文全拼**或**语种编码**指定源语言和目标语言。文本、图片与文档翻译均支持源语言自动检测（auto）。

### **文本、网页与**文档**翻译**

**英文全拼**

**中文名称**

**语种编码**

English

英语

en

Chinese

简体中文

zh

Traditional Chinese

繁体中文

zh\_tw

Russian

俄语

ru

Japanese

日语

ja

Korean

韩语

ko

Spanish

西班牙语

es

French

法语

fr

Portuguese

葡萄牙语

pt

German

德语

de

Italian

意大利语

it

Thai

泰语

th

Vietnamese

越南语

vi

Indonesian

印度尼西亚语

id

Malay

马来语

ms

Arabic

阿拉伯语

ar

Hindi

印地语

hi

Hebrew

希伯来语

he

Burmese

缅甸语

my

Tamil

泰米尔语

ta

Urdu

乌尔都语

ur

Bengali

孟加拉语

bn

Polish

波兰语

pl

Dutch

荷兰语

nl

Romanian

罗马尼亚语

ro

Turkish

土耳其语

tr

Khmer

高棉语

km

Lao

老挝语

lo

Cantonese

粤语

yue

Czech

捷克语

cs

Greek

希腊语

el

Swedish

瑞典语

sv

Hungarian

匈牙利语

hu

Danish

丹麦语

da

Finnish

芬兰语

fi

Ukrainian

乌克兰语

uk

Bulgarian

保加利亚语

bg

Serbian

塞尔维亚语

sr

Telugu

泰卢固语

te

Afrikaans

南非荷兰语

af

Armenian

亚美尼亚语

hy

Assamese

阿萨姆语

as

Asturian

阿斯图里亚斯语

ast

Basque

巴斯克语

eu

Belarusian

白俄罗斯语

be

Bosnian

波斯尼亚语

bs

Catalan

加泰罗尼亚语

ca

Cebuano

宿务语

ceb

Croatian

克罗地亚语

hr

Egyptian Arabic

埃及阿拉伯语

arz

Estonian

爱沙尼亚语

et

Galician

加利西亚语

gl

Georgian

格鲁吉亚语

ka

Gujarati

古吉拉特语

gu

Icelandic

冰岛语

is

Javanese

爪哇语

jv

Kannada

卡纳达语

kn

Kazakh

哈萨克语

kk

Latvian

拉脱维亚语

lv

Lithuanian

立陶宛语

lt

Luxembourgish

卢森堡语

lb

Macedonian

马其顿语

mk

Maithili

迈蒂利语

mai

Maltese

马耳他语

mt

Marathi

马拉地语

mr

Mesopotamian Arabic

美索不达米亚阿拉伯语

acm

Moroccan Arabic

摩洛哥阿拉伯语

ary

Najdi Arabic

内志阿拉伯语

ars

Nepali

尼泊尔语

ne

North Azerbaijani

北阿塞拜疆语

az

North Levantine Arabic

北黎凡特阿拉伯语

apc

Northern Uzbek

北乌兹别克语

uz

Norwegian Bokmål

书面语挪威语

nb

Norwegian Nynorsk

新挪威语

nn

Occitan

奥克语

oc

Odia

奥里亚语

or

Pangasinan

邦阿西楠语

pag

Sicilian

西西里语

scn

Sindhi

信德语

sd

Sinhala

僧伽罗语

si

Slovak

斯洛伐克语

sk

Slovenian

斯洛文尼亚语

sl

South Levantine Arabic

南黎凡特阿拉伯语

ajp

Swahili

斯瓦希里语

sw

Tagalog

他加禄语

tl

Ta’izzi-Adeni Arabic

塔伊兹-亚丁阿拉伯语

acq

Tosk Albanian

托斯克阿尔巴尼亚语

sq

Tunisian Arabic

突尼斯阿拉伯语

aeb

Venetian

威尼斯语

vec

Waray

瓦来语

war

Welsh

威尔士语

cy

Western Persian

西波斯语

fa

### **图片翻译**

#### **轻量版Flash**

支持将中文或英文图片翻译到日、韩、法、西等12个小语种

译图语种

英文全拼

中文名称

语种编码

Chinese

简体中文

zh

English

英语

en

Japanese

日语

ja

Korean

韩语

ko

French

法语

fr

Spanish

西语

es

Portuguese

葡萄牙语

pt

Italian

意大利语

it

Russian

俄语

ru

Thai

泰语

th

Vietnamese

越南语

vi

Malay

马来语

ms

Indonesian

印尼语

id

Arabic

阿拉伯语

ar

#### **通用版General**

**原图语种**

**译图语种**

英文全拼

中文名称

语种编码

英文全拼

中文名称

语种编码

Chinese

简体中文

zh

Chinese

简体中文

zh

English

英语

en

English

英语

en

Japanese

日语

ja

Japanese

日语

ja

Korean

韩语

ko

Korean

韩语

ko

French

法语

fr

French

法语

fr

Spanish

西语

es

Spanish

西语

es

Portuguese

葡萄牙语

pt

Portuguese

葡语

pt

Italian

意大利语

it

Italian

意大利语

it

Russian

俄语

ru

Russian

俄语

ru

German

德语

de

Thai

泰语

th

Vietnamese

越南语

vi

Vietnamese

越南语

vi

Malay

马来语

ms

Indonesian

印尼语

id

Arabic

阿拉伯语

ar
