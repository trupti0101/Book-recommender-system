#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

# Load the dataset
ratings = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\ratings.csv",engine="python")


books = pd.read_csv("C:\\Users\\trupti\\Desktop\\BookRack\\home\\book_data2.csv",engine="python")

# display(ratings.head())
# display(books.head())


# In[4]:


# Merge the two tables then pivot so we have Users X Books dataframe. 
ratings_title = pd.merge(ratings, books[['book_id', 'book_title']], on='book_id' )
user_book_ratings = pd.pivot_table(ratings_title, index='user_id', columns= 'book_title', values='rating')

print('dataset dimensions: ', user_book_ratings.shape, '\n\nSubset example:')
#user_book_ratings.iloc[:25, :10]


# In[5]:


# Drop users that have given fewer than 100 ratings of these most-rated books
user_book_ratings = user_book_ratings.dropna(thresh=100)

# print('dataset dimensions: ', user_book_ratings.shape, '\n\nSubset example:')
# user_book_ratings.iloc[:25, :10]


# In[6]:


from sklearn.decomposition import TruncatedSVD

# replace NaN's with zeroes for Truncated SVD
user_book_ratings_without_nan = user_book_ratings.fillna(0)

tsvd = TruncatedSVD(n_components=200, random_state=42)
user_book_ratings_tsvd = tsvd.fit(user_book_ratings_without_nan).transform(user_book_ratings_without_nan)

# print('Original number of features:', user_book_ratings_without_nan.shape[1])
# print('Reduced number of features:', user_book_ratings_tsvd.shape[1])
# print('Explained variance ratio:', tsvd.explained_variance_ratio_[0:200].sum())


# In[7]:


# view result in a Pandas dataframe, applying the original indices
indices = user_book_ratings.index

book_ratings_for_clustering = pd.DataFrame(data=user_book_ratings_tsvd).set_index(indices)
print('dataset dimensions: ', book_ratings_for_clustering.shape, '\n\nSubset example:')

book_ratings_for_clustering.iloc[:25, :10]


# In[58]:


from sklearn.model_selection import train_test_split
book_ratings_training, book_ratings_testing = train_test_split(book_ratings_for_clustering, test_size=0.20, random_state=42)

# print('Training data shape: ', book_ratings_training.shape)
# print('Testing data shape: ', book_ratings_testing.shape)
# book_ratings_testing.head()


# In[11]:


# find the per-book ratings of the test set
indices = book_ratings_testing.index
test_set_ratings = user_book_ratings.ix[indices]
test_set_ratings.head()


# In[12]:


mean_ratings_for_random_10 = []

# for each user, pick 10 books at random that the reader has rated and get the reader's average score for those books
for index, row in test_set_ratings.iterrows():
    ratings_without_nas = row.dropna()
    random_10 = ratings_without_nas.sample(n=10)
    random_10_mean = random_10.mean()
    mean_ratings_for_random_10.append(random_10_mean)

# get the mean of the users' mean ratings for 10 random books each    
mean_benchmark_rating = sum(mean_ratings_for_random_10) / len(mean_ratings_for_random_10)

# print('Mean rating for 10 random books per test user: ', mean_benchmark_rating)


# In[19]:


# trying with the training data after preprocessing 
from sklearn.cluster import KMeans

clusterer_KMeans = KMeans(n_clusters=7).fit(book_ratings_training)
preds_KMeans = clusterer_KMeans.predict(book_ratings_training)

from sklearn.metrics import silhouette_score
kmeans_score = silhouette_score(book_ratings_training, preds_KMeans)
print(kmeans_score)


# In[18]:


# trying with the training data after preprocessing 
from sklearn.mixture import GaussianMixture

clusterer_GMM = GaussianMixture(n_components=7).fit(book_ratings_training)
preds_GMM = clusterer_GMM.predict(book_ratings_training)

GMM_score = silhouette_score(book_ratings_training, preds_GMM)
print(GMM_score)


# In[20]:


indices = book_ratings_training.index
preds = pd.DataFrame(data=preds_KMeans, columns=['cluster']).set_index(indices)
preds.head()


# In[21]:


# get a list of the highest-rated books for each cluster
def get_cluster_favorites(cluster_number):
    # create a list of cluster members
    cluster_membership = preds.index[preds['cluster'] == cluster_number].tolist()
    # build a dataframe of that cluster's book ratings
    cluster_ratings = user_book_ratings.ix[cluster_membership]
    # drop books that have fewer than 10 ratings by cluster members
    cluster_ratings = cluster_ratings.dropna(axis='columns', thresh=10)
    # find the cluster's mean rating overal and for each book
    means = cluster_ratings.mean(axis=0)
    # sort books by mean rating
    favorites = means.sort_values(ascending=False)
    return favorites

# for each cluster, determine the overall mean rating cluster members have given books
def get_cluster_mean(cluster_number):
    # create a list of cluster members
    cluster_membership = preds.index[preds['cluster'] == cluster_number].tolist()
    # create a version of the original ratings dataset that only includes cluster members
    cluster_ratings = ratings[ratings['user_id'].isin(cluster_membership)]
    # get the mean rating
    return cluster_ratings['rating'].mean()


