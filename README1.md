# COMP7640数据库系统与管理
## 小组项目作业
### 目标
在本项目中，每个小组的任务是创建并执行一个多供应商电子商务平台，重点关注个性化的用户体验。
### 基本要求
- **供应商资料**：平台上的每个供应商都将维护一个唯一的资料，其中包括供应商ID、企业名称、客户反馈评分、地理分布以及产品库存。产品通过唯一的产品ID进行标识，有名称、标价，并且最多有三个由供应商设置的概括产品特性的标签。
- **客户资料**：必须为客户维护一个全面的数据库，其中包括客户ID、联系电话、送货详情和订单历史。
- **交易记录**：每笔购买交易都与一个客户资料相关联，并且必须详细记录从供应商目录中购买至少一种产品的情况。同一订单中的交易可以涉及多个供应商。
### 所需功能
- **供应商管理**：平台应具备以下功能：1）显示所有供应商的列表；2）将新供应商引入市场。
- **产品目录管理**：用户应能够：1）浏览特定供应商提供的所有产品；2）向供应商的目录中添加新产品。
- **产品发现**：系统必须提供搜索功能，允许用户使用标签查找产品。搜索应返回标签与产品名称的任何部分或其相关标签匹配的产品。
- **产品购买**：应支持产品购买，并在数据库中记录哪个客户购买了哪个产品。
- **订单修改**：用户必须有选项在订单进入发货流程之前修改订单，包括移除特定产品或取消整个订单。
### 系统实现
编写一个Python程序（命令行界面或图形用户界面）来实现在线零售应用程序及所需功能。对于软件版本，强烈推荐Python 3.5，其他版本可能在系里的电脑上无法运行，从而影响成绩。

使用PyMySQL从Python程序访问MySQL。MySQL是开源的，可以在此处免费下载。
### 项目进度安排
本项目应以4 - 6人为一组进行，分为两个阶段。
- **阶段1：分组**
每个小组应有一名组长，并在2025年2月27日晚上11:59前在香港浸会大学Moodle平台上完成小组注册。请注意，无论小组人数多少，每个小组都将按照相同标准进行评分。如果在截止日期前未注册任何小组，将被随机分配到一个小组。

同一小组的每个成员将获得相同的分数，因此需要认真组建小组并学会与小组成员协作。请注意，小组人数多并不一定就好。
- **阶段2：数据库设计与系统实现**
1. 每个小组必须设计一个ER图，并将该图转换为关系表。
2. 每个小组必须实现所需的功能。
3. 每个小组需要提交最终报告的电子副本和实现代码的电子副本。
4. 每个小组需要编写一个README文件，描述如何运行代码。
5. 每个小组需要录制一个视频，时长必须小于或等于6分钟，向讲师（客户）推销数据库系统，内容包括ER图设计、关系表设计以及功能演示。
### 评分标准
- **正确性（40%）**：如果实现正确，将获得满分。部分正确的提交将获得部分分数。
- **视频演示（40%）**：将根据以下标准进行评分。
    1. 演示的清晰度（用于解释ER图、关系表和功能）（20%）
    2. 语言能力（10%）
    3. 演示的功能数量（10%）

请注意，此部分每个小组的总分将乘以系数(3 - x)÷3，其中x是视频超出6分钟的分钟数。如果视频时长大于或等于9分钟，该小组在此部分将得零分。
- **文档（20%）**：报告应简短、清晰、简洁且内容丰富。
### 提交（截止时间为2025年4月10日晚上11:59）
每个小组应提交一个名为groupX.zip的压缩文件。

groupX.zip文件应包含以下内容：
1. groupX_project.zip（Python项目源文件，其中包括所有实现函数的注释）
2. groupX_insert_sql.txt（用于创建表（含约束）和插入示例数据的SQL命令文件）
3. groupX_report.pdf（项目报告应包括：1. 小组成员，包括学生ID和姓名；2. ER图、表设计、规范化（如有）以及相应的解释，以帮助讲师/助教理解设计；3. 运行代码的自述说明）
4. groupX_video.mp4（视频）

注意：在上述文件中，将“X”替换为小组编号。

将压缩文件groupX.zip上传到BUMoodle。

