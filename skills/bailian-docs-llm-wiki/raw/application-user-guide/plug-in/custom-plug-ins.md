# 自定义插件

当阿里云百炼的官方插件无法满足您的业务需求时，您可以通过创建自定义插件来扩展大模型的能力。本文档将引导您完成从创建、调试到使用的全过程，轻松集成所需 API。

## **工作流程**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5012457771/CAEQZhiBgICczru.2hkiIGNhZjkzMjM4YWJlZjRhOGU5NzA1Mzk1MWFkNGI1MzBh4867389_20250110113852.335.svg)

1.  **创建****/导入****插件：**定义插件的基础信息，或直接从云市场导入。
    
2.  **添加工具**（导入插件无需此步）**：**为插件配置具体的 API 路径、请求参数和返回数据。
    
3.  **调试与发布：**在线测试 API 的连通性，确保功能正常后发布。
    
4.  **在应用中使用：**将插件关联到智能体，通过对话测试或 API 集成来调用。
    

## **创建自定义插件**

## **创建个性化开发的插件**

### **步骤一：创建插件**

1.  访问**[插件](https://bailian.console.aliyun.com/?tab=app#/component-manage)**页面，单击**创建插件**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3387656671/p948583.png)
    
2.  填写插件信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5197455471/p948589.png)
    
    **插件名称**：输入具有语义的名称，支持中英文。
    
    > 示例：寝室公约查询工具test
    
    **插件描述**：对插件功能和使用场景的简要说明。能帮助大模型判断当前任务是否需要调用当前插件，请使用自然语言进行描述。
    
    > 示例：根据输入的数字索引查询特定条目的寝室公约内容。
    
    **插件URL**：插件的访问地址。
    
    > 示例：https://domitorgreement-plugin-example-icohrkdjxy.cn-beijing.fcapp.run
    
    -   同一个域名下，不同的路径被拆分成了不同的API（即下方创建工具中的**工具路径**）
        
    -   同一插件下的不同工具使用相同的域名，每个工具的工具路径对应一个独立的API
        
        例如：xx插件下包含两个API：
        
        查询：https://xxx.com/query
        
        删除：https://xxx.com/delete
        
        在这个示例中，`https://xxx.com`对应**插件URL**，`/query`和`/delete`对应下方创建工具中的**工具路径**。这表明该插件下包含两个工具。
        
    
    如需要鉴权请打开**是否鉴权**开关，填写鉴权配置信息。
    
    **鉴权参数说明**
    
    **Header列表**（可选）
    
    需要鉴权时，可以通过自定义Header传递鉴权信息。
    
    **是否鉴权**（可选）
    
    当阿里云百炼应用调用您的自定义插件时是否需要鉴权。此处是否需要鉴权主要取决于API提供方的安全策略。
    
    **鉴权类型**
    
    鉴权包括**服务级鉴权**和**用户级鉴权**两种方式。
    
    -   **位置**：支持将鉴权信息放在Header或Query中。
        
        -   **Header**：将鉴权信息放在HTTP请求头的Authorization字段中，这些信息在URL中不可见。
            
        -   **Query**：将鉴权信息放在URL中，例如https://example.com?api\_key=123456。
            
    -   **参数名**：如果将鉴权信息放在Query中需填写鉴权时使用的参数，如“api\_key”。如果将鉴权信息放在Header中将默认此参数为“Authorization”。
        
    -   **Type**：
        
        -   **basic**：不会在您提供的Token前加任何内容；
            
        -   **bearer**：会在Token前增加“Bearer”；
            
        -   **appcode**：会在Token前增加“APPCODE”。
            
        
        两种type都会放在鉴权参数字段中。例如：选择bearer，则调用插件时会变成（“Authorization”： “Bearer <YOUR\_TOKEN>”）。
        
    -   **Token**（服务级鉴权）：从API提供方获取的鉴权Token，如API Key。
        
    
3.  填写完成后单击**确认创建插件** > **创建工具**或单击**继续添加工具**。
    

### **步骤二：创建工具**

