import numpy as np 
import pandas as pd
import json

# read data
#od = pd.read_csv('../data/od.csv')
pop = pd.read_csv('../data/haikou.csv')
poi = pd.read_csv('../data/hkparking.csv')

lats = pop.y.unique()
lons = pop.x.unique()
gap = 0.0008333

pop['grid_x'] = ((pop.x - pop.x.min())/ gap).astype(int)
pop['grid_y'] = ((pop.y - pop.y.min())/ gap).astype(int)
pop['uid'] = ((pop.x - pop.x.min())/ gap).astype(int) * len(lats) + ((pop.y - pop.y.min())/ gap).astype(int)
pop['pop_percent'] = pop.haikou / pop.haikou.sum()


# od_count = np.load('od_count.npy')
# trajectory = pd.DataFrame(od_count).stack().reset_index()
# trajectory.columns = ['grid_x','grid_y','count']
# trajectory['uid'] = trajectory['grid_x']*len(lats) +trajectory['grid_y']

poi['grid_x']= ((poi.long - pop.x.min())/ gap).astype(int)
poi['grid_y']= ((poi.lat - pop.y.min())/ gap).astype(int)
poi['uid'] = ((poi.long - pop.x.min())/ gap).astype(int) * len(lats) + ((poi.lat - pop.y.min())/ gap).astype(int)
poi_dedu = poi.drop_duplicates(subset=['uid'])


def get_dist(gid,gid1,m =len(lats)):
    tmp_x,tmp_x1 = int(gid / m),int(gid1 / m)
    tmp_y,tmp_y1 = gid - tmp_x * m, gid1 - tmp_x1 * m
    #print(tmp_x,tmp_y,tmp_x1,tmp_y1)
    return np.sqrt((int(tmp_x-tmp_x1))**2 +(int(tmp_y-tmp_y1))**2) 

def cal_sat_delta_nearest(df,gid,selected_ids,theta=1,lda=1,delta=10):
    tmp_dist = sorted([get_dist(gid,j) for j in selected_ids])
    sat = 0
    for _ in range(len(selected_ids)):
        if tmp_dist[_]<=delta:
            sat +=  np.exp(-tmp_dist[_] / lda) * df.pop_percent[df.uid==gid].values[0] * (theta**(_))
    return sat

def cal_gain_delta_nearest(df,gid,selected_ids,theta=1,lda=1,delta=10):
    '''
    :param df: dataframe containing population and trajectory info
    :param gid: grid id
    :param selected_ids: selected ids
    :param theta: turning parameter
    :return:
    '''
    inc_gain = 0
    n = len(df)
    tmp_x = int(gid / len(lats))
    tmp_y = gid - tmp_x * len(lats)
    if len(selected_ids) == 0:
        for i in range(n):
            # if gid within range delta, calculate gain
            tmp_dist = np.sqrt((int(df.grid_x[i]-tmp_x))**2 +(int(df.grid_y[i]-tmp_y))**2)    
            if tmp_dist <= delta:
                inc_gain += np.exp(-tmp_dist / lda) * df.pop_percent[i]
            # otherwise gain unchanged
            else:
                inc_gain += 0
    else:
        for i in range(n):
            tmp_dist = np.sqrt((int(df.grid_x[i]-tmp_x))**2 +(int(df.grid_y[i]-tmp_y))**2)             
            # if gid with range delta :
            if tmp_dist <= delta:
                # find the location of gid 
                inc_gain += cal_sat_delta_nearest(df,df.uid[i],selected_ids+[gid],theta,lda,delta)- \
                cal_sat_delta_nearest(df,df.uid[i],selected_ids,theta,lda,delta)
            # otherwise inc = 0:
            else:
                inc_gain += 0
    return inc_gain

def greedy_selection(k,df,poi,theta=1,lda=1,delta = 10):
    '''
    :param k: number of sensors available
    :param df: data frame containing population, poi, and trajectory info
    :param theta: tuning parameter
    :param lda: tuning parameter
    :param delta: tuning parameter
    :return:
    selected ids
    '''
    selected_ids = []
    n = len(poi)
    candidates = poi.uid
    for i in range(k):
        tmp_gain = 0
        tmp_id = 0
        print(i)
        for gid in candidates:
            if gid not in selected_ids:
                inc_gain = cal_gain_delta_nearest(df,gid,selected_ids,theta,lda,delta)
                if inc_gain >tmp_gain:
                    tmp_gain = inc_gain
                    tmp_id = gid
        selected_ids.append(tmp_id)
    return selected_ids


per_threshold = 1e-5 
theta = 0.5
lda = 1
k = 40
delta = 10
pop_small = pop[pop.pop_percent  > per_threshold].reset_index(drop=True)
results = {}
selected_ids = greedy_selection(k,pop_small,poi,theta,lda,delta)
print(selected_ids)
    
results['per_threshold'] = per_threshold
results['selected_ids'] = selected_ids
results['theta'] = theta
results['delta'] = delta
results['lda'] = lda
results['k'] = k