每个小组只需提交一次，多次提交的情况下，仅收取最新的一次提交。

COMP7640 Database Systems and Administration
Group Project Assignment

Objective
In this project, each group is tasked with the creation and execution of a multi-vendor ecommerce platform with a focus on personalized user experiences.

Basic Requirements
Vendor Portfolios: Each vendor on the platform will maintain a unique profile that includes a vendor ID, business name, customer feedback score, geographical presence, and an inventory of products. Products are identified by a unique product ID, have a name, listed price, and up to three tags that encapsulate the product's nature, which are set by the vendor.
Customer Profiles: A comprehensive database must be maintained for customers, which includes a customer ID, contact number, shipping details, and order history.
Transaction Records: Every purchase transaction is linked to a customer profile and must detail the acquisition of at least one product from a vendor's catalog. Transactions can span multiple vendors within the same order.

Required Functionalities
Vendor Administration: The platform should enable functionality to 1) display a listing of all vendors, 2) onboard new vendors onto the marketplace.
Product Catalog Management: Users should have the ability to 1) browse all products offered by a specific vendor, 2) introduce new products to a vendor's catalog.
Product Discovery: The system must facilitate a search feature that allows users to discover products using tags. The search should return products where the tag matches any part of the product's name or its associated tags.
Product Purchase: You should support product purchase. Record in database which customer purchases which product.
Order Modification: Users must have the option to modify their orders, including the removal of specific products or the cancellation of the entire order before it enters the shipping process.

System Implementation
Write a Python program (command line interface or GUI) to implement the online retail application and required functions. For software versions, Python 3.5 are strongly recommended, while other versions might fail on departmental computers and affect the grading.
Use PyMySQL to access MySQL from the Python program, respectively. MySQL is open source and can be freely download here.

Project Schedule
The project should be carried out in groups of 4 - 6 members, which includes two phases.
Phase 1: Group forming
Each group should have a group leader and complete the group enrollment on HKBU Moodle by 11:59PM 27th February 2025. Kindly note that each group will be graded using the same standard regardless of the number of members. If you fail to enroll any group before the due date, you will be assigned to a group randomly.
Each member of the same group will receive the same marks, so you need to form your group carefully and learn how to collaborate with your group members. Note that it is not necessary to be good if there are many members in a group.
Phase 2: Database design & System implementation
1. Each group must design an ER diagram and convert the diagram to relational tables.
2. Each group must implement the required functionalities.
3. Each group needs to submit a soft copy of the final report and a soft copy of your code of implementation.
4. Each group needs to write a README file to describe how to run your code.
5. Each group needs to record a video, which must be less than or equal to 6 minutes, for selling the database system to the instructor (customer), which includes the design of ER diagram, the design of relational tables, and the demonstration of functionalities.

Grading Criteria
Correctness (40%): You will get full marks if your implementation is correct. Partial credit will be given to a partially correct submission.
Video demonstration (40%): You will be graded based on the following criteria.
1. Clearness of the presentation (for explaining the ER diagram, relational tables, and functionalities) (20%)
2. Language proficiency (10%)
3. Number of functionalities in the demonstration (10%)
Note that the total marks of this component for each group will be multiplied by the factor (3 - x) ÷3, where x is the number of minutes that the video time exceeds 6 minutes. If the video is more than or equal to 9 minutes, we will give this group zero mark in this component.
Documentation (20%): The report should be short, clear, concise, and informative.

Submission (due by 11:59pm, 10th April 2025)
Each group should submit a compressed file named groupX.zip.
The groupX.zip file should include the following items:
1. groupX_project.zip (Python project source files, which include comments of all your implemented functions.)
2. groupX_insert_sql.txt (the SQL command file for creating your tables (with constraints) and inserting sample data)
3. groupX_report.pdf (the project report should include: 1. group members, including student IDs and names; 2. ER diagram, table designs, normalization (if any), and the corresponding explanation for helping the instructor/TAs understand your design; 3. a readme description for running your code.) 4. groupX_video.mp4 (the video)
Note: Replace 'X' with your group no. in the above-mentioned files.
Upload your compressed file groupX.zip to BUMoodle.
Only ONE submission is required for each group, for multiple submissions, only the latest one will be collected.

