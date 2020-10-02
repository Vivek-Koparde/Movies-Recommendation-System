#!/usr/bin/env python

# ## Nearest Neighbor item based Collaborative Filtering

##Dataset url: https://grouplens.org/datasets/movielens/latest/
import pandas as pd
import numpy as np



movies_df = pd.read_csv('movies.csv',usecols=['movieId','title'],dtype={'movieId': 'int32', 'title': 'str'})
rating_df=pd.read_csv('ratings.csv',usecols=['userId', 'movieId', 'rating'],
    dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})


filter=movies_df['title']=='Toy Story (1995)'
print(filter)



df = pd.merge(rating_df,movies_df,on='movieId')




combine_movie_rating = df.dropna(axis = 0, subset = ['title'])
movie_ratingCount = (combine_movie_rating.
     groupby(by = ['title'])['rating'].
     count().
     reset_index().
     rename(columns = {'rating': 'totalRatingCount'})
     [['title', 'totalRatingCount']]
    )
movie_ratingCount.head()


# In[93]:


rating_with_totalRatingCount = combine_movie_rating.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
rating_with_totalRatingCount.head()



pd.set_option('display.float_format', lambda x: '%.3f' % x)
print(movie_ratingCount['totalRatingCount'].describe())


# 
popularity_threshold = 50
rating_popular_movie= rating_with_totalRatingCount.query('totalRatingCount >= @popularity_threshold')
rating_popular_movie.head()


# In[96]:


rating_popular_movie.shape


# In[97]:


## First lets create a Pivot matrix

movie_features_df=rating_popular_movie.pivot_table(index='title',columns='userId',values='rating').fillna(0)
movie_features_df.head()




from scipy.sparse import csr_matrix

movie_features_df_matrix = csr_matrix(movie_features_df.values)

from sklearn.neighbors import NearestNeighbors


model_knn = NearestNeighbors(metric = 'cosine', algorithm = 'brute')
model_knn.fit(movie_features_df_matrix)




movie_features_df.index[3]



query_index = np.random.choice(movie_features_df.shape[0])
print(query_index)
distances, indices = model_knn.kneighbors(movie_features_df.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 6)


# In[101]:


movie_features_df.index.values[2]

indexNamesArr = movie_features_df.index.values
def give_rec(name):
    index=0
    # convert ndarray to list
    listOfRowIndexLabels = list(indexNamesArr)
    for i in range(len(listOfRowIndexLabels)):
        m_name=listOfRowIndexLabels[i]
        m_name=m_name[:-7]
        if m_name==name:
            index=i
            print(i)
    ls=[]
    distances, indices = model_knn.kneighbors(movie_features_df.iloc[index,:].values.reshape(1, -1), n_neighbors = 6)
    for i in range(0, len(distances.flatten())):
        if i == 0:
            print('Recommendations for {0}:'.format(movie_features_df.index[index]))
            #return('Recommendations for {0}:'.format(movie_features_df.index[index]))
        else:
            print('{0}: {1}, with distance of {2}:'.format(i, movie_features_df.index[indices.flatten()[i]], distances.flatten()[i]))
            ls.append(str(movie_features_df.index[indices.flatten()[i]]))
    return ls


# ## Cosine Similarity
# 
# ![image.png](attachment:image.png)



#GUI
from tkinter import *  
import pandas as pd
from sklearn.model_selection import train_test_split

from tkinter import ttk
from tkinter import messagebox



def similar_movie():
    
    sim_str = ''
    sim_list = []
    #try:
    movie_name = str(user_id.get())
    print(movie_name,len(movie_name))
    if(len(movie_name)<1):
        messagebox.showinfo('Try Again','Enter Movie Name')
    else:
        sim_list = give_rec(movie_name)
        print(sim_list)
        sim_str = '\n'.join(sim_list)
        lbl['text'] = sim_str
    # print(sim_str)
    #except:
        #messagebox.showinfo('Try Again','No Matched Movie Found')




omk = Tk()  
omk.title("Movie Recommendation System")
omk.resizable(height = None, width = None)

lbl = Label(omk, text = "Movie Recommender System",font=("Times New Roman", 20))
lbl.grid(row=0,column=0,padx=(10, 10),pady=(10 ,10))


frame = ttk.Frame(omk, padding=10)
frame.grid(row=3,column=0)

global user_id


user_id = None

lbl1 = Label(frame, text = "Enter Movie Name",font=("Times New Roman", 10))
lbl1.grid(row=2,column=0,padx=(10, 0))

entry = Entry(frame, width=25)
entry.grid(row=4,column=0,padx=(10, 0))
user_id = entry





btn2 = ttk.Button(frame,text = 'Similar Movies', command=similar_movie)
btn2.grid(row=5,column=0,padx=(10,0))


omk.mainloop()  




