# qwen-long

Qwen-Long是在通义千问针对超长上下文处理场景的大语言模型，支持中文、英文等不同语言输入，支持最长1000万tokens(约1500万字或1.5万页文档)的超长上下文对话。配合同步上线的文档服务，可支持文本文件（ TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV）和图片文件（BMP、PNG、JPG/JPEG、GIF 以及PDF扫描件）的解析和对话。说明：通过HTTP直接提交请求，支持1M tokens长度，超过此长度建议通过文件方式提交。

## 推理服务供应商

`qwen-long`模型的推理服务供应商为阿里云百炼。

## 模型能力

能力项

支持情况

能力项

支持情况

输入模态

**Text**

输出模态

**Text**

模型体验

支持

Function Calling

不支持

结构化输出

支持 JSON Object

联网搜索

不支持

前缀续写

不支持

上下文缓存

不支持

批量推理

不支持

模型调优

不支持

`qwen-long`仅支持 JSON Object 模式。参数设置与调用方法请参见[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)。

## 上下文限制

参数

值

参数

值

最大输入长度

10000000

最大输出长度

8192

上下文长度

10000000

## 模型价格

本文仅展示模型调用原价，不包含限时优惠等活动信息，请前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)查看活动优惠。

#### 华北2（北京）

计费项

价格（元）

单位

输入

0.5

每百万tokens

输出

2

每百万tokens

输入（Batch File）

0.25

每百万tokens

输出（Batch File）

1

每百万tokens

## 限流

#### 华北2（北京）

参数

值

RPM（每分钟请求数）

1200

TPM（每分钟tokens）

3,000,000
