# QuestionPicConverter

**Exam Question Image Recognition Assistant**

---

## Introduction

QuestionPicConverter, the Exam Question Image Recognition Assistant, is an image recognition and data organization tool specially designed for IELTS and TOEFL preparation.

It can automatically identify screenshots featuring question types from IELTS Speaking and TOEFL Listening, Reading and Writing. Powered by AI models, it extracts structured information and exports data in batches to Excel spreadsheets, addressing the low efficiency and high error rate of manually organizing exam screenshots.

The tool comes with two optional built-in AI models that strike a balance among recognition accuracy, processing speed and cost, and it also features a visual operation interface.

---

## 简介

考题识图助手（QuestionPicConverter）是一款专为雅思/托福备考场景设计的图片识别与数据整理工具。

该工具能够自动识别包含雅思口语、托福听力/阅读/写作题型的截图内容，通过 AI 模型提取结构化信息并批量导出为 Excel 表格，解决了手动整理试题截图效率低、易出错的问题。

工具内置两款可供选择的 AI 模型，兼顾识别准确率、速度与成本，同时提供可视化操作界面。

---

# Features

1. **Multi-question Type Adaptation**
   It accurately identifies and structurally extracts content for four question types:

   * IELTS Speaking (Part 1 / Part 2 & 3)
   * TOEFL Listening
   * TOEFL Reading (multiple-choice questions)
   * TOEFL Writing (sentence-building tasks)

2. **Selectable AI Models**
   Two built-in models are available for flexible switching as needed:

   * `qwen3.7-plus` (high accuracy, moderate speed, low cost)
   * `kimi-k2.6` (high accuracy, fast speed, high cost)

3. **Batch Processing Capability**
   Supports batch image recognition at the folder level and automatically recursively scans all screenshots in JPG/JPEG/PNG formats within folders.

4. **Visual Operation Interface**
   Featuring a modern dark-mode UI built with CustomTkinter, it delivers a straightforward workflow with interactive elements including progress bars, status prompts and result pop-up windows.

5. **Structured Data Output**
   AI recognition results are automatically converted into standard JSON format, and all data can be compiled and exported as Excel spreadsheets for easy subsequent editing and reuse.

6. **Strict Data Validation**
   Built-in mechanisms verify API Key formats, folder paths and extracted JSON content to reduce operational errors.

7. **Automatic Temporary File Cleanup**
   Temporary JSON files generated during recognition are deleted automatically to prevent redundant file accumulation.

---

# 功能特点

1. **多题型适配**
   支持以下四类题型的精准识别与结构化提取：

   * 雅思口语（Part 1 / Part 2&3）
   * 托福听力
   * 托福阅读（选择题）
   * 托福写作（造句题）

2. **AI 模型可选**
   内置两款模型，可根据需求灵活切换：

   * `qwen3.7-plus`（高准确率 / 中速 / 低成本）
   * `kimi-k2.6`（高准确率 / 高速 / 高成本）

3. **批量处理能力**
   支持文件夹级别的图片批量识别，自动递归扫描文件夹内所有 JPG/JPEG/PNG 格式截图。

4. **可视化操作界面**
   基于 CustomTkinter 构建现代化深色 UI，提供进度条、状态提示、结果弹窗等交互反馈。

5. **数据结构化输出**
   AI 识别结果自动转换为标准 JSON 格式，最终汇总导出为 Excel 表格，便于后续编辑与复用。

6. **严格的数据校验**
   内置 API Key 格式校验、文件夹路径验证、JSON 内容提取等机制，降低操作失误概率。

7. **自动清理临时文件**
   自动删除识别过程中生成的 JSON 临时文件，避免冗余文件堆积。

---

# Instructions

## Environment Preparation

1. Ensure Python 3.8 or a later version is installed.

2. Install the required packages:

```bash
pip install customtkinter pandas dashscope CTkMessagebox openpyxl
```

3. Obtain and prepare your DashScope API Key (Qwen).

---

## 环境准备

1. 确保已安装 Python 3.8 及以上版本；

2. 安装依赖包：

```bash
pip install customtkinter pandas dashscope CTkMessagebox openpyxl
```

