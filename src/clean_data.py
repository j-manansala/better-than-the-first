import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import pandas as pd
import numpy as np

class Process():
    
    def __init__(self, filenames):
        self.filenames = filenames
        
    def groupby_year(self):
        df_merged = self.filenames
        df_merged_per_year = (df_merged.groupby('Year').apply(lambda x: 
                                          x.nlargest(25,'Worldwide Gross')))
        df_merged_per_year = df_merged_per_year.drop(columns="Year")
        df_merged_per_year['Rank'] = (df_merged_per_year
                                     .groupby('Year')['Worldwide Gross']
                                     .rank(method = 'dense', ascending=False))
        df_merged_per_year['Sequel'] = df_merged_per_year['New Count'].isna()
        df_merged_per_year['Sequel'] = (df_merged_per_year['Sequel']
                                        .apply(lambda x: 0 if x else 1))
        return df_merged_per_year
   
    def format_tables(self):
        df_merged = self.filenames
        df_merged['Metascore'] = (df_merged['Metascore']
                                  .apply(lambda x: int(x) if x else None))
        df_merged['Ratings Star'] = (df_merged['Ratings Star']
                                  .apply(lambda x: float(x) if x else None))
        df_merged['Runtime'] = (df_merged['Runtime'].str.replace("min", "")
                                  .apply(lambda x: int(x) if x else None))
        df_merged['Votes'] = (df_merged['Votes'].str.replace(",", "")
                                  .apply(lambda x: int(x) if x else None))
        df_merged[['Currency Budget', 'Budget']] = (df_merged['Budget'].str
                                  .extract(r'(\$|[A-Za-z]{3})([\d, ]*)'))
        df_merged[['Currency Gross', 'Worldwide Gross']] = (df_merged
                                  ['Worldwide Gross'].str
                                  .extract(r'(\$|[A-Za-z]{3})([\d, ]*)'))
        df_merged['Budget'] = (df_merged['Budget'].str.replace(",", "")
                               .apply(lambda x: float(x) if x else x))
        df_merged['Worldwide Gross'] = (df_merged['Worldwide Gross']
                                   .str.replace(",", "")
                                   .apply(lambda x: float(x) if x else x))
        df_merged['New Count'] = (df_merged.groupby('Movie Series')['Movie']
                                  .transform('count'))
        df_merged['Movie Series'] = df_merged['Movie Series'].str.strip()
        df_merged['Genre'] = df_merged['Genre'].str.split()
        currency = pd.Series({'$':1, 'GBP': 1.23, 'EUR':1.12, 'CAD':0.73, 
                              'FRF':0.1704, 'INR':0.013, 'SEK':0.11, 
                              'HUF':0.0032, 'ZAR':0.058, 'NZD':0.65, 
                              'NGN':0.0026, 'VEB':0.0005, 'ARS':0.0014, 
                              'TRL':0.15, 'TWD':0.034, 'MYR':0.23, 
                              'AZM':0.59, 'GHC':0.17, 'NPR':0.0083, 
                              'AED':0.27, 'HRK':0.15, 'IRR': 0.000024, 
                              'UAH':0.038, 'IDR':0.00071, 'LKR':0.0054,
                              'BGL':0.58, 'MKD':0.018, 'KES':0.0094,
                              'THB':0.032, 'AUD':0.68, 'DEM':0.001111, 
                              'CNY':0.14, 'HKD':0.13, 'ITL':0.0005773, 
                              'RUR': 0.014, 'BEF':0.03, 'PLN':0.25,
                              'JPY':0.0094, 'MXN':0.044, 'KRW':0.00083, 
                              'ATS':0.08, 'ESP':1.12, 'CHF':1.05, 
                              'ISK':0.0073, 'PHP':0.020, 'JMD':0.0072, 
                              'ILS':0.29, 'IEP':1.44, 'NOK':0.10, 
                              'DKK':0.15, 'BRL':0.15, 'FIM':0.19, 
                              'CZK':0.042, 'SGD':0.72, np.nan: 0})
        df_merged['Currency Budget'] = (df_merged['Currency Budget']
                                        .replace(np.nan, "$"))
        df_merged['Budget'] = (df_merged['Budget'] *
                               df_merged['Currency Budget']
                               .transform(lambda x: currency[x]))
        df_merged['Currency Gross'] = (df_merged['Currency Gross']
                                       .replace(np.nan, "$"))
        df_merged['Worldwide Gross'] = (df_merged['Worldwide Gross'] * 
                                        df_merged['Currency Gross']
                                        .transform(lambda x: currency[x]))   
        return df_merged
    
    def group_by_series(self):
        df_sequels = self.filenames
        list_sequels = list(df_sequels['Movie Series'].unique())
        movie_first = []
        movie_mids = []
        movie_finale = []
        for movie_series in list_sequels:
            grouped = (df_sequels.groupby('Movie Series')
                       .get_group(movie_series).sort_values("Year"))
            grouped['Order'] = grouped["Year"].rank(method="min")
            if len(grouped) ==2:
                for i in range(len(grouped)):
                    data = ([((grouped.iloc[i]['Ratings Star']*10 
                               + grouped.iloc[i]['Metascore'])/2), 
                            (grouped.iloc[i]['Worldwide Gross']/
                             grouped.iloc[i]['Budget'])])
                    if i == 0: 
                        data = ([((grouped.iloc[i]['Ratings Star']*10 
                                   + grouped.iloc[i]['Metascore'])/2), 
                                (grouped.iloc[i]['Worldwide Gross']/
                                 grouped.iloc[i]['Budget']) 
                                 if (grouped.iloc[i]['Worldwide Gross']/
                                   grouped.iloc[i]['Budget']) <100 else 100])
                        movie_first.append(data)
                    else:
                        movie_finale.append(data)
            elif len(grouped) ==3:
                for i in range(len(grouped)):
                    data = ([((grouped.iloc[i]['Ratings Star']*10 
                               + grouped.iloc[i]['Metascore'])/2), 
                            (grouped.iloc[i]['Worldwide Gross']/
                             grouped.iloc[i]['Budget'])])
                    if i == 0: 
                        data = ([((grouped.iloc[i]['Ratings Star']*10 
                                   + grouped.iloc[i]['Metascore'])/2), 
                                (grouped.iloc[i]['Worldwide Gross']/
                                 grouped.iloc[i]['Budget']) 
                                 if (grouped.iloc[i]['Worldwide Gross']/
                                   grouped.iloc[i]['Budget']) <100 else 100])
                        movie_first.append(data)
                    elif i == len(grouped)-1:
                        movie_finale.append(data)
                    else:
                        movie_mids.append(data)
            elif len(grouped) >3 and len(grouped) <=6:
                for i in range(len(grouped)):
                    data = ([((grouped.iloc[i]['Ratings Star']*10 
                               + grouped.iloc[i]['Metascore'])/2), 
                            (grouped.iloc[i]['Worldwide Gross']/
                             grouped.iloc[i]['Budget'])])
                    if i == 0:
                        data = ([((grouped.iloc[i]['Ratings Star']*10 
                                   + grouped.iloc[i]['Metascore'])/2), 
                                (grouped.iloc[i]['Worldwide Gross']/
                                 grouped.iloc[i]['Budget']) 
                                 if (grouped.iloc[i]['Worldwide Gross']/
                                   grouped.iloc[i]['Budget']) <100 else 100])
                        movie_first.append(data)
                    elif i == len(grouped)-1:
                        movie_finale.append(data)
                    else:
                        movie_mids.append(data)
            elif len(grouped) >=7 and len(grouped) <10:
                for i in range(len(grouped)):
                    data = ([((grouped.iloc[i]['Ratings Star']*10 
                               + grouped.iloc[i]['Metascore'])/2), 
                            (grouped.iloc[i]['Worldwide Gross']/
                             grouped.iloc[i]['Budget'])])
                    if i == 0 or i == 1:
                        data = ([((grouped.iloc[i]['Ratings Star']*10 
                                   + grouped.iloc[i]['Metascore'])/2), 
                                (grouped.iloc[i]['Worldwide Gross']/
                                 grouped.iloc[i]['Budget']) 
                                 if (grouped.iloc[i]['Worldwide Gross']/
                                   grouped.iloc[i]['Budget']) <100 else 100])
                        movie_first.append(data)
                    elif i == len(grouped)-1 or i == len(grouped)-2:
                        movie_finale.append(data)
                    else:
                        movie_mids.append(data)
            elif len(grouped) >=10:
                for i in range(len(grouped)):
                    data = ([((grouped.iloc[i]['Ratings Star']*10 
                               + grouped.iloc[i]['Metascore'])/2), 
                            (grouped.iloc[i]['Worldwide Gross']/
                             grouped.iloc[i]['Budget'])])
                    if i == 0 or i == 1 or i==2:
                        data = ([((grouped.iloc[i]['Ratings Star']*10 
                                   + grouped.iloc[i]['Metascore'])/2), 
                                (grouped.iloc[i]['Worldwide Gross']/
                                 grouped.iloc[i]['Budget']) 
                                 if (grouped.iloc[i]['Worldwide Gross']/
                                   grouped.iloc[i]['Budget']) <100 else 100])
                        movie_first.append(data)
                    elif (i == len(grouped)-1 or i == len(grouped)-2 
                          or i == len(grouped)-3):
                        movie_finale.append(data)
                    else:
                        movie_mids.append(data)
        movie_first = (pd.DataFrame(movie_first)
                   .rename(columns={0:'Audience Scores', 1:'Profitability'})
                   .dropna())
        movie_mids = (pd.DataFrame(movie_mids)
                   .rename(columns={0:'Audience Scores', 1:'Profitability'})
                   .dropna())
        movie_finale = (pd.DataFrame(movie_finale)
                    .rename(columns={0:'Audience Scores', 1:'Profitability'})
                    .dropna()) 
        return movie_first, movie_mids, movie_finale
    