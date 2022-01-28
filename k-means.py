import numpy as np
import csv

def read_data(state):
    with open(f'data/{state}_input_t.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        header = []
        header = next(csvreader)
        rows = []
        for row in csvreader:
                rows.append(row)

    points = []

    for item in rows:
        points.append([float(x) for x in np.array(item)[1:5]])
    return points



def cardinality(cluster):
    return np.sum(np.array(cluster), axis=0)[1] # sum of population in cluster

def make_county(clusters, j, dic):
    cluster = clusters[j]
    for point in cluster:
        county = float(point[0])
        if county not in dic: dic[county] = []
        if j not in dic[county]: dic[county] += [j] # add district to dic for county in point
    return dic

def find_county(j, county, gamma, input_dic):
    if j in input_dic[county]: return (len(input_dic[county]))**gamma # return number of districts county is in
    else: return (len(input_dic[county]) + 1)**gamma # if the county that the point is in is not in that district -> return num + 1
    
def weighted(current_cluster, alpha, denom):
    num = cardinality(current_cluster)**alpha # size of current district with alpha parameter
    return(num / denom)

def distance(x1, x2):
    x1 = x1[2:] # lat and long of first pt
    x2 = x2[2:] # lat and long of second pt
    return np.linalg.norm(np.array(x1) - np.array(x2)) 

def initial_voronoi(X, anchors, k):
    clusters = {}
    for n in range(k): # for each cluster initialize dic
        clusters[n] = []
    for i in range(len(X)):
        point = X[i] # ith point
        closest_val = np.argmin([distance(point, anchors[j]) for j in range(k)]) # find the centroid w shortest distance to point
        clusters[closest_val] += [point]
    return clusters

def voronoi(X, anchors, weights, k, gamma, input_dic):
    clusters = {}
    for n in range(k): # for each cluster
        clusters[n] = []
    for i in range(len(X)):
        point = X[i]
        c_list = []
        for j in range(k):
            d = distance(point, anchors[j]) 
            w = weights[j] # population weight
            sp = (1 + find_county(j, point[0], gamma, input_dic)) # county splitting weight
            c_list.append(d*w*sp)
        closest_val = np.argmin(c_list) # find minimum combo of these coefficients
        clusters[closest_val] += [point]
    return clusters


def centroid(clusters, k):
    ret = []
    for i in range(k):
        if len(clusters[i]) > 0:
            ret.append(np.mean(clusters[i], axis = 0)) # find the centroid
        else: ret.append(clusters[np.argmax([cardinality(clusters[j]) for j in range(k)])][0]) # if the cluster is empty take a point from the largest cluster as new centroid
    return ret

def kmeans(X, k, alpha = 5, beta = 0.5, gamma = 1, it = 100, t = 0.01):
    bo = True
    index = np.array([g for g in np.arange(0, len(X), int(len(X)/k))]) # find "evenly" spaced indices
    centroids = np.array(X)[index] # assign centroids "randomly"
    clusters = initial_voronoi(X, centroids, k) # initialize clisters
    i = 0
    s = [1/k]*k
    while(bo and i < it):
        new_centroids = centroid(clusters, k)
        if np.mean([distance(new_centroids[m], centroids[m]) for m in range(k)]) < t:
            bo = False # if the distance between previously defined centroids and current centroids is small enough stop
            break
        centroids = new_centroids
        denom = 0
        input_dic = {}
        for n in range(k):
            cluster = clusters[n]
            denom += cardinality(cluster)**alpha # needed for weight calculations
            input_dic = make_county(clusters, n, input_dic) # used for county splitting calculations
        for j in range(k):
            current_cluster = clusters[j]
            wj = weighted(current_cluster, alpha, denom)
            s[j] = s[j]*beta + (1-beta)*wj # weighting coefficient formula from guest paper
        clusters = voronoi(X, centroids, s, k, gamma, input_dic) # re assign clusters 
        i += 1
    return centroids, clusters
    

