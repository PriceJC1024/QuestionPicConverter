from src import utils, logic
from tkinter import filedialog
from pathlib import Path
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import config
import threading
import re


class MainWindow:
    def __init__(self, root: ctk.CTk):
        # Global ctk configuration
        ctk.set_appearance_mode(config.APPEARANCE_MODE)
        ctk.set_default_color_theme(config.COLOR_THEME)
        ctk.ThemeManager.theme["CTkFont"] = ctk.CTkFont(size=config.DEFAULT_FONT_SIZE)

        # App instance initialization
        self.root: ctk.CTk = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.APP_WINDOW_SIZE)
        self.root.resizable(config.APP_WINDOW_HORI_RESIZABLE, config.APP_WINDOW_VERTI_RESIZABLE)
        self.api_key_content = "Null"
        self.pic_path_collection = None
        self.smooth_progress_target = 0
        self.smooth_progress_running = False
        self.op_value = config.TF_L_PROMPT
        self.ai_model = config.DEFAULT_AI

        # Initialize backend logic
        self.logic_obj: logic.Logic = logic.Logic()  # 后端逻辑对象

        # Build widgets
        self._set_up_widgets()

    def _set_up_widgets(self) -> None:
        """
        Set up app widgets.

        :return: None
        """
        # =============== 标题 & 介绍 ===============  #
        self.frame_title = ctk.CTkFrame(self.root)
        self.frame_title.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.title: ctk.CTkLabel = ctk.CTkLabel(self.frame_title,
                                                text=config.APP_WIN_TITLE,
                                                font=("Arial", 22, "bold"), )
        self.title.grid(row=0, column=0, pady=10)

        self.desc_text: ctk.CTkLabel = ctk.CTkLabel(self.frame_title, text=config.APP_DESC,
                                                    text_color="green",)
        self.desc_text.grid(row=1, column=0, sticky="w")

        # =============== 设置Qwen-API KEY ===============  #
        self.frame_api_box = ctk.CTkFrame(self.root)
        self.frame_api_box.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.api_input_desc: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="请输入你的Qwen API Key: ")
        self.api_input_desc.grid(row=0, column=0, sticky="w")

        self.api_input_entry: ctk.CTkEntry = ctk.CTkEntry(self.frame_api_box, width=350)
        self.api_input_entry.grid(row=0, column=1, sticky="w")
        self.api_input_entry.bind("<KeyRelease>", self._on_input_change)

        self.api_show_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="读取到的API Key：", text_color="red")
        self.api_show_hint.grid(row=1, column=0, sticky="w")
        self.api_show_label: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="")
        self.api_show_label.grid(row=1, column=1, sticky="w")

        # =============== 设置存放图片文件夹路径 ===============  #
        self.frame_pic_handle_box = ctk.CTkFrame(self.root)
        self.frame_pic_handle_box.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.choose_f_path_desc: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box,
                                                             text="请选择存放图片的【文件夹】路径: ")
        self.choose_f_path_desc.grid(row=0, column=0, sticky="w")
        self.choose_f_path_bt: ctk.CTkButton = ctk.CTkButton(self.frame_pic_handle_box, text="选择文件夹",
                                                             command=self._on_select_folder_finished)
        self.choose_f_path_bt.grid(row=0, column=1, sticky="w")

        self.chosen_f_path_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="读取到的文件夹路径：",
                                                             text_color="red")
        self.chosen_f_path_hint.grid(row=1, column=0, sticky="w")
        self.chosen_f_path_lbl: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="", text_color="red")
        self.chosen_f_path_lbl.grid(row=1, column=1, sticky="w")

        self.pic_count_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="文件夹内图片数：",
                                                         text_color="red")
        self.pic_count_hint.grid(row=2, column=0, sticky="w")
        self.pic_count_lbl: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="", text_color="red")
        self.pic_count_lbl.grid(row=2, column=1, sticky="w")

        # ===================== 下拉选项组件 =====================
        self.frame_options = ctk.CTkFrame(self.root)
        self.frame_options.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.option_menu = ctk.CTkOptionMenu(
            self.frame_options,
            values=config.MODE_OPS,
            width=300,
            font=("Arial", 18, "bold"),
            command=self._on_op_change
        )
        op_desc = ctk.CTkLabel(self.frame_options, text="请选择任务类型：")
        op_desc.grid(row=0, column=0)
        self.option_menu.grid(row=0, column=1, )

        # =============== 模型选择区 ===============  #
        self.model_op_frame: ctk.CTkFrame = ctk.CTkFrame(self.root)
        self.model_op_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.model_op_menu = ctk.CTkOptionMenu(
            master=self.model_op_frame,
            values=config.AI_MODEL_OPS,
            width=400,
            font=("Arial", 18, "bold"),
            command=self._on_ai_op_change
        )
        ai_op_desc = ctk.CTkLabel(self.model_op_frame, text="请选择AI模型：")
        ai_op_desc.grid(row=0, column=0)
        self.model_op_menu.grid(row=0, column=1, )

        # =============== 执行按钮区 ===============  #
        self.main_process_bt: ctk.CTkButton = ctk.CTkButton(self.root, text="开始执行", command=self._main_process)
        self.main_process_bt.grid(row=6, column=0, pady=10)

        # =============== 进度条区 ===============  #
        self.progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(self.root, width=570, height=30)
        self.progress_bar.grid_forget()

    def _on_ai_op_change(self, selected_value: str) -> None:
        self.ai_model = config.AI_MAP.get(selected_value, config.DEFAULT_AI)
        print("当前选择的模型:", self.ai_model)

    def _on_op_change(self, selected_value: str) -> None:
        self.op_value = config.PROMPT_MAP.get(selected_value, config.TF_L_PROMPT)

    def _update_progress(self, current, total) -> None:
        """设置目标进度，由动画平滑过去"""
        self.smooth_progress_target = current / total
        if not self.smooth_progress_running:
            self._smooth_progress_animation()

    def _main_process(self) -> None:
        """
        Launch subprocess to abstract infos from pics in given pic folder,
        then write result into several .json files, and finally
        write it into .xlsx file.

        This is the mian function of the app.

        :return: None
        """

        self.main_process_bt.configure(text="处理中...",
                                       state=ctk.DISABLED)
        task_thread = threading.Thread(
            target=self._background_task,
            daemon=True
        )

        task_thread.start()
        # 重置平滑进度
        self.progress_bar.set(0)
        self.smooth_progress_target = 0
        self.progress_bar.set(0.0)  # initialize progress bar
        self.progress_bar.grid(row=7, column=0, pady=20)

    def _background_task(self) -> None:
        """
        Background process logic.
        This function should only be invoked by _main_process().

        :return: None
        """
        try:
            print(self.api_key_content)

            self.logic_obj.launch_ai_recog(api_key=self.api_key_content,
                                           img_path_list=self.pic_path_collection,
                                           prompt=self.op_value,
                                           ai_model=self.ai_model,
                                           progress_callback=lambda current, total: self.root.after(
                                               0, self._update_progress, current, total
                                           ))
            self.logic_obj.json_to_excel()

            self.root.after(0, lambda: self.progress_bar.set(1.0))

            self.root.after(0,
                            lambda: CTkMessagebox(title="执行完成",
                                                  message="图像识别完成，数据已成功写入表格！",
                                                  width=400,
                                                  height=250,
                                                  icon="check",
                                                  icon_size=(40, 40),
                                                  font=("Arial", 16)))


        except Exception as e:
            err_msg = f"错误：{str(e)}"
            self.root.after(0,
                            lambda: CTkMessagebox(title="错误",
                                                  message=err_msg,
                                                  width=400,
                                                  height=250,
                                                  icon="cancel",
                                                  icon_size=(40, 40),
                                                  font=("Arial", 16)))
        finally:
            self.root.after(0, lambda: self.main_process_bt.configure(text="开始执行", state=ctk.NORMAL))
            self.progress_bar.grid_forget()

    def _smooth_progress_animation(self):
        """进度条平滑增长动画"""
        self.smooth_progress_running = True

        current = self.progress_bar.get()
        target = self.smooth_progress_target

        if abs(current - target) < 0.001:
            self.progress_bar.set(target)
            self.smooth_progress_running = False
            return

        new_progress = current + (target - current) * 0.15
        self.progress_bar.set(new_progress)

        self.root.after(15, self._smooth_progress_animation)

    def _on_select_folder_finished(self) -> None:
        """
        Invoke system asking-directory dialogue. Once this is done, catch
        that chosen folder path, automatically and recursively get all images (.jpg, .jpeg, .png)
        in that folder. After that, count them and update label display.

        :return: None
        """
        self.pic_folder_path: str = filedialog.askdirectory(title="选择存放图片的文件夹路径")
        self.pic_path_collection: list[Path] = utils.get_images_in_folder(self.pic_folder_path)
        (self.pic_folder_path, path_is_correct) = Validator.pic_folder_path_validation(self.pic_folder_path)
        if path_is_correct:
            pic_count = len(self.pic_path_collection)
        else:
            pic_count = 0

        simplified_pic_folder_path: str = Validator.simplify_folder_path(self.pic_folder_path)
        self.chosen_f_path_lbl.configure(text=simplified_pic_folder_path)
        self.pic_count_lbl.configure(text=pic_count)

        self.api_key_content: str = self.api_input_entry.get().strip()
        self.api_key_content = Validator.validate_api_string(self.api_key_content)
        self.api_show_label.configure(text=f"{self.api_key_content}", text_color="red")

    def _on_input_change(self, event) -> None:
        """
        Once user finishes input, update api-keys display.

        :param event:
        :return: None
        """
        self.api_key_content: str = self.api_input_entry.get().strip()
        self.api_key_content = Validator.validate_api_string(self.api_key_content)
        self.api_show_label.configure(text=f"{self.api_key_content}", text_color="red")

    def launch(self) -> None:
        """
        launch the app main window, just like you double-click a .exe file.

        :return: None
        """
        self.root.mainloop()


