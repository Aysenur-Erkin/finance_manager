from tabulate import tabulate

class Reporter:
    def __init__(self, db_manager):
        self.db = db_manager

    def format_summary(self, summary: dict) -> str:
        if not summary:
            return "No summary available."

        rows = [(category, total) for category, total in summary.items()]
        table = tabulate(
            rows,
            headers=["Category", "Total"],
            tablefmt="grid",
            floatfmt=".2f"
        )
        return table

    def ascii_chart(self, summary: dict, width: int = 40) -> str:
        if not summary:
            return ""

        max_value = max(summary.values())
        chart_lines = []
        for category, value in summary.items():
            length = int((value / max_value) * width) if max_value > 0 else 0
            bar = "#" * length
            chart_lines.append(f"{category.ljust(15)} | {bar} {value:.2f}")
        return "\n".join(chart_lines)
