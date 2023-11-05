import numpy as np
import pandas as pd
import datetime as dt
import pendulum as pen
from icecream import ic
import time

import tensorflow as tf
from tensorflow_hub import hub


embader = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

ic("Done")

quit()
import dash
from dash import Dash, html, dcc, callback, Output, Input, State, dash_table

import dash_bootstrap_components as dbc

data = pd.read_csv("data/content_data/not_na_data_price.csv")
not_na_df = pd.read_csv("data/content_data/full_not_na_data.csv")


# print(data.shape)
# data.dropna(inplace=True)

# print(data.shape)

data[['lower_country','lower_location','lower_city','lower_state']] = data[['Country','Location','City','State']].apply(lambda x: x.str.lower())
data['location_list'] = data['lower_location'].apply(lambda x: list(map(str.strip,x.split(","))))

    

# print(data[['lower_country','lower_location','lower_city','lower_state']].head(2))
 

sections = data['Section'].unique().tolist()
countries = data['Country'].unique().tolist()
cities = data['City'].unique().tolist()
states = data['State'].unique().tolist()
host_level = data['HostLevel'].unique().tolist()

max_price,min_price,median_price = data['CurrentPrice'].max(),data['CurrentPrice'].min(),data['CurrentPrice'].median()
max_nguest,min_nguest,median_nguest = data['NumberOfGuest'].max(),data['NumberOfGuest'].min(),data['NumberOfGuest'].median()
max_bedrooms,min_bedrooms,median_bedrooms = data['NumberOfBedrooms'].max(),data['NumberOfBedrooms'].min(),data['NumberOfBedrooms'].median()
max_beds,min_beds,median_beds = data['NumberOfBeds'].max(),data['NumberOfBeds'].min(),data['NumberOfBeds'].median()
max_baths,min_baths,median_baths = data['NumberOfBaths'].max(),data['NumberOfBaths'].min(),data['NumberOfBaths'].median()

max_bedrooms,max_beds= max_bedrooms+10,max_beds+10

# all types of accomodataion

accomodation_types = data['Section'].unique().tolist()


data.index = list(range(len(data)))
app = Dash()



tabs = dcc.Tabs([
    dcc.Tab(id='welcome-page',label='Welcome',value='welcome'),
    dcc.Tab(id='simple-flter-page',label='Constraint-based',value='simple-filter'),
    dcc.Tab(id='advanced-filter-page',label='Case-based',value='advaneced-filter')

    ],
    id = 'tabs',
    value='advaneced-filter')

# app.server()


