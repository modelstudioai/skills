# 获取与配置 API Key

在控制台获取或创建 API Key 后，您将使用它来安全地调用百炼的模型服务。

## 第一步：获取 API Key

1.  前往阿里云百炼的**密钥管理**（[中国大陆版](https://bailian.console.aliyun.com/?tab=model#/api-key) | [国际版](https://modelstudio.console.aliyun.com/?tab=playground#/api-key)）页面。
    
2.  若已有可用 API Key，直接在列表中复制即可。若需创建，请遵循以下步骤：
    
    1.  在**API Key** 页签单击**创建 API Key**。若无法创建，请联系您的组织或 IT 管理员。
        
    2.  在**创建 API Key**弹窗中，选择 API Key 的**归属账号**及**归属业务空间**，并单击**确定**。
        
        -   **归属账号**：选择**阿里云账号（主账号）**即可，账号名通常为一串数字。
            
            如需为团队成员或应用创建权责独立的 API Key，并结合归属业务空间进行精细化的模型访问控制，归属账号应选择[RAM 用户](https://help.aliyun.com/zh/ram/user-guide/overview-of-ram-users)。
            
            > RAM 用户的账号格式为`username@<AccountAlias>.onaliyun.com`。
            
        -   **归属业务空间：**选择“**默认业务空间**”，此空间下的 Key 可调用所有[标准模型](raw/model-user-guide/get-started-with-models/models.md)。
            
            > 单个业务空间最多支持创建 20 个 API Key。
            
            如需以下功能，请选择非默认的业务空间，相关信息请参考[业务空间管理](raw/model-user-guide/security-and-compliance/permission-management-overview.md)：
            
            -   对不同项目（业务空间）进行权限隔离
            -   精细化的模型访问控制
            -   进行独立的成本核算
        -   **权限**：建议选择**全部**，若有更精细的权限控制需求，可以选择**自定义**来控制可访问 IP 和 可访问模型。
            
            > IP 白名单默认设置：IPv4（`0.0.0.0/0`）全部放通；IPv6 仅华北2（北京）地域支持，美国（弗吉尼亚）地域仅支持 IPv4。最多支持 **20** 个地址或网段，批量输入请用英文逗号隔开。
            
    3.  点击新创建的 API Key 旁的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8412544571/p994217.png)图标复制 API Key。
        

## 第二步：配置 API Key

-   **方式一：在**[**第三方工具**](https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool)**中进行配置**
    
    如果在 Chatbox 等工具或平台中调用模型，您可能需要输入三个信息：
    
    -   本文获取的 API Key
        
    -   Base URL：
        
        -   中国大陆版：`https://dashscope.aliyuncs.com/compatible-mode/v1`
        -   国际版：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
    -   模型名称，如 qwen-plus、qwen3-8b、deepseek-r1 等。
        
    
    我们也提供了一些常用工具的配置方法：[Dify](raw/model-user-guide/use-chat-client-or-development-tool/dify.md)、[Chatbox](raw/model-user-guide/use-chat-client-or-development-tool/chatbox.md)、[Cline](raw/model-user-guide/use-chat-client-or-development-tool/cline.md)、[Claude Code](raw/model-user-guide/use-chat-client-or-development-tool/claude-code.md)、[Postman](raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)。
    
-   **方式二：配置 API Key 到环境变量，后续支持 cURL 和代码调用**
    
    **重要**请勿在客户端代码（如浏览器、移动应用）或不可信环境中配置或使用长期有效的 API Key。可以使用[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（最长 1800 秒）。
    
    > **请将**`<YOUR_API_KEY>` 部分替换为真实的 API Key。
    
    #### Linux系统
    
    #### 添加永久性环境变量
    
    将环境变量设置追加到`~/.bashrc`文件中。
    
    ```
    echo "export DASHSCOPE_API_KEY='<YOUR_API_KEY>'" >> ~/.bashrc
    source ~/.bashrc
    echo "百炼 API Key 永久配置为：${DASHSCOPE_API_KEY:0:10}*********"
    ```
    
    #### 添加临时性环境变量
    
    ```
    export DASHSCOPE_API_KEY='<YOUR_API_KEY>'
    echo "当前会话百炼 API Key 配置为：${DASHSCOPE_API_KEY:0:10}*********"
    ```
    
    #### 服务管理器 (systemd)
    
    > 以下操作适用于将应用作为后台服务部署的场景。
    
    1.  **创建环境文件**
    
    ```
    sudo sh -c "echo 'DASHSCOPE_API_KEY=<YOUR_API_KEY>' > /etc/your-app/env"
    sudo chmod 600 /etc/your-app/env # 限制只有root用户有访问权限
    ```
    
    2.  **修改 systemd 服务文件**（如 `/etc/systemd/system/your-app.service`）：
    
    ```
    [Service]
    # 加载密钥文件
    EnvironmentFile=/etc/your-app/env
    ExecStart=/usr/bin/python /opt/your-app/main.py
    ```
    
    3.  **重载服务**
    
    ```
    sudo systemctl daemon-reload
    sudo systemctl restart your-app
    ```
    
    #### macOS系统
    
    #### 添加永久性环境变量
    
    将环境变量设置追加到`~/.bash_profile`或`~/.zshrc`文件中。
    
    ```
    VAR_VALUE="<YOUR_API_KEY>"; \
    echo "export DASHSCOPE_API_KEY='$VAR_VALUE'" >> ~/.zshrc 2>/dev/null
    echo "export DASHSCOPE_API_KEY='$VAR_VALUE'" >> ~/.bash_profile 2>/dev/null
    source ~/."${SHELL##*/}rc" 2>/dev/null
    echo "百炼 API Key 永久配置为：${DASHSCOPE_API_KEY:0:10}*********"
    ```
    
    #### 添加临时性环境变量
    
    ```
    export DASHSCOPE_API_KEY='<YOUR_API_KEY>'
    echo "当前会话百炼 API Key 配置为：${DASHSCOPE_API_KEY:0:10}*********"
    ```
    
    #### Windows系统
    
    在Windows系统中，您可以通过系统属性、CMD或PowerShell配置环境变量。
    
    #### 系统属性
    
    **说明**
    
    -   此方式配置的环境变量永久生效。
    -   修改系统环境变量需具备管理员权限。
    -   配置环境变量后不会立即影响已经打开的命令窗口、IDE或其他正在运行的应用程序。您需要重新启动这些程序或者打开新的命令行使环境变量生效。
    
    1.  在Windows系统桌面中按`Win+Q`键，在搜索框中搜索**编辑系统环境变量**，单击打开**系统属性**界面。
        
    2.  在**系统属性**窗口，单击**环境变量**，然后在**系统变量**区域下单击**新建**，**变量名**填入`DASHSCOPE_API_KEY`，**变量值**填入您的DashScope API Key。
        
    3.  依次单击三个窗口的**确定**，关闭系统属性配置页面，完成环境变量配置。
        
    4.  打开CMD（命令提示符）窗口或Windows PowerShell窗口，执行如下命令检查环境变量是否生效。
        
        -   CMD查询命令：
    
    ```
    echo 百炼 API Key 永久配置为：%DASHSCOPE_API_KEY:~0,10%*********
    ```
    
    -   Windows PowerShell查询命令：
    
    ```
    Write-Host "百炼 API Key 永久配置为：$($env:DASHSCOPE_API_KEY.Substring(0, [Math]::Min(10, $env:DASHSCOPE_API_KEY.Length)))*********"
    ```
    
    #### CMD
    
    #### 添加永久性环境变量
    
    如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。
    
    1.  在CMD中运行以下命令。
    
    ```
    setx DASHSCOPE_API_KEY "<YOUR_API_KEY>"
    ```
    
    2.  打开一个新的CMD窗口。
    3.  在新的CMD窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo 百炼 API Key 永久配置为：%DASHSCOPE_API_KEY:~0,10%*********
    ```
    
    #### 添加临时性环境变量
    
    如果您仅希望在当前会话中使用该环境变量，可以在CMD中运行以下命令。
    
    ```
    set "DASHSCOPE_API_KEY=<YOUR_API_KEY>"
    ```
    
    您可以在当前会话运行以下命令检查环境变量是否生效。
    
    ```
    echo 当前会话百炼 API Key 配置为：%DASHSCOPE_API_KEY:~0,10%*********
    ```
    
    #### PowerShell
    
    #### 添加永久性环境变量
    
    如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。
    
    1.  在PowerShell中运行以下命令。
    
    ```
    [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "<YOUR_API_KEY>", [EnvironmentVariableTarget]::User)
    ```
    
    2.  打开一个新的PowerShell窗口。
    3.  在新的PowerShell窗口运行以下命令，检查环境变量是否生效。
    
    ```
    Write-Host "百炼 API Key 永久配置为：$($env:DASHSCOPE_API_KEY.Substring(0, [Math]::Min(10, $env:DASHSCOPE_API_KEY.Length)))*********"
    ```
    
    #### 添加临时性环境变量
    
    如果您仅希望在当前会话中使用该环境变量，可以在PowerShell中运行以下命令。
    
    ```
    $env:DASHSCOPE_API_KEY = "<YOUR_API_KEY>"
    Write-Host "当前会话百炼 API Key 配置为：$($env:DASHSCOPE_API_KEY.Substring(0, [Math]::Min(10, $env:DASHSCOPE_API_KEY.Length)))*********"
    ```
    

## API Key 时效性说明

API Key 没有失效时间限制，若需要有时效性的 API Key，可生成[临时 API Key](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)（有效期最多1800秒）。

API Key 的状态随账号操作而变化：

**触发操作**

**主账号的 API Key**

**RAM 账号的 API Key**

**主动删除 API Key**

不支持 失效，不可恢复

不支持 失效，不可恢复

**将账号移出业务空间**

—

不支持 失效

> 重新加入业务空间后 API Key 恢复生效

**在**[RAM 控制台](https://ram.console.aliyun.com/roles)**删除账号/角色**

—

不支持 失效，不可恢复

## API 调用

请访问[文本生成](raw/model-api-reference/qwen-api-reference.md)以及更多模型的 API 参考。

OpenAI SDK 支持的模型，请参考[OpenAI 兼容](https://help.aliyun.com/zh/model-studio/toolkits-and-frameworks)。

## 常见问题

#### 无法创建 API Key？

API Key 的创建需使用[超级管理员](https://help.aliyun.com/zh/model-studio/permission-management-overview#982297bd47p3i)或[业务空间管理员](https://help.aliyun.com/zh/model-studio/permission-management-overview#c82f37c2033vw)操作。

#### 如何管理 API Key 的权限？

API Key 的调用权限完全由其**归属业务空间**决定。**同一空间内的 API Key 权限相同**，无需为不同模型（如文生文、文生图、语音合成）创建不同的 API Key。

-   **默认业务空间下的 API Key：**可调用所有[标准模型](raw/model-user-guide/get-started-with-models/models.md)，以及默认业务空间内的[应用](raw/application-user-guide/llm-application/application-introduction.md)。
-   **子业务空间下的 API Key：**可调用该子业务空间已获得[模型调用授权](raw/model-user-guide/security-and-compliance/permission-management-overview.md)的标准模型，以及该业务空间内的应用。

**调用在阿里云百炼**[**调优后的模型**](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)**：**此类模型部署成功后，仅能用其所在业务空间的API Key调用。

如需在业务空间之外做更细粒度的控制，可在创建或编辑 API Key 时将**权限**切换为**自定义**，配置：

-   **IP 访问白名单**：仅允许名单内的 IP 使用该 API Key 发起调用。支持 IPv4 与网段，默认 IPv4（`0.0.0.0/0`）全部放通；IPv6 仅华北2（北京）地域支持，美国（弗吉尼亚）地域仅支持 IPv4。最多支持 **20** 个地址或网段，批量输入请用英文逗号隔开。
-   **访问模型范围**：开关开启后，该 API Key 仅能调用已勾选的模型，可选模型限于该业务空间已授权的模型。

#### 环境变量已设置，为何代码仍提示找不到 API Key？

具体原因如下：

-   情况一：**没有设置永久性环境变量**。临时环境变量只在当前终端会话中有效，对于已经启动的 IDE 或其他应用程序并不会生效。请参考本文中设置永久性环境变量的方法。
    
-   情况二：**没有重启IDE、命令行工具或应用**。
    
    -   通常需要重启 IDE（如 VS Code）或命令行工具，使其能够加载最新的环境变量。
    -   如果在部署应用后设置了环境变量，可能需要重启应用服务，让应用能够重新加载环境变量。
-   情况三：**需要在配置文件添加环境变量**。如果您的应用是通过服务管理器（如 systemd、supervisord）启动的，可能需要在服务管理器的配置文件中添加环境变量。
    
-   情况四：**用了sudo命令**。如果使用`sudo python xx.py`运行脚本，可能会遗漏当前用户环境变量，因为`sudo`默认不继承所有环境变量。您可采用`sudo -E python xx.py`命令，其中的`-E` 参数确保环境变量被传递。如有权限执行该脚本，可以直接执行 `python xx.py`。
    

#### 单个主账号下最多能创建多少个API Key？

每个主账号下最多可创建20个业务空间（包括默认业务空间），每个业务空间下最多可创建20个API Key。
