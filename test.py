from os import close
import akshare as ak
import pandas as pd
import datetime as dt
import time

if __name__ == "__main__":

    # e_date = dt.date.today().isoformat()
    e_date = dt.date(2021, 5, 14).isoformat()

    stock_dict = {"GLDQ": "sz000651",
                  "ZXTG": "sz000708"
                  }

    fund_dict = {"HSHL": "513330",
                 "PH-JZ": "009086",
                 "YFD-ZZHW": "006327",
                 "JY-DQZF": "519732",
                 "XQ-XSY": "001511",
                 "ZO-YL": "003095",
                 "XQ-HX": "163418",
                 "HA-NSDK": "040046",
                 "JS-XXCZ": "260108",
                 "XQ-HR": "163406",
                 "YFD-ZXP": "110011",
                 "PH-HB": "000409",
                 "PH-FL": "003547",
                 "PH-FR": "000345",
                 "PH-GM": "160644",
                 "PH-KJ": "008811"
                 }

    arr_fund_name = []
    arr_fund_value = []

    for fund_name, fund_code in fund_dict.items():
        df_fund = ak.fund_em_open_fund_info(
            fund=fund_code, indicator="单位净值走势")
        df_fund = df_fund.set_index("净值日期")
        arr_fund_name.append(fund_name)
        arr_fund_value.append(df_fund["单位净值"][-1])
        print(fund_name)
        time.sleep(1)

    for stock_name, stock_code in stock_dict.items():
        df_stock = ak.stock_zh_a_daily(
            symbol=stock_code, start_date=e_date, end_date=e_date, adjust="qfq")
        arr_fund_name.append(stock_name)
        arr_fund_value.append(df_stock.loc[e_date, 'close'])
        print(stock_name)
        time.sleep(1)

    df = pd.DataFrame({'date_time': e_date,
                       'item': 'price',
                       'fund_name': arr_fund_name,
                       'fund_value': arr_fund_value,
                       'Currency': 'CNY'})

    print(df)
