
import b_logger
"""
固定消息返回，固定内容不允许进行修改。
"""
def success(msg="", data=[], params={}, print_logger=False):
    if print_logger:
        b_logger.success(msg)
    return {
        "success": True,
        "msg": msg,
        "data": data,
        "request_params": params
    }

def error(msg="", data=[], params={}, print_logger=False):
    if print_logger:
        b_logger.error(msg)
    return {
        "success": False,
        "msg": msg,
        "data": data,
        "request_params": params
    }