1.  填写工具信息、配置输入/输出参数以及高级配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5197455471/p948908.png)
    
    **工具参数说明**
    
    **工具信息**
    
    **工具名称**
    
    输入具有语义的名称，支持中英文。
    
    **工具描述**
    
    对工具功能和使用场景的简要说明。
    
    帮助大模型判断当前任务是否需要调用该工具，请使用自然语言进行描述，尽量给出使用示例。
    
    **工具路径**
    
    指向**插件URL**的相对路径。
    
    字段名必须以正斜杠（/）开头。
    
    此路径将拼接到**插件URL**上，以构建完整的URL。
    
    **请求方法**
    
    根据实际需求选择GET或POST请求方法来调用API接口。
    
    **提交方式**
    
    请求或响应的编码类型。
    
    -   **application/json**：主体内容是JSON格式的数据。
        
    -   **application/x-www-form-urlencoded**：将表单数据编码为键值对。
        
        -   这种编码方式用于 POST 请求，表单数据编码为键值对，并通过 URL 编码传输。多个键值对之间用 & 分隔，每个键和值之间用 = 分隔。URL 编码会将特殊字符转换为 % 后跟两位十六进制数的形式。例如，空格会被编码为 %20，& 会被编码为 %26，= 会被编码为 %3D
            
        -   示例：`name=John Doe&age=25` 被编码为 `name=John%20Doe&age=25`
            
    
    **配置输入参数与输出参数**
    
    **配置输入参数**
    
    单击**增加入参**，配置参数信息。
    
    **参数名称**：尽可能带有含义，帮助大模型理解当前需要识别的参数信息是什么。例如`city`。
    
    **参数描述**：对该入参的功能描述，要简练且准确，帮助大模型进一步理解取参的方式。例如，`date`，描述为日期的同时，可以再进一步描述date的形式，比如`yyyy-MM-dd`。
    
    **类型**：指参数类型。
    
    **重要**
    
    Object类型下的子属性不能为空。请单击该对象行末的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905454.png)图标新增子属性。
    
    **传参方式**：要设置准确。
    
    -   **大模型识别**：表示该参数的值需要大模型从用户输入中提取。
        
    -   **业务透传**：表示该参数的值从外部主动透传，传递过程中不对数据进行处理或修改。
        
        使用DashScope SDK或HTTP接口调用应用时，插件中的业务透传类型的输入参数信息通过 `biz_params`和`user_defined_params`传递给应用。具体请参见[应用的参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters)。
        
    
    **配置输出参数**
    
    单击**增加出参**，配置参数信息，所有参数均为**必填**项。
    
    大模型会根据出参的定义，结合用户的问题，对API返回的结果进行筛选、重新组合，作为最终的答案返回给用户。
    
    出参与入参一样，需要尽可能精简和准确描述，嵌套的层级也尽可能少。
    
    **重要**
    
    无论请求方式是GET还是POST，参数都支持Object类型。但Object类型下的子属性不能为空。请单击该对象行末的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905454.png)图标新增子属性。
    
    **高级配置（可选）**
    
    **高级配置**
    
    为大模型增加调用示例，减少漏召回和误召回的情况。
    
    通常用于入参比较复杂，模型构造容易出错的场景，通过提供一些样例，提升大模型调用插件的准确性。
    
    **Value**：表示用户输入当前的Query时，期望大模型构造出的调用入参。示例：用户输入：“查询杭州明天的天气”，期望构造入参为：`{"city": "杭州", "date": "2025-04-25"}`。
    
2.  配置完成后单击**保存草稿**。
    
3.  在线调试工具API能否调通。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5197455471/p948913.png)
    
    单击**测试工具**，输入鉴权信息（开启鉴权时填写）及入参的值，单击**开始运行**。
    
    > 如果运行失败，请根据**运行结果**中的报错信息对配置进行调整，并重新进行测试，直至成功运行。
    
    入参的值可以手动输入，也可以通过代码输入。对于入参较为复杂的情况，建议采用**代码模式编辑**。您可以在代码编辑器中提交完整的JSON格式的入参及其相应的值。
    
4.  测试通过后单击**发布**。只有**已发布**的工具才能在应用中被调用。
    

