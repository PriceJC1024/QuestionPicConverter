# 考题识图助手 QuestionPicConverter

## 简介
考题识图助手(QuestionPicConverter)是一款专为雅思/托福备考场景设计的图片识别与数据整理工具。该工具能够自动识别包含雅思口语、托福听力/阅读/写作题型的截图内容，通过AI模型提取结构化信息并批量导出为Excel表格，解决了手动整理试题截图效率低、易出错的问题。工具内置多AI模型可选，兼顾识别准确率、速度与成本，同时提供可视化操作界面，无需编程基础即可轻松使用。

## 功能亮点
1. **多题型适配**：支持雅思口语（Part 1/Part 2&3）、托福听力、托福阅读（选择题）、托福写作（造句题）四类题型的精准识别与结构化提取；
2. **AI模型可选**：内置 qwen3.7-plus（高准确率/中速/低成本）、kimi-k2.6（高准确率/高速/高成本）两款模型，可根据需求灵活切换；
3. **批量处理能力**：支持文件夹级别的图片批量识别，自动递归扫描文件夹内所有jpg/jpeg/png格式截图；
4. **可视化操作界面**：基于CustomTkinter构建的现代化深色UI，操作流程清晰，包含进度条、状态提示、结果弹窗等交互反馈；
5. **数据结构化输出**：AI识别结果自动转换为标准JSON格式，最终汇总导出为Excel表格，便于后续编辑与复用；
6. **严格的数据校验**：内置API Key格式校验、文件夹路径验证、JSON内容提取等机制，降低操作失误概率；
7. **自动清理临时文件**：识别过程中生成的JSON临时文件会自动清理，避免冗余文件堆积。



## 使用说明
### 环境准备
1. 确保已安装Python 3.8+版本；
2. 安装依赖包：
   ```bash
   pip install customtkinter pandas dashscope CTkMessagebox openpyxl
   ```
3. 获取并准备DashScope API Key（通义千问/阶跃星辰Kimi API）。

### 操作步骤
1. 运行程序：
   ```bash
   python main.py
   ```
2. 输入API Key：在界面中填写有效的DashScope API Key，系统会自动校验格式；
3. 选择图片文件夹：点击「Select Folder」按钮，选择存放试题截图的文件夹，程序会自动统计图片数量；
4. 选择任务类型：从下拉菜单中选择对应的题型（雅思口语/托福听力/托福阅读/托福写作）；
5. 选择AI模型：根据需求选择AI模型（qwen3.7-plus/kimi-k2.6）；
6. 开始处理：点击「Proceed」按钮，程序会批量识别图片并生成Excel文件；
7. 查看结果：处理完成后，程序会弹出提示，当前目录下会生成以日期命名的Excel文件（如`OutputTable2024-01-01.xlsx`）。

### 注意事项
- AI识别结果并非100%准确，建议手动核对Excel文件内容；
- 确保截图内容清晰，无严重模糊/遮挡，否则会影响识别效果；
- 处理大量图片时，建议选择合适的AI模型（kimi-k2.6速度更快但成本更高）。

## 技术栈
- **前端UI**：CustomTkinter（UI框架）、CTkMessagebox（弹窗组件）；
- **后端核心**：Python 3.x、多线程（ThreadPoolExecutor/threading）；
- **AI交互**：DashScope SDK（阿里云通义千问）；
- **数据处理**：Pandas（Excel导出）、JSON（结构化数据存储）、Pathlib（文件路径处理）；
- **辅助工具**：正则表达式（数据校验）、Shutil（文件/文件夹操作）。

## 开源协议
本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源协议，您可以自由使用、修改、分发本项目，商用需保留原作者版权声明。


<img width="1187" height="795" alt="image" src="https://github.com/user-attachments/assets/cb015b8b-ca59-4421-87ee-8e364a51094f" />
<img width="2001" height="1002" alt="image" src="https://github.com/user-attachments/assets/8f67d99f-65aa-4cdc-ab3e-b2a6f0f1f341" />
