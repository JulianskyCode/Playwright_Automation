class TransactionsPage:
    def __init__(self, page):
        self.page = page

    def get_transactions(self):
        """Retrieve the list of transactions as a list of dictionaries."""
        rows = self.page.locator("table#transactions tbody tr").all()
        transactions = []
        for row in rows:
            date = row.locator("td").nth(0).inner_text().strip()
            amount = row.locator("td").nth(1).inner_text().strip()
            type_ = row.locator("td").nth(2).inner_text().strip()
            transactions.append({"date": date, "amount": amount, "type": type_})
        return transactions

    def sort_by_date(self):
        """Click the date header to sort transactions by date."""
        self.page.click("th#dateHeader")
        