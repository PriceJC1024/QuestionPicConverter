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
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.APP_WINDOW_SIZE)
        self.root.resizable(config.APP_WINDOW_HORI_RESIZABLE, config.APP_WINDOW_VERTI_RESIZABLE)
        self.api_key_content = "Null"
        self.pic_path_collection = None
        self.smooth_progress_target = 0
        self.smooth_progress_running = False
        self.op_value = config.IELTS_O_PROMPT
        self.ai_model = config.DEFAULT_AI

        # Initialize backend logic
        self.logic_obj: logic.Logic = logic.Logic()

        # Build widgets
        self._set_up_widgets()

    def _set_up_widgets(self) -> None:
        """
        Set up app widgets.

        :return: None
        """
        # =============== Zone: Title & Intro ===============  #
        self.frame_title = ctk.CTkFrame(self.root)
        self.frame_title.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.title: ctk.CTkLabel = ctk.CTkLabel(self.frame_title,
                                                text=config.APP_WIN_TITLE,
                                                font=("Arial", 22, "bold"), )
        self.title.grid(row=0, column=0, pady=10)

        self.desc_text: ctk.CTkLabel = ctk.CTkLabel(self.frame_title, text=config.APP_DESC,
                                                    text_color="green", pady=10,
                                                    justify="left")
        self.desc_text.grid(row=1, column=0, sticky="w")

        # =============== Zone: Set Qwen-API KEY ===============  #
        self.frame_api_box = ctk.CTkFrame(self.root)
        self.frame_api_box.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.api_input_desc: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="Qwen API Key: ")
        self.api_input_desc.grid(row=0, column=0, sticky="w")

        self.api_input_entry: ctk.CTkEntry = ctk.CTkEntry(self.frame_api_box, width=350)
        self.api_input_entry.grid(row=0, column=1, sticky="w")
        self.api_input_entry.bind("<KeyRelease>", self._on_input_change)

        self.api_show_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="API Key read：", text_color="red")
        self.api_show_hint.grid(row=1, column=0, sticky="w")
        self.api_show_label: ctk.CTkLabel = ctk.CTkLabel(self.frame_api_box, text="")
        self.api_show_label.grid(row=1, column=1, sticky="w")

        # =============== Zone: Set Folder Path ===============  #
        self.frame_pic_handle_box = ctk.CTkFrame(self.root)
        self.frame_pic_handle_box.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.choose_f_path_desc: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box,
                                                             text="Picture Folder Path: ")
        self.choose_f_path_desc.grid(row=0, column=0, sticky="w")
        self.choose_f_path_bt: ctk.CTkButton = ctk.CTkButton(self.frame_pic_handle_box, text="Select Folder",
                                                             font=("Arial", 18, "bold"),
                                                             command=self._on_select_folder_finished)
        self.choose_f_path_bt.grid(row=0, column=1, sticky="w")

        self.chosen_f_path_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="Folder path read：",
                                                             text_color="red")
        self.chosen_f_path_hint.grid(row=1, column=0, sticky="w")
        self.chosen_f_path_lbl: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="", text_color="red")
        self.chosen_f_path_lbl.grid(row=1, column=1, sticky="w")

        self.pic_count_hint: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="Image read：",
                                                         text_color="red")
        self.pic_count_hint.grid(row=2, column=0, sticky="w")
        self.pic_count_lbl: ctk.CTkLabel = ctk.CTkLabel(self.frame_pic_handle_box, text="", text_color="red")
        self.pic_count_lbl.grid(row=2, column=1, sticky="w")

        # ===================== Zone: Dropdown Menu =====================
        self.frame_options = ctk.CTkFrame(self.root)
        self.frame_options.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.option_menu = ctk.CTkOptionMenu(
            self.frame_options,
            values=config.MODE_OPS,
            width=550,
            font=("Arial", 18, "bold"),
            command=self._on_task_type_op_change
        )
        op_desc = ctk.CTkLabel(self.frame_options, text="Task Type：")
        op_desc.grid(row=0, column=0)
        self.option_menu.grid(row=0, column=1, )

        # =============== Zone: AI Model Select ===============  #
        self.model_op_frame: ctk.CTkFrame = ctk.CTkFrame(self.root)
        self.model_op_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        self.model_op_menu = ctk.CTkOptionMenu(
            master=self.model_op_frame,
            values=config.AI_MODEL_OPS,
            width=550,
            font=("Arial", 18, "bold"),
            command=self._on_ai_op_change
        )
        ai_op_desc = ctk.CTkLabel(self.model_op_frame, text="AI Model：")
        ai_op_desc.grid(row=0, column=0)
        self.model_op_menu.grid(row=0, column=1, )

        # =============== Zone: Proceed Button ===============  #
        self.main_process_bt: ctk.CTkButton = ctk.CTkButton(self.root,
                                                            text="Proceed",
                                                            font=("Arial", 18, "bold"),
                                                            command=self._main_process)
        self.main_process_bt.grid(row=6, column=0, pady=10)

        # =============== Zone: Progress Bar ===============  #
        self.progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(self.root, width=650, height=30)
        self.progress_bar.grid_forget()

    def _on_ai_op_change(self, selected_value: str) -> None:
        """
        Callback triggered when the AI model selection changes.

        Retrieves the corresponding AI model configuration based on the selected option
        and updates the current AI model setting.

        :param selected_value: Selected AI model name string
        :return: None
        """

        self.ai_model = config.AI_MAP.get(selected_value, config.DEFAULT_AI)

    def _on_task_type_op_change(self, selected_value: str) -> None:
        """
        Callback triggered when the task type selection changes.

        Retrieves the corresponding prompt content based on the selected option
        and updates the global prompt configuration.

        :param selected_value: Selected task type string
        :return: None
        """
        self.op_value = config.PROMPT_MAP.get(selected_value, config.TF_L_PROMPT)

    def _update_progress(self, current: int, total: int) -> None:
        """
        Updates the target progress value for the smooth progress animation.

        Calculates the progress ratio from the current and total task values, sets
        the target progress, and starts the animation loop if it's not already running.

        :param current: Current number of completed tasks
        :param total: Total number of tasks to be processed
        :return: None
        """
        self.smooth_progress_target = current / total
        if not self.smooth_progress_running:
            self._smooth_progress_animation()

    def _main_process(self) -> None:
        """
        Main entry point for the core application workflow.

        Starts the background thread to process images, extracts information using AI recognition,
        saves results to JSON files, and exports data to an Excel file.
        Disables the main button and shows the progress bar during execution.

        :return: None
        """

        self.main_process_bt.configure(text="Proceeding...",
                                       state=ctk.DISABLED)
        task_thread = threading.Thread(
            target=self._background_task,
            daemon=True
        )

        task_thread.start()
        self.progress_bar.set(0)
        self.smooth_progress_target = 0
        self.progress_bar.set(0)
        self.progress_bar.grid(row=7, column=0, pady=20)

    def _background_task(self) -> None:
        """
        Executes the core processing logic in a background thread.

        This method performs AI image recognition, exports results to an Excel file,
        and updates the UI with success or error messages. It should ONLY be called
        by the _main_process() method to ensure thread safety.

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

            self.root.after(0, lambda: self.progress_bar.set(1.0), )

            self.root.after(0,
                            lambda: CTkMessagebox(title="Done",
                                                  message="Image recognition completed. Data has been successfully written to the table!",
                                                  width=400,
                                                  height=250,
                                                  icon="check",
                                                  icon_size=(40, 40),
                                                  font=("Arial", 16)))


        except Exception as e:
            err_msg = f"错误：{str(e)}"
            self.root.after(0,
                            lambda: CTkMessagebox(title="Error",
                                                  message=err_msg,
                                                  width=400,
                                                  height=250,
                                                  icon="cancel",
                                                  icon_size=(40, 40),
                                                  font=("Arial", 16)))
        finally:
            self.root.after(0, lambda: self.main_process_bt.configure(text="Proceed", state=ctk.NORMAL))
            self.progress_bar.grid_forget()

    def _smooth_progress_animation(self) -> None:
        """
        Animates the progress bar with a smooth, gradual easing effect towards the target value.

        Uses recursive updates with a small time delay to create smooth growth animation.
        Stops automatically when the progress bar reaches the target value.

        :return: None
        """
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
        Triggered when the folder selection dialog is closed by the user.

        Opens a system dialog to select an image folder, retrieves and validates the path,
        recursively collects all .jpg, .jpeg, .png images, updates the UI with the
        simplified folder path and image count, and refreshes the API key display.

        :return: None
        """
        self.pic_folder_path: str = filedialog.askdirectory(title="Select the folder path for storing images")
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
        Updates the displayed API key when the input content changes.

        Retrieves and trims the input text, validates the content, then refreshes
        the display label with the result in red text.

        :param event: Event object triggered by input modification
        :return: None
        """
        self.api_key_content: str = self.api_input_entry.get().strip()
        self.api_key_content = Validator.validate_api_string(self.api_key_content)
        self.api_show_label.configure(text=f"{self.api_key_content}", text_color="red")

    def _on_closing(self) -> None:
        """
        Callback function when user close this app.
        :return: None
        """
        self.logic_obj.remove_json_folder()
        self.root.destroy()

    def launch(self) -> None:
        """
        Launches the application main window and starts the main event loop.
        Behaves like double-clicking an executable file to run the program.

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
        Validates and cleans a given folder path string.

        Checks if the input path is empty. If empty, returns an empty string and False.
        If not empty, strips whitespace from both ends and returns the cleaned path with True.

        :param org_path: Original folder path string to validate
        :return: Tuple containing (cleaned path, validation success flag).
                 Returns ("", False) if input is empty; returns (stripped path, True) otherwise
        """
        if len(org_path) == 0:
            return "", False
        else:
            org_path = org_path.strip()
            return org_path, True

    @staticmethod
    def simplify_folder_path(org_path: str) -> str:
        """
        Simplifies a folder path by truncating intermediate directories with an ellipsis.

        Splits the input path by forward slashes. If the path contains more than 3 segments,
        replaces all middle segments with "...", preserving only the first, second, and last segments.
        Returns the original path if it has 3 or fewer segments.

        :param org_path: Original file system path separated by forward slashes (/)
        :return: Simplified path with intermediate directories truncated if necessary
        """
        text_elements: list = org_path.split("/")
        if len(text_elements) > 3:
            result: str = "/".join([text_elements[0], text_elements[1], "...", text_elements[-1]])
            return result
        else:
            return org_path

    @staticmethod
    def validate_api_string(org_api_content: str) -> str:
        """
        Validates and checks the format of the input API Key string.

        Trims whitespace and verifies the API Key only contains letters, numbers, and hyphens.
        Also checks for empty input and maximum length limit.

        :param org_api_content: Raw input string for the API Key validation
        :return: Original valid API Key if passed checks; error message string if validation failed
        """
        org_api_content = org_api_content.strip()
        if re.search(r'[^a-zA-Z0-9-]', org_api_content):
            return "The API Key can only contain letters, numbers and hyphens!"
        elif len(org_api_content) >= 40:
            return "The API Key is too long. Please check it!"
        elif len(org_api_content) == 0:
            return "Failed to read the API Key!"
        else:
            return org_api_content
