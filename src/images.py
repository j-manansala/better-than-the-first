import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import pandas as pd
import seaborn as sns

class Show_figures():
    
    def __init__(self, filenames):
        self.filenames = (filenames.set_index("Movie")
                          .sort_values("Year", ascending=True))
    
    def scatter_plot(self):
        df_merged = self.filenames
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,5))
        ax[0].scatter(x = [], y = [])
        for x in [0,1]:
            ax[x].set_xlim(0,20)
            ax[x].set_ylim(0,100)
            ax[x].set_yticks(range(0,101,25))
            ax[x].axhline(50, ls ='--', c='black', lw="0.7")
            ax[x].axvline(10, ls ='--', c='black', lw="0.7")
            ax[x].axvline(1, ls ='--', c='red', lw="1")
            ax[x].set_title("Profitability vs. Audience Score")

        ax[0].text(1.5,50,'Breakeven',style='italic', 
                   bbox={'facecolor': 'pink'})
        ax[0].text(13,75,'Higher Profits,\n High Ratings',style='italic', 
                   bbox={'facecolor': 'lightblue'})
        ax[0].text(3,75,'Profitable,\n High Ratings',style='italic', 
                   bbox={'facecolor': 'lightblue'})
        ax[0].text(13,20,'Higher Profits,\n Low Ratings',style='italic', 
                   bbox={'facecolor': 'lightblue'})
        ax[0].text(3,20,'Profitable,\n Low Ratings',style='italic', 
                   bbox={'facecolor': 'lightblue'});

        sample = df_merged[df_merged.index=='Avatar']
        audience = (sample['Ratings Star']*10 + sample['Metascore'])/2
        profitability = sample['Worldwide Gross']/sample['Budget']
        ax[1].scatter(x = profitability, y = audience)
        ax[1].annotate(xy =(profitability, audience),s=sample.index[0]);

        sample = df_merged[df_merged.index=='A Quiet Place']
        audience = (sample['Ratings Star']*10 + sample['Metascore'])/2
        profitability = sample['Worldwide Gross']/sample['Budget'] - 0.5
        ax[1].scatter(x = profitability, y = audience)
        ax[1].annotate(xy =(profitability, audience),s=sample.index[0]);

        sample = df_merged[df_merged.index=='Escape Room']
        audience = (sample['Ratings Star']*10 + sample['Metascore'])/2
        profitability = sample['Worldwide Gross']/sample['Budget'] 
        ax[1].scatter(x = profitability, y = audience)
        ax[1].annotate(xy =(profitability, audience),s=sample.index[0]);

        sample = df_merged[df_merged.index=='Space Jam']
        audience = (sample['Ratings Star']*10 + sample['Metascore'])/2
        profitability = sample['Worldwide Gross']/sample['Budget']
        ax[1].scatter(x = profitability, y = audience)
        ax[1].annotate(xy =(profitability, audience),s=sample.index[0]);
        ax[0].set_xlabel("Profitability Ratio")
        ax[0].set_ylabel("Audience Scores") 
        ax[1].set_xlabel("Profitability Ratio")
        ax[1].set_ylabel("Audience Scores")  
        plt.tight_layout()
        return ax
    
    def poster(self):
        poster = self.filenames['Poster']
        if len(poster) <=4:
            fig,ax = plt.subplots(1,len(poster)+2, figsize=(20,3))
            for i, link in enumerate(poster):
                response = requests.get(link)
                img = Image.open(BytesIO(response.content))
                ax[i+1].imshow(img)
                ax[i+1].axis('off')
                ax[i+1].set_title(self.filenames['Year'][i])
            ax[0].axis('off')
            ax[len(poster)+1].axis('off')
            return ax        
        
        if len(poster) >=5:
            fig,ax = plt.subplots(1,len(poster), figsize=(20,3))
            for i, link in enumerate(poster):
                response = requests.get(link)
                img = Image.open(BytesIO(response.content))
                ax[i].imshow(img)
                ax[i].axis('off')
                ax[i].set_title(self.filenames['Year'][i])
            return ax
    
    def plots(self):
        df_show = self.filenames.set_index("Year")
        fig,ax = plt.subplots(1,3, figsize=(20,5))
        ((df_show["Ratings Star"]*10 + 
                  df_show["Metascore"])/2).plot.line(ax=ax[0], style=['o-'])
        (df_show[["Worldwide Gross", 
                  "Budget"]].plot.line(ax=ax[1], style=['o-']))
        ax[0].set_ylim(0,100)
        (ax[1].set_yticklabels([str(int(x)/1_000_000) + "M" for x in ax[1]
                                .get_yticks().tolist()]))
        
        profitability = df_show["Worldwide Gross"] / df_show["Budget"]
        updated_profitability = [x if x<=20 else 20 for x in profitability]
        audience_respose = ((df_show["Ratings Star"]*10 + 
                             df_show["Metascore"])/2)
        color = ['r'] + ['b'] * (len(df_show)-1)
        ax[2].scatter(x = updated_profitability, y = audience_respose, 
                      c = color)
        ax[2].set_xlim(0,20)
        ax[2].set_ylim(0,100)
        ax[0].set_xlabel("Year")
        ax[0].set_ylabel("Audience Scores")        
        ax[1].set_xlabel("Year")
        ax[1].set_ylabel("Profitability Ratio")        
        ax[2].set_xlabel("Profitability Ratio")
        ax[2].set_ylabel("Audience Scores")  
        
        movie_list = list(df_show.index)
        for idx, label in enumerate(movie_list):
            ax[2].annotate(label, (updated_profitability[idx], 
                                   audience_respose[idx]))

        ax[0].set_title("Trend of Audience Scores")
        ax[1].set_title("Trend of Worldwide Gross")
        ax[2].set_title("Profitability vs. Audience Scores");
        ax[2].axvline(10, ls="--", lw="1", c="grey")
        ax[2].axhline(50, ls="--", lw="1", c="grey")
        ax[2].axvline(1, ls ='--', c='red', lw="1")
        ax[2].set_yticks(range(0,101,25))
        plt.tight_layout()
        return ax
    
