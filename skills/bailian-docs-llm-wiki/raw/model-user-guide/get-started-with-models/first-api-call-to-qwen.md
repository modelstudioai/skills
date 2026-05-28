# 首次调用千问API

阿里云百炼支持通过API调用大模型，涵盖OpenAI兼容接口、DashScope SDK等接入方式。

**说明**

-   若您熟悉大模型调用，可直接查看API参考文档[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。
    
-   若您不熟悉编程，可参考[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)，通过图形化界面与千问模型对话。
    

本文以千问为例，引导您完成大模型API调用。您将了解到：

-   如何获取 API Key
    
-   如何配置本地开发环境
    
-   如何调用千问 API
    

## 账号设置

1.  **注册账号**：若无阿里云账号，需首先[注册](https://account.aliyun.com/register/qr_register.htm)。
    
    > 如遇问题，请参见[注册阿里云账号](https://help.aliyun.com/zh/account/step-1-register-an-alibaba-cloud-account)。
    
2.  **开通阿里云百炼：**使用**阿里云主账号**前往[阿里云百炼大模型服务平台](https://bailian.console.aliyun.com/?tab=model#/model-market)，阅读并同意协议后，将自动开通阿里云百炼，如果未弹出服务协议，则表示您已经开通。
    
    > 如果开通服务时提示“您尚未进行实名认证”，请先进行[实名认证](https://help.aliyun.com/zh/account/verify-your-identity-individual-account)。
    
3.  **获取API Key：**前往[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)页面，单击**创建API Key****，**即可通过API KEY调用大模型。
    

## **配置API Key到环境变量**

建议您把API Key配置到环境变量，避免在代码里显式地配置API Key，降低泄露风险。

**配置步骤**

### Linux系统

#### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  执行以下命令来将环境变量设置追加到`~/.bashrc` 文件中。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
    ```
    
    也可以手动修改`~/.bashrc` 文件。
    
    **手动修改**
    
    执行以下命令，打开`~/.bashrc` 文件。
    
    ```
    nano ~/.bashrc
    ```
    
    在配置文件中添加以下内容。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
    在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
    
2.  执行以下命令，使变更生效。
    
    ```
    source ~/.bashrc
    ```
    
3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

#### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

### macOS系统

#### 添加永久性环境变量

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以添加永久性环境变量。

1.  在终端中执行以下命令，查看默认Shell类型。
    
    ```
    echo $SHELL
    ```
    
2.  根据默认Shell类型进行操作。
    
    ##### **Zsh**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.zshrc` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
        ```
        
        也可以手动修改`~/.zshrc` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.zshrc
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.zshrc
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    
    ##### **Bash**
    
    1.  执行以下命令来将环境变量设置追加到 `~/.bash_profile` 文件中。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bash_profile
        ```
        
        也可以手动修改`~/.bash_profile` 文件。
        
        **手动修改**
        
        执行以下命令，打开Shell配置文件。
        
        ```
        nano ~/.bash_profile
        ```
        
        在配置文件中添加以下内容。
        
        ```
        # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
        export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
        ```
        
        在nano编辑器中，按Ctrl + X，接着按Y，再按Enter以保存并关闭文件。
        
    2.  执行以下命令，使变更生效。
        
        ```
        source ~/.bash_profile
        ```
        
    3.  重新打开一个终端窗口，运行以下命令检查环境变量是否生效。
        
        ```
        echo $DASHSCOPE_API_KEY
        ```
        
    

#### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以添加临时性环境变量。

> 以下命令适用于 Zsh 和 Bash。

1.  执行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  执行以下命令，验证该环境变量是否生效。
    
    ```
    echo $DASHSCOPE_API_KEY
    ```
    

### Windows系统

在Windows系统中，您可以通过系统属性、CMD或PowerShell配置环境变量。

#### **系统属性**

**说明**

-   此方式配置的环境变量永久生效。
    
-   修改系统环境变量需具备管理员权限。
    
-   配置环境变量后不会立即影响已经打开的命令窗口、IDE或其他正在运行的应用程序。您需要重新启动这些程序或者打开新的命令行使环境变量生效。
    

1.  在Windows系统桌面中按`Win+Q`键，在搜索框中搜索**编辑系统环境变量**，单击打开**系统属性**界面。
    
2.  在**系统属性**窗口，单击**环境变量**，然后在**系统变量**区域下单击**新建**，**变量名**填入`DASHSCOPE_API_KEY`，**变量值**填入您的DashScope API Key。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8252115371/p894015.png)
    
3.  依次单击三个窗口的**确定**，关闭系统属性配置页面，完成环境变量配置。
    
4.  打开CMD（命令提示符）窗口或Windows PowerShell窗口，执行如下命令检查环境变量是否生效。
    
    -   CMD查询命令：
        
        ```
        echo %DASHSCOPE_API_KEY%
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)
        
    -   Windows PowerShell查询命令：
        
        ```
        echo $env:DASHSCOPE_API_KEY
        ```
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912525.png)
        

#### **CMD**

##### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在CMD中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
    ```
    
2.  打开一个新的CMD窗口。
    
3.  在新的CMD窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo %DASHSCOPE_API_KEY%
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)
    

##### **添加临时性环境变量**

如果您仅希望在当前会话中使用该环境变量，可以在CMD中运行以下命令。

```
REM 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
set DASHSCOPE_API_KEY=YOUR_DASHSCOPE_API_KEY
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo %DASHSCOPE_API_KEY%
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912522.png)

#### **PowerShell**

##### **添加永久性环境变量**

如果您希望API Key环境变量在当前用户的所有新会话中生效，可以按如下操作。

1.  在PowerShell中运行以下命令。
    
    ```
    # 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
    [Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
    ```
    
2.  打开一个新的PowerShell窗口。
    
3.  在新的PowerShell窗口运行以下命令，检查环境变量是否生效。
    
    ```
    echo $env:DASHSCOPE_API_KEY
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912525.png)
    

##### 添加临时性环境变量

如果您仅希望在当前会话中使用该环境变量，可以在PowerShell中运行以下命令。

```
# 用您的阿里云百炼API Key代替YOUR_DASHSCOPE_API_KEY
$env:DASHSCOPE_API_KEY = "YOUR_DASHSCOPE_API_KEY"
```

您可以在当前会话运行以下命令检查环境变量是否生效。

```
echo $env:DASHSCOPE_API_KEY
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1317988371/p912525.png)

## **选择开发语言**

选择您熟悉的语言或工具，用于调用大模型API。

## Python

### **步骤 1：配置Python环境**

### **检查您的Python版本**

您可以在终端中输入以下命令查看当前计算环境是否安装了Python和pip：

您的Python需要为3.8或以上版本，请您参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)进行安装。

```
python -V
pip --version
```

以Windows的CMD为例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2419779371/p914717.png)

#### **常见问题**

Q：执行`python -V`、`pip --version`报错：

-   `'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。`
    
-   `'pip' 不是内部或外部命令，也不是可运行的程序或批处理文件。`
    
-   `-bash: python: command not found`
    
-   `-bash: pip: command not found`
    

解决办法如下：

##### **Windows系统**

1.  请确认是否已参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)，在您的计算环境中安装Python，并将python.exe添加至环境变量PATH中。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917218.png)
    
2.  如果已安装了Python并添加了环境变量，仍报此错，请关闭当前终端，重新打开一个新的终端窗口，再进行尝试。
    

## Linux、macOS系统

1.  请确认是否已参考[安装Python](https://help.aliyun.com/zh/sdk/developer-reference/installing-python)，在您的计算环境中安装的Python。
    
2.  如果已安装Python后，仍报此错，请输入`which python pip`命令查询系统中是否有`python`、`pip`。
    
    -   如果返回如下结果，请关闭当前连接终端，重新打开一个新的终端窗口，再进行尝试。
        
        ```
        /usr/bin/python
        /usr/bin/pip
        ```
        
    -   如果返回如下结果，则再次输入`which python3 pip3`查询。
        
        ```
        /usr/bin/which: no python in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        /usr/bin/which: no pip in (/root/.local/bin:/root/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin)
        ```
        
        如果返回结果如下，则使用`python3 -V`、`pip3 --version`查询版本。
        
        ```
        /usr/bin/python3
        /usr/bin/pip3
        ```
        

### **配置虚拟环境（可选）**

如果您的Python已安装完成，可以创建一个虚拟环境来安装OpenAI Python SDK或DashScope Python SDK，这可以帮助您避免与其它项目发生依赖冲突。

1.  **创建虚拟环境**
    
    您可以运行以下命令，创建一个命名为**.venv**的虚拟环境：
    
    ```
    # 如果运行失败，您可以将python替换成python3再运行
    python -m venv .venv
    ```
    
2.  **激活虚拟环境**
    
    若您使用Windows系统，请运行以下命令来激活虚拟环境：
    
    ```
    .venv\Scripts\activate
    ```
    
    如果您使用macOS或者Linux系统，请运行以下命令来激活虚拟环境：
    
    ```
    source .venv/bin/activate
    ```
    

### **安装**OpenAI Python SDK或DashScope Python SDK

您可以通过OpenAI的Python SDK或DashScope的Python SDK来调用阿里云百炼平台上的模型。

## 安装 OpenAI Python SDK

通过运行以下命令安装或升级 OpenAI Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U openai
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917092.png)

当终端出现`Successfully installed ... openai-x.x.x`的提示后，表示您已经成功安装OpenAI Python SDK。

## 安装 DashScope Python SDK

通过运行以下命令安装或升级 DashScope Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U dashscope
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917093.png)

