# 官方和第三方插件

大模型本身虽然具备强大的自然语言处理能力，但在特定领域或特定任务上，可能需要额外的功能辅助（如联网搜索实时信息、图像处理等）。阿里云百炼提供了一系列官方插件和三方插件。您可以根据具体需求选择适合的插件，进一步增强大模型功能，扩展其应用场景。

## **首次访问插件页面**

如果您的主账号或RAM用户（子账号）从未授权过AliyunServiceRoleForSFMAccessCloudAPI角色权限，您将无法访问插件。请参考以下操作进行授权。

## 主账号

如果您使用主账号登录阿里云百炼，请在**[插件](https://bailian.console.aliyun.com/#/plugin-market)**页面，勾选同意上述条款，单击**授权并进入**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9200547371/p907876.png)

## RAM用户（子账号）

如果您使用RAM用户（子账号）登录阿里云百炼，在**[插件](https://bailian.console.aliyun.com/#/plugin-market)**页面，勾选同意上述条款，单击**授权并进入**时，会有如下提示：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9200547371/p907884.png)

这是因为该RAM用户（子账号）不具备创建服务关联角色的权限。请按照下述操作先授予RAM用户（子账号）创建服务关联角色的权限。获得授权后，RAM用户（子账号）即可进入**插件**页面。

1.  授权RAM用户（子账号）创建服务关联角色的权限。
    
    1.  使用主账号登录[RAM控制台](https://ram.console.aliyun.com/)。
        
    2.  在左侧导航栏，选择**权限管理** **>** **权限策略**。
        
    3.  单击**创建权限策略**。
        
    4.  在**脚本编辑**的`Effect`、`Action`、`Resource`、`Condition`中分别输入以下脚本中的对应内容。
        
        ```
        {
            "Action": [
                "ram:CreateServiceLinkedRole"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Condition": {
                "StringEquals": {
                    "ram:ServiceName": "cloundapi-access.sfm.aliyuncs.com"
                }
            }
        }
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9200547371/p907881.png)
        
    5.  单击**确定**。
        
    6.  设置权限策略名称，单击**确定**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9200547371/p907882.png)
        
    7.  在左侧导航栏，选择。
        
    8.  找到待授权的RAM用户（子账号），单击RAM用户（子账号）**操作**列的**添加权限**。
        
    9.  在权限策略中选择刚才创建的权限策略，单击**确认新增授权**。
        
        至此，RAM用户（子账号）拥有了创建服务关联角色的权限。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9200547371/p907880.png)
        
2.  返回**[插件](https://bailian.console.aliyun.com/#/plugin-market)**页面，勾选同意上述条款，单击**授权并进入**。
    

## **官方插件说明**

**组件广场**中预置了阿里云百炼的官方插件，您无需配置其输入和输出参数，即可直接调用。

**官方插件名称**

**工具ID**

**说明**

**计费方案**

[Python代码解释器](#f8658b5c70a93)

code\_interpreter

使大模型可以执行Python代码片段，例如数学计算、数据分析与可视化、数据处理。

免费

[计算器](#12e61be838qub)

calculator

使大模型可以进行复杂的数学计算，例如计算“12313x13232”。

免费

[图片生成](#da38f8a429lso)

text\_to\_image

使大模型可以基于文本生成图片，例如“请画一只在笑的小狗”。

限时免费，需申请开通

[夸克搜索](#2c23406bd0sca)

quark\_search

使大模型可以搜索实时信息，查找公开的网络知识和信息，例如“杭州今天天气如何”。

> 夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情。

限时免费，需申请开通

[生成二维码](#dbdea0e23ap97)

generate\_qrcode

使大模型可以根据网站链接地址生成二维码，例如“请给阿里云百炼简介文档生成二维码：https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio”。

免费

[GitHub搜索](#112834c291kd3)

github\_search

使大模型可以在GitHub中搜索相关项目列表，例如“GitHub搜索：千问”。

免费

Python代码解释器

**示例输入**

**无插件时输出**

**有插件时输出**

```
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 100)
y1 = np.sqrt(1 + x**2)
y2 = -np.sqrt(1 + x**2)

plt.plot(x, y1, label='y = sqrt(1 + x^2)')
plt.plot(x, y2, label='y = -sqrt(1 + x^2)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Hyperbola')
plt.legend()
plt.show()
```

大模型应用无法执行Python代码，只会针对代码进行语言描述。

大模型应用具备了执行Python代码的能力，能够对数据进行可视化分析。

![python不插.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p834102.jpeg)

![python插.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p834103.jpeg)

> Python代码解释器插件不支持对外访问网络以及上传本地文件，可用依赖：json5~=0.9.6、jupyter\_client~=8.1.0、ipykernel~=6.25.0、seaborn、sympy、pydantic~=1.10.8、pillow~=9.4.0、fastapi~=0.101.1、dynaconf~=3.2.1、oss2~=2.18.1、matplotlib、starlette~=0.27.0、uvicorn~=0.23.2、requests~=2.31.0、scipy、html2text、matplotlib、pandas、pdf2image、pdfminer-six、pillow、pypdf、python-pptx、seaborn、sympy、wordcloud。

计算器

**示例输入**

**无插件时输出**

**有插件时输出**

12313x13232

大模型应用无法准确计算复杂数学问题，会出现计算错误的情况。正确结果应为162,925,616。

大模型应用具备了良好的计算能力，能够生成准确的计算结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906990.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906988.png)

图片生成

**示例输入**

**无插件时输出**

**有插件时输出**

请画一只在笑的小狗。

大模型应用无法直接绘制图片或图形，只能通过文字来描述画面。

大模型应用具备了直接绘制图片的能力，能够按指令生成小狗图片。

![图文.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p834097.jpeg)

![图文插.jpeg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p834098.jpeg)

夸克搜索

**示例输入**

**无插件时输出**

**有插件时输出**

杭州今天天气如何？

大模型应用无法获取实时信息，不能回答与实时天气有关的问题。

大模型应用具备了联网搜索，获取实时信息的能力，能够回答与实时天气有关的问题。

您可以在**输出参数**中查看大模型的回答参考了哪些网页。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906959.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906960.png)

生成二维码

**示例输入**

**无插件时输出**

**有插件时输出**

请给阿里云百炼简介文档生成二维码：https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio

大模型应用无法直接生成二维码，而是提供了将链接转化为二维码的操作指南。

大模型应用具备了生成二维码的能力，能够根据阿里云百炼简介文档的URL链接生成对应二维码。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906994.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906995.png)

GitHub搜索

**示例输入**

**无插件时输出**

**有插件时输出**

GitHub搜索：通义千问

大模型应用无法直接查询GitHub，而是给出了查询GitHub的操作指南。

大模型应用具备了查询GitHub项目的能力，能够给出与千问有关的项目列表。

> GitHub搜索插件目前支持检索出项目标题、链接和摘要，不支持访问项目详情。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906997.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3333247371/p906998.png)

组合使用插件

阿里云百炼支持在同一个任务中调用多个工具，下面是一个参考示例，您可以根据实际需求来选择插件。

**插件**

**示例输入**

**应用输出**

**夸克搜索**+**图片生成**+**生成二维码**

请根据杭州今天的天气画一幅画并将画的地址生成二维码。

![三插件.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p836940.png)

扫描二维码可以下载图片：

![35efefdb-753e-4594-a96d-b33d0aa1bee3-1.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7689504271/p836944.png)

### **调用官方插件**

**步骤一：在子业务空间调用官方插件时，需要先执行以下步骤为子业务空间授权。在默认业务空间调用官方插件不需要执行此步骤。**

1.  访问**[插件](https://bailian.console.aliyun.com/#/plugin-market)**页面，找到需要授权的目标插件并单击**查看详情**。
    
2.  单击**授权**，选择待授权的子业务空间，单击**确定**完成授权。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1145514671/p905060.png)
    

**步骤二：**[调用插件](#55bb7f428fczt)**。**

## 三方插件说明

第三方插件涵盖了商业服务、图像视频、学习教育等多个领域，并且经过了效果测试，您可以在开通后直接调用，无需进行额外配置。

### **调用三方插件**

**步骤一：开通三方插件。**

1.  访问**[插件](https://bailian.console.aliyun.com/#/plugin-market)**页面，找到目标插件并单击**查看详情**。
    
2.  选择套餐，单击**免费试用**或**立即购买**，根据界面指引开通插件。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5626098371/p910094.png)
    

**步骤二：**[调用插件](#55bb7f428fczt)**。**

## 调用插件

-   **方式一**：在**插件**页面，将工具添加至智能体应用。
    
    > 官方插件只能与**位于相同的业务空间**里的**智能体应用**关联。
    
    1.  找到目标插件，单击**添加至智能体**。
        
    2.  选择工具，单击**下一步**。
        
    3.  选择智能体应用，单击**确认添加**。
        
    4.  在应用详情页面，您可以看到工具已经自动添加。
        
        > 您也可以单击**选择插件**，继续添加其他工具。最多支持添加10个工具。智能体应用会根据输入选择调用一个或多个工具。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1145514671/p944232.png)
        
    5.  在输入框中与大模型进行对话，测试工具的使用效果是否符合预期。
        
    6.  测试完成后，发布应用。
        
-   **方式二**：访问**[应用管理](https://bailian.console.aliyun.com/#/app-center)**页面，在指定智能体或工作流应用内，添加指定插件，测试插件使用效果，并**发布**应用。具体操作请参见[智能体应用插件能力](https://help.aliyun.com/zh/model-studio/single-agent-application#550c6b3ddevkl)、[工作流应用插件节点](https://help.aliyun.com/zh/model-studio/workflow-application/#341c98019dvo8)。
    
-   **方式三**：通过Assistant API调用工具。请在[Assistant API文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)中搜索`tools`关键字，查看如何使用Assistant API调用工具。
    

## 获取工具ID

工具ID用于标识具体的工具。通过API调用工具时，需要正确传递工具ID，以确保请求能够被正确识别。

1.  在**插件**页面，找到目标插件并单击**查看详情**。
    
2.  在**插件工具**下获取工具ID。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0971396371/p905217.png)
    

## 相关文档

除了官方插件和三方插件外，百炼还支持用户引入自定义插件，具体操作请参见[自定义插件](https://help.aliyun.com/zh/model-studio/custom-plug-ins)。

## 常见问题

**夸克搜索和联网搜索（enable\_search）有什么区别？**

-   开启夸克搜索插件时，模型将直接调用插件执行搜索，并将搜索结果以文本形式返回，这些结果可以直接用于生成最终输出。夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情。
    
-   联网搜索（enable\_search）也是基于夸克搜索。联网搜索开启后，模型会尝试利用互联网上的信息来丰富其生成的内容，但不会完全依赖或返回互联网搜索结果。
