import pandas as pd
import altair as alt

alt.renderers.enable('jupyterlab')

data = pd.DataFrame()
data['from'] = [dt.datetime(2018, 7, 17, 0, 15),
             dt.datetime(2018, 7, 17, 0, 30),
             dt.datetime(2018, 7, 17, 0, 45), 
             dt.datetime(2018, 7, 17, 1, 0), 
             dt.datetime(2018, 7, 17, 1, 15), 
             dt.datetime(2018, 7, 17, 1, 30)]
data['to'] = [dt.datetime(2018, 7, 17, 0, 30),
             dt.datetime(2018, 7, 17, 0, 45),
             dt.datetime(2018, 7, 17, 1, 0), 
             dt.datetime(2018, 7, 17, 1, 15), 
             dt.datetime(2018, 7, 17, 1, 30), 
             dt.datetime(2018, 7, 17, 1, 45)]
data['activity'] = ['sleep','eat','work','sleep','eat','work']
#data

alt.Chart(data).mark_bar().encode(
    x='from',
    x2='to',
    y='activity',
    color=alt.Color('activity', scale=alt.Scale(scheme='dark2'))
)
