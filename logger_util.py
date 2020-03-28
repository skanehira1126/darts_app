#!/user/bin/env python3
from logging import getLogger, FileHandler, Formatter
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

def init_logger(logger_name="logger", log_file_name="temp.log"):
    logger = getLogger(logger_name)
    
    #ロガーのレベル
    logger.setLevel(DEBUG)
    #ログファイル名
    file_handler = FileHandler(log_file_name, "a")
    #ファイルハンドラーの出力ログレベル
    file_handler.setLevel(DEBUG)
    #ログのフォーマット
    logger_format = Formatter("%(asctime)s [%(levelname)-8s] [%(process)d] %(module)-18s %(funcName)-10s %(lineno)4s: %(message)s")
    file_handler.setFormatter(logger_format)
    #ハンドラーの追加
    logger.addHander(file_handler)
    
    
    
    