当终端出现`Successfully installed ... dashscope-x.x.x`的提示后，表示您已经成功安装DashScope Python SDK。

### **步骤 2：调用大模型API**

## OpenAI Python SDK

如果您安装完成了Python以及OpenAI的Python SDK，可以参考以下步骤发送您的API请求。

1.  新建一个文件，命名为`hello_qwen.py`。
    
2.  将以下代码复制到`hello_qwen.py`中并保存。
    
    ```
    import os
    from openai import OpenAI
    
    try:
        client = OpenAI(
            # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
    
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': '你是谁？'}
            ]
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
    ```
    
3.  通过命令行运行`python hello_qwen.py`或`python3 hello_qwen.py`。
    
    > 若提示`No such file or directory`，则需在文件名前指定具体文件路径。
    
    运行后您将会看到输出结果：
    
    ```
    我是阿里云开发的一款超大规模语言模型，我叫千问。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917326.png)
    

## DashScope Python SDK

如果您安装完成了Python以及DashScope的Python SDK，可以参考以下步骤发送您的API请求。

1.  新建一个文件，命名为`hello_qwen.py`。
    
2.  将以下代码复制到`hello_qwen.py`中并保存。
    
    ```
    import os
    from dashscope import Generation
    import dashscope 
    
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}
    ]
    response = Generation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"), 
        model="qwen-plus",   # 模型列表：https://help.aliyun.com/model-studio/getting-started/models
        messages=messages,
        result_format="message"
    )
    
    if response.status_code == 200:
        print(response.output.choices[0].message.content)
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
    ```
    
3.  通过命令行运行`python hello_qwen.py`或`python3 hello_qwen.py`。
    
    **说明**
    
    本示例使用的运行命令需在Python文件所在目录执行，如果想要在任意位置执行，请在文件名前指定具体文件路径。
    
    运行后您将会看到输出结果：
    
    ```
    我是来自阿里云的大规模语言模型，我叫千问。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917332.png)
    

