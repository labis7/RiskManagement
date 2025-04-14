import pandas as pd
print("=========================================================")

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
    average_pl_pct = (average_pl / average_position if average_position else 0 )*100

    print(f"Average PL: {average_pl:.2f}")
    print(f"Average Position Size: {average_position:.2f}")
    print(f"Average PL in %: {average_pl_pct:.2f}")
    print(f"Average Take Profit %: {average_tp_pct:.2f}")
    print(f"Average Stop Loss %: {average_sl_pct:.2f}")
    print(f"Average Trade Duration (days): {average_days:.2f}") #todo, import better datetime resolution for more accurate representation of my moves

        

    return


def calculateAdvanced():
    for period in range(1, 6):
        filtered_df = df[(df["endDate"] - df["startDate"]).dt.days == period]

        if filtered_df.empty:
            print(f"\n--- {period}-Day Trades: No Data ---")
            continue

        total_pl = filtered_df["PL"].sum()
        total_position = (filtered_df["Quantity"] * filtered_df["buyPrice"]).sum()
        average_position = total_position / len(filtered_df)
        average_pl = total_pl / len(filtered_df)
        average_pl_pct = (average_pl / average_position if average_position else 0) * 100

        tp_df = filtered_df[filtered_df["PL(%)"] > 0]
        sl_df = filtered_df[filtered_df["PL(%)"] < 0]

        average_tp_pct = tp_df["PL(%)"].mean() if not tp_df.empty else 0
        average_sl_pct = sl_df["PL(%)"].abs().mean() if not sl_df.empty else 0

        # Largest and smallest trades
        filtered_df["Position"] = filtered_df["Quantity"] * filtered_df["buyPrice"]
        largest_trade_qty = filtered_df.loc[filtered_df["Quantity"].idxmax()]
        smallest_trade_qty = filtered_df.loc[filtered_df["Quantity"].idxmin()]
        largest_trade_val = filtered_df.loc[filtered_df["Position"].idxmax()]
        smallest_trade_val = filtered_df.loc[filtered_df["Position"].idxmin()]

        # Distances from High and Low
        sell_distances = ((filtered_df["Price High"] - filtered_df["sellPrice"]) / filtered_df["Price High"]) * 100
        buy_distances = ((filtered_df["buyPrice"] - filtered_df["Price Low"]) / filtered_df["Price Low"]) * 100

        avg_sell_distance = sell_distances.mean()
        avg_buy_distance = buy_distances.mean()

        print(f"\n--- {period}-Day Trades ---")
        print(f"Trades Count: {len(filtered_df)}")
        print(f"Average PL: {average_pl:.2f}")
        print(f"Average Position Size: {average_position:.2f}")
        print(f"Average PL in %: {average_pl_pct:.2f}")
        print(f"Average Take Profit %: {average_tp_pct:.2f}")
        print(f"Average Stop Loss %: {average_sl_pct:.2f}")
        print(f"Avg Sell Distance from High: {avg_sell_distance:.2f}%")
        print(f"Avg Buy Distance from Low: {avg_buy_distance:.2f}%")

        print(f"Largest Trade (Qty): {largest_trade_qty['Quantity']} on {largest_trade_qty['startDate'].date()}")
        print(f"Smallest Trade (Qty): {smallest_trade_qty['Quantity']} on {smallest_trade_qty['startDate'].date()}")
        print(f"Largest Trade ($): {largest_trade_val['Position']:.2f} on {largest_trade_val['startDate'].date()}")
        print(f"Smallest Trade ($): {smallest_trade_val['Position']:.2f} on {smallest_trade_val['startDate'].date()}")

    # Additional segment: trades longer than 5 days
    filtered_df = df[(df["endDate"] - df["startDate"]).dt.days > 5]
    if not filtered_df.empty:
        period = "6+"
        total_pl = filtered_df["PL"].sum()
        total_position = (filtered_df["Quantity"] * filtered_df["buyPrice"]).sum()
        average_position = total_position / len(filtered_df)
        average_pl = total_pl / len(filtered_df)
        average_pl_pct = (average_pl / average_position if average_position else 0) * 100

        tp_df = filtered_df[filtered_df["PL(%)"] > 0]
        sl_df = filtered_df[filtered_df["PL(%)"] < 0]
        average_tp_pct = tp_df["PL(%)"].mean() if not tp_df.empty else 0
        average_sl_pct = sl_df["PL(%)"].abs().mean() if not sl_df.empty else 0

        filtered_df["Position"] = filtered_df["Quantity"] * filtered_df["buyPrice"]
        largest_trade_val = filtered_df.loc[filtered_df["Position"].idxmax()]
        smallest_trade_val = filtered_df.loc[filtered_df["Position"].idxmin()]
        avg_sell_distance = ((filtered_df["Price High"] - filtered_df["sellPrice"]) / filtered_df["Price High"]).mean() * 100
        avg_buy_distance = ((filtered_df["buyPrice"] - filtered_df["Price Low"]) / filtered_df["Price Low"]).mean() * 100

        print(f"\n--- {period}-Day Trades ---")
        print(f"Trades Count: {len(filtered_df)}")
        print(f"Average PL: {average_pl:.2f}")
        print(f"Average Position Size: {average_position:.2f}")
        print(f"Average PL in %: {average_pl_pct:.2f}")
        print(f"Average Take Profit %: {average_tp_pct:.2f}")
        print(f"Average Stop Loss %: {average_sl_pct:.2f}")
        print(f"Avg Sell Distance from High: {avg_sell_distance:.2f}%")
        print(f"Avg Buy Distance from Low: {avg_buy_distance:.2f}%")
        print(f"Largest Trade ($): {largest_trade_val['Position']:.2f} on {largest_trade_val['startDate'].date()}")
        print(f"Smallest Trade ($): {smallest_trade_val['Position']:.2f} on {smallest_trade_val['startDate'].date()}")

    return


