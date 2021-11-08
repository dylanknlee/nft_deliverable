# packages for deliverable
import streamlit as st
import streamlit.components.v1 as components

# packages for the dataset
import pandas as pd
import numpy as np

# packages for visualizations
from pyvis import network as net
from IPython.core.display import display, HTML
import streamlit.components.v1 as components
from PIL import Image
import plotly.express as px

st.title('Analyzing the Legitimacy of NFT Transactions Using Graph Theory')
st.subheader('By Dylan Lee')

# 1.) INTRODUCTION - get the audience acquainted with the context of our project
st.header("Introduction: NFT's Explained")

intro_text = "Non-fungible tokens (NFT's) have been rapidly trending in \
popularity during a modern era where digital transactions such as Venmo and \
Apple Pay are mainstream while the advent of cryptocurrency is ever rising. \
NFT's encompass a wide variety of digital artifacts that contain intrinsic and \
monetary value, such as art, video and audio clips, and much more. NFT's are \
often marketed and sold amongst users within a virtual blockchain with some \
even skyrocketing to tens of millions of dollars in value. Given their \
potential value, we were interested in further analyzing the movement of NFT's \
throughout the market, to detect any indicators of fradualency or deceitful \
transactions. \n \n In particular, this project specifically hones in on the \
Topps MLB Series 1 NFT's, a collection of digital baseball trading cards available \
on the World Asset eXchange NFT Blockchain (WAX). Because these NFT's are a \
relatively new market, we believed that users could engage in illegitimate \
transactions early on to quickly capitalize and artificially inflate the prices \
of their NFT's."

st.write(intro_text)

image1, image2 = st.columns(2)
# potential gifs
#st.markdown("![Alt Text](https://d9hhrg4mnvzow.cloudfront.net/on.wax.io/toppsmlb/0e5c1650-rare-gif.gif)")

# display cool GIFs
with image1:
    st.markdown("![](https://media.giphy.com/media/g99NuX1EAqe2s/giphy.gif)")
    #st.markdown("![Alt Text](https://d9hhrg4mnvzow.cloudfront.net/on.wax.io/toppsmlb/0e5c1650-rare-gif.gif)")

with image2:
    st.markdown("![](https://images.squarespace-cdn.com/content/v1/512cd3f8e4b087d8ea2c9220/1382022283162-PWBI8ACGTSPO481YPLU3/ku-medium.gif?format=500w)")

st.caption("Examples of the MLB Topps NFT")

# 2.) API - data collection, describe the table used
st.header("Data Collection: The WAX Blockchain API")

# add text about the need and use of the APIs
api_text = "Prior to beginning our analysis, we first had to obtain any data \
necessary that represented user transactions of the Topps MLB NFT's on the WAX \
Blockchain. In order to do this, we relied on two separate API's \
(Application Programming Interface) made available by the WAX Blockchain: the \
Atomic Asset API, and the Atomic Market API. An API is an intermediary interface \
that allows us to request and obtain data from the blockchain directly, \
eliminating any hassle of web-scraping or other forms of messy data collection."
st.write(api_text)

# ATOMIC ASSET API
st.subheader("Atomic Asset API: Collecting Each Unique NFT")
asset_text = "Our first API, the Atomic Asset API, allows us to obtain a \
random selection of MLB Topps NFT's that have been made available on the market. \
In the data table below provides a glimpse of the data we've worked with: each \
row within the table features various aspects about a unique NFT."

st.write(asset_text)
st.write(pd.read_csv('assets.csv').head())

# ATOMIC MARKET API
st.subheader("Atomic Market API: Tracking the Movement of Each NFT")
market_text = "The above table may seem convoluted, and it definitely is! The \
raw data is messy, but it contains a key column we want to use- the \
identification number (asset_id) assigned to each unique NFT. We can implement the ID \
number of each NFT as a parameter in our next API, the Atomic Market API, to pull \
the oldest transaction history of that NFT from our previous table, which is displayed \
in the table below. Like the previous dataframe, this one is a bit messy, but it \
contains two key pieces of information about the transaction histories- the seller \
and buyer. While we've provided only a small sample of the data, for this project, \
over 250,000 different transactions were used in our dataset!"

st.write(market_text)
st.write(pd.read_csv('sales.csv'))

# 3.) GRAPH ALGORITHMS
st.header("Implementing Graph Theory to NFT Transactions")

