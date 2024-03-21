#!/usr/bin/env python
# coding: utf-8

# In[36]:


#Import the libraries

import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
pd.options.mode.chained_assignment = None

#read in the data

df= pd.read_csv(r'/Users/nehathombare/Downloads/movies.csv')


# In[37]:


# Look at the data
df.head()


# In[12]:


#Finding missing values or Data cleaning 

for col in df.columns:
    pct_missing = np.mean(df[col].isnull())
    print('{} - {}%'.format(col,pct_missing))


# In[13]:


# Data types for column

df.dtypes


# In[19]:


# Shape of the data
df.shape


# In[20]:


df["genre"].unique()


# In[21]:


# Calculating the missing values in different columns
df.isnull().sum().sort_values(ascending=False)


# In[24]:


# Removing Missing Values
dfFrame = df.dropna()


# In[25]:


# Calculating the missing values in different columns
dfFrame.isnull().sum().sort_values(ascending=False)


# In[26]:


dfFrame.shape
#showing the how many movies are left


# In[27]:


#Adding new columns

dfFrame["profit"] = dfFrame["gross"] - dfFrame["budget"]
dfFrame['result'] = dfFrame['profit'].apply(lambda x: 'hit' if x > 0 else 'flop')
dfFrame.head(10)

 #will calculate profit from the gross revenue and budget and also classified films as hit/flop based on the profit.


# In[28]:


#Analyze by the score

highest_rated_movies = dfFrame.groupby('year').apply(lambda x: x.loc[x['score'].idxmax()])
highest_rated_movies.head(10)


# In[29]:


# Highest rated movies over the years

hit_count = len(highest_rated_movies[highest_rated_movies['result']=="hit"])
flop_count = len(highest_rated_movies[highest_rated_movies['result'] == "flop"])


print(f"Number of Hit Films: {hit_count}")
print(f"Number of Flop Films: {flop_count}")


# In[30]:


# Analyze by the budget

movies_with_highest_budget = dfFrame.groupby('year').apply(lambda x: x.loc[x['budget'].idxmax()])
movies_with_highest_budget.head(10)


# In[31]:


#Movies with the highest budget over the years

hit_count = len(movies_with_highest_budget[movies_with_highest_budget['result']=="hit"])
flop_count = len(movies_with_highest_budget[movies_with_highest_budget['result'] == "flop"])


print(f"Number of Hit Films: {hit_count}")
print(f"Number of Flop Films: {flop_count}")


# In[40]:


#Analyze by the votes

movies_with_highest_votes = dfFrame.groupby('year').apply(lambda x: x.loc[x['votes'].idxmax()])
movies_with_highest_votes.head(10)


# In[41]:


#Highest watched movies over the years

hit_count = len(movies_with_highest_votes[movies_with_highest_votes['result']=="hit"])
flop_count = len(movies_with_highest_votes[movies_with_highest_votes['result'] == "flop"])


print(f"Number of Hit Films: {hit_count}")
print(f"Number of Flop Films: {flop_count}")


# In[34]:


# Analyze by the gross revenue
movies_with_highest_gross_revenue = dfFrame.groupby('year').apply(lambda x: x.loc[x['gross'].idxmax()])
movies_with_highest_gross_revenue.head(10)


# In[42]:


#Movies with the highest gross revenue over the years

hit_count = len(movies_with_highest_gross_revenue[movies_with_highest_gross_revenue['result']=="hit"])
flop_count = len(movies_with_highest_gross_revenue[movies_with_highest_gross_revenue['result'] == "flop"])


print(f"Number of Hit Films: {hit_count}")
print(f"Number of Flop Films: {flop_count}")


# In[45]:


# Analyze by the profit
highest_profit_generating_movies = dfFrame.groupby('year').apply(lambda x: x.loc[x['profit'].idxmax()])
highest_profit_generating_movies.head(10)


# In[46]:


#Visualizing different Aspects and Trends
#Audience preferences for different genres of movies

def create_pie_chart_data(subset, title):
    genre_counts = subset['genre'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=genre_counts.index, values=genre_counts.values, textinfo='percent+label')])
    fig.update_layout(title_text=title)
    return fig



