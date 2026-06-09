import threading
import pandas as pd
import dashscope
import config
import json
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from shutil import rmtree
from src import utils


class Logic:
    """
    Backend functions of the App.
    """

    def __init__(self):
        self.j_folder_name = "JSONrecogs"

    @staticmethod
    def _set_up_json_folder(folder_name: str) -> None:
        """
        Resets the target folder for JSON files.

        Deletes the entire folder if it already exists, then creates a new empty folder.

        :param folder_name: Name or path of the target folder
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
        Calls the DashScope multimodal AI model to analyze a single image and return structured information.

        Sends the image path and prompt to the specified AI model, requests JSON format response,
        and returns the extracted text content on success. Returns empty string on API failure.

        :param api_key: API key for authenticating with the DashScope service
        :param img: Local file path of the image to be analyzed
        :param ai_model: Name of the AI model to use for recognition
        :param prompt: Instruction prompt defining what information to extract from the image
        :return: Extracted text result from AI response; empty string if request fails
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
            self.result = str(self.result)
            return self.result
        else:
            print(f"❌ AI recognition failed：{resp.status_code}")
            return ""

    def launch_ai_recog(self,
                        api_key: str,
                        img_path_list: list[str] | list[Path],
                        ai_model: str,
                        workers: int = 4,
                        prompt: str = config.TF_L_PROMPT,
                        progress_callback=None) -> None:
        """
        Performs AI image recognition using multi-threading.

        Creates a dedicated folder to store JSON results, processes images concurrently
        via thread pool, calls the AI model for each image, saves returned data as JSON files,
        and invokes the progress callback to report processing progress. Thread lock is used
        to ensure thread safety for progress updates. Failed tasks will print error details.

        :param api_key: Authentication key for accessing the AI service
        :param img_path_list: List of paths pointing to target images
        :param ai_model: Name or identifier of the selected AI model
        :param workers: Maximum number of concurrent threads, defaults to 4
        :param prompt: Instruction prompt sent to the AI model, uses default prompt if not specified
        :param progress_callback: Callback function to report completed count and total tasks
        :return: None
        """
        self._set_up_json_folder(self.j_folder_name)
        total = len(img_path_list)

        # A thread lock used to protect progress callbacks and print outputs,
        # preventing output confusion or abnormal callback states in multi-threaded environments
        progress_lock = threading.Lock()
        completed_count = 0

        def _process_single_image(img_path):
            nonlocal completed_count

            img_path_str = str(img_path)

            result: str = self._ask_ai_about_img(
                api_key=api_key,
                img=img_path_str,
                prompt=prompt,
                ai_model=ai_model
            )
            result = utils.jsonized(result)
            name = Path(img_path_str).stem
            with open(f"{self.j_folder_name}/{name}.json", "w", encoding="utf-8") as f:
                f.write(result)

            with progress_lock:
                completed_count += 1
                if progress_callback:
                    progress_callback(completed_count, total)

            return img_path_str

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_path = {
                executor.submit(_process_single_image, img_path): img_path
                for img_path in img_path_list
            }

            for future in as_completed(future_to_path):
                try:
                    future.result()
                except Exception as e:
                    img_path = future_to_path[future]
                    print(f"❌ failed to recognize:：{img_path}， Error Info：{e}")

    def json_to_excel(self) -> None:
        """
        Transform JSON files to excel.
        Then delete JSON files folder.

        :return: None
        """
        folder: Path = Path(self.j_folder_name)
        files: list = list(folder.rglob("*.json"))
        df_list: list = []

        for f in files:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            df_list.append(pd.DataFrame([data]))

        final: pd.DataFrame = pd.concat(df_list, ignore_index=True)
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"OutputTable{date_str}.xlsx"
        final.to_excel(filename, index=False)

        # Delete JSON files folder.
        if Path(self.j_folder_name).exists():
            rmtree(Path(self.j_folder_name))