## Node.js

### **步骤 1：配置Node.js环境**

### 检查Node.js安装状态

您可以在终端中输入以下命令查看当前计算环境是否安装了Node.js和npm：

```
node -v
npm -v
```

以Windows的CMD为例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2419779371/p914719.png)

这将打印出您当前Node.js 版本。如果您的环境中没有Node.js，请访问[Node.js官网](https://nodejs.org/en/download/package-manager)进行下载。

### 安装模型调用SDK

您可以在终端运行以下命令：

```
npm install --save openai
# 或者
yarn add openai
```

**说明**

如果安装失败，您可以通过配置镜像源的方法来完成安装，如：

```
npm config set registry https://registry.npmmirror.com/
```

配置镜像源后，您可以重新运行安装SDK的命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917106.png)

当终端出现`added xx package in xxs`的提示后，表示您已经成功安装OpenAI SDK。您可以使用`npm list openai`查询具体版本信息。

### 步骤 2：调用大模型API

1.  新建一个`hello_qwen.mjs`文件。
    
2.  将以下代码复制到文件中。
    
    ```
    import OpenAI from "openai";
    
    try {
        const openai = new OpenAI(
            {
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: apiKey: "sk-xxx",
                // 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
                apiKey: process.env.DASHSCOPE_API_KEY,
                // 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
                baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
            }
        );
        const completion = await openai.chat.completions.create({
            model: "qwen-plus",  //模型列表: https://help.aliyun.com/model-studio/getting-started/models
            messages: [
                { role: "system", content: "You are a helpful assistant." },
                { role: "user", content: "你是谁？" }
            ],
        });
        console.log(completion.choices[0].message.content);
    } catch (error) {
        console.log(`错误信息：${error}`);
        console.log("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code");
    }
    ```
    
