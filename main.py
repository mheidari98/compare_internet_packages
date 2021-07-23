#!/usr/bin/env python

import argparse
import numpy as np
import pandas as pd
from modules.mci import MciScrap
from modules.irancell import irancell
from modules.rightel import rightel

def main() -> None:
    parser = argparse.ArgumentParser(description="compare internet packages")
    parser.add_argument('-b', '--budget', help="<Required> max budget", required=True)
    parser.add_argument('-p','--provider', nargs='+', help='<Required> Set provider', required=True)
    args = parser.parse_args()

    budget = int(args.budget)
    provider = args.provider
    print(provider)

    col = ['provider', 'id', 'volume', 'price']
    df = pd.DataFrame(columns = col)

    if 'mci' in provider :
        MciInfo, df1  = MciScrap()
        df1['provider'] = 'mci'
        df = pd.concat([df, df1.rename(columns={'package_volume_info':'volume', 'package_price':'price'})], 
                                        ignore_index=True)

    if 'mtn' in provider :
        df2  = irancell()
        df2['provider'] = 'mtn'
        df2['id'] = df2.index
        df2['volume'] =  df2['volume'].astype(np.float64)
        df = pd.concat([df, df2[col]], ignore_index=True)

    if 'rightel' in provider :
        df3  = rightel()
        df3['provider'] = 'rightel'
        df = pd.concat([df, df3], ignore_index=True)


    df['price/meg'] = df['price']/df['volume']
    df.sort_values('price/meg', ascending=True, inplace=True)

    for index, row in df.iterrows():
        count = 0
        if budget <=0 :
            break
        while row['price'] <= budget :
            budget -= row['price']
            count+=1
        if count :
            print(f"you should buy {count} of package {row['id']} from {row['provider']}")
            if row['provider'] == 'mci' :
                print( MciInfo.loc[ row['id'] ] )
            elif row['provider'] == 'mtn' :
                print( df2.loc[ row['id'] ] )

if __name__ == '__main__':
    main()