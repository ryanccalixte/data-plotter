# libraries
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numbers


def format_stat(value):
    if pd.isna(value):
        return "N/A"
    if isinstance(value, numbers.Integral):
        return int(value)
    if isinstance(value, numbers.Number):
        return round(float(value), 3)
    return str(value)


def build_plot_stats(df, plottype):
    columns = df.columns.drop('number of rows')
    column_stats = []
    for column in columns:
        series = df[column]
        stats = series.agg(['min', 'max', 'mean', 'std']).to_dict()
        column_stats.append({
            'name': column,
            'min': format_stat(stats['min']),
            'max': format_stat(stats['max']),
            'mean': format_stat(stats['mean']),
            'std': format_stat(stats['std']),
        })

    return {
        'plot_type': plottype.capitalize(),
        'total_rows': len(df),
        'total_columns': len(columns),
        'traces_count': len(columns),
        'columns': list(columns),
        'column_stats': column_stats,
    }


def update_figure(figure, plot_stats, plottype):
    if plottype in ["scatter3d", "surface3d", "bubble3d", "line3d"]:
        figure.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0), dragmode="orbit", showlegend=False)
    else:
        figure.update_layout(autosize=True, margin=dict(l=0, r=0, t=0, b=0), dragmode="pan", showlegend=False)
    plotdiv = figure.to_html(
        full_html=False,
        include_plotlyjs='cdn',
        config={
            "responsive": True,
            "scrollZoom": True,
            "displayModeBar": False
            }
    )
    
    traces = []
    for trace in figure.data:
        if plottype == "line":
            traces.append({"name": trace.name, "color": trace.line.color})
        elif plottype in ["scatter", "bar", "scatter3d", "surface3d", "bubble3d", "line3d"]:
            traces.append({"name": trace.name, "color": trace.marker.color})
        
    
    return plotdiv, traces, plot_stats


def graphdata(cleandata, plottype):
    cleandata['number of rows'] = range(1, len(cleandata) + 1)
    plot_stats = build_plot_stats(cleandata, plottype)

    y_columns = cleandata.columns.drop('number of rows').tolist()
    
    if plottype == 'scatter':
        fig = px.scatter(cleandata, x='number of rows', y=y_columns)
    elif plottype == 'line':
        fig = px.line(cleandata, x='number of rows', y=y_columns)
    elif plottype == 'bar':
        fig = px.bar(cleandata, x='number of rows', y=y_columns)
    elif plottype == 'scatter3d':
        x_col = y_columns[0] if len(y_columns) > 0 else 'number of rows'
        y_col = y_columns[1] if len(y_columns) > 1 else 'number of rows'
        z_col = y_columns[2] if len(y_columns) > 2 else 'number of rows'
        
        fig = go.Figure(data=[go.Scatter3d(
            x=cleandata[x_col],
            y=cleandata[y_col],
            z=cleandata[z_col],
            mode='markers',
            marker=dict(size=5, color=cleandata[y_columns[0]], colorscale='Viridis', showscale=True)
        )])
        fig.update_layout(scene=dict(
            xaxis_title=x_col, yaxis_title=y_col, zaxis_title=z_col
        ))
    elif plottype == 'line3d':
        x_col = y_columns[0] if len(y_columns) > 0 else 'number of rows'
        y_col = y_columns[1] if len(y_columns) > 1 else 'number of rows'
        z_col = y_columns[2] if len(y_columns) > 2 else 'number of rows'
        
        fig = go.Figure(data=[go.Scatter3d(
            x=cleandata[x_col],
            y=cleandata[y_col],
            z=cleandata[z_col],
            mode='lines+markers',
            line=dict(width=4, color=cleandata[y_columns[0]], colorscale='Plasma'),
            marker=dict(size=4)
        )])
        fig.update_layout(scene=dict(
            xaxis_title=x_col, yaxis_title=y_col, zaxis_title=z_col
        ))
    elif plottype == 'bubble3d':
        x_col = y_columns[0] if len(y_columns) > 0 else 'number of rows'
        y_col = y_columns[1] if len(y_columns) > 1 else 'number of rows'
        z_col = y_columns[2] if len(y_columns) > 2 else 'number of rows'
        size_col = y_columns[3] if len(y_columns) > 3 else y_columns[0]
        
        size_values = cleandata[size_col]
        normalized_size = (size_values - size_values.min()) / (size_values.max() - size_values.min()) * 20 + 3
        
        fig = go.Figure(data=[go.Scatter3d(
            x=cleandata[x_col],
            y=cleandata[y_col],
            z=cleandata[z_col],
            mode='markers',
            marker=dict(size=normalized_size, color=size_values, colorscale='Viridis', showscale=True)
        )])
        fig.update_layout(scene=dict(
            xaxis_title=x_col, yaxis_title=y_col, zaxis_title=z_col
        ))
    elif plottype == 'surface3d':
        x_col = y_columns[0] if len(y_columns) > 0 else 'number of rows'
        y_col = y_columns[1] if len(y_columns) > 1 else 'number of rows'
        z_col = y_columns[2] if len(y_columns) > 2 else 'number of rows'
        
        fig = go.Figure(data=[go.Scatter3d(
            x=cleandata[x_col],
            y=cleandata[y_col],
            z=cleandata[z_col],
            mode='markers',
            marker=dict(size=3, color=cleandata[z_col], colorscale='Viridis', showscale=True)
        )])
        fig.update_layout(scene=dict(
            xaxis_title=x_col, yaxis_title=y_col, zaxis_title=z_col
        ))

    return update_figure(fig, plot_stats, plottype)