3.  通过命令行运行以下命令来发送API请求：
    
    ```
    node hello_qwen.mjs
    ```
    
    **说明**
    
    -   本示例使用的运行命令需在`hello_qwen.mjs`文件所在目录执行，如果想要在任意位置执行，请在文件名前指定具体文件路径。
        
    -   请确保已在`hello_qwen.mjs`文件所在目录中安装了SDK，如果SDK与文件不在同一目录下，则会报错`Cannot find package 'openai' imported from xxx`。
        
    
    运行成功后您将会看到输出结果：
    
    ```
    我是来自阿里云的语言模型，我叫千问。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917344.png)
    

## Java

### **步骤 1：配置Java环境**

### **检查您的Java版本**

您可以在终端运行以下命令：

```
java -version
# （可选）如果使用maven管理和构建java项目，还需确保maven已正确安装到您的开发环境中
mvn --version
```

以Windows的CMD为例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2419779371/p914723.png)

为了使用DashScope Java SDK，您的Java需要在Java 8或以上版本。您可以查看打印信息中的第一行确认Java版本，例如打印信息：`openjdk version "16.0.1" 2021-04-20`表明当前Java版本为Java 16。如果您当前计算环境没有Java，或版本低于Java 8，请前往[Java下载](https://www.oracle.com/cn/java/technologies/downloads/)进行下载与安装。

### **安装模型调用SDK**

如果您的环境中已安装Java，请安装DashScope Java SDK。SDK的版本请参考：[DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java)。执行以下命令来添加 Java SDK 依赖，并将 `the-latest-version` 替换为最新的版本号。

## XML

1.  打开您的Maven项目的`pom.xml`文件。
    
2.  在`<dependencies>`标签内添加以下依赖信息。
    
    ```
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>dashscope-sdk-java</artifactId>
        <!-- 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
        <version>the-latest-version</version>
    </dependency>
    ```
    
3.  保存`pom.xml`文件。
    
4.  使用Maven命令（如`mvn compile`或`mvn clean install`）来更新项目依赖，这样Maven会自动下载并添加DashScope Java SDK到您的项目中。
    

以Windows的IDEA集成开发环境为例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917125.png)

## Gradle

1.  打开您的Gradle项目的`build.gradle`文件。
    
2.  在`dependencies`块内添加以下依赖信息。
    
    ```
    dependencies {
        // 请将 'the-latest-version' 替换为最新版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
        implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
    }
    ```
    
3.  保存`build.gradle`文件。
    
4.  在命令行中，切换到您的项目根目录，执行以下Gradle命令来更新项目依赖。这将会自动下载并添加DashScope Java SDK到您的项目中。
    
    ```
    ./gradlew build --refresh-dependencies
    ```
    

以Windows的IDEA集成开发环境为例：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917168.png)

### **步骤 2：调用大模型API**

您可以运行以下代码来调用大模型API。

```
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    //  若使用新加坡地域的模型，请释放下列注释
    //  static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            System.out.println("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code");
        }
        System.exit(0);
    }
}
```

运行后您将会看到对应的输出结果：

```
我是阿里云开发的一款超大规模语言模型，我叫千问。
```

## curl

您可以通过OpenAI兼容的HTTP方式或DashScope的HTTP方式来调用阿里云百炼平台上的模型。模型列表请参考：[选择模型](https://help.aliyun.com/zh/model-studio/models)。

**说明**

若没有配置环境变量，请用阿里云百炼API Key将：-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\ 换为：-H "Authorization: Bearer sk-xxx" \\ 。

## OpenAI兼容-HTTP

您可以运行以下命令发送API请求：

**Windows**

在CMD（命令提示符）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" ^
-H "Authorization: Bearer %DASHSCOPE_API_KEY%" ^
-H "Content-Type: application/json" ^
-d "{
    \"model\": \"qwen-plus\",
    \"messages\": [
        {
            \"role\": \"system\",
            \"content\": \"You are a helpful assistant.\"
        },
        {
            \"role\": \"user\",
            \"content\": \"你是谁？\"
        }
    ]
}"
```

