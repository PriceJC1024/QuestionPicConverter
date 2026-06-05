from pathlib import Path
from itertools import chain


def jsonized(json_like_content: str) -> str:
    """
    Attempts to extract the outermost {} or [] structure from a JSON-like text.
    Returns a safe default value if extraction fails.

    :param json_like_content: The text containing potential JSON fragments
    :return: The extracted JSON string
    """
    default: str = "{}"

    if not isinstance(json_like_content, str):
        return default

    # 尝试提取对象 { }
    start_obj = json_like_content.find('{')
    end_obj = json_like_content.rfind('}')

    # 尝试提取数组 [ ]
    start_arr = json_like_content.find('[')
    end_arr = json_like_content.rfind(']')

    # 优先提取完整的 JSON 结构（对象或数组）
    candidates = []
    if start_obj != -1 and end_obj > start_obj:
        candidates.append((start_obj, end_obj))
    if start_arr != -1 and end_arr > start_arr:
        candidates.append((start_arr, end_arr))

    if candidates:
        # 取最长的有效片段
        start, end = max(candidates, key=lambda x: x[1] - x[0])
        return json_like_content[start:end + 1]

    return default


def get_images_in_folder(folder_path: str) -> list[Path]:
    """
    recursively getting images (.jpg, .jpeg, .png) in a given folder path.

    return a list that contains all images file paths (Path form).

    :param folder_path: str
    :return: list[Path]
    """

    folder_path: Path = Path(folder_path)
    if folder_path.exists():
        pics = list(chain(folder_path.rglob("*.jpg"),
                          folder_path.rglob("*.jpeg"),
                          folder_path.rglob("*.png")))
        return pics

    else:
        return []
