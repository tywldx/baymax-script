import sys, os
import traceback
import b_logger
# def handel():
#     exc_type, exc_obj, exc_tb = sys.exc_info()
#     print(exc_type, exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)

def log_traceback(ex):
    tb_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
    tb_text = ''.join(tb_lines)
    b_logger.error(tb_text)
    return tb_text