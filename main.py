#!/usr/bin/env python


from modules.mci import MciScrap


def main() -> None:
    budget = 10000

    MciInfo, df  = MciScrap()

    df['price/meg'] = df['package_price']/df['package_volume_info']
    df.sort_values('price/meg', ascending=True, inplace=True)

    for index, row in df.iterrows():
        count = 0
        if budget <=0 :
            break
        while row['package_price'] <= budget :
            budget -= row['package_price']
            count+=1
        if count :
            print(f"you should buy {count} of package {row['id']}")
            print( MciInfo.loc[ row['id'] ] )

if __name__ == '__main__':
    main()