class Validator:
    """
    This class has a lot of validation function
    to clean data.

    """

    @staticmethod
    def pic_folder_path_validation(org_path: str) -> tuple[str, bool]:
        """
        Validate a folder path in str form.
        Return a tuple that the first element is the cleaned path, and the second
        element is a True value to symbol that the path is corrected.
        Otherwise, return "" the tuple's first element, and False in the second element,
        in order to symbolize that the path is incorrect.


        :param org_path: str
        :return: tuple[str, bool]
        """
        if len(org_path) == 0:
            return "", False
        else:
            org_path = org_path.strip()
            return org_path, True

    @staticmethod
    def simplify_folder_path(org_path: str) -> str:
        """
        Simplifies a given folder path string by truncating intermediate directories.
        If the path has more than 3 segments after splitting by '/', replace all middle segments
        with an ellipsis (...), keeping only the first, second, and last segments.
        If the path has 3 or fewer segments, returns the original path unchanged.

        :param org_path: Original folder path string separated by forward slashes (/)
        :return: Simplified path string with intermediate directories abbreviated if applicable
        """
        text_elements: list = org_path.split("/")
        if len(text_elements) > 3:
            result: str = "/".join([text_elements[0], text_elements[1], "...", text_elements[-1]])
            return result
        else:
            return org_path

    @staticmethod
    def validate_api_string(org_api_content: str) -> str:
        org_api_content = org_api_content.strip()
        if re.search(r'[^a-zA-Z0-9-]', org_api_content):
            return "Api Key中只能包含英文、数字和短横线！"
        elif len(org_api_content) >= 40:
            return "长度过长的Api Key，请检查！"
        elif len(org_api_content) == 0:
            return "没有读取到Api Key!"
        else:
            return org_api_content
