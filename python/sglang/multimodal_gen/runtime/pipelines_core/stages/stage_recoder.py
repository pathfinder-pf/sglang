import functools
import json

import torch


def log_io(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数名和类名
        func_name = func.__name__
        # args[0] 是 self，获取类名用 type(args[0]).__name__
        class_name = type(args[0]).__name__ if args else "Unknown"

        print(f"--- Calling: {class_name}.{func_name} ---")
        print(f"Input Args: {args}")
        print(f"Input Kwargs: {kwargs}")

        try:
            # 保存调用前的状态
            data = {}
            if len(args) > 1 and hasattr(args[1], '__dict__'):
                data["before"] = {k: v.detach().cpu().numpy().tolist() if type(v) is torch.Tensor else str(v) for k, v in args[1].__dict__.items()}

            # 执行原函数
            result = func(*args, **kwargs)

            # 保存调用后的状态
            if hasattr(result, '__dict__'):
                data["after"] = {k: v.detach().cpu().numpy().tolist() if type(v) is torch.Tensor else str(v) for k, v in result.__dict__.items()}

            # 使用类名和函数名作为文件名
            file_name = f"{class_name}_{func_name}"
            with open(f"{file_name}.json", "w") as f:
                f.write(json.dumps(data, indent = 2, default = str))

            return result

        except Exception as e:
            print(f"Exception in {class_name}.{func_name}: {e}")
            raise e

    return wrapper