3. 获取并准备 DashScope API Key（通义千问）。

---

## Operating Steps

1. Run the program:

```bash
python main.py
```

2. Enter the API Key.
   Fill in a valid DashScope API Key on the interface. The system will automatically verify its format.

3. Select image folder.
   Click the **Select Folder** button and choose the folder storing exam screenshots. The program will automatically count the number of images.

4. Select task type.
   Pick the corresponding question type from the dropdown menu:

   * IELTS Speaking
   * TOEFL Listening
   * TOEFL Reading
   * TOEFL Writing

5. Select AI model.
   Choose an AI model as needed:

   * `qwen3.7-plus`
   * `kimi-k2.6`

6. Start processing.
   Click the **Proceed** button. The program will recognize images in batches and generate an Excel file.

7. Check results.
   A prompt will pop up once processing is finished. An Excel file named by date (e.g., `OutputTable2024-01-01.xlsx`) will be created in the current directory.

---

## 操作步骤

1. 运行程序：

```bash
python main.py
```

2. 输入 API Key。
   在界面中填写有效的 DashScope API Key，系统会自动校验格式。

3. 选择图片文件夹。
   点击 **Select Folder** 按钮，选择存放试题截图的文件夹，程序会自动统计图片数量。

4. 选择任务类型。
   从下拉菜单中选择对应题型：

   * 雅思口语
   * 托福听力
   * 托福阅读
   * 托福写作

5. 选择 AI 模型。
   根据需求选择：

   * `qwen3.7-plus`
   * `kimi-k2.6`

6. 开始处理。
   点击 **Proceed** 按钮，程序会批量识别图片并生成 Excel 文件。

7. 查看结果。
   处理完成后会弹出提示，并在当前目录生成以日期命名的 Excel 文件（例如：`OutputTable2024-01-01.xlsx`）。

---

# Notes

* The AI recognition results are not 100% accurate. It is recommended to manually check the content in the Excel file.
* Please ensure the screenshots are clear without severe blurriness or obstruction; otherwise, recognition performance will be affected.
* When processing a large number of images, select the appropriate AI model (`kimi-k2.6` delivers faster speed at a higher cost).

---

# 注意事项

* AI 识别结果并非 100% 准确，建议手动核对 Excel 文件内容；
* 请确保截图内容清晰，无严重模糊或遮挡，否则会影响识别效果；
* 处理大量图片时，建议选择合适的 AI 模型（`kimi-k2.6` 速度更快，但成本更高）。

---

# Technology Stack

* **Frontend UI:** CustomTkinter (UI framework), CTkMessagebox (popup component)
* **Backend Core:** Python 3.x, Multithreading (ThreadPoolExecutor / threading)
* **AI Integration:** DashScope SDK (Alibaba Cloud Tongyi Qianwen)
* **Data Processing:** Pandas (Excel export), JSON (structured data storage), Pathlib (file path handling)
* **Auxiliary Functions:** Regular expressions (data validation), Shutil (file and folder operations)

---

# 技术栈

* **前端 UI：** CustomTkinter（UI 框架）、CTkMessagebox（弹窗组件）
* **后端核心：** Python 3.x、多线程（ThreadPoolExecutor / threading）
* **AI 交互：** DashScope SDK（阿里云通义千问）
* **数据处理：** Pandas（Excel 导出）、JSON（结构化数据存储）、Pathlib（文件路径处理）
* **辅助功能：** 正则表达式（数据校验）、Shutil（文件/文件夹操作）

---

# License

This project is licensed under the **MIT License**.

You are free to use, modify and distribute this project. For commercial use, please retain the original copyright notice of the author.

---

# 协议

本项目采用 **MIT License** 开源协议。

您可以自由使用、修改、分发本项目；商用时请保留原作者版权声明。

---


<img width="1187" height="795" alt="image" src="https://github.com/user-attachments/assets/cb015b8b-ca59-4421-87ee-8e364a51094f" />
<img width="2001" height="1002" alt="image" src="https://github.com/user-attachments/assets/8f67d99f-65aa-4cdc-ab3e-b2a6f0f1f341" />
