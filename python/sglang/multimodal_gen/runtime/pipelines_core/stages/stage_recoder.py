import functools
import json

def log_io(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. 打印输入参数
        # args 是位置参数元组，kwargs 是关键字参数字典
        print(f"--- Calling: {func.__name__} ---")
        print(f"Input Args: {args}")
        print(f"Input Kwargs: {kwargs}")

        try:
            # 执行原函数
            file_name = args[0].__name__
            data = {}
            data |= {"before": args[1]}
            result = func(*args, **kwargs)
            data |= {"after": result.__dict__}
            with open(f"{file_name}.json", "w") as f:
                f.write(json.dumps(data))
            return result

        except Exception as e:
            print(f"Exception in {func.__name__}: {e}")
            raise e

    return wrapper
