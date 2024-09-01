
import datetime
from matplotlib import pyplot as plt
import japanize_matplotlib
import pandas as pd
import seaborn as sns

fortravel = pd.read_csv('fortravel_flavor_texture.csv',header = 0 ,encoding='cp932', parse_dates=['date'])
fortravel['total'] = fortravel.iloc[:,18:].sum(axis=1)
fortravel['date'] = fortravel['date'].dt.month

fig, axes = plt.subplots(1, figsize=(20,5))

 

flavor = fortravel[fortravel['keyword']=='flavor']



flavor_season = flavor.groupby('date').sum()


flavor_season_words = flavor_season.iloc[:,18:-1]
flavor_season_words


def on_button_press( event):


    
    print(event.xdata)
    

    word_vec = flavor_season_words.iloc[int(event.xdata),:]
    word_vec = word_vec.sort_values(ascending=False)
    text = word_vec[:5].index.tolist()
    text = ','.join(text)
    print(text)

    plt.clf()
    
    #fig, axes = plt.subplots(1, figsize=(20,5))
    axes = fig.add_subplot(1, 1, 1)
    sns.lineplot(data=flavor_season[['total']],ax=axes)
    axes.text(float(event.xdata), float(event.ydata),text, size=10)
    axes.legend(loc='lower left')
    axes.set_title("flavor")

    plt.xticks()    
    plt.pause(1)

fig = plt.figure(figsize=(14, 6))
axes = fig.add_subplot(1, 1, 1)

#fig, axes = plt.subplots(1, figsize=(20,5))

sns.lineplot(data=flavor_season[['total']],ax=axes)
fig.canvas.mpl_connect('button_press_event', on_button_press)
axes.legend(loc='lower left')
axes.set_title("flavor")



plt.xticks()
plt.show()