# graph intro text
graph_intro_text = "Now that we have data consisting of the sellers and buyers \
within the WAX market blockchain, we're going to transition into representing \
the marketplace in terms of graphs, a data structure that will help us analyze \
and identify and discernable patterns within its ledgers. More specifically \
we'll be using undirected, weighted graphs. \n \n Within a graph, there are key \
components to look out for when examining the overall network of the WAX \
marketplace. First are the discernable nodes, each of which simply represents \
a unique person within the marketplace albeit a seller or buyer. Secondly the \
edges between a pair of nodes indicates that a transaction between those two \
people have occurred. In the specificity of a weighted graph, \
each edge has a numerical weight denoting the number of transactions between \
any pair of users. Note that our graph is also undirected such that edges have \
no direction, since it isn't particularly important knowing which individual \
nodes represents the buyer or the seller in each pair. \n \n Below, there is provided \
a very basic example of the undirected, weighted graphs we're working with. Here, \
this graph contains two people who've had three transactions between them in their \
ledgers. You can interact with this graph, and even adjust some of the physics \
to alter the way they move!"
st.write(graph_intro_text)

# create a simple graph of two users for a visual demonstration
simple_graph = net.Network(height='400px', width='50%')

# nodes of the simple graph
simple_graph.add_node(1, title = "User 1", label = "User 1", color = "#dd4b39")
simple_graph.add_node(2, title = "User 2", label = "User 2", color = "#dd4b39")
simple_graph.add_edge(1,2, label = 3)

# html code of the simple graph
html_simple = open("simple_graph.html", 'r', encoding='utf-8')
source_code_simple = html_simple.read()

# display the graph onto the deliverable
st.subheader("Transactions Between Two Users")
components.html(source_code_simple, height = 370, width = 1000)
st.caption("Try moving the graph around and adjusting its physics!")

# add precursor text to introduce the need and use of algorithms
precursor_text = "This seems simple enough, but it's worthwhile to recall \
that the above graph only captures the ledger between two users. But now imagine \
if we were to include all members of the WAX blockchain! The graph would then \
be a densely populated network consisting of the hundreds of thousands of nodes \
for each user alongside web of weighted edges linking all pairs of those who \
have engaged in commerce amongst each other. As you can probably imagine, this \
will get quite complicated even to visually see, so we need a way to somehow \
reduce and simplify our graph to focus solely on transactions we deem could be \
illegitimate."
st.write(precursor_text)

# discuss the graph algorithms here
st.subheader("Identifying Illegitimacy")
algorithms_text = "Two graph algorithms that we'll use to untangle this \
interwoven network are Kruskal's and Prim's Algorithm, both of which will \
derive the minimum spanning forest of an undirected, weighted graph just like \
our own. The minimum spanning tree of a graph is a subset of that graph that \
contains enough edges to connect all nodes together while still having the \
smallest sum of edge weights, and a collection of separate trees forms a forest. However, for the purposes of our project, these algorithms can be reversed to find the maximum spanning forest instead. \n \n \
But why do we want the maximum spanning forest? \n \n Let's backtrack to \
when we first discussed that users could capitalize on the recent release \
of the Topps MLB NFT's to quickly artificially inflate the price of their NFT's. \
We believe that any two users could intentionally exchange an NFT back and forth \
repeatedly between each other, making it appear valuable once after it's gone through \
multiple transactions; each at a steadily increasing cost, before other users \
could have a change to participate in any transactions of their own. Relating \
this to our graph, this would correspond to an abnormally large weight for the \
edge linking their two nodes together. By creating a maximum spanning forest, \
we can spot such high edge weights if they exist, while filtering out those that \
don't suggest fradualency!"
st.write(algorithms_text)

# create a more complex network
complex_graph = net.Network(height = '400px', width = '50%')
for i in range(1, 7):
    name = "User " + str(i)
    complex_graph.add_node(i, title = name, label = name, color = "#dd4b39")

# maximum edges of complex graph
complex_graph.add_edge(1,4, label = 93)
complex_graph.add_edge(4,5, label = 107)
complex_graph.add_edge(2,5, label = 86)
complex_graph.add_edge(2,3, label = 102)
complex_graph.add_edge(3,6, label = 113)

# non maximum edges of complex graph
complex_graph.add_edge(1,2, label = 8, color = "#162347")
complex_graph.add_edge(1,3, label = 3, color = "#162347")
complex_graph.add_edge(3,5, label = 6, color = "#162347")
complex_graph.add_edge(4,2, label = 1, color = "#162347")
complex_graph.add_edge(6,5, label = 11, color = "#162347")

# html code of the complex graph
html_complex = open("complex_graph.html", 'r', encoding='utf-8')
source_code_complex = html_complex.read()

# create an MST of the above complex network
mst_graph = net.Network(height = '400px', width = '50%')
for i in range(1, 7):
    name = "User " + str(i)
    mst_graph.add_node(i, title = name, label = name, color = "#dd4b39")

# edges of the mst_graph
mst_graph.add_edge(1,4, label = 93)
mst_graph.add_edge(4,5, label = 107)
mst_graph.add_edge(2,5, label = 86)
mst_graph.add_edge(2,3, label = 102)
mst_graph.add_edge(3,6, label = 113)

