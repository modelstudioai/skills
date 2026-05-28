# 如何进行基于对话分析Agent方式创建应用

本文档介绍了如何通过对话分析Agent方式创建应用

## **创建应用**

-   第一步：首先点击**我的应用**按钮，再点击**创建应用**按钮；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935525.png)
    
-   第二步：进入新建应用弹窗，编辑应用名称与应用创建方式。点击**确定**。进入调试窗口。
    
    -   **应用名称：**根据实际业务需要修改应用名称。
        
    -   **应用创建方式：**
        
        -   这里选择**基于对话分析Agent创建**：通过预置最佳实践示例或上传对话数据，体验大模型生成式摘要、总结、服务质检等全场景应用能力。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935528.png)
            

### 基于对话分析Agent创建

**说明**

注意：当选择基于对话分析Agent创建方式，只有选择自**定义指令**\-**专业构建模式**可以用图片分析，其他方式无法对图片进行分析。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006405.png)

进入已经创建完成的应用中后，可以选择**对话分析Agent**、**自定义指令**方式。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914644.png)

1.  #### **选择对话分析Agent方式**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914645.png)
    
    **对话分析维度：**可以根据实际业务需求的需要通过对话分析Agent来选择对应的维度。
    
    -   **标准指令：**已预置标准prompt，可快速生成理想结果。可选值为【标题、摘要、关键词、Q&A、问题解决方案】，至少选择一个选项。
        
    -   **高级指令：**服务质检、标签分类等高级指令有一定的业务属性，该部分指令在示例通话中已预置标准prompt，若自行上传通话数据且对结果有一定要求，建议在预置指令模板→专业模式中编辑自定义指令进行调试。可选值为【服务质检、关键信息、标签分类】。
        
    
    **分析对象类型：**根据自己业务需要分析的数据类型选择【纯文本、语音】。当选择**纯文本**时，可以上传不超过15000字的文本内容，同时我们还提供了行业对话示例来进行测试；当选择**语音**时，支持单个不超过40MB的WAV或MP3格式文件，上传完成后会自动将其转译为文本信息内容。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9479940671/p1008496.png)
    
    **信息内容：**需要按照以下格式编写对话信息，可以通过使用已经提供的行业对话示例。
    
    -   对话信息建议按如下格式填写：
        
        客户：xxx
        
        客服：xxx
        
        客户：xxx
        
        客服：xxx
        
    -   可直接插入内置的行业对话示例文本。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914647.png)
        
    
    **点击“测试”按钮，查看输出结果：**测试出来的结果生成的指令与我选择的对话分析维度相对应。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0986579371/p914651.png)
    
2.  #### **选择自定义模板方式**
    
    可以选择简单构建模式&专业构建模式。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914696.png)
    
    -   ##### **简单构建模式说明** ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914697.png)
        
        -   **模型配置**：通义晓蜜-Plus、通义晓蜜-Turbo。
            
        -   **指令类型：**可以根据实际业务需求分析的全部维度，根据选择的标准指令与高级指令，在指令信息中编辑指令的prompt。
            
            -   标准指令：可以选择【标题、摘要、关键词、Q&A、问题解决方案】，并在下方指令信息中展示出系统内置prompt，可以对其进行自定义修改。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850108.png)
                
            -   高级指令：可以选择【服务质检、关键信息、标签分类】，并在下面指令信息中展示对应配置，进行自定义修改。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6344413771/p1057646.png)
                
                -   **服务质检：**对通话中存在的客户情绪、敏感词、服务质量等内容进行检测。可根据业务需要质检的场景和质检项。
                    
                -   **质检项（名称+描述）：**设置服务质检中需要质检的名称与描述。
                    
                -   **关键信息（名称+类型）：**提取通话中配置的关键信息，通过名称与类型配置。
                    
                -   **标签分类（名称+描述）：**对通话内容进行分类定义，标签长度不超过10个字。
                    
        -   **分析对象类型：**需要按照以下格式编写对话信息，可选择纯文本、语音两种方式。
            
            -   对话信息建议按如下格式填写：
                
                客户：xxx
                
                客服：xxx
                
                客户：xxx
                
                客服：xxx
                
            -   可以选择行业对话示例进行插入内置对话文本。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850123.png)
                
        -   **点击“测试”按钮，查看测试结果。**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0986579371/p914710.png)
            
    -   ##### 专业构建模式说明![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914716.png)
        
        **说明**
        
        在模式切换时，当前模式所编辑的内容不再生效，对话内容将会重置。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6344413771/p1057648.png)
        
        -   **模型配置：**通义晓蜜-Plus、通义晓蜜-Turbo。
            
        -   **选择指令模板：**选择指令模板，可以选择直接使用官方预置模板，当前线上提供了总结摘要、信息抽取、服务质检、标签分类、多指令任务，共五类模板。同时支持自定义指令模板，或在官方预置模板基础上自定义修改的指令模板。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006412.png)
            
        -   **保存指令模板：**在自定义编写指令信息或者自定义修改系统行业示例后，可以点击“保存指令模板”按钮，进行保存，选择指令模板保存方式，可选【新增指令模板、覆盖已有指令模板】，在“指令模板管理”中可以查看。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006414.png)
            
        -   **指令模板管理：**可以查看预置模板和自定义保存的模板指令。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914728.png)
            
        -   **变量配置：**除了内置${field}、${dialogue}两个变量以外，如需在分析过程中引用更多变量，可以完成变量配置。测试数据可以作为测试过程中的模拟数据，临时使用。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939566.png)
            
            -   在编辑完成后，即可在指令信息中插入，使用“/”进行插入保存的变量。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939584.png)
                
        -   **分析对象类型：**可以分为三种，纯文本、语音、图片，同时支持添加知识库进行辅助分析，支持添加热词组有助于提升语音转译准确性。
            
            -   **知识库：**开启后可添加文档、表格、图片等类型知识用于辅助分析，当分析对象类型选择为图片时无法使用知识库。具体介绍可参考文档：[知识库的使用](https://help.aliyun.com/zh/model-studio/using-the-knowledge-base)。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6344413771/p1057649.png)
                
            -   **选择文本时**：需要按照以下格式编写对话信息，同时也可以通过使用已经提供的行业对话示例。
                
                客户：xxx
                
                客服：xxx
                
                客户：xxx
                
                客服：xxx![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006434.png)
                
            -   **选择语音时：**自定义上传一个不超过40MB、WAV、MP3格式的文件，同时可以选择添加/新建热词组，提升语音转译效果![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006437.png)
                
                上传完成后将自动识别语音内容，并可以设置客户/客服先发言顺序。
                
            -   **选择图片识别后**：可点击上传一张不超过10MB、JPEG/JPG/PNG等常见图片格式，上传成功后可以通过指令信息对图片进行检测分析。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006443.png)
                
        -   **字段信息：**当使用“信息抽取预置模板”、“多指令模板”创建指令任务，可引入变量${fields}填写字段信息。
            
            填写格式为：字段名：字段描述。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850538.png)
            
        -   点击**“测试”**按钮**，**查看输出结果![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939588.png)
