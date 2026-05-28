# 如何基于自定义方式创建应用

本文档介绍了如何通过自定义方式创建应用

## **创建应用**

-   第一步：首先点击**我的应用**，再点击**创建应用**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935525.png)
    
-   第二步：进入新建应用弹窗，编辑应用名称与应用创建方式。点击**确定**。进入应用调试界面。
    
    -   **应用名称：**根据实际业务需要修改应用名称。
        
    -   **应用创建方式：**
        
        -   这里选择**自定义创建**：通过编写自定义指令（Prompt）来构建应用逻辑，用户可使用内置或自定义指令模板进行测试，适合有一定经验的人员。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935528.png)
            

## **应用配置**

进入已经创建完成的应用中进行配置。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009398.png)

-   **模型配置：**通义晓蜜Plus 和 Turbo 模型仅支持语音与文本分析；当分析对象为图片时，系统将默认使用通义晓蜜VL模型，该模型不可手动选择。
    
-   **指令信息：**通过编写指令信息来配置对应的任务、格式、要求等，来完成对应分析任务。
    
    -   **变量配置：**若需要在对话过程中引用更多变量可以在此配置，在指令编辑器中输入 `/` 可触发变量自动补全，选择后插入对应变量引用。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009509.png)
        
    -   **选择指令模板：**同时可以选择直接使用官方预置模板，当前线上提供了总结摘要、信息抽取、服务质检、标签分类、多指令任务，共五类模板。同时支持自定义指令模板，或在官方预置模板基础上自定义修改的指令模板。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009498.png)
        
    -   **保存指令模板：**在编写指令信息或者自定义修改系统行业示例后，可以点击“保存指令模板”按钮，进行保存，选择指令模板保存方式，可选【新增指令模板、覆盖已有指令模板】，在“指令模板管理”中可以查看。选择‘覆盖已有指令模板’，需从下拉列表中选择目标模板名称。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009505.png)
        
    -   **指令优化：**对编写完成的指令信息进行AI优化。![指令优化示例图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009511.png)
        
-   **分析对象类型**
    
    分析对象类型可以分为三种，纯文本、语音、图片，同时支持添加知识库进行辅助分析，支持添加热词组有助于提升语音转译准确性。
    
    -   **知识库：**开启后可添加文档、表格、图片等类型知识用于辅助分析，当分析对象类型选择为图片时无法使用知识库。具体介绍可参考文档：[知识库的使用](https://help.aliyun.com/zh/model-studio/using-the-knowledge-base)。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3624933771/p1059909.png)
        
    -   **选择文本时**：需要按照以下格式编写对话信息，同时也可以通过使用已经提供的行业对话示例。
        
        客户：xxx
        
        客服：xxx
        
        客户：xxx
        
        客服：xxx![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006434.png)
        
    -   **选择语音时：**自定义上传一个不超过40MB、WAV、MP3格式的文件，可以选择添加/新建热词组，提升语音转译效果![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006437.png)
        
        上传完成后将自动识别语音内容，并可以设置客户/客服先发言顺序。
        
    -   **选择图片识别后**：可点击上传一张不超过10MB、JPEG/JPG/PNG等常见图片格式，上传成功后可以通过指令信息对图片进行检测分析。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3501767571/p1006443.png)
        
-   **字段信息：**当需要获取到对话内容的字段信息时，可以使用“信息抽取预置模板”、“多指令模板”创建指令任务，同时也需要引入变量${fields}填写字段信息。
    
    填写格式为：字段名：字段描述。![字段信息示例图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850538.png)
    
-   点击**“测试”**按钮**，**查看测试结果![测试结果示例图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6379940671/p1009528.png)
