import os
from enum import Enum

import pandas as pd
import swissparlpy as spp


class Backend(Enum):
    OPENPARLDATA = "openparldata"
    ODATA = "odata"


def get_votes(backend: Backend):
    if backend == Backend.ODATA:
        data = spp.get_data("Vote", backend="odata", Language="DE")
    else:
        data = spp.get_data("votings", backend="openparldata")

    return pd.DataFrame(data)


def get_voting_of_votes(votes, path, backend: Backend):
    for _, vote in votes.head(100).iterrows():
        vote_id = vote["ID"] if backend == Backend.ODATA else vote["id"]
        save_voting_of_vote(vote_id, path, backend)

    df_voting = pd.concat(
        [pd.read_pickle(os.path.join(path, x)) for x in os.listdir(path)]
    )

    return df_voting


def save_voting_of_vote(id, path, backend: Backend):
    if not os.path.exists(path):
        os.mkdir(path)

    if backend == Backend.ODATA:
        data = spp.get_data("Voting", Language="DE", IdVote=id, backend=backend.value)
        print(f"{data.count} rows loaded.")
        df = pd.DataFrame(data)
        pickle_path = os.path.join(path, f"{id}.pks")
        df.to_pickle(pickle_path)
        print(f"Saved pickle at {pickle_path}")
    else:
        data = spp.get_data("votes", voting_id=id, backend=backend.value)
        print(f"{data.count} rows loaded.")
        df = pd.DataFrame(data)
        pickle_path = os.path.join(path, f"{id}.pks")
        df.to_pickle(pickle_path)
        print(f"Saved pickle at {pickle_path}")


def main():
    backend = Backend.OPENPARLDATA
    print(f"You selected the backend: {backend}")

    votes = get_votes(backend)
    print(votes.columns)

    df_voting = get_voting_of_votes(votes, "./voting", backend)

    print(df_voting.head(5))
    print("Finished")


if __name__ == "__main__":
    main()
