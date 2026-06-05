APP_TITLE: str = "QuestionPicConverter  Ver.2.1"
APP_WIN_TITLE: str = "~ 题图识别制表工具 Ver.2.1 ~"
APP_DESC: str = "识别不同类型的题目截图，提取内容到excel表格。\n【警告】AI识别不能保证100%准确，请勿跳过人工审查步骤。"

APPEARANCE_MODE: str = "Dark"
COLOR_THEME = "blue"
DEFAULT_FONT_SIZE: int = 19
APP_WINDOW_SIZE: str = "600x500"
APP_WINDOW_HORI_RESIZABLE: bool = False
APP_WINDOW_VERTI_RESIZABLE: bool = False

IELTS_O_PROMPT: str = """
        背景：你拿到的是一张记载了雅思口语题目的图片。图片可能仅包含Part 1，也可能仅包含Part 2 & Part 3
        任务： 提取图片中的题目内容文字，将结果按照要求保存为JSON格式。

        要求：
        1. 如果图片是 Part 1 的数据，那么按照以下JSON格式返回你的结果：
        {
        "title":
        "part": Part 1，
        "q1": 
        "q2":
        ...（图片中有多少小问，就依次添加相应的键）
        }

        2. 如果图片是 Part 2 & Part 3 的数据，那么按照以下JSON格式返回你的结果：
        {
        "title":
        "part": Part 2，
        "directions": (将Part 2题目内容全部放入，不区分小题。该内容通常包含1句指令和You should say部分)
        "part": Part 3
        "q1": 
        "q2":
        ...（图片中有多少小问，就依次添加相应的键）
        }

        3. 对于无法归入的数据，比如“待补充”这样的文本，舍弃。

        4. 严格遵守任务要求和格式契约，纯净输出，不要有额外内容。

"""

TF_L_PROMPT: str = """
        背景：你拿到的是一张记载了托福听力试题的图片。图片包括题干和可供考生选择的4个选项。
        任务： 提取图片中的题干文字和选项文字，将结果按照要求保存为JSON格式。

        JSON格式要求：
        {
        "Question Stem":
        "Option A":
        "Option B": 
        "Option C": 
        "Option D":
        }
        
        其它要去：
        1. 对于不属于听力题目的数据，请舍弃，不要识别。
        2. 严格遵守JSON格式和内容约定，纯净输出，不要有额外内容。

"""

TF_R_PROMPT: str = """
        背景：你拿到的是一张记载了托福阅读试题的图片。图片包括阅读材料、题干和可供考生选择的4个选项。
        任务： 提取图片中的阅读材料文字、题干文字和选项文字，将结果按照要求保存为JSON格式。

        JSON格式要求：
        {
        "Reading Material":
        "Question Stem":
        "Option A":
        "Option B": 
        "Option C": 
        "Option D":
        }

        其它要去：
        1. 对于不属于阅读题目的数据，请舍弃，不要识别。
        2. 严格遵守JSON格式和内容约定，纯净输出，不要有额外内容。

"""

TF_BS_PROMPT: str = """
        背景：你拿到的是一张记载了托福写作BuildSentence试题的图片。
        此题向考生提供完整的上句、挖空的下句和待填入词项。
        任务： 提取图片中的完整上句，挖空的下句和待填入词项，将结果按照要求保存为JSON格式。

        JSON格式要求：
        {
        "Complete Sentence":
        "Incomplete Sentence":
        "Word 1":
        "Word 2": 
        "Word 3": 
        "Word 4":
        (根据Word数量动态添加相应键...)
        }

        其它要去：
        1. 对于不属于阅读题目的数据，请舍弃，不要识别。
        2. Incomplete Sentence 挖空数量需要与图片中内容严格一致，且一个空用4个英文半角下划线表示。
        3. 严格遵守JSON格式和内容约定，纯净输出，不要有额外内容。

"""

MODE_OPS: list = ["雅思口语", "托福听力", "托福阅读（选择题）", "托福写作(组句题)"]
PROMPT_MAP: dict = {
    "托福听力": TF_L_PROMPT,
    "雅思口语": IELTS_O_PROMPT,
    "托福阅读（选择题）": TF_R_PROMPT,
    "托福写作(组句题)": TF_BS_PROMPT,
}

AI_MODEL_OPS: list = ["qwen3.7-plus（准确，稍慢，便宜）", "kimi-k2.6（准确，极快，贵）"]
AI_MAP: dict = {
    "qwen3.7-plus（准确，稍慢，便宜）": "qwen3.7-plus",
    "kimi-k2.6（准确，极快，贵）": "kimi-k2.6",
}
DEFAULT_AI = AI_MAP["qwen3.7-plus（准确，稍慢，便宜）"]
