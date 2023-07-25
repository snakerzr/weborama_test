import click
import pandas as pd


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath: str, output_filepath: str) -> None:
    """Counts number and fraction for each answer in each columns including NaNs
    except first 2 with dates and saves it in a file.

    Args:
        input_filepath (str): Filepath to xlsx file with data.
        output_filepath (str): Filepath for a new file.

    Example:
        >>>python ./xlsx_value_counts.py "Тестовое.xlsx" "result.csv"
        result.csv created
    """
    xls = pd.read_excel(input_filepath)

    xls = xls.iloc[:, 2:]

    result = pd.DataFrame()

    for i in range(len(xls.columns)):
        temp_1 = xls.iloc[:, i].value_counts(dropna=False)
        temp_2 = xls.iloc[:, i].value_counts(normalize=True, dropna=False)
        col_name = temp_1.name

        temp_3 = pd.concat([temp_1, temp_2], axis=1)
        temp_3.columns = ["count", "frac"]
        temp_3 = pd.concat([temp_3], keys=[col_name], names=["col_name"])
        result = pd.concat([result, temp_3], axis=0)

    result.index.names = ["col_name", "answer"]

    result.to_csv(output_filepath)
    print(output_filepath, "created")


if __name__ == "__main__":
    main()
