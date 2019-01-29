import os
import pandas as pd

def load_df_from_directory(path: str) -> pd.DataFrame:
    df_list = []
    for file in os.listdir(path):
        df_list.append(pd.read_json(os.path.join(path, file), lines=True))
    return pd.concat(df_list)


def main():
    print("Hello World!")
    df_mlb = load_df_from_directory('raw_data/mlb/2019_01_27')
    df_aaa = load_df_from_directory('raw_data/aaa/2019_01_27')
    df_aa = load_df_from_directory('raw_data/aa/2019_01_27')
    df_a_adv = load_df_from_directory('raw_data/a_adv/2019_01_27')
    df_a = load_df_from_directory('raw_data/a/2019_01_27')

    print(4860  - len(df_mlb.index))
    print(4230  - len(df_aaa.index))
    print(4230  - len(df_aa.index))
    print(4230  - len(df_a_adv.index))
    print(4230  - len(df_a.index))


  
if __name__== "__main__":
  main()


    