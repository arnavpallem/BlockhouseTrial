import pandas as pd
import numpy as np


def load_data(path):
    df = pd.read_csv(path)

    df = df.sort_values(['ts_event', 'publisher_id'])
    df = df.drop_duplicates(['ts_event', 'publisher_id'], keep = 'first')
    print(df.head())
    return

#Need to implement class for venues with given methods
def allocate(order_size, venues, lam_over, lam_under, theta_queue):
    step = 100
    splits = []
    for v in range(len(venues)):
        new_splits = []
        for alloc in splits:
            used = sum(alloc)
            max_v = min(order_size - used, venues[v].ask_size)
            for q in range(0, max_v+1, step):
                new_splits.append(alloc + [q])
        splits = new_splits
    best_cost = float('inf')
    best_split = []
    for alloc in splits:
        if sum(alloc) != order_size:
            continue
        cost = compute_cost(alloc, venues, order_size, lam_over, lam_under, theta_queue)
        if cost < best_cost:
            best_cost = cost
            best_split = alloc
    return best_split, best_cost

def compute_cost(split, venues, order_size, lam_over, lam_under, theta):
    executed = 0
    cash_spent = 0
    for i in range(len(venues)):
        exe = min(split[i], venues[i].ask_size)
        executed += exe
        cash_spent += exe * (venues[i].ask + venues[i].fee)
        maker_rebate = max(split[i]-exe, 0) * venues[i].rebate
        cash_spent -= maker_rebate
    underfill = max(order_size - executed, 0)
    overfill = max(executed-order_size, 0)
    risk_pen = theta * (underfill + overfill)
    cost_pen = lam_under * underfill + (lam_over * overfill)
    return cash_spent + risk_pen + cost_pen


if __name__ == "__main__":
   load_data("l1_day.csv")
    