# html of the mst_graph
html_mst = open("mst.html", 'r', encoding = 'utf-8')
source_code_mst = html_mst.read()

# display the complex and MST graphs onto the deliverable
st.subheader("An Example Maximum Spanning Tree")
# checkbox to toggle between the complete graph and its MST
show_mst = st.checkbox("Show the Maximum Spanning Tree of this Graph!")

# text to explain the MST visualization
mst_text = ""
st.write(mst_text)

st.caption("Try clicking on the checkbox!")
if show_mst:
    components.html(source_code_mst, height = 415, width = 1000)
else:
    components.html(source_code_complex, height = 415, width = 1000)

# 4.) Results and Conclusion
st.header("Results and Analysis")
# text for the results
results_text = "Both Kruskal's and Prim's algorithm can be applied to our graph \
consisting of approximately 250,000 different transactions to form unique maximum \
spanning forests, which we can then compare. After running both algorithms, we \
are outputted with the two graphs shown below."
st.write(results_text)

# MST from Kruskal's Algorithm
st.subheader("Maximum Spanning Forest via Kruskal's Algorithm")
kruskal_mst = Image.open('KruskalGraph.png')
st.image(kruskal_mst)

# MST from Prim's Algorithm
st.subheader("Maximum Spanning Forest via Prim's Algorithm")
prim_mst = Image.open('PrimGraph.png')
st.image(prim_mst)

# text for analysis
analysis_text = "In both graphs, the blue circles are the nodes representing \
unique users whose transactions are denoted by the red edges. The users \
that appear are those suspected by the algorithms to be fraudulent, \
while edges show specific pairs of users that have been engaging in \
illegitimate transactions amongst each other. But the \
graphs created by each algorithm visually differ and appear cluttered due \
to the high density of data from our initial dataset. Luckily, for ease of \
analysis, such graphs can be represented as data frames."
st.write(analysis_text)

# read in the dataframes
kruskal = pd.read_csv('TransactionsBtwnParties_Kruskal.csv')
prim = pd.read_csv('TransactionsBtwnParties_Prim.csv')

# reformat the dataframes
kruskal = kruskal.drop(columns = ["Unnamed: 0"]).head()
prim = prim.drop(columns = ["Unnamed: 0"]).head()

# display both dataframes
col_kruskal, col_prim = st.columns(2)

with col_kruskal:
    st.subheader("Kruskal's Algorithm")
    st.write(kruskal)

with col_prim:
    st.subheader("Prim's Algorithm")
    st.write(prim)
st.caption("The top 5 pairs of users from the maximum spanning forests of both algorithms.")

# add more analysis text
analysis_text2 = "We can see that both algorithms performed very similarly, \
outputting the same pairs of users with the highest edge weights between them. \
More so, the highest number of transactions between any two users in our dataset \
is 51, followed by 43 and then 40. But we want to investigate if \
such a number of transactions is typical, or rather suspiciously high. To do so, \
a histogram and box plot of the edge weights is created below, which respectively visualize \
the distribution and spread of the edge weights from the maximum spanning forests."
st.write(analysis_text2)

st.subheader("Distribution and Spread of Edge Weights")
kruskal = pd.read_csv('TransactionsBtwnParties_Kruskal.csv')
fig = px.histogram(kruskal, x="Weights", marginal = 'box')
st.plotly_chart(fig)
st.caption("Interact with the features of the graph to get a closer look at the data!")

decision_text = "Examining the distribution and spread of the edge weights \
from the maximum spanning forest, we see that a majority of approximately 2,500 \
edges denote only 2-4 transactions between pairs of users. Whereas higher \
magnitude weights shown in the data tables above appear much more rarely, \
becoming outliers when the entire distribution is taken into consideration. \
Because large edge weights account for such a negligible fraction of all \
possible edge weights in the maximum spanning forest, the possibility that \
these users are conducting in illegitimate transactions should definitely be \
taken into serious consideration."
st.write(decision_text)

st.header("What's Next: Further Steps to Take")
conclusion_text = "While this analysis \
doesn't empirically determine users guilty of fraudulence, it is \
definitely a step in the right direction. Further analyses can be conducted \
to support the objective of this research project, and to solidify \
additional concrete evidence of users performing illegitimate transactions. Given \
a greater bandwidth of resources and time, it would be interesting to examine if \
certain features of NFT's promote fraudulent transactions, or even explore different markets. \
Performing statistical tests with greater volumes of data to calculate the probabilistic \
likelihood of certain edge weights or even implementing machine \
learning models to classify fair transactions are directions to possibly take. \
\n \n Nevertheless, it remains important that the goal and purpose of this research \
project is kept in mind. Much of our world is becoming digitized, and with monetary \
assets and currency already exchanged virtually, it's important that we ensure \
that such transactions are enacted securely and fairly for the sake of its users."
st.write(conclusion_text)
