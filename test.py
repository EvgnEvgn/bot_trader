import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ArbitrageTradingAlgorithm as ATA
import os
import json
from CurrencyPair import CurrencyPair
from TradingAnalyzeException import TradingAnalyzeException
import ArbitrageTradingAlgorithm as ATA
from config import BinanceConfig
import dateparser as dp

x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=lambda kv: print(kv))
print(sorted_x)