welcome_page_div = html.Div([

])
# ----------------------------------------------------------------------------FILTER DIV---------------------------------------------------------------------------------------------
simple_filter_div = html.Div([


            html.Div([

                html.Div([
                    html.Div([

                        html.H3("Location")

                    ]),

                    html.Div([
                        dcc.Input(id='country-search',
                                type='text',name="Location",
                                placeholder='Enter country/state/city',
                                style={'display':'inline-block', 'border': '1px solid black',
                                       "width":"170px",
                                       "height":"30px"}),

                    ])
                ]),


                html.Div([
                    html.Div([

                        html.H3("Type")

                    ]),

                    html.Div([
                        dcc.Dropdown(id='accomodation-type',
                                     clearable=True,options=accomodation_types,multi=True,searchable=True,placeholder='Beach',
                                style={'border': '1px solid black',"width":"170px"}),
                    ])
                ]),


                html.Div([

                    html.Div([
                        html.H3("Price (USD)")
                    ]),

                    html.Div([

                        dbc.Row([

                            dbc.Col([
                                dcc.Input(type='number',id='price-from',min=0,max=10000,placeholder='min price',
                                          style={"width":"150px","height":"20px"}),

                            ],
                            width=1),
                            dbc.Col([
                                dcc.Input(type='number',id='price-to',min=0,max=10000,placeholder='max price',
                                          style={"width":"150px","height":"20px"})                      
                            ])
                        ]),
                    ]),
                ]),


                html.Div([

                    html.Div([
                        html.H3("Number of guests")
                    ]),

                    html.Div([

                        dbc.Row([

                            dbc.Col([
                                dcc.Input(type='number',id='guest-from',min=0,max=10000,placeholder='min guests',
                                          style={"width":"150px","height":"20px"}),

                            ]),
                            dbc.Col([
                                dcc.Input(type='number',id='guest-to',min=0,max=10000,placeholder='max guests',
                                          style={"width":"150px","height":"20px"})                      
                            ])
                        ]),
                    ])
                ]),


                html.Div([

                    html.Div([
                        html.H3("Number of bedrooms")
                    ]),

                    html.Div([
                        dbc.Row([

                            dbc.Col([
                                dcc.Input(type='number',id='bedrooms-from',min=0,max=10000,placeholder='min bedrooms',
                                          style={"width":"150px","height":"20px"}),

                            ]),
                            dbc.Col([
                                dcc.Input(type='number',id='bedrooms-to',min=0,max=10000,placeholder='max bedrooms',
                                          style={"width":"150px","height":"20px"})                      
                            ])
                        ])
                    ])
                ]),


                html.Div([

                    html.Div([
                        html.H3("Number of beds")
                    ]),

                    html.Div([
                        dbc.Row([

                            dbc.Col([
                                dcc.Input(type='number',id='beds-from',min=0,max=10000,placeholder='min beds',
                                          style={"width":"150px","height":"20px"}),

                            ]),
                            dbc.Col([
                                dcc.Input(type='number',id='beds-to',min=0,max=10000,placeholder='max beds',
                                          style={"width":"150px","height":"20px"})                      
                            ])
                        ])
                    ])
                ]),


                html.Div([

                    html.Div([
                        html.H3("Number of baths")
                    ]),

                    html.Div([
                        dbc.Row([

                            dbc.Col([
                                dcc.Input(type='number',id='baths-from',min=0,max=10000,placeholder='min baths',
                                          style={"width":"150px","height":"20px"}),
                            ]),

                            dbc.Col([
                                dcc.Input(type='number',id='baths-to',min=0,max=10000,placeholder='max baths',
                                          style={"width":"150px","height":"20px"})                      
                            ])
                        ])
                    ])    
                ]),


                html.Div([

                    html.Br(),
                    html.Div([
                        html.Button('Serch',id='submit-country-search',n_clicks=0,
                                    style={"width":"160px","height":"30px","backgroundColor":"blue","bold":True}),
                    ])
                ]),

        ],
        style={"display":"10%"}
        
        ),

            html.Div([
            
        ],
        id = 'search-result',
        style={'display':"90%"}
        ),
    ],
    style={"display":"flex"}

)
# ----------------------------------------------------------------------------FILTER DIV---------------------------------------------------------------------------------------------


advanced_filter_div = html.Div([

    html.Div([
        html.Div([
            dbc.Textarea(id='enter-item-description',
                  size='lg',
                  placeholder='Description',
                  rows=10,
                  style={"marginRight":"100px","marginLeft":"100px",
                         "marginTop":"100px","width":"400px","height":"200px"})
        ],
        # style={"flex":"90%"}
        ),

        html.Div([
          dbc.Col([
              dbc.Row([
                  dbc.Input(type='number',placeholder='100',id='case-based-price')
                  
              ]),
              dbc.Row([
                  
              ]),
              dbc.Row([
                  
              ])
          ])  
        ],
        # style={"flex":"10%"}
        )
        
    ],style={"display":"flex"}
    )
])

# ddiv = html.Div(['Display children'])
app.layout = html.Div([


    html.Div([
        dbc.Row([
            dbc.Col(html.Div("KNOWLEDGE-BASED RECOMMENDER SYSTEMS",
                            style={'fontSize': 50, 'textAlign': 'center'}))
        ]),
        tabs
    ]),



    html.Div([

        welcome_page_div   
    ],
    id = 'welcome-page-div',
    style = {"display":"none"}
    ),

    html.Div([

        simple_filter_div

    ],
    id = 'simple-filter-div',
    style = {"display":"none"}
    ),

    html.Div([
        advanced_filter_div
    ],
    id='advanced-filter-div',
    style={"display":"none"}
    )
])