**Linux/macOS**

在Terminal（终端）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为: https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "你是谁？"
        }
    ]
}'
```

发送API请求后，可以得到以下回复：

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是来自阿里云的大规模语言模型，我叫千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 22,
        "completion_tokens": 16,
        "total_tokens": 38
    },
    "created": 1728353155,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-39799876-eda8-9527-9e14-2214d641cf9a"
}
```

## DashScope-HTTP

您可以运行以下命令发送API请求：

**Windows**

在CMD（命令提示符）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key: https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" ^
-H "Authorization: Bearer %DASHSCOPE_API_KEY%" ^
-H "Content-Type: application/json" ^
-d "{
  \"model\": \"qwen-plus\",
  \"input\": {
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a helpful assistant.\"
      },
      {
        \"role\": \"user\",
        \"content\": \"你是谁？\"
      }
    ]
  },
  \"parameters\": {
    \"result_format\": \"message\"
  }
}"
```

**Linux/macOS**

在Terminal（终端）中执行如下命令：

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[      
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你是谁？"
            }
        ]
    },
    "parameters": {
        "result_format":"message"
    }
}'
```

发送API请求后，可以得到以下回复：

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": "我是来自阿里云的大规模语言模型，我叫千问。"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 38,
        "output_tokens": 16,
        "input_tokens": 22
    },
    "request_id": "87f776d7-3c82-9d39-b238-d1ad38c9b6a9"
}
```

## 其它语言

**调用大模型API**

Go

```
package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}
type RequestBody struct {
	Model    string    `json:"model"`
	Messages []Message `json:"messages"`
}

func main() {
	// 创建 HTTP 客户端
	client := &http.Client{}
	// 构建请求体
	requestBody := RequestBody{
		// 模型列表：https://help.aliyun.com/model-studio/getting-started/models
		Model: "qwen-plus",
		Messages: []Message{
			{
				Role:    "system",
				Content: "You are a helpful assistant.",
			},
			{
				Role:    "user",
				Content: "你是谁？",
			},
		},
	}
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatal(err)
	}
	// 创建 POST 请求
	// 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
	req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatal(err)
	}
	// 设置请求头
	// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey := "sk-xxx"
	// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
	apiKey := os.Getenv("DASHSCOPE_API_KEY")
	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")
	// 发送请求
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	// 读取响应体
	bodyText, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	// 打印响应内容
	fmt.Printf("%s\n", bodyText)
}
```

PHP

```
<?php
// 设置请求的URL
// 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
$url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
// 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：$apiKey = "sk-xxx";
// 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
$apiKey = getenv('DASHSCOPE_API_KEY');
// 设置请求头
$headers = [
    'Authorization: Bearer '.$apiKey,
    'Content-Type: application/json'
];
// 设置请求体
$data = [
    // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
    "model" => "qwen-plus",
    "messages" => [
        [
            "role" => "system",
            "content" => "You are a helpful assistant."
        ],
        [
            "role" => "user",
            "content" => "你是谁？"
        ]
    ]
];
// 初始化cURL会话
$ch = curl_init();
// 设置cURL选项
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
// 执行cURL会话
$response = curl_exec($ch);
// 检查是否有错误发生
if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
}
// 关闭cURL资源
curl_close($ch);
// 输出响应结果
echo $response;
?>
```

C#

```
using System.Net.Http.Headers;
using System.Text;

class Program
{
    private static readonly HttpClient httpClient = new HttpClient();

    static async Task Main(string[] args)
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：string? apiKey = "sk-xxx";
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/model-studio/get-api-key
        string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

