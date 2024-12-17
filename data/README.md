Download historical quote data from the Nasdaq website, for example: https://www.nasdaq.com/market-activity/stocks/meta/historical.

The CSV files do not include the stocks symbol as a column. To add a symbol column run the `add_symbol.py` Python script.

```bash
python3 -m venv env
source env/bin/activate
(env) pip install -r requirements.txt
(env) python add_symbol.py AAPL_historical_max.csv
(env) head AAPL_historical_max.csv
Symbol,Date,Close/Last,Volume,Open,High,Low
AAPL,12/05/2024,$243.04,40033880,$243.99,$244.54,$242.13
AAPL,12/04/2024,$243.01,44383940,$242.87,$244.11,$241.25
AAPL,12/03/2024,$242.65,38861020,$239.81,$242.76,$238.90
AAPL,12/02/2024,$239.59,48137100,$237.27,$240.79,$237.16
AAPL,11/29/2024,$237.33,28481380,$234.805,$237.81,$233.97
AAPL,11/27/2024,$234.93,33498440,$234.465,$235.69,$233.8101
AAPL,11/26/2024,$235.06,45986190,$233.33,$235.57,$233.33
AAPL,11/25/2024,$232.87,90152830,$231.46,$233.245,$229.74
AAPL,11/22/2024,$229.87,38168250,$228.06,$230.7199,$228.06
```
