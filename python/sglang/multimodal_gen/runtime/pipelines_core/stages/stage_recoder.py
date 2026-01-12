import functools
import json

import torch


def serialize_value(v):
    """安全地序列化值"""
    try:
        if isinstance(v, torch.Tensor):
            return v.detach().cpu().numpy().tolist()
        elif isinstance(v, list):
            if len(v) == 0:
                return []
            elif isinstance(v[0], torch.Tensor):
                return [t.detach().cpu().numpy().tolist() for t in v]
            else:
                return [str(item) for item in v]
        else:
            return str(v)
    except Exception as e:
        return f"<serialize error: {e}>"


def log_io(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数名和类名
        func_name = func.__name__
        class_name = type(args[0]).__name__ if args else "Unknown"

        print(f"--- Calling: {class_name}.{func_name} ---")

        try:
            data = {}

            # 保存调用前的状态
            if len(args) > 1 and hasattr(args[1], '__dict__'):
                data["before"] = {}
                for k, v in args[1].__dict__.items():
                    data["before"][k] = serialize_value(v)

            # 执行原函数
            result = func(*args, **kwargs)

            # 保存调用后的状态 (注意这里是 "after" 不是 "before")
            if hasattr(result, '__dict__'):
                data["after"] = {}  # 修复：创建 "after" 字典
                for k, v in result.__dict__.items():
                    data["after"][k] = serialize_value(v)  # 修复：写入 "after"

            # 使用类名和函数名作为文件名
            file_name = f"{class_name}_{func_name}"
            with open(f"{file_name}.json", "w") as f:
                f.write(json.dumps(data, indent = 2, default = str))

            return result

        except Exception as e:
            print(f"Exception in {class_name}.{func_name}: {e}")
            raise e

    return wrapper