# In[25]:


cluster0_books_storted = get_cluster_favorites(0)
cluster0_mean = get_cluster_mean(0)

print('The cluster 0 mean is:', cluster0_mean)
cluster0_books_storted[0:10]


# In[23]:


cluster1_books_storted = get_cluster_favorites(1)
cluster1_mean = get_cluster_mean(1)

print('The cluster 1 mean is:', cluster1_mean)
cluster1_books_storted[0:10]


# In[24]:


cluster2_books_storted = get_cluster_favorites(2)
cluster2_mean = get_cluster_mean(2)

print('The cluster 2 mean is:', cluster2_mean)
cluster2_books_storted[0:10]


# In[26]:


cluster3_books_storted = get_cluster_favorites(3)
cluster3_mean = get_cluster_mean(3)

print('The cluster 3 mean is:', cluster3_mean)
cluster3_books_storted[0:10]


# In[27]:


cluster4_books_storted = get_cluster_favorites(4)
cluster4_mean = get_cluster_mean(4)

print('The cluster 4 mean is:', cluster4_mean)
cluster4_books_storted[0:10]


# In[28]:


cluster5_books_storted = get_cluster_favorites(5)
cluster5_mean = get_cluster_mean(5)

print('The cluster 5 mean is:', cluster5_mean)
cluster5_books_storted[0:10]


# In[29]:


cluster6_books_storted = get_cluster_favorites(6)
cluster6_mean = get_cluster_mean(6)

print('The cluster 6 mean is:', cluster6_mean)
cluster6_books_storted[0:10]


# In[74]:


# associate each test user with a cluster
test_set_preds = clusterer_KMeans.predict(book_ratings_testing)
test_set_indices = book_ratings_testing.index
test_set_clusters = pd.DataFrame(data=test_set_preds, columns=['cluster']).set_index(test_set_indices)

test_set_clusters.head()


# In[32]:


mean_ratings_for_cluster_favorites = []

# put each cluster's sorted book list in an array to reference
cluster_favorites = [cluster0_books_storted, cluster1_books_storted, cluster2_books_storted, cluster3_books_storted, cluster4_books_storted, cluster5_books_storted, cluster6_books_storted]


# for each user, find the 10 books the reader has rated that are the top-rated books of the cluster. 
# get the reader's average score for those books
for index, row in test_set_ratings.iterrows():
    user_cluster = test_set_clusters.loc[index, 'cluster']
    favorites = cluster_favorites[user_cluster].index
    user_ratings_of_favorites = []
    # proceed in order down the cluster's list of favorite books
    for book in favorites:
        # if the user has given the book a rating, save the rating to a list
        if np.isnan(row[book]) == False:
            user_ratings_of_favorites.append(row[book])
        # stop when there are 10 ratings for the user
        if len(user_ratings_of_favorites) >= 10:
            break
    # get the mean for the user's rating of the cluster's 10 favorite books
    mean_rating_for_favorites = sum(user_ratings_of_favorites) / len(user_ratings_of_favorites)
    mean_ratings_for_cluster_favorites.append(mean_rating_for_favorites)
    
mean_favorites_rating = sum(mean_ratings_for_cluster_favorites) / len(mean_ratings_for_cluster_favorites)

print('Mean rating for 10 random books per test user: ', mean_benchmark_rating)
print('Mean rarting for 10 books that are the cluster\'s favorites: ', mean_favorites_rating)
print('Difference between ratings: ', mean_favorites_rating-mean_benchmark_rating)


# In[79]:


import random
def recommend(cluster_assignments, user_id):
    user_cluster = cluster_assignments
    favorites = get_cluster_favorites(user_cluster).index
    favorites = random.choices(favorites, k=9)     
    return favorites
    

# recommendation27229 = recommend(test_set_clusters, user_book_ratings, 27229)
# recommendation31159 = recommend(test_set_clusters, user_book_ratings, 31159)
# recommendation10579 = recommend(test_set_clusters, user_book_ratings, 10579)
# recommendation8667 = recommend(test_set_clusters, user_book_ratings, 8667)

# print('Recommendation for user 27229: ', recommendation27229)
# print('Recommendation for user 31159: ', recommendation31159)
# print('Recommendation for user 10579: ', recommendation10579)
# print('Recommendation for user 8667: ', recommendation8667)

recommendation8667 = recommend(5, 8667)
print(recommendation8667)



def sim_distance(prefs,person1,person2):
    si = {} 
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1    
    if len(si) == 0: 
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item],2) 
                          for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squares)

# Checks for similarity to Person using Euclidean distance score
def top_matches(prefs, person, n=10, similarity = sim_distance):
    scores = [(similarity(prefs,person,other), other)
            for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

# Gets recommendation using a weighted average of all other users using Euclidean distance score
def get_recommendations(prefs, person, n=10, similarity = sim_distance):
    totals = {} 
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item,0) 
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item,0)
                simSums[item] += sim
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]



# In[ ]:




