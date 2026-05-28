# 智能审校

本文档主要介绍全妙-智能审校的功能。

## **功能概述**

一款面向客户内容审查校对需求的产品，基于千问最新系列模型，支持文稿内容基础质量、安全合规、政敏性内容、企业专业知识、图片等审核场景，同时支持用户审校规则自定义、专有名词自定义，审核覆盖广，准确率高。

## **功能入口**

进入[妙笔](https://aimiaobi.console.aliyun.com/?product_code=g_broadscope_media&from=bailian#/home)，功能入口在**内容理解Agent>智能审校**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023481.png)

## **功能介绍**

### **审校页面介绍**

-   点击**审校设置**，查看审校的配置内容，如下图所示：
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023501.png)

-   审校的配置界面分为五个部分：
    
    -   审校维度设置：配置审校的维度，控制审校的范围，每个一级维度下都有细分维度；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023502.png)
        
    -   标记样式设置：可以配置在右侧的文本中标记的样式，整体审核的程度分为八个种类；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023504.png)
        
    -   词典：支持设置专有名词的校验规则，当前为管理界面，词典的配置方式可参考本文档中《词典的配置方法》；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023505.png)
        
    -   规则库：支持设置专属文本的审校的规则要求，当前为管理界面，规则库的配置方式可参考《规则库的配置方法》；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023506.png)
        
    -   信源：设置事实性审核的对应参考信源，信源的配置方式可参考《信源的配置方法》；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023508.png)
        

### **词典的配置方法**

1.  点击**词典**进入词典操作界面，支持通过手动单个和批量的方式添加；
    
2.  点击**新增**，打开词典新增弹窗，按照要求填写关键词、建议词、审核依据、例外语境；
    
    -   关键词：需要被审核出来的错误词；
        
    -   建议词：建议被修改成的正确词；
        
    -   审核依据：建议修改的意见；
        
    -   例外语境：输入带有当前建议词的语境。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023511.png)
    
3.  如下图为填写后的结果页面：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023516.png)
    
4.  点击**确定**即可添加成功；
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023518.png)
    
5.  在**审核维度设置**界面，需要选中自定义词库，在文本审核时会应用于审校；
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023519.png)
    

### **规则库的配置方法**

1.  点击**规则库**。进入自定义规则操作界面，按照模板要求上传自定义规则要求，模型即可分析规则内容，形成自定义规则要求，用于文本的审校；
    
2.  按照要求填写审校依据、依据出处，如图为创建的新的审校规则；![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023492.png)
    
3.  点击上传审校规则文件，系统会自动化进行解析审核规则结果。可下载查看解析后的结果，如果对审核结果没问题，就可点击**直接用作规则库**；如果对审核结果存在疑问，可重新**上传修改后的解析结果**；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023524.png)
    
4.  点击**直接用作规则库**，如图为添加成功状态；
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023525.png)
    
5.  在**审核维度设置**界面，需要选中规则库审核，在文本审核时会应用于审校；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023534.png)
    

### **信源的配置方法**

1.  点击**信源**进入信源配置操作界面；
    
2.  点击新增，按照要求添加http/https开头的信源地址，最多支持添加10个信源；
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023538.png)

3.  点击**确定**，如图为添加成功的状态；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023541.png)
    
4.  在**审核维度设置**界面，需要选中事实性审核-正确项或者事实性审核-正错误项，在文本审核时会应用于审校。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023542.png)
    

### **审校的效果展示**

1.  您可以选择上传本地文本、粘贴文本、在内容管理中的选择对应的文本，在左侧添加待审核内容，然后点击**开始审校**即可开始审校，右侧为审校的结果。
    

-   文本审校结果展示：
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023496.png)
    
-   图片审核结果展示：
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0135332671/p1023497.png)
    

2.  左侧的审核结果每个卡片展示审核原文和建议修改，当点开单个审核结果的卡片，可看见审核的维度，以及一些操作按钮。
    

-   采纳：当对审核结果判断为合理，即可点击**采纳**，左侧文本中即可进行修正；
    
-   忽略：当对审核结果判断为可修改可不修改，可点击**忽略**，右侧的审核结果中会删除当前审核结果项；
    
-   加入词典：支持对审核结果加入到词典中，可点击**加入词典**，可作为自定义词库用于其他文本的审校；
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1135332671/p1023537.png)
