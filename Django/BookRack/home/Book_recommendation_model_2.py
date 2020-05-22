#!/usr/bin/env python
# coding: utf-8

# In[33]:




# In[36]:




# In[37]:


# Returns a distance-based similarity score for person1 and person2
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
    rankings = [[total/simSums[item], item] for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]



# Top recommendation for user_id= 1
#get_recommendations(d, 1)


# 

# In[ ]:




