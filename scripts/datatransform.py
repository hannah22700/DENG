import pandas as pd
import re

def clean_up_votes(votes):
    df = votes.drop("Language",axis=1)

    return df

def clean_up_voting(voting):
    df_voting = voting.reset_index()
    df = df_voting.drop(["Language", "ParlGroupColour","index"],axis=1)
    return df


def create_party_summary(voting):
    mode_df = voting.groupby(['BusinessTitle','IdVote', 'ParlGroupName'])['DecisionText'].agg(lambda x: x.mode().iloc[0]).reset_index()
    counts = pd.crosstab([voting['BusinessTitle'], voting['IdVote'], voting["ParlGroupName"]], voting['DecisionText'])
    vote_values = counts.columns.tolist()
    final_df = pd.merge(mode_df, counts, on=['BusinessTitle', 'IdVote','ParlGroupName'])
    final_df["TotalSeats"] = final_df[vote_values].sum(axis=1)
    final_df.columns = [clean_column(col) for col in final_df.columns]

    return final_df


def clean_column(name):
    name = str(name)          
    name = name.replace(" ", "_")  
    name = re.sub(r'\W', '', name)
    return name