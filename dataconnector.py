import pandas as pd
import swissparlpy as spp


def get_votes():
    data = spp.get_data('Vote', Language="DE")
    df = pd.DataFrame(data)
    return df

def get_relatedBusiness(numbers):
    df_combined = pd.DataFrame()
    for number in numbers:
        data = spp.get_data('Business', ID=number, Language='DE')
        df = pd.DataFrame(data)
        df_combined = pd.concat([df_combined, df],ignore_index=True)
        print(number)
    return df_combined