class Show_template():    
    
    def prof_vs_scores(self):
        string = "Movie Sequels"
        index_names = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 
                       'Eight', 'Nine', 'Ten', 'More']
        index_names = [x + " " + string for x in index_names]
        a, b, c = 1, 2, 3
        row1 = {0: a, 1: c}
        row2 = {0: a, 1: b, 2: c}
        row3 = {0: a, 1: b, 2: b, 3: c}
        row4 = {0: a, 1: b, 2: b, 3: b, 4:c}
        row5 = {0: a, 1: b, 2: b, 3: b, 4:b, 5: c}
        row6 = {0: a, 1: a, 2: b, 3: b, 4:b, 5: c, 6:c }
        row7 = {0: a, 1: a, 2: b, 3: b, 4:b, 5: b, 6:c , 7:c, }
        row8 = {0: a, 1: a, 2: b, 3: b, 4:b, 5: b, 6:b , 7:c, 8:c}
        row9 = {0: a, 1: a, 2: a, 3: b, 4:b, 5: b, 6:b , 7:c, 8:c, 9: c}
        row10 = {0: a, 1: a, 2: a, 3: b, 4:b, 5: b, 6:b , 7:b, 8:c, 9: c, 
                 10: c}
        cmap = sns.color_palette("Paired", 5 ) 
        return sns.heatmap(pd.DataFrame([row1, row2, row3, row4, row5, row6, 
                    row7, row8, row9, row10], index=index_names), 
                    cmap=cmap, cbar=None, xticklabels=['1st', '2nd', '3rd', 
                                                       '4th', '5th', '6th', 
                                                       '7th', '8th', '9th', 
                                                       '10th', '11th']);
        
        