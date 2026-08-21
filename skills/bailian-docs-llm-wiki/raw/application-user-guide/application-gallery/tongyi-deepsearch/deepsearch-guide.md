# 操作指南

## **应用开通**

1.在阿里云百炼控制台的应用广场中点击[通义深度搜索](https://bailian.console.aliyun.com/#/app/app-market/deep-search/)卡片，进入**应用详情**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1019151.png)

2.首次试用时，点击右上角**免费开通**完成应用开通。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1019150.png)

## **应用管理**

点击**我的应用**进入应用管理页面。页面展示所有已创建的应用和应用key等信息，首次使用需要新增应用。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1019153.png)

## **应用配置**

点击应用卡片或新增应用进入应用配置界面。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1017819.png)

### **通用场景**

#### **1.互联网检索配置**

开启后支持实时互联网全栈信息检索，提升模型回答准确性及时效性。

##### **1.1检索策略**

在检索策略上，您可以在标准版本和自定义版本中选择一种。

###### **标准版本**

标准的检索策略，选择标准版本时，可以进一步根据对于搜索效果与搜索耗时的偏好选择不同的性能版本。

-   **Max版本**：效果优先，检索更深入，结果更全面，但响应时间较长
    
-   **Turbo版本**：速度优先，响应时间短，适合对实时性要求高的场景
    

###### **自定义版本**

选择自定义检索策略时，有更多的配置项可供更细化的配置。

-   支持限定检索时间范围
    
-   支持限定网站范围，最多添加20个网站，配置后**优先**从此范围网站检索信息，如果无匹配信息则会扩展到**全网**检索，网站录入时会自动去重
    
-   支持配置recall数量，数量越高信息越全，但会占用更多资源，增加耗时
    
-   支持配置网页读取开关，开启后搜索结果更详细但是耗时增加![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1017928.png)
    

##### **1.2策略选择**

可根据搜索效果与rt偏好选择max版本和turbo版本。

#### **2.自有知识库配置**

支持接入非百炼的自有知识库作为搜索来源，开启选项后可进行配置，点击添加知识库配置

输入知识库名称、知识库描述、服务地址、授权信息，点击“服务测试”，验证通过后点击“保存”以完成添加。可参考[示例文档](https://help.aliyun.com/zh/model-studio/docking-self-built-database)进行知识库对接配置。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1017934.png)

#### **3.百炼知识库**

支持接入[百炼知识库](https://bailian.console.aliyun.com/#/knowledge-base)，选择已配置的知识库，如无百炼知识库，需要先在百炼控制台创建知识库。并添加知识库描述，知识库描述需要认真填写，以便模型更好地理解。

#### **4.code\_interpret**

开启后可提升对复杂计算问题的效果。

#### **5.动态文件解析**

开启动态文件解析后，支持在输入query同时添加本地文件作为临时上下文知识。一次对话最多可上传10个文件，单文件不超过10MB，支持.docx/.doc/.pdf/.txt/.md等格式。

#### **7.生成配置**

开启输出报告后，对话最终会生成报告文件。关闭则不生成报告。

### **法律场景**

#### **1.策略选择**

选择法律场景下的具体研究策略。

##### **1.1法律研究**

对案件或判决内容进行深度分析，生成详细研究报告。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9019000771/p1049545.png)

##### **1.2法律阅卷**

对上传案件文件进行解析理解，提取关键要素，进行判决分析。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4219049671/p1047626.png)

###### **1.2.1案件检索**

会结合最新案件库检索，并持续自动更新，默认开启，不可关闭。

###### **1.2.2法条检索**

会结合最新国家官方法条作为检索信源，并持续自动更新，默认开启，不可关闭。

###### **1.2.3对话测试**

## 应用测试

**重要**

请注意，在配置页面测试也会计算使用量并产生费用。

### **通用场景**

配置完成后，可在输入框输入query进行测试，对话框展示chat内容、计划规划、思考过程、检索过程、工具调用过程等多个深度搜索研究步骤。最终生成报告文件。右侧报告区域支持“预览”模式和“代码”模式。切换到“代码”模式可查看用于生成报告的Markdown原文。提供文件下载。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3171121671/p1018037.png)

### **法律场景**

#### **法律研究**

配置完成后，可在输入框输入query进行测试，对话框展示chat内容、计划规划、思考过程、检索过程、工具调用过程等多个深度搜索研究步骤。最终生成报告文件。右侧报告区域支持“预览”模式和“代码”模式。切换到“代码”模式可查看用于生成报告的Markdown原文。提供文件下载。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9019000771/p1049548.png)

#### **法律阅卷**

支持上传多个法律文件进行解析，同时支持上传文件夹。上传后可点击“查看上传文件”进行查看和管理。支持对已上传文件进行拖拽移动、文件夹收纳管理、查看详情、删除等操作。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9019000771/p1049931.png)

支持根据上传的文件与应用对话，对文件进行阅卷，给出信息整理和法律分析。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9019000771/p1049451.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9019000771/p1049452.png)

## **应用发布**

配置测试完成后，可以点击发布，将应用发布后，可参考API文档正式使用。
