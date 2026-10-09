class Reporter:
    def __init__(self, db_manager):
        self.db = db_manager

    def report(self, period: str):
        summary = self.db.get_summary(period=period)
        total = sum(summary.values())
        rows = []
        for category, amount in sorted(summary.items(), key=lambda item: item[1], reverse=True):
            share = amount / total * 100 if total else 0
            rows.append((category, amount, share))
        return rows, total