## **从云市场导入插件**

云市场提供了丰富的API，您可在云市场开通需要的API并将其导入至阿里云百炼插件列表中，以便应用进行调用。

1.  访问**[插件](https://bailian.console.aliyun.com/?tab=app#/component-manage)**页面，单击**从云市场导入**。
    
2.  首次在阿里云百炼平台上导入云市场 API 作为插件，需要先进行服务关联角色授权。
    
    ## 主账号
    
    如果您使用主账号登录百炼，请在**SLR授权**弹窗中，勾选同意上述条款，单击**确认授权**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905283.png)
    
    ## RAM用户（子账号）
    
    如果您使用RAM用户（子账号）登录百炼，在**SLR授权**弹窗中，勾选同意上述条款，单击**确认授权**时，会有如下提示：
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0593247371/p905985.png)
    
    这是因为该RAM用户（子账号）不具备创建服务关联角色的权限。请按照下述操作先授予RAM用户（子账号）创建服务关联角色的权限。获得授权后，RAM用户（子账号）即可自行从云市场导入插件至百炼或使用主账号已经导入的插件。
    
    1.  授权RAM用户（子账号）创建服务关联角色的权限。
        
        1.  使用主账号登录[RAM控制台](https://ram.console.aliyun.com/)。
            
        2.  在左侧导航栏，选择**权限管理** > **权限策略**。
            
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
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0593247371/p906017.png)
            
        5.  单击**确定**。
            
        6.  设置权限策略名称，单击**确定**。
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0593247371/p906000.png)
            
        7.  在左侧导航栏，选择。
            
        8.  找到待授权的RAM用户（子账号），单击RAM用户（子账号）**操作**列的**添加权限**。
            
        9.  在权限策略中选择刚才创建的权限策略，单击**确认新增授权**。
            
            至此，RAM用户（子账号）拥有了创建服务关联角色的权限。
            
            ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0593247371/p906024.png)
            
    2.  RAM用户（子账号）自行从云市场导入插件至阿里云百炼或使用主账号已经导入的插件。
        
        返回阿里云百炼控制台，单击**从云市场导入**，在**SLR授权**弹窗中，勾选同意上述条款，单击**确认授权**
        
    
3.  在**导入云市场插件**弹窗中，单击**点击查看**进入云市场开通需要的API。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905284.png)
    
4.  您可以查看**云市场**页面，等待商品**状态**为**已开通**。
    
    当前页面还提供了API的AppKey、AppSecret、AppCode，如果插件需要鉴权，您可以在此处获取鉴权信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8398001571/p979365.png)
    
5.  开通成功后，返回阿里云百炼控制台，单击**从云市场导入**，重新打开**导入云市场插件**弹窗。选择已开通的API，再单击**确定**，进入**工具列表**页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905297.png)
    
6.  从云市场导入的插件为草稿状态，需要测试、发布后再使用。
    
    1.  单击工具所在行的**调试**，进入**工具测试**页面。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905298.png)
        
    2.  输入参数后，单击**开始运行**。
        
        若**运行成功**，则说明接口正常。否则，请参考界面提示信息修改配置。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905592.png)
        
    3.  返回**编辑工具**页面，单击**发布**，发布工具。
        
        > 从云市场导入插件时，系统将自动填充出参和入参信息，但可能会存在信息缺失的情况。在发布工具时，您需要关注无法发布的错误信息，以便根据错误提示有效地解决问题。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905316.png)
        
    4.  **已发布**且**启用**状态的工具才能用于后续调用。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905318.png)
        

## 使用插件

## 控制台

