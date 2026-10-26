import tempfile
import unittest
from pathlib import Path

import pandas as pd
from tobacco_data import load_data, MEASURES
from tobacco_analysis_dashboard import create_app


class DashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "sample.csv"
        rows = []
        for i, state in enumerate(["NY", "KY", "CT", "CA", "TX", "WA"]):
            for year in range(1989, 2020):
                values = [100 + i * 8 - (year - 1989), .3 + i * .1, .8 + i * .1, 20, 4, 1000]
                for name, value in zip(MEASURES, values):
                    rows.append(dict(LocationAbbr=state, Year=year, SubMeasureDesc=name, Data_Value=value))
        self.raw = pd.DataFrame(rows)
        self.raw.to_csv(self.path, index=False)

    def test_pivot_filter_and_tax_shares(self):
        df = load_data(self.path)
        self.assertEqual(len(df), 180)
        self.assertEqual(df.Year.min(), 1990)
        self.assertEqual(df.Year.max(), 2019)
        ny = df.loc[df.state == "NY"].iloc[0]
        self.assertAlmostEqual(ny.state_tax_pct, .075)
        self.assertAlmostEqual(ny.federal_tax_pct, .125)
        self.assertAlmostEqual(ny.total_tax_pct, .2)

    def test_duplicate_rejected(self):
        pd.concat([self.raw, self.raw.iloc[[6]]]).to_csv(self.path, index=False)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            load_data(self.path)

    def test_missing_measure_rejected(self):
        self.raw.drop(index=6).to_csv(self.path, index=False)
        with self.assertRaisesRegex(ValueError, "Missing measures"):
            load_data(self.path)

    def test_invalid_price_rejected(self):
        self.raw.loc[self.raw.SubMeasureDesc == "Average Cost per pack", "Data_Value"] = 0
        self.raw.to_csv(self.path, index=False)
        with self.assertRaisesRegex(ValueError, "Prices"):
            load_data(self.path)

    def test_all_tabs_and_themes(self):
        app = create_app(self.path)
        for theme in ["Light", "Dark"]:
            for n in range(1, 8):
                with self.subTest(theme=theme, tab=n):
                    self.assertIsNotNone(app.render_tab(f"tab{n}", theme))
            fig = app.compare_states("NY", "KY", theme)
            self.assertEqual(len(fig.data), 2)
            self.assertEqual(len(fig.data[0].x), 30)
        client = app.server.test_client()
        for url in ["/", "/_dash-layout", "/_dash-dependencies"]:
            self.assertEqual(client.get(url).status_code, 200)


if __name__ == "__main__":
    unittest.main()
