import pandas as pd
##df = pd.DataFrame(columns=list('A'))
df = pd.read_pickle('All_user.pkl')
##df.append({'A':'Divanshu'},ignore_index=True)
##df.append({'A':'abvc'},ignore_index=True)
##df.append({'A':'xyz'},ignore_index=True)
##
##df.to_pickle('Username.pkl')
print(df)
##df = pd.read_pickle('All_user.pkl')