        if (string.IsNullOrEmpty(apiKey))
        {
            Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
            return;
        }
        // 以下是北京地域url，如果使用新加坡地域的模型，需要将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
        string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
        // 模型列表：https://help.aliyun.com/model-studio/getting-started/models
        string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""messages"": [
                {
                    ""role"": ""system"",
                    ""content"": ""You are a helpful assistant.""
                },
                {
                    ""role"": ""user"", 
                    ""content"": ""你是谁？""
                }
            ]
        }";

        // 发送请求并获取响应
        string result = await SendPostRequestAsync(url, jsonContent, apiKey);

        // 输出结果
        Console.WriteLine(result);
    }

    private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
    {
        using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
        {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsStringAsync();
            }
            else
            {
                return $"请求失败: {response.StatusCode}";
            }
        }
    }
}
```

## **API参考**

-   关于千问API的输入输出参数，请参见[千问](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)。
    
-   关于其他模型，请参见[选择模型](https://help.aliyun.com/zh/model-studio/models)。
    

## **常见问题**

### [**免费额度**](https://bailian.console.aliyun.com/#/model-market/detail/qwen-max-latest)**用完后如何购买 Token？**

A：您可以访问[费用与成本](https://usercenter2.aliyun.com/home)中心，确保您的账户没有欠费即可调用千问模型。

> 调用千问模型会自动扣费，出账周期为分钟级（即一条账单代表一分钟内的费用）。消费明细请前往**[账单详情](https://billing-cost.console.aliyun.com/finance/expense-report/expense-detail-by-instance)**进行查看。

### **调用大模型API后报错**`**Model.AccessDenied**`**，如何处理？**

A：该报错是因为您使用子业务空间的API Key，子业务空间无法访问**主账号空间**的应用或模型。使用子空间API Key需由主账号管理员为对应子空间开通模型授权（如本文使用`千问-Plus`模型）。详细操作步骤请参见[设置模型调用权限](https://help.aliyun.com/zh/model-studio/permission-management-overview#f642213a1f38l)。

### **如何接入** [**Chatbox**](https://chatboxai.app/zh)**、**[**Cherry Studio**](https://cherry-ai.com/)**、**[Cline](https://cline.bot/)**或** [Dify](https://cloud.dify.ai/apps)**？**

A：请根据您的使用情况参考以下步骤：

> 此处以使用较多的工具为例，其它大模型工具接入的方法较为类似。

## Chatbox

请参见[Chatbox](https://help.aliyun.com/zh/model-studio/chatbox)。

## Cherry Studio

1.  单击左下角的设置按钮，在**模型服务**栏中找到**阿里云百炼**，**API 密钥**输入您的 API Key，获取方法请参见：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)；**API 地址**填入`https://dashscope.aliyuncs.com/compatible-mode/v1/`；单击**添加**。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3274214671/p920483.png)
    
2.  在**模型 ID**填入您需要使用的千问模型，此处以 qwen-max-latest 为例（更多可用的模型请参考[选择模型](https://help.aliyun.com/zh/model-studio/models)中的千问模型）； **模型名称**与**分组名称**会自动生成。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7845540471/p920486.png)
    
3.  在界面上方选中添加的模型，部分模型支持联网搜索，打开输入框处的联网搜索按钮。输入“杭州天气咋样？”进行测试：
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7845540471/p920490.png)
    

## Cline

请参见[Cline](https://help.aliyun.com/zh/model-studio/cline)。

## Dify

请参见[Dify](https://help.aliyun.com/zh/model-studio/dify)。

## **下一步**

**查看更多模型**

示例代码以 qwen-plus 模型为例，阿里云百炼还支持其他千问模型与 DeepSeek、Llama 等第三方模型，**支持的模型**以及对应的**API参考**文档请参见[选择模型](https://help.aliyun.com/zh/model-studio/models)。

**了解进阶用法**

示例代码仅完成了简单问答，如果您想了解千问 API 的更多用法，如[流式输出](https://help.aliyun.com/zh/model-studio/stream)、[结构化输出](https://help.aliyun.com/zh/model-studio/qwen-structured-output)、[Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)等，请参见[概述](https://help.aliyun.com/zh/model-studio/text-generation)目录。

**在线体验大模型**

如果您想像[千问官网](https://tongyi.aliyun.com/qianwen/)一样，通过**对话框**与大模型互动，请访问模型体验（[北京](https://bailian.console.aliyun.com/?tab=model#/efm/model_experience_center/text)或[新加坡](https://modelstudio.console.aliyun.com/?tab=dashboard#/efm/model_experience_center/text)）。

> 千问官网将千问 API 与联网搜索、网页解析等工具进行了集成，与直接调用千问 API 效果略有差异。

**0代码进行大模型微调**

通常来说，对大模型微调需要有人工智能知识背景与工程能力，阿里云百炼提供了0代码对大模型进行微调的功能，您仅需提供数据集即可。详情请参见[在控制台进行模型调优](https://help.aliyun.com/zh/model-studio/model-training-on-console)。
