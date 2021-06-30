from dash_core_components.Dropdown import Dropdown
from neo4j import GraphDatabase
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
import datetime
import json
from dash.dependencies import Input, Output

external_stylesheets = ["https://gistcdn.githack.com/rdas3/a210f167998bb6d572e84f99800490d5/raw/566623e9e29c9ba25c599f7b75c9bfb9cf410821/style.css"]
app=dash.Dash(__name__,update_title="please wait",external_stylesheets=external_stylesheets)
app.title="football dashboard"

driver=GraphDatabase.driver(uri="bolt://localhost:7687",auth=("neo4j","Rambo@1234"))
session=driver.session()

q1="""
match(m:Game)-[:PLAYED_ON]->(ci:City)<-[:HAS]-(c:Country) return c.Name as name ,count(m) as count
"""
q2="""
match(m:Game)-[:PLAYED_ON]->(ci:City)<-[:HAS]-(c:Country{Name:"Germany"}) return m.Name as name ,count(m) as count
"""
result_total=session.run(q1)
li_total=[{"Name":row["name"],"Count":row["count"]}for row in result_total]
df_total=pd.DataFrame(li_total)
df_total=df_total.sort_values("Count",ascending=False)
fig1=px.bar(df_total.head(20),x="Name",y="Count",color="Name",barmode="group")
fig1.update_xaxes(showgrid=True,gridcolor="black",gridwidth=1)
fig1.update_yaxes(showgrid=True,gridcolor="black",gridwidth=1)
for data in fig1.data:
    data["width"]=.5
fig1.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="black",
    font_family="Arial Black",
    height=500,
    title_font_color="black"


)
x=df_total["Name"].values
label=[]
for xx in x:
    label.append({"label":xx,"value":xx})
result_tournament=session.run(q2)
li_tournament=[{"Name":row["name"],"Count":row["count"]}for row in result_tournament]
df_tournament=pd.DataFrame(li_tournament)
df_tournament=df_tournament.sort_values("Count",ascending=False)
fig2=px.bar(df_tournament,x="Name",y="Count",color="Name",barmode="group")
fig2.update_xaxes(showgrid=True,gridcolor="black",gridwidth=1)
fig2.update_yaxes(showgrid=True,gridcolor="black",gridwidth=1)
for data in fig2.data:
    data["width"]=.5
fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="black",
    font_family="Arial Black",
    height=500,
    title_font_color="black"
)


app.layout=html.Div(id="page-content",children=[
    html.Div([
        html.Div([
            html.Div(id="app1",children="football dashboard"),
            html.Br(),
            dcc.Graph(
                id="fig1",
                figure=fig1

            ),


        ],style={"width":"100%","textAlign":"center","fontSize":20})

    ], className="row"),

    html.Div([
        html.Div([
            html.Div(id="app2",children="football tournament dashboard"),
            html.Br(),
            dcc.Dropdown(
                id="country",
                options=label,
                value="Germany",
                multi=False,
                clearable=False
            ),
            dcc.Graph(
                id="fig2",
                figure=fig2

            ),


        ],style={"width":"100%","textAlign":"center","fontSize":20})

    ], className="row")



    

]
)
@app.callback(
    Output("fig2",'figure'),
    Input("country","value"))
def render(value):
    x={"param":value}
    q2="""
    match(m:Game)-[:PLAYED_ON]->(ci:City)<-[:HAS]-(c:Country{Name:$param}) return m.Name as name ,count(m) as count
    """
    result_tournament=session.run(q2,x)
    li_tournament=[{"Name":row["name"],"Count":row["count"]}for row in result_tournament]
    df_tournament=pd.DataFrame(li_tournament)
    df_tournament=df_tournament.sort_values("Count",ascending=False)
    fig2=px.bar(df_tournament,x="Name",y="Count",color="Name",barmode="group")
    fig2.update_xaxes(showgrid=True,gridcolor="black",gridwidth=1)
    fig2.update_yaxes(showgrid=True,gridcolor="black",gridwidth=1)
    for data in fig2.data:
        data["width"]=.5
    fig2.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font_color="black",
    font_family="Arial Black",
    height=500,
    title_font_color="black"
)
    return (fig2)


if __name__=="__main__":
    app.run_server(host="0.0.0.0",port=8066)

