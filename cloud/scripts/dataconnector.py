import pandas as pd
import swissparlpy as spp
import os



def get_votes(since, until):
    since = pd.to_datetime(since).tz_localize("UTC")
    until = pd.to_datetime(until).tz_localize("UTC")
    data = spp.get_data('Vote', Language="DE", VoteEnd__gt=since, VoteEnd__lt=until)
    return data

def get_voting_of_votes(votes,path):
    for vote in votes:
        save_voting_of_vote(vote['ID'], path)

    df_voting = pd.concat([pd.read_pickle(os.path.join(path, x)) for x in os.listdir(path)])
    delete_pickels(path)
    return df_voting


def save_voting_of_vote(id, path):
    if not os.path.exists(path):
        os.mkdir(path)
    data = spp.get_data("Voting", Language="DE", IdVote=id)
    df = pd.DataFrame(data)
    pickle_path = os.path.join(path, f'{id}.pks')
    df.to_pickle(pickle_path)

def delete_pickels(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    print("Removed pickles in", path)