@callback(
        [Output(component_id='welcome-page-div',component_property='style'),
        Output(component_id='simple-filter-div',component_property='style'),
        Output(component_id='advanced-filter-div',component_property='style')],
        Input(component_id='tabs',component_property='value')
)
def start_filter(tab):

    if tab == 'welcome':
        return {"display":"block"},{"display":"none"},{"display":"none"}

    if tab == 'simple-filter':

        return {"display":"none"},{"display":"block"},{"display":"none"}
    
    else:
        return {"display":"none"},{"display":"none"},{"display":"block"}
                # {"display":"none"}]
    


@callback(
    Output(component_id='search-result',component_property='children'),
    Input(component_id='submit-country-search',component_property='n_clicks'),
    State(component_id='country-search',component_property='value'),
    Input(component_id='price-from',component_property='value'),
    Input(component_id='price-to',component_property='value'),
    Input(component_id='guest-from',component_property='value'),
    Input(component_id='guest-to',component_property='value'),
    Input(component_id='beds-from',component_property='value'),
    Input(component_id='beds-to',component_property='value'),
    Input(component_id='bedrooms-from',component_property='value'),
    Input(component_id='bedrooms-to',component_property='value'),
    Input(component_id='baths-from',component_property='value'),
    Input(component_id='baths-to',component_property='value'),
    # State(component_id='item-review',component_property='value'),
    State(component_id='accomodation-type',component_property='value'),
    prevent_initial_call = True
)
def return_df(click,location,price_from,price_to,guests_from,guests_to,beds_from,beds_to,bedrooms_from,bedrooms_to,baths_from,baths_to,home_type):


    if  click:


        price_from =  0 if price_from is None else price_from
        price_to = max_price if price_to is None else price_to
        guests_from = 0 if guests_from is None else guests_from
        guests_to = max_nguest if guests_to is None else guests_to
        beds_from = 0 if beds_from is None else beds_from
        beds_to = max_beds if beds_to is None else beds_to
        bedrooms_from = 0 if bedrooms_from is None else bedrooms_from
        bedrooms_to = max_bedrooms if bedrooms_to is None else bedrooms_to
        baths_from = 0 if baths_from is None else baths_from
        baths_to = max_baths if baths_to is None else baths_to

        # print(price_from,price_to,beds_from,beds_to,baths_from,baths_to,bedrooms_from,bedrooms_to,guests_to,guests_from)

        if location:

            location_list = location.split(" ")

            if len(location_list) == 1:
                location = location.lower()
                index_list = list({i for i in data.index if location in data.loc[i,'location_list']})

            else:

                index_list = [i for location in location_list for i in data.index if location.lower() in data.loc[i,'location_list']]

            df = data.loc[index_list,].copy()

        else:

            if home_type is None:
                home_type = accomodation_types
            elif isinstance(home_type,str):
                home_type = [home_type]
            


            
            try:
                df = df[(df['PriceBefore'] >= price_from) & (df['PriceBefore'] <= price_to)].copy()

            except:
                 df = data[(data['PriceBefore'] >= price_from) & (data['PriceBefore'] <= price_to)].copy()


            df = df[(df['NumberOfGuest'] >= guests_from) & (df['NumberOfGuest'] <= guests_to)]
            df = df[(df['NumberOfGuest'] >= beds_from) & (df['NumberOfGuest'] <= beds_to)]
            df = df[(df['NumberOfGuest'] >= bedrooms_from) & (df['NumberOfGuest'] <= bedrooms_to)]
            df = df[(df['NumberOfGuest'] >= baths_from) & (df['NumberOfGuest'] <= baths_to)]
            # df = df[(df['NumberOfGuest'] >= item_review[0]) & (df['NumberOfGuest'] <= item_review[1])]

            df = df[df['Section'].isin(home_type)]
            



        if len(df) == 0:
            return html.Div(children=["No result!!!"])
        
        df.drop("location_list",axis=1,inplace=True)

        
        return html.Div(children=[dash_table.DataTable(data=df.to_dict('records'),columns=[{"name":i,"id":i} for i in df.columns])])


    


if __name__ == "__main__":
    app.run_server(debug=True,port=8889)