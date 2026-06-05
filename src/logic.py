from pathlib import Path
from shutil import rmtree
from src import utils
import pandas as pd
import dashscope
import config
import json
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


class Logic:

    def __init__(self):
        self.j_folder_name = "JSON识别文件"

    def _set_up_json_folder(self, folder_name: str) -> str:
        """
        Detect whether target folder exists.
        If it is, delete all files in it.
        If it is not, create a new folder with the exact name.
        :param folder_name: str
        :return: None
        """
        f_path = Path(folder_name)
        if f_path.exists():
            rmtree(f_path)
        f_path.mkdir()

    def _ask_ai_about_img(self,
                          api_key: str,
                          img: str,
                          ai_model: str,
                          prompt: str = config.TF_L_PROMPT) -> str:
        """
        Primary function to call AI to abstract correct info from pictures.
        The prompt is set in config.



        :param ai_model: str
        :param api_key: str
        :param img: str
        :param prompt: str
        :return:
        """

        messages = [
            {
                "role": "user",
                "content": [
                    {"image": img},
                    {"text": prompt}
                ]
            }
        ]

        resp = dashscope.MultiModalConversation.call(
            api_key=api_key,
            model=ai_model,
            messages=messages,
            enable_thinking=False,
            response_format={"type": "json_object"},
        )

        if resp.status_code == 200:
            self.result = resp.output.choices[0].message.content[0]["text"]
            return self.result
        else:
            print(f"❌ AI 识别失败：{resp.status_code}")
            return ""

    def launch_ai_recog(self,
                        api_key: str,
                        img_path_list: list[str] | list[Path],
                        ai_model: str,
                        workers: int = 4,
                        prompt: str = config.TF_L_PROMPT,
                        progress_callback=None) -> None:
        """
        多线程并发调用 AI 识别图片
        """
        self._set_up_json_folder(self.j_folder_name)
        total = len(img_path_list)

        # 用于保护进度回调和打印输出的线程锁，防止多线程下输出混乱或回调状态异常
        progress_lock = threading.Lock()
        completed_count = 0

        def _process_single_image(img_path):
            """单张图片的处理逻辑（在线程中执行）"""
            nonlocal completed_count

            img_path_str = str(img_path)
            print(f"🔍 正在识别：{img_path_str}")

            # 调用 AI 识别
            result: str = self._ask_ai_about_img(
                api_key=api_key,
                img=img_path_str,
                prompt=prompt,
                ai_model=ai_model
            )
            result = utils.jsonized(result)

            # 写入 JSON 文件（每个线程写不同文件，无需加锁）
            name = Path(img_path_str).stem
            with open(f"{self.j_folder_name}/{name}.json", "w", encoding="utf-8") as f:
                f.write(result)

            # 线程安全地更新进度
            with progress_lock:
                completed_count += 1
                if progress_callback:
                    progress_callback(completed_count, total)

            return img_path_str

        # 使用 ThreadPoolExecutor 进行多线程并发
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # 提交所有任务
            future_to_path = {
                executor.submit(_process_single_image, img_path): img_path
                for img_path in img_path_list
            }

            # 等待任务完成并处理可能的异常
            for future in as_completed(future_to_path):
                try:
                    future.result()
                except Exception as e:
                    img_path = future_to_path[future]
                    print(f"❌ 识别失败：{img_path}，错误信息：{e}")

        print("✅ AI 识别全部完成")

    def json_to_excel(self) -> None:

        folder: Path = Path(self.j_folder_name)
        files: list = list(folder.rglob("*.json"))
        df_list: list = []

        for f in files:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            df_list.append(pd.DataFrame([data]))

        final: pd.DataFrame = pd.concat(df_list, ignore_index=True)
        # final["part"] = final["part"].replace("Part 3", "Part 2&3")
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"导出表{date_str}.xlsx"
        final.to_excel(filename, index=False)
        print(f"✅ Excel 已生成：{filename}")
