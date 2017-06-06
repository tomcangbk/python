import pandas as pd
from emoji import emojize
list_emj = [':car:',':horse:', ':dog:', ':chicken:', ':ship:']
em = "".join(str(x) for x in list_emj)
a = (emojize(em, use_aliases=True))
