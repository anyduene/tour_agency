import pandas as pd
import plotly.express as px
from bokeh.io import show
from bokeh.resources import CDN
from django.shortcuts import render
from bokeh.plotting import figure
from bokeh.embed import components, file_html
from bokeh.models import ColumnDataSource

from api.NetworkHelper import NetworkHelper


BASE_URL = 'http://127.0.0.1:8001/'


def dashboard_v1(request):
    network_helper = NetworkHelper(BASE_URL)
    graphs = []
    labels = []

    # Отримання параметрів із запиту
    avg_price = int(request.GET.get('avg_price', 0))
    total_tours = int(request.GET.get('total_tours', 0))
    selected_country = request.GET.get('country', 'Italy')

    # 1. Average Tour Price
    avg_tour_price = network_helper.get_avg_tour_price()
    avg_tour_price_list = avg_tour_price.get('avg_tour_prices', [])
    if avg_tour_price_list:
        df = pd.DataFrame(avg_tour_price_list)
        if not df.empty and {'destination_country', 'avg_price'}.issubset(df.columns):
            fig = px.bar(df, x='destination_country', y='avg_price',
                         labels={"destination_country": "Country", "avg_price": "Average Price"},
                         title="Average Tour Price by Country")
            graphs.append(fig.to_html(full_html=False))
            labels.append('Average Tour Price by Country')

    # 2. Tours by Country
    tours_by_country = network_helper.get_tours_by_country()
    tours_by_country_list = tours_by_country.get('tours_by_country', [])
    if tours_by_country_list:
        df = pd.DataFrame(tours_by_country_list)
        if not df.empty and {'destination_country', 'total_tours'}.issubset(df.columns):
            fig = px.bar(df, x='destination_country', y='total_tours',
                         labels={"destination_country": "Country", "total_tours": "Total Tours"},
                         title="Total Tours by Country")
            graphs.append(fig.to_html(full_html=False))
            labels.append('Total Tours by Country')

    # 3. Tours Summary
    tours_summary = network_helper.get_tours_summary()
    tours_summary_list = tours_summary.get('tours_summary', [])
    if tours_summary_list:
        df = pd.DataFrame(tours_summary_list)
        if not df.empty and {'destination_country', 'total_tours'}.issubset(df.columns):
            fig = px.bar(df, x='destination_country', y='total_tours',
                         labels={"destination_country": "Country", "total_tours": "Total Tours"},
                         title="Tours Summary")
            graphs.append(fig.to_html(full_html=False))
            labels.append('Tours Summary')

    # 4. Transport Data
    transport_data = network_helper.get_transport_data()
    transport_data_list = transport_data.get('transport_data', [])
    if transport_data_list:
        df = pd.DataFrame(transport_data_list)
        if not df.empty and {'type', 'transports'}.issubset(df.columns):
            fig = px.bar(df, x='type', y='transports',
                         labels={"type": "Transport", "transports": "Number of Tours"},
                         title="Transport Data")
            graphs.append(fig.to_html(full_html=False))
            labels.append('Transport Data')

    # 5. Tours with Conditions
    tours_with_conditions = network_helper.get_tours_with_conditions(avg_price_more_than=avg_price, total_tours_more_than=total_tours)
    tours_with_conditions_list = tours_with_conditions.get('tours_with_conditions', [])
    interactive_graph = None
    if tours_with_conditions_list:
        df = pd.DataFrame(tours_with_conditions_list)
        if not df.empty and {'destination_country', 'total_tours'}.issubset(df.columns):
            fig = px.bar(df, x='destination_country', y='total_tours',
                         labels={"destination_country": "Country", "total_tours": "Total Tours"},
                         title=f"Tours with Avg Price > {avg_price} USD and Total Tours > {total_tours}")
            interactive_graph = fig.to_html(full_html=False)

    # 6. Tours per Month by Country
    tours_per_month_by_country = network_helper.get_tours_per_month_by_country(selected_country)
    tours_per_month_by_country_list = tours_per_month_by_country.get('tours_per_month_by_country', [])
    tours_per_month_by_country_graph = None
    if tours_per_month_by_country_list:
        df = pd.DataFrame(tours_per_month_by_country_list)
        if not df.empty and {'month', 'total_tours'}.issubset(df.columns):
            df['month'] = pd.to_datetime(df['month'])  # Convert to datetime for better plotting
            fig = px.line(df, x='month', y='total_tours',
                          labels={"month": "Month", "total_tours": "Total Tours"},
                          title=f"Tours per Month in {selected_country}",
                          markers=True)  # Add markers for better visibility
            tours_per_month_by_country_graph = fig.to_html(full_html=False)

    # Combine all graphs and labels
    graph_data = zip(graphs, labels)
    countries = network_helper.get_countries()
    countries_list = countries.get('countries', [])
    countries_list = [country['destination_country'] for country in countries_list]

    return render(request, 'dashboards/dashboard_v1.html', {
        'graph_data': graph_data,
        'interactive_graph': interactive_graph,
        'tours_per_month_by_country_graph': tours_per_month_by_country_graph,
        'countries': countries_list,
        'avg_price': avg_price,
        'total_tours': total_tours,
        'selected_country': selected_country,
    })






#using bokeh
def dashboard_v2(request):
    network_helper = NetworkHelper(BASE_URL)
    graphs = []
    labels = []

    # Get parameters from request
    avg_price = int(request.GET.get('avg_price', 0))
    total_tours = int(request.GET.get('total_tours', 0))
    selected_country = request.GET.get('country', 'Italy')

    # 1. Average Tour Price
    avg_tour_price = network_helper.get_avg_tour_price()
    avg_tour_price_list = avg_tour_price.get('avg_tour_prices', [])
    df = pd.DataFrame(avg_tour_price_list)
    source = ColumnDataSource(df)
    x_range = df['destination_country'].unique().tolist()
    p = figure(x_range=x_range, title="Average Tour Price by Country",
               toolbar_location=None, tools="")
    p.vbar(x='destination_country', top='avg_price', width=0.9, source=source)
    p.xaxis.axis_label = "Country"
    p.yaxis.axis_label = "Average Price"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    graph = file_html(p, CDN)
    graphs.append(graph)
    labels.append('Average Tour Price by Country')


    # 2. Tours by Country
    tours_by_country = network_helper.get_tours_by_country()
    tours_by_country_list = tours_by_country.get('tours_by_country', [])
    df = pd.DataFrame(tours_by_country_list)
    source = ColumnDataSource(df)
    x_range = df['destination_country'].unique().tolist()
    p = figure(x_range=x_range, title="Total Tours by Country",
               toolbar_location=None, tools="")
    p.vbar(x='destination_country', top='total_tours', width=0.9, source=source)
    p.xaxis.axis_label = "Country"
    p.yaxis.axis_label = "Total Tours"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    graph = file_html(p, CDN)
    graphs.append(graph)
    labels.append('Total Tours by Country')


    # 3. Tours Summary
    tours_summary = network_helper.get_tours_summary()
    tours_summary_list = tours_summary.get('tours_summary', [])
    df = pd.DataFrame(tours_summary_list)
    source = ColumnDataSource(df)
    x_range = df['destination_country'].unique().tolist()
    p = figure(x_range=x_range, title="Tours Summary",
               toolbar_location=None, tools="")
    p.vbar(x='destination_country', top='total_tours', width=0.9, source=source)
    p.xaxis.axis_label = "Country"
    p.yaxis.axis_label = "Total Tours"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    graph = file_html(p, CDN)
    graphs.append(graph)
    labels.append('Tours Summary')


    # 4. Transport Data
    transport_data = network_helper.get_transport_data()
    transport_data_list = transport_data.get('transport_data', [])
    df = pd.DataFrame(transport_data_list)
    source = ColumnDataSource(df)
    x_range = df['type'].unique().tolist()
    p = figure(x_range=x_range, title="Transport Data",
               toolbar_location=None, tools="")
    p.vbar(x='type', top='transports', width=0.9, source=source)
    p.xaxis.axis_label = "Transport"
    p.yaxis.axis_label = "Number of Tours"
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    graph = file_html(p, CDN)
    graphs.append(graph)
    labels.append('Transport Data')


    # 5. Tours with Conditions
    tours_with_conditions = network_helper.get_tours_with_conditions(avg_price_more_than=avg_price, total_tours_more_than=total_tours)
    tours_with_conditions_list = tours_with_conditions.get('tours_with_conditions', [])
    if tours_with_conditions_list:
        df = pd.DataFrame(tours_with_conditions_list)
        x_range = df['destination_country'].tolist()
    else:
        df = pd.DataFrame()
    source = ColumnDataSource(df)
    p = figure(x_range=x_range, title=f"Tours with Avg Price > {avg_price} USD and Total Tours > {total_tours}",
               toolbar_location=None, tools="")
    p.vbar(x='destination_country', top='total_tours', width=0.9, source=source)
    p.xaxis.axis_label = "Country"
    p.yaxis.axis_label = "Total Tours"

    interactive_graph = file_html(p, CDN)
    labels.append(f'Tours with Avg Price > {avg_price} USD and Total Tours > {total_tours}')


    # 6. Tours per Month by Country
    tours_per_month_by_country = network_helper.get_tours_per_month_by_country(selected_country)
    tours_per_month_by_country_list = tours_per_month_by_country.get('tours_per_month_by_country', [])
    df = pd.DataFrame(tours_per_month_by_country_list)
    df['month'] = pd.to_datetime(df['month'])
    df = df.sort_values('month')
    source = ColumnDataSource(df)
    p = figure(x_axis_type="datetime", title=f"Tours per Month in {selected_country}",
               toolbar_location=None, tools="", sizing_mode="stretch_width")
    p.line(x='month', y='total_tours', source=source)
    p.circle(x='month', y='total_tours', source=source)
    p.xaxis.axis_label = "Month"
    p.yaxis.axis_label = "Total Tours"

    tours_per_month_by_country_graph = file_html(p, CDN)
    labels.append(f'Tours per Month in {selected_country}')




    graph_data = zip(graphs, labels)
    countries = network_helper.get_countries()
    countries_list = countries.get('countries', [])
    countries_list = [country['destination_country'] for country in countries_list]

    return render(request, 'dashboards/dashboard_v2.html', {
        'graph_data': graph_data,
        'countries': countries_list,
        'interactive_graph': interactive_graph,
        'tours_per_month_by_country_graph': tours_per_month_by_country_graph,
        'avg_price': avg_price,
        'total_tours': total_tours,
        'selected_country': selected_country,
    })