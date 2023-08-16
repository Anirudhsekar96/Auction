import pandas as pd


class Bids:
    def __init__(self):
        """
        Initializes class to store bids
        """
        self.__bids = list()

    def add_bid(self, user_name: str, qty: int, price: int) -> None:
        """
        Adds bids to the auction
        """
        self.__bids.append((user_name, qty, price))

    def get_bids(self) -> pd.DataFrame:
        """
        Returns current bids at auction
        """
        bids_df = pd.DataFrame(
            self.__bids,
            columns=["User", "Quantity", "Price"],
        )
        return bids_df

    def get_bids_sorted_by_price(self) -> pd.DataFrame:
        """
        Returns current bids at auction sorted on price
        """
        bids_df = self.get_bids()
        bids_df = bids_df.sort_values(
            by="Price",
            ascending=False,
            inplace=False,
        ).reset_index(drop=True)
        return bids_df

    def get_price_levels(self) -> pd.DataFrame:
        """
        Returns the quantity at each price level sorted on highest price first
        """
        price_levels = self.get_bids()
        price_levels = price_levels.groupby("Price")["Quantity"].sum()
        price_levels = price_levels.reset_index(drop=False, inplace=False)
        price_levels = price_levels.sort_values(
            by="Price",
            ascending=False,
            inplace=False,
        )
        price_levels = price_levels.reset_index(drop=True, inplace=False)

        return price_levels