def applyStrategy():
    tp_pct_target = 3.0
    sl_pct_target = 1.0

    results = []

    for period in ["All"] + list(range(1, 6)) + ["6+"]:
        if period == "All":
            data = df
        elif period == "6+":
            data = df[(df["endDate"] - df["startDate"]).dt.days > 5]
        else:
            data = df[(df["endDate"] - df["startDate"]).dt.days == period]

        if data.empty:
            print(f"\n--- {period}-Day Strategy Simulation: No Data ---")
            continue

        data = data.copy()
        data["Position"] = data["Quantity"] * data["buyPrice"]

        # TP strategy: if Price High hit target
        tp_condition = (data["Price High"] >= (1 + tp_pct_target / 100) * data["buyPrice"])
        tp_success = data[tp_condition]
        tp_count = len(tp_success)

        # SL strategy: if Price Low hit threshold
        sl_condition = (data["Price Low"] <= (1 - sl_pct_target / 100) * data["buyPrice"])
        sl_success = data[sl_condition]
        sl_count = len(sl_success)

        # Simulated TP scenario
        data_tp = data.copy()
        data_tp["sim_sellPrice"] = data_tp["sellPrice"]
        data_tp.loc[tp_condition, "sim_sellPrice"] = data_tp.loc[tp_condition, "buyPrice"] * (1 + tp_pct_target / 100)
        data_tp["sim_PL"] = (data_tp["sim_sellPrice"] - data_tp["buyPrice"]) * data_tp["Quantity"]
        avg_segment_tp_pl = data_tp["sim_PL"].mean()

        # Simulated SL scenario
        data_sl = data.copy()
        data_sl["sim_sellPrice"] = data_sl["sellPrice"]
        data_sl.loc[sl_condition, "sim_sellPrice"] = data_sl.loc[sl_condition, "buyPrice"] * (1 - sl_pct_target / 100)
        data_sl["sim_PL"] = (data_sl["sim_sellPrice"] - data_sl["buyPrice"]) * data_sl["Quantity"]
        avg_segment_sl_pl = data_sl["sim_PL"].mean()

        print(f"\n--- {period}-Day Strategy Simulation ---")
        print(f"Trades Count: {len(data)}")
        print(f"TP {tp_pct_target}% Hit: {tp_count} times")
        print(f"Simulated Avg PL with TP strategy: {avg_segment_tp_pl:.2f}")
        print(f"SL {sl_pct_target}% Hit: {sl_count} times")
        print(f"Simulated Avg PL with SL strategy: {avg_segment_sl_pl:.2f}")
        print(f"Original Avg PL in this segment: {data['PL'].mean():.2f}")

        results.append({
            "period": period,
            "original": data["PL"].mean(),
            "TP": avg_segment_tp_pl,
            "SL": avg_segment_sl_pl
        })

    analyzeResults(results)
    return


def analyzeResults(results):
    print("\n=== Strategy Comparison Summary ===")
    best_segment = max(results, key=lambda x: x["original"])
    worst_segment = min(results, key=lambda x: x["original"])
    best_tp = max(results, key=lambda x: x["TP"])
    best_sl = max(results, key=lambda x: x["SL"])

    print(f"Best Original Segment: {best_segment['period']} with Avg PL {best_segment['original']:.2f}")
    print(f"Worst Original Segment: {worst_segment['period']} with Avg PL {worst_segment['original']:.2f}")
    print(f"Best Segment with TP Strategy: {best_tp['period']} with Simulated Avg PL {best_tp['TP']:.2f}")
    print(f"Best Segment with SL Strategy: {best_sl['period']} with Simulated Avg PL {best_sl['SL']:.2f}")

calculateBasics()
#calculateAdvanced()
applyStrategy()