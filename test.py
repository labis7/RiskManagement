import pandas as pd
print("Hello!")

df = pd.read_csv("Trades_clean.csv" , sep=";") #, decimal=","
#print(df.head())

# Clean and convert columns
df["PL"] = df["PL"].astype(str).str.replace(",", ".").astype(float)
# Remove " US$" and convert 'Price Low' and 'Price High' to float
df["Price Low"] = df["Price Low"].astype(str).str.replace(r"\s*US\$", "", regex=True).str.replace(",", ".").astype(float)
df["Price High"] = df["Price High"].astype(str).str.replace(r"\s*US\$", "", regex=True).str.replace(",", ".").astype(float)

# Convert buyPrice, sellPrice, Quantity, PL(%)
df["buyPrice"] = df["buyPrice"].astype(str).str.replace(",", ".").astype(float)
df["sellPrice"] = df["sellPrice"].astype(str).str.replace(",", ".").astype(float)
df["Quantity"] = df["Quantity"].astype(str).str.replace(",", ".").astype(float)
df["PL(%)"] = df["PL(%)"].astype(str).str.replace(",", ".").astype(float)

# Convert startDate and endDate to datetime
df["startDate"] = pd.to_datetime(df["startDate"])
df["endDate"] = pd.to_datetime(df["endDate"])

# for reference
'''
for index, row in df.iterrows():
    #print(f"Row {index}:")
    for column in df.columns:
        print(f"  {column}: {row[column]}")
    print("column field selection, PL: ", row["PL"])
    break
'''



def calculateBasics():

    total_pl = 0
    total_position = 0
    total_tp_pct = 0
    total_sl_pct = 0
    total_days = 0
    count = 0
    tp_count = 0
    sl_count = 0

    for index, row in df.iterrows():
        total_pl += row["PL"]
        position = row["Quantity"] * row["buyPrice"]
        total_position += position
        duration = (row["endDate"] - row["startDate"]).days
        total_days += duration

        pl_pct = row["PL(%)"]
        if pl_pct > 0:
            total_tp_pct += pl_pct
            tp_count += 1
        elif pl_pct < 0:
            total_sl_pct += abs(pl_pct)
            sl_count += 1

        count += 1

    average_pl = total_pl / count if count else 0
    average_position = total_position / count if count else 0
    average_tp_pct = total_tp_pct / tp_count if tp_count else 0
    average_sl_pct = total_sl_pct / sl_count if sl_count else 0
    average_days = total_days / count if count else 0

    print(f"Average PL: {average_pl:.2f}")
    print(f"Average Position Size: {average_position:.2f}")
    print(f"Average Take Profit %: {average_tp_pct:.2f}")
    print(f"Average Stop Loss %: {average_sl_pct:.2f}")
    print(f"Average Trade Duration (days): {average_days:.2f}") #todo, import better datetime resolution for more accurate representation of my moves

        

    return


calculateBasics()