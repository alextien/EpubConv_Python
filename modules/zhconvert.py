# 繁化姬模組
import json

import requests
from modules.utils.error import (RequestError, ZhconvertKeyNotFound,
                                 ZhConvertMissNecessarykey)


class ZhConvert:
    """ 繁化姬模組 """

    def __init__(self):
        """  """
        self.api = f'https://api.zhconvert.org'

    def __request(self, endpoint: str, playload):
        with requests.get(f'{self.api}{endpoint}', data=playload) as req:
            if req.status_code != 200:
                raise RequestError(f'zhconvert Request error. status code: {req.status_code}')
            req.encoding = 'utf-8'
            return json.loads(req.text)

    def __check(self):
        allow_converter = ["Simplified",
                           "Traditional",
                           "China",
                           "Taiwan",
                           "WikiSimplified",
                           "WikiTraditional"]

    def convert(self, **args):
        """繁化姬轉換

        API doc : https://docs.zhconvert.org/api/convert/

        Arguments:
            text : 欲轉換的文字
            converter : 所要使用的轉換器。有 Simplified （簡體化）、 Traditional （繁體化）、 
                        China （中國化）、  Taiwan （台灣化）、WikiSimplified （維基簡體化）、 
                        WikiTraditional （維基繁體化）。
            ignoreTextStyles : 由那些不希望被繁化姬處理的 "樣式" 以逗號分隔所組成的字串。
                               通常用於保護特效字幕不被轉換，
                               例如字幕組的特效字幕若是以 OPJP 與 OPCN 作為樣式名。
                               可以設定 "OPJP,OPCN" 來作保護。
            jpTextStyles : 告訴繁化姬哪些樣式要當作日文處理（預設為伺服器端自動猜測）。
                           若要自行設定，則必須另外再加入 *noAutoJpTextStyles 這個樣式。
                           所有樣式以逗號分隔組成字串，
                           例如： "OPJP,EDJP,*noAutoJpTextStyles" 表示不讓伺服器自動猜測，
                           並指定 OPJP 與 EDJP 為日文樣式。
            jpStyleConversionStrategy : 對於日文樣式該如何處理。 
                                        "none" 表示 無（當成中文處理） 、 "protect" 表示 保護 、 
                                        "protectOnlySameOrigin" 表示 僅保護原文與日文相同的字 、 
                                        "fix" 表示 修正 。	
            jpTextConversionStrategy : 對於繁化姬自己發現的日文區域該如何處理。 
                                       "none" 表示 無（當成中文處理） 、 "protect" 表示 保護 、 
                                       "protectOnlySameOrigin" 表示 僅保護原文與日文相同的字 、 
                                       "fix" 表示 修正 。	
            modules : 強制設定模組啟用／停用 。 -1 / 0 / 1 分別表示 自動 / 停用 / 啟用 。
                      字串使用 JSON 格式編碼。使用 * 可以先設定所有模組的狀態。
                      例如：{"*":0,"Naruto":1,"Typo":1} 表示停用所有模組，
                      但啟用 火影忍者 與 錯別字修正 模組。	
            userPostReplace : 轉換後再進行的額外取代。
                              格式為 "搜尋1=取代1\\n搜尋2=取代2\\n..." 。 
                              搜尋1 會在轉換後再被取代為 取代1 。	
            userPreReplace : 轉換前先進行的額外取代。
                             格式為 "搜尋1=取代1\\n搜尋2=取代2\\n..." 。 
                             搜尋1 會在轉換前先被取代為 取代1 。	
            userProtectReplace : 保護字詞不被繁化姬修改。
                                 格式為 "保護1\\n保護2\\n..." 。 
                                 保護1 、 保護2 等字詞將不會被繁化姬修改。
        """
        allow_keys = [
            'text',
            'converter',
            'ignoreTextStyles',
            'jpTextStyles',
            'jpStyleConversionStrategy',
            'jpTextConversionStrategy',
            'modules',
            'userPostReplace',
            'userPreReplace',
            'userProtectReplace',
        ]
        error_key = [key for key in args.keys() if key not in allow_keys]
        if error_key:
            raise ZhconvertKeyNotFound(', '.join(error_key))
        if args.get('text', None) is None or args.get('converter', None) is None:
            raise ZhConvertMissNecessarykey()
        self.convert_obj = self.__request('/convert', args)
        return self.convert_obj

    @property
    def text(self):
        if self.convert_obj['code'] != 0:
            return None
        return self.convert_obj['data']['text']
