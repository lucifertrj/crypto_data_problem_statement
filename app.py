import pandas as pd
import streamlit as st
import ast

st.title("SuperMind")
st.header("Bloomberg of Crypto")

problem = st.radio("Problem Statement Analysis",('Most Active Folks',
                                               "Least Active Folks",
                                               "Total Image Data",
                                               "Total Text Data",
                                               "Total number of messages sent to the channel",
                                               "Total Number of Unique Sender",
                                               "View Word Cloud",
                                               "Engagement"
                                               )
                 )
try:
    data = pd.read_csv("crypto_supermind.csv")
except FileNotFoundError:
    st.header("Dataset not found. Data is safe not pushed to GitHub")

st.header("Answers for the problem statements")

if problem == "Most Active Folks": 
    group_common = data.groupby("sender.name")[['text','image']].count()
    top10_text = group_common.sort_values(['text'])[::-1].iloc[:10]
    st.markdown("#### More number of Text sent")
    st.dataframe(top10_text)
    st.markdown("#### More number of Image sent")
    top10_images = group_common.sort_values(['image'])[::-1].iloc[:10]
    st.dataframe(top10_images)
    st.image("active.jpeg")

elif problem == "Least Active Folks":
    least_group = data.groupby("sender.name")[['text','image']].count()
    bottom10_text = least_group.sort_values(['text']).iloc[:10]
    st.markdown("#### Least number of Text")
    st.dataframe(bottom10_text)
    bottom10_images = least_group.sort_values(['image']).iloc[:10]
    st.markdown("#### Least number of Image sent")
    st.dataframe(bottom10_images)
    st.image("notactive.jpeg")

elif problem == "View Word Cloud":
    st.markdown("#### Text Word Cloud")
    st.image("text.jpeg")
    st.markdown("#### Senders Name Word Cloud")
    st.image("sender.name.jpeg")
    
elif problem == "Total Image Data":
    st.markdown("#### Total Images sent: 911")

elif problem == "Total Text Data":
    st.markdown("#### Total Text Messages sent: 33125")

elif problem == "Total number of messages sent to the channel":
    st.markdown("#### Total Number of messages sent: 34139")

elif problem == "Total Number of Unique Sender":
    st.markdown("#### Total Number of Unique Sender: 99")
    
elif problem == "Engagement":
    engagement_col = ["reaction_list","mentions_list","hashtag_list","external_links_list"]
    more_col = engagement_col + ['sender.name','id','sender.ref','text','image']
    engagement_data = data[more_col]
    
    emojis = []
    likes = []
    for reactions in engagement_data['reaction_list']:
        #reaction list is a string
        #within string we have list
        #and within list we have dictionary and tuple
        #lets decode it
        if len(reactions)>3:
            #why 3?
            #because [] calulates to 2, so we need something more than 2
            get_dict = ast.literal_eval(reactions[1:-1])
            if isinstance(get_dict,tuple):   
                for from_tuple in get_dict:
                    emojis.append(from_tuple['emoji_unicode'])
                    likes.append(from_tuple['count'])
                    break   #break because we need to match the total length of dataset
            else:
                emojis.append(get_dict['emoji_unicode'])
                likes.append(get_dict['count'])
        else:
            emojis.append("")
            likes.append("")
    engagement_data['emoji'] = emojis
    engagement_data['like_count'] = likes
    ok_mess = engagement_data[engagement_data['emoji']=="👍"][['text','image','sender.name','emoji']]
    st.dataframe(ok_mess)
    st.image("reaction.jpeg")
    st.markdown("#### When people upvoted and downvoted")
    st.image("up_down.jpeg")
