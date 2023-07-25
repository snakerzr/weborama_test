import click
import pandas as pd
from tqdm import tqdm


@click.command()
@click.argument("impressions_filepath", type=click.Path(exists=True))
@click.argument("events_filepath", type=click.Path(exists=True))
@click.argument("conversions_filepath", type=click.Path(exists=True))
@click.option(
    "-c",
    "--chains_with_conversion_included_only",
    default=False,
    is_flag=True,
    help="Whenever use chains with conversion included only",
)
def main(
    impressions_filepath: str,
    events_filepath: str,
    conversions_filepath: str,
    chains_with_conversion_included_only: bool = False,
):
    """Prints top-10 most popular chains. Any chain or conversion tag included only.

    Args:
        impressions_filepath (str): Filepath to impressions.csv
        events_filepath (str): Filepath to events.csv
        conversions_filepath (str): Filepath to conversions.csv
        chains_with_conversion_included_only (bool, optional): 
            Whenever use chains with conversion only. Defaults to False.

    Example:
        >>>python .\chains.py .\impressions.csv .\events.csv .\conversions.csv
        or with flag
        >>>python .\chains.py -c .\impressions.csv .\events.csv .\conversions.csv
    """
    impressions = pd.read_csv(impressions_filepath)
    events = pd.read_csv(events_filepath)
    conversions = pd.read_csv(conversions_filepath)

    def correct_action_type(col: pd.Series) -> pd.Series:
        dict_ = {"tracker": "conversions", "events": "clicks"}

        result = col.replace(dict_)
        return result

    for df in [impressions, events, conversions]:
        df["Action_type"] = correct_action_type(df["Action_type"])

    cols = ["USER_ID", "DH_SERV", "Insertion_ID", "Action_type"]
    df = pd.concat([impressions[cols], events[cols], conversions[cols]])

    df["DH_SERV"] = pd.to_datetime(df["DH_SERV"])

    df["Insertion_ID_and_Action_type"] = (
        df["Insertion_ID"].astype(str) + " " + df["Action_type"]
    )

    result = pd.Series(dtype="object")

    if chains_with_conversion_included_only:
        for _, actions in tqdm(df.groupby("USER_ID")):
            had_conversion = "conversions" in actions["Action_type"].unique()
            if had_conversion:
                actions = actions.sort_values("DH_SERV", kind="stable")
                actions = actions["Insertion_ID_and_Action_type"].str.cat(sep=" -> ")
                result = pd.concat([result, pd.Series(actions)], ignore_index=True)
    else:
        for _, actions in tqdm(df.groupby("USER_ID")):
            actions = actions.sort_values("DH_SERV", kind="stable")
            actions = actions["Insertion_ID_and_Action_type"].str.cat(sep=" -> ")
            result = pd.concat([result, pd.Series(actions)], ignore_index=True)

    print("\n" * 2, "Top 10 chains:", sep="")
    print(result.value_counts().head(10))


if __name__ == "__main__":
    main()