fig1 = create_pie_chart_data(highest_rated_movies, "Genre Distribution of Highest Score")
fig2 = create_pie_chart_data(movies_with_highest_budget, "Genre Distribution of Highest Budget")
fig3 = create_pie_chart_data(movies_with_highest_votes, "Genre Distribution of Highest Vote ")
fig4 = create_pie_chart_data(highest_profit_generating_movies, "Genre Distribution of Highest Profit ")


fig = make_subplots(rows=2, cols=2, subplot_titles=["Highest Score", "Highest Budget", "Highest Vote", "Highest Profit"],specs=[[{"type": "pie"}, {"type": "pie"}],
           [{"type": "pie"}, {"type": "pie"}]],
)
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=1, col=2)
fig.add_trace(fig3.data[0], row=2, col=1)
fig.add_trace(fig4.data[0], row=2, col=2)

fig.update_layout(width=1000, height=800,title="Genre Distribution", showlegend=False)
fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    paper_bgcolor="LightSteelBlue")
fig.show()


# In[47]:


#Analyzing the performance of the directors of the years

def create_bar_plot_data(subset, column_name):
    top_counts = subset[column_name].value_counts().nlargest(10)
    colors = px.colors.qualitative.Set3
    color_mapping = dict(zip(top_counts.index, colors))
    fig = go.Figure(data=[go.Bar(x=top_counts.index, y=top_counts.values)])
    fig.update_layout(xaxis_title=column_name, yaxis_title='Count')
    top_counts_color = top_counts.index.map(color_mapping)
    fig = px.bar(top_counts, x=top_counts.index, y=top_counts.values)
    fig.update_traces(marker=dict(color=top_counts_color))
    return fig


fig1 = create_bar_plot_data(highest_rated_movies, 'director')
fig2 = create_bar_plot_data(movies_with_highest_budget, 'director')
fig3 = create_bar_plot_data(movies_with_highest_votes, 'director')
fig4 = create_bar_plot_data(highest_profit_generating_movies, 'director')


fig = make_subplots(rows=4, cols=1, subplot_titles=["Highest Scored Films", "Highest Budgeted Films", "Highest Voted Films", "Highest Profit Films"])
fig.add_trace(fig1.data[0], row=1, col=1)
fig.add_trace(fig2.data[0], row=2, col=1)
fig.add_trace(fig3.data[0], row=3, col=1)
fig.add_trace(fig4.data[0], row=4, col=1)


fig.update_layout(width=1000, 
                height=1200, 
                title="Top Directors over the Years", 
                showlegend=False)


fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    paper_bgcolor="LightSteelBlue")

fig.show()


# In[48]:


#Highest Film Budget Over the years

fig = px.line(movies_with_highest_budget, x='year', y='budget', title='Highest Film Budgets over the Years')
fig.update_layout(width=1000, height=800,xaxis_title='Year', yaxis_title='Budget')
fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    paper_bgcolor="LightSteelBlue")
fig.update_traces(mode='lines+markers', marker_line_width=2, marker_size=10)
fig.show()


# In[49]:


#Profit generation over the years 

fig = px.line(movies_with_highest_budget, x='year', y='profit', title='Highest Profit over the Years')
fig.update_layout(width=1000, height=800,xaxis_title='Year', yaxis_title='Profit Generatinon over the Years')
fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    paper_bgcolor="LightSteelBlue")
fig.update_traces(mode='lines+markers', marker_line_width=2, marker_size=10)
fig.show()


# In[50]:


#Run Time Breakdown For Profit Generating Genres

fig = px.scatter(highest_profit_generating_movies, x="profit", y="runtime", color="genre", symbol="genre",
                 size='votes', hover_data=['runtime'], title="Run Time Breakdown For Profit Generating Genres")
fig.update_layout(width=1000, height=800,xaxis_title='Profit($/USD)', yaxis_title='Run Time (minutes)')
fig.update_layout(
    margin=dict(l=40, r=40, t=40, b=40),
    paper_bgcolor="LightSteelBlue")
fig.show()


# In[ ]:




