import base64
import io

def draw_graphs(feat_val1,feat_val2,feat_val3):
    import pandas as pd 
    import networkx as nx
    import matplotlib.pyplot as plt

    data = pd.read_excel("Names.xlsx")
    def conn_count(Feature_Name1,Feature_value1,Feature_Name2,Feature_value2):
        df = pd.DataFrame(columns=['A', 'B'])
        j=0
        for i in range(4000):
            if data[Feature_Name1].iloc[i] == Feature_value1 and data[Feature_Name2].iloc[i] == Feature_value2:
                df.loc[j]= [data[Feature_Name1].iloc[i],data[Feature_Name2].iloc[i]]
                j=j+1
        return df 

    feature1 = 'Approving_officer'
    feature2 = 'Requesting_officer'
    feature3 = 'Supplier_Name'
    
    value1 = feat_val1
    value2 = feat_val2
    value3 = feat_val3
    # Function to get connections 

    df1 = conn_count(feature1,value1,feature2,value2)
    df2 = conn_count(feature1,value1,feature3,value3)
    df3 = conn_count(feature2,value2,feature3,value3)

    G1 = nx.Graph()
    G2 = nx.Graph()
    G3 = nx.Graph()
    G1 = nx.from_pandas_edgelist(df1, 'A', 'B')
    G2 = nx.from_pandas_edgelist(df2, 'A','B')
    G3 = nx.from_pandas_edgelist(df3, 'A','B')
    nx.set_edge_attributes(G1, values = 2, name = 'Connections')
    nx.set_edge_attributes(G2, values = 1, name = 'Connections')
    nx.set_edge_attributes(G3, values = 1, name = 'Connections')

    G4 = nx.compose(G1, G2)  # Compose of two Two Graphs
    G5 = nx.compose(G4, G3)  # Compose of two Two Graphs

    # Drawing graph
    plt.figure(figsize=(16,16))
    plt.title('All the connections between them',size=30,color='orange')
    ax = plt.gca()
    #ax.set_title('All the connections between them',size=30,color='white')
    options = {
        "node_size": 25000,
        "node_color": "lightblue",
        "edgecolors": "black",
        "linewidths": 3,
    }
    pos = nx.spring_layout(G5)
    nx.draw_networkx_edges(G5,pos,width=3,edge_vmax=2)
    nx.draw_networkx_nodes(G5,pos, **options)
    nx.draw_networkx_labels(G5,pos,font_size=18,font_color='red')
    nx.draw_networkx_edge_labels(G5,pos, font_size=18,ax=ax)
    ax.axis('off')
    # to Save Total Connections Graphs Png
    #im = plt.savefig("static/Graph1.jpeg",format="JPEG")
    img1 = io.BytesIO()              # create file-like object in memory to save image without using disk
    plt.savefig(img1, format='png')  # save image in file-like object
    img1.seek(0)                     # move to beginning of file-like object to read it later
    img1 = img1.getvalue() 
    img1 = base64.b64encode(img1)
    img1 = img1.decode() 
    del df1,df2,df3
    # ------------------------------------------------------------------------#   
    #           Drawing 2nd Graph                
    # ------------------------------------------------------------------------#

    def Fraud_conn_count(Feature_Name1,Feature_value1,Feature_Name2,Feature_value2):
        df = pd.DataFrame(columns=['A', 'B'])
        j=0
        for i in range(4000):
            if data[Feature_Name1].iloc[i] == Feature_value1 and data[Feature_Name2].iloc[i] == Feature_value2 and data.Fraud.iloc[i]==1:
                df.loc[j]= [data[Feature_Name1].iloc[i],data[Feature_Name2].iloc[i]]
                j=j+1
        return df  

    df4 = Fraud_conn_count(feature1,value1,feature2,value2)
    df5 = Fraud_conn_count(feature1,value1,feature3,value3)
    df6 = Fraud_conn_count(feature2,value2,feature3,value3)


    G21 = nx.Graph()
    G22 = nx.Graph()
    G23 = nx.Graph()          

    G21 = nx.from_pandas_edgelist(df4, 'A', 'B')
    G22 = nx.from_pandas_edgelist(df5, 'A','B')
    G23 = nx.from_pandas_edgelist(df6, 'A','B')
    nx.set_edge_attributes(G21, values = 2, name = 'Connections')
    nx.set_edge_attributes(G22, values = 1, name = 'Connections')
    nx.set_edge_attributes(G23, values = 1, name = 'Connections')

    G24 = nx.compose(G21, G22)
    G25 = nx.compose(G24, G23)

    plt.figure(figsize=(16,16))
    plt.title('Fraudulent Connections Between them ',size=30,color='red')
    ax = plt.gca()
    #ax.set_title('Fraudulent connections between them',size=30,color='white')
    options = {
        "node_size": 25000,
        "node_color": "lightblue",
        "edgecolors": "black",
        "linewidths": 3,
    }

    if len(df4)==0 and len(df5)==0 and len(df6)==0:
        G25.add_nodes_from(G5)
        plt.title('No Fraudulent Connections Between them',size=30,color='red')
        #ax.set_title('There are No Fraudulent connections between them',size=30,color='white') 
    pos = nx.spring_layout(G25)
    #pos = {'Rowney Cortin':(1, 0.7), 'Bunny Spraggs':(0.5, 0.5), 'Rosenbaum Group': (0.7, 1.5)} 
    nx.draw_networkx_edges(G25,pos,width=3,edge_vmax=2)
    nx.draw_networkx_nodes(G25,pos, **options)
    nx.draw_networkx_labels(G25,pos,font_size=18,font_color='red')
    nx.draw_networkx_edge_labels(G25,pos, font_size=18,ax=ax)
    ax.axis('off')
    #plt.set_facecolor("none")
    #im = plt.savefig("static/Graph2.jpeg",format="JPEG")
        # create PNG image in memory
    img2 = io.BytesIO()              # create file-like object in memory to save image without using disk
    plt.savefig(img2, format='png')  # save image in file-like object
    img2.seek(0)                     # move to beginning of file-like object to read it later
    img2 = img2.getvalue()         # get data from file (BytesIO)
    img2 = base64.b64encode(img2) # convert to base64 as bytes
    img2 = img2.decode()
    del df4,df5,df6,data
    return img1,img2

    return encoded_img_data1,encoded_img_data2

#App_off_in,Req_off_in,supp_in = 'Rafael Penchen', 'Jayme Birth','Walsh Group'

#draw_graphs(App_off_in,Req_off_in,supp_in)
