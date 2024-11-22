import pandas as pd
import plotly.express as px
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from api.repositories.context import context


def dashboard_v1(request):
    graphs = []
    labels = []

    df = context.tours.avg_tour_price()
    fig = px.bar(df, x='destination_country', y='avg_price',
                 labels={"destination_country": "Country", "avg_price": "Average Price"},)
    graphs.append(fig.to_html(full_html=False))
    labels.append('Average Tour Price by Country')

    df = context.tours.tours_by_country()
    fig = px.pie(df, names='destination_country', values='total_tours',
                 labels={"destination_country": "Country", "total_tours": "Total Tours"})
    graphs.append(fig.to_html(full_html=False))
    labels.append('Tour Distribution by Country')


    country = request.GET.get('country', 'UAE')
    fig = px.line(context.tours.tours_per_month_by_country(country), x='month', y='total_tours',
                  labels={"month": "Month", "total_tours": "Number of Tours"},)
    graph = fig.to_html(full_html=False)


    fig = px.bar(context.tours.tours_summary(), x='destination_country', y='total_tours',
                    labels={"destination_country": "Country", "total_tours": "Total Tours"})
    graphs.append(fig.to_html(full_html=False))
    labels.append('Tours Summary by Country')

    fig = px.bar(context.transports.get_transport_data(), x='type', y='transports',
                 labels={"type": "Type", "transports": "Number of Tours"})
    graphs.append(fig.to_html(full_html=False))
    labels.append('Number of Tours by Transport Type')

    avg_price = int(request.GET.get('avg_price', 0))
    total_tours = int(request.GET.get('total_tours', 0))
    df = context.tours.tours_with_conditions(avg_price_more_than=avg_price, total_tours_more_than=total_tours)
    fig = px.bar(df, x='destination_country', y='total_tours',
                 labels={"destination_country": "Country", "total_tours": "Total Tours"})
    interactive_graph = fig.to_html(full_html=False)

    tours = context.tours.get_all()
    countries = list(set(tour['destination_country'] for tour in tours))
    graph_data = zip(graphs, labels)
    return render(request, 'dashboards/dashboard_v1.html', {'graph_data': graph_data, 'interactive_graph': interactive_graph, 'countries': countries, 'country': country, 'graph': graph})


def avg_tour_price_by_country(request):
    return context.tours.avg_tour_price()
