import pandas as pd


class SealedBidAuctions:
    def __init__(
        self,
        bids: pd.DataFrame,
        inventory_qty: int,
        price_sorted_bids: bool = False,
    ) -> None:
        """
        Initialize class with bids and total inventory quantity for auction


        """

        self.__bids = bids
        self.__inventory_qty = inventory_qty

        if not price_sorted_bids:
            self.sort_bids_by_highest_price()

    def sort_bids_by_highest_price(self) -> None:
        """
        Sort bids by highest price
        """
        self.__bids = self.__bids.sort_values(
            by="Price",
            ascending=False,
            inplace=False,
        ).reset_index(drop=True)

    def first_price_sealed(self):
        """
        Bidder with the highest price gets allocated at highest price
        """
        winning_bids = [
            {
                "Quantity": min(
                    self.__bids["Quantity"][0],
                    self.__inventory_qty,
                ),
                "Price": self.__bids["Price"][0],
            }
        ]

        return winning_bids

    def second_price_sealed(self):
        """
        Bidder with the highest price gets allocated at the second highest
        price
        """

        if len(self.__bids) < 2:
            return self.first_price_sealed()

        winning_bids = [
            {
                "Quantity": min(
                    self.__bids["Quantity"][0],
                    self.__inventory_qty,
                ),
                "Price": self.__bids["Price"][1],
            }
        ]

        return winning_bids

    def dutch_auction(self):
        """
        Allocate bids based on price of security, stops when available
        inventory becomes non-positive
        """
        qty = self.__inventory_qty
        bids = self.__bids
        winning_bids = list()
        bid_counter = 0
        while qty > 0 and bid_counter < len(bids):
            curr_bid = bids.iloc[bid_counter]
            curr_qty = min(curr_bid["Quantity"], qty)
            curr_price = curr_bid["Price"]

            qty -= curr_qty
            bid_counter += 1

            winning_bids.append(
                {
                    "Quantity": curr_qty,
                    "Price": curr_price,
                }
            )
        return winning_bids

    def min_price_dutch_auction(self):
        """
        Allocates inventory on the basis of best price then assigns minimum
        price to all winning bids
        """
        winning_bids = self.dutch_auction()
        min_price = winning_bids[-1]["Price"]
        winning_bids = [
            {
                "Quantity": b["Quantity"],
                "Price": min_price,
            }
            for b in winning_bids
        ]
        return winning_bids

    def hybrid_dutch_auction(self):
        """
        Allocates inventory on the basis of best price then assigns weighted
        average price to bids with higher price than weighted average price

        """

        winning_bids = self.dutch_auction()

        price_sum, qty_sum = 0, 0
        for bid in winning_bids:
            price_sum += bid["Quantity"] * bid["Price"]
            qty_sum += bid["Quantity"]

        weighted_average_price = price_sum / qty_sum

        winning_bids = [
            {"Quantity": b["Quantity"], "Price": weighted_average_price}
            if b["Price"] > weighted_average_price
            else b
            for b in winning_bids
        ]

        return winning_bids