-   **方式一**：将插件发布为MCP服务，然后在智能体应用中添加该MCP服务。
    
    **步骤一：将插件发布为MCP服务**
    
    1.  在**插件列表**中，将鼠标悬浮在目标插件卡片上，单击**发布为MCP服务**。
        
        > 如果插件已转为MCP服务，按钮显示为**查看MCP服务**，单击可跳转到MCP管理页面查看服务详情。
        
    2.  发布成功后，可在**MCP管理**页面查看该MCP服务的详细信息，包括服务名称、服务描述、服务ID等。
        
    
    **步骤二：在智能体应用中添加MCP服务**
    
    1.  进入**智能体应用**的编排页面，在**MCP**区块中，单击**+**。
        
    2.  在**选择MCP服务**面板中，切换到**自定义MCP**页签，找到从插件转换的MCP服务，单击**添加全部**将其添加到应用中。
        
        > 您也可以单击**从插件转MCP**，将尚未转换的插件直接发布为MCP服务。
        
    3.  测试插件的使用效果是否符合预期。
        
        -   无鉴权：您可以在输入框中与大模型进行对话，测试插件使用效果。
            
        -   用户级鉴权、服务级鉴权：您需要在开启对话前，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905403.png)配置需要传入的鉴权Token。如果不离开当前页面，可以只配置一次。
            
            > 从云市场导入的插件，不需要在当前页面输入鉴权Token。
            
        -   工具入参的**传参方式**选择了**业务透传**：您需要在开启对话前，单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905403.png)配置需要传入的变量值。如果不离开当前页面，可以只输入一次。
            
    4.  测试完成后，**发布**应用。
        
-   **方式二**：在**[应用管理](https://bailian.console.aliyun.com/#/app-center)**页面中，进入**智能体应用**的编排页面，在**MCP**区块中添加MCP服务，测试插件使用效果，并**发布**应用。
    

## API

**获取工具 ID**

工具ID用于标识具体的工具。通过API调用工具时，需要正确传递工具ID，以确保请求能够被正确识别。

1.  在**插件列表**中，找到工具所属的插件，单击**查看详情**。
    
2.  将鼠标悬浮于工具名称旁边的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p902180.png)图标上。
    
3.  单击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p902183.png)图标，复制工具ID。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0593247371/p906346.png)
    

-   当通过API调用应用时，如果应用中关联的插件存在业务透传参数或开启了**用户级鉴权**，则需要通过参数`biz_params`传递鉴权信息或透传参数信息。具体操作请参见[工作流与旧版智能体应用 API](https://help.aliyun.com/zh/model-studio/agent-and-workflow-application-api-reference)。
    
-   通过Assistant API调用工具。请在[Assistant API文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)中搜索`tools`关键字，查看如何使用Assistant API调用工具。
    

## **管理自定义插件与工具**

**删除插件**

**重要**

删除插件会删除插件下的所有工具，并且调用了插件的应用会失效，此操作不可撤回，请谨慎操作。

在**插件列表**中，找到目标插件，单击**删除**。

**编辑插件**

1.  在**插件列表**中，找到目标插件，单击**查看详情**。
    
2.  单击右上角的**编辑插件**，修改插件信息并保存。
    
    插件信息保存后立即生效。如果修改了插件的URL、Header、鉴权信息，可能会影响工具调用，请重新测试并发布工具。
    

**编辑工具**

工具信息修改完成后，需要重新测试并发布，才能生效。

1.  在**插件列表**中，找到工具所属插件，单击**查看详情**。
    
2.  单击工具所在行的**编辑**，修改工具信息并单击**保存草稿**。
    
3.  单击**测试工具**，在线调试工具。
    
4.  运行成功后单击**发布**。
    

**删除工具**

**重要**

删除工具后，调用了此工具的应用会失效，此操作不可撤回，请谨慎操作。

1.  在**插件列表**中，找到工具所属插件，单击**查看详情**。
    
2.  单击工具所在行的**删除**。
    

## **错误码**

发布工具时的常见错误信息如下表所示：

**错误码**

**错误信息**

**说明**

**130040**

xx缺少参数描述信息

原因：xx参数的参数描述缺失。

解决方案：请您补充参数描述后重新发布工具。

**130022**

保存工具信息异常/请检查示例参数是否正确

可能原因一：输入参数或输出参数中的Object类型参数子属性为空。

解决方案：请点击该对象行末的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905454.png)图标新增子属性。

可能原因二：请求方法选择了GET，但输入参数配置时，存在参数为Object类型。

解决方案：GET请求方法下的输入参数不支持Object类型，请选择其他类型。
