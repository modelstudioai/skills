# 接入多模态备忘录Agent

基于多模态备忘录Agent，可以实现通过语音创建、查询、修改和删除备忘信息，适合应用于闹钟、日程管理、时间备忘等场景。

### 备忘录管理

在多模态备忘录Agent中，主要支持以下三种场景：

-   闹钟：设定时间提醒，包含时间、循环，如“定个明天下午两点的闹钟”、“每天早上八点提醒我”
    
-   日程：设定日程提醒，包含时间、时间和循环，如“一小时后提醒我提交报告”、“提醒我每周二下午3点开会”
    
-   记录：记录重要信息，不包含时间，如“记录一下陈经理的电话，159xxxxxxxx”
    

在支持视觉理解的设备中，可以实现下发拍照指令，并基于图像信息创建备忘。如“帮我记录停车位”，可以下发拍照指令，并基于上传的图像提取停车位信息存入备忘录。

#### 创建备忘

##### 1\. 创建日程/闹钟

<时间>+<事件>+<循环>（可选）

###### 1.1. 单次提醒

入参样例：

提醒我明天中午12点吃饭

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称。

例如：set\_reminder

\[0\].params

Array

指令参数列表

\[0\].content

String

否

提醒的内容

\[0\].date

String

否

提醒的日期，yyyy-MM-dd

\[0\].time

String

否

提醒的时间（HH:mm:ss）

\[0\].pic\_url\_list

List<String>

否

视觉备忘时的图片列表

\[0\].reminder\_id

String

是

单条指令的唯一id

###### 1.2. 循环提醒

入参样例：

提醒我每周三中午12点吃饭

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称。

例如：set\_reminder

\[0\].params

Array

指令参数列表

\[0\].content

String

否

提醒的内容

\[0\].time

String

否

提醒的时间（HH:mm:ss）

\[0\].daysOfWeek

List<Integer>

否

每周几。

例如：提醒我每周1到周3下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].daysOfMonth

List<Integer>

否

每月几号。

例如：提醒我每月1号到3号下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].monthsOfYear

List<Integer>

否

每年几月。

例如：提醒我每年1月到3月下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].type

String

否

时间间隔的单位。默认为none，

minutely ：隔几分钟

hourly：隔几小时

daily：隔几天

weekly：隔几周

monthly：隔几月

yearly：隔几年

\[0\].interval

Integer

否

时间间隔的值。

当type有值时，此字段值不为空

\[0\].pic\_url\_list

List<String>

否

视觉备忘时的图片列表

\[0\].reminder\_id

String

是

单条指令的唯一id

###### 1.3. 间隔时间提醒

入参样例：

提醒我每隔两个小时喝一次水

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称。

例如：set\_reminder

\[0\].params

Array

指令参数列表

\[0\].content

String

否

提醒的内容

\[0\].type

String

否

时间间隔的单位。默认为none，

minutely ：隔几分钟

hourly：隔几小时

daily：隔几天

weekly：隔几周

monthly：隔几月

yearly：隔几年

\[0\].interval

Integer

否

时间间隔的值。当type有值时，此字段值不为空

\[0\].pic\_url\_list

List<String>

否

视觉备忘时的图片列表

\[0\].reminder\_id

String

是

单条指令的唯一id

  

##### 2\. 创建记录

<事件>

入参样例：

记住我的身份证件都放在书桌抽屉里

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称，例如：set\_reminder

\[0\].params

Array

指令参数列表

\[0\].content

String

否

提醒的内容

\[0\].pic\_url\_list

List<String>

否

视觉备忘时的图片列表

\[0\].reminder\_id

String

是

单条指令的唯一id

#### 修改备忘

入参样例：

把今晚6点吃饭的提醒推迟到今晚8点

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称，例如：update\_reminder

\[0\].params

Array

指令参数列表

\[0\].content

String

否

提醒的内容

\[0\].date

String

否

提醒的日期，yyyy-MM-dd

\[0\].time

String

否

提醒的时间（HH:mm:ss）

\[0\].daysOfWeek

List<Integer>

否

每周几。例如：提醒我每周1到周3下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].daysOfMonth

List<Integer>

否

每月几号。例如：提醒我每月1号到3号下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].monthsOfYear

List<Integer>

否

每年几月。例如：提醒我每年1月到3月下午3点睡觉，则该字段值为\[1,2,3\]

\[0\].type

String

否

时间间隔的单位。默认为none，

minutely ：隔几分钟

hourly：隔几小时

daily：隔几天

weekly：隔几周

monthly：隔几月

yearly：隔几年

\[0\].interval

Integer

否

时间间隔的值。当type有值时，此字段值不为空

\[0\].pic\_url\_list

List<String>

否

视觉备忘时的图片列表

\[0\].reminder\_id

String

是

单条指令的唯一id

* * *

#### 删除备忘

入参样例：

工作报告不需要提交了，这个事情取消

出参：

**参数**

**类型**

**必填**

**描述**

commands

Array

指令列表

\[0\].command\_request\_id

String

是

请求的uuid

\[0\].name

String

是

指令名称，例如：delete\_reminder

\[0\].params

Array

指令参数列表

\[0\].reminder\_id

String

是

单条指令的唯一id
