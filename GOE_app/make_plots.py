import os
import plotly.express as px
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.colors as colors
from pathlib import Path

# global_palette = 'coolwarm'
global_palette = 'viridis'
# -----------------------------------------------------------------------------
#  temp plots
def plot_O2_flux_lb_vs_mixrat(data, species, color='temp_lb', flux='O2_flux_lb',
    fratio='0.3'):
    data = data.astype({color: str})
    ncolors = len(data[color].unique())
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[species].min(), 1e-30)
    range_y_max = data[species].max()
    range_y = [range_y_min, range_y_max] if data[species].min() != range_y_max\
        else None
    O2_flux_range = 6e12 if fratio == '0.45' else 1e12
    range_x = [0.9e11, O2_flux_range] if flux == 'O2_flux_lb' else [0.9e10, 8e11]
    fig = px.scatter(data_frame=data, x=flux, y=species,
                     symbol='converged', color=color, log_y=True, 
                     range_x=range_x,
                     range_y=range_y,
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         species: 'Surface Mixig Ratio',
                         'temp_lb': 'Temp [K]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    # animation_frame='alt',
                    title=species + ' surface mixing ratio')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_O2_flux_lb_vs_atm_cols(data, species, color='temp_lb', flux='O2_flux_lb',
    fratio='0.3'):
    data = data.astype({color: str})
    ncolors = len(data[color].unique())
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[species].min(), 1e-30)
    range_y_max = data[species].max()
    range_y = [range_y_min, range_y_max] if data[species].min() != range_y_max\
        else None
    O2_flux_range = 6e12 if fratio == '0.45' else 1e12
    range_x = [0.9e11, O2_flux_range] if flux == 'O2_flux_lb' else [0.9e10, 8e11]
    fig = px.scatter(data_frame=data, x=flux, y=species,
                     symbol='converged', color=color, log_y=True,
                     range_x=range_x,
                     range_y=range_y,
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         species: 'Atmospheric column [molecules /cm^2]',
                         'temp_lb': 'Temp [k]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    title=species + ' atmospheric column')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_vars_vs_alt_by_flowO2(data, species, color='temp_lb', flux='O2_flux_lb'):
    data = data.iloc[0:-1:2]
    color_unique = data[color].unique()
    ncolors = len(color_unique)
    data[flux] = data[flux].apply(lambda col: '{:.2E}'.format(col))
    
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_x_min = max(data[species].min(), 1e-30)
    range_x = [range_x_min, data[species].max()] if data[species].min() !=\
        data[species].max() else None
    fig = px.line(data_frame=data, x=species, y='alt', color=color, 
                     range_x = range_x,
                     range_y = [0, 100],
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         species: 'Mixig Ratio',
                         'temp_lb': 'Temp [k]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame=flux,
                    title=species + ' mixing ratio profile')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

        
def plot_O2_flux_lb_vs_rates(data, reaction, color='temp_lb', flux='O2_flux_lb',
    fratio='0.3'):
    data = data.astype({color: str})
    ncolors = len(data[color].unique())
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[reaction].min(), 1e-30)
    range_y_max = data[reaction].max()
    range_y = [range_y_min, range_y_max] if data[reaction].min() != range_y_max\
        else None
    O2_flux_range = 6e12 if fratio == '0.45' else 1e12
    range_x = [0.9e11, O2_flux_range] if flux == 'O2_flux_lb' else [0.9e10, 8e11]
    fig = px.scatter(data_frame=data, x=flux, y=reaction,
                     symbol='converged', color=color, log_y=True, 
                     range_x=range_x,
                     range_y=range_y,
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         reaction: 'Surface reaction rate [molecules/cm^3 s]',
                         'temp_lb': 'Temp [K]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    # animation_frame='alt',
                    title=reaction + ' surface rate')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_O2_flux_lb_vs_integrated_rates(data, reaction, color='temp_lb', 
    flux='O2_flux_lb', fratio='0.3'):
    data = data.astype({color: str})
    ncolors = len(data[color].unique())
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_y_min = max(data[reaction].min(), 1e-30)
    range_y_max = data[reaction].max()
    range_y = [range_y_min, range_y_max] if data[reaction].min() != range_y_max\
        else None
    O2_flux_range = 6e12 if fratio == '0.45' else 1e12
    range_x = [0.9e11, O2_flux_range] if flux == 'O2_flux_lb' else [0.9e10, 8e11]
    fig = px.scatter(data_frame=data, x=flux, y=reaction,
                     symbol='converged', color=color, log_y=True, 
                     range_x=range_x,
                     range_y=range_y,
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         reaction: 'Integrated reaction rate [molecules / cm^2 s]',
                         'temp_lb': 'Temp [K]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    title=reaction + ' integrated rate')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_rates_vs_alt(data, reaction, color='temp_lb', flux='O2_flux_lb'):
    data = data.iloc[0:-1:2]
    color_unique = data[color].unique()
    ncolors = len(color_unique)
    data[flux] = data[flux].apply(lambda col: '{:.2E}'.format(col))
    # print(data)
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    range_x_min = max(data[reaction].min(), 1e-30)
    range_x = [range_x_min, data[reaction].max()] if data[reaction].min() !=\
        data[reaction].max() else None
    fig = px.line(data_frame=data, x=reaction, y='alt', color=color, 
                     range_x = range_x,
                     range_y = [0, 100],
                     log_x=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         reaction: 'Reaction rate [molecules / cm^3 s]',
                         'temp_lb': 'Temp [k]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame=flux,
                    title=reaction + ' rate profile')
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_radiative_flux(data, altitude, color='temp_lb', flux='O2_flux_lb'):
    color_unique = data[color].unique()
    ncolors = len(color_unique)
    data[flux] = data[flux].apply(lambda col: '{:.2E}'.format(col))
    palette = sns.color_palette(global_palette, ncolors)
    palette = [colors.to_hex(x) for x in palette]
    fig = px.line(data_frame=data, x='wavl', y=altitude, color=color,
                     range_y = [1e-10, 1e16],
                     range_x = [0, 500],
                     log_y=True, labels={
                         'O2_flux_lb': 'Surface O2 flux [pu]',
                         'CO_flux_lb': 'Surface CO flux [pu]',
                         'time': 'Time [years]',
                         altitude: 'Radiative flux [hv/cm^2/s/nm]',
                         'temp_lb': 'Temp [k]',
                         'relh_lb': 'Relative Humidity',
                         'converged': 'Converged',
                         'alt': 'Altitude [Km]'},
                    color_discrete_sequence=palette,
                    animation_frame=flux,
                    title='Radiative flux at ' + altitude[altitude.find('_') + 1:])
    fig.update_xaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_yaxes(exponentformat='power', title={'font':dict(size=18)},
        showgrid=True,  gridcolor='grey', showline=True,  linecolor='black',
        mirror=True, tickfont_size=13, zerolinecolor='grey')
    fig.update_layout(legend = dict(font = dict(size = 15)), title={'x':0.5,
        'xanchor': 'center', 'font':dict(size=25)},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig


def split_species_data(mixrat_data, cols_data, folder, sp_names,
    flux='O2_flux_lb'):
    Path(folder).mkdir(exist_ok=True)
    Path(folder + '/surface').mkdir(exist_ok=True)
    Path(folder + '/column').mkdir(exist_ok=True)
    Path(folder + '/profiles').mkdir(exist_ok=True)
    if flux == 'O2_flux_lb':
        mixrat_data = mixrat_data[mixrat_data.O2_flux_lb > 1e11]
        mixrat_data = mixrat_data[mixrat_data.O2_flux_lb < 6.3e12]
        cols_data = cols_data[cols_data.O2_flux_lb > 1e11]
        cols_data = cols_data[cols_data.O2_flux_lb < 6.3e12]
    for s in sp_names:
        print(s)
        new_data_mixrat = mixrat_data[['alt', 'temp_lb', 'converged', 'relh_lb',
            flux, s]]
        cols = cols_data[['temp_lb', 'converged', 'relh_lb',
            flux, s]]
        mixrat_lb = new_data_mixrat[new_data_mixrat.alt == 0.25]
        fluxes = new_data_mixrat[flux].unique()   
        idxs = np.round(np.linspace(0, len(fluxes) - 1, 30)).astype(int)
        fluxes = fluxes[idxs]
        mixrat_profiles = new_data_mixrat[new_data_mixrat[flux].isin(fluxes)]
        path_lb = os.path.join(folder, 'surface', s) + '.csv'
        path_cols = os.path.join(folder, 'column', s) + '.csv'
        path_profiles = os.path.join(folder, 'profiles',s) + '.csv'
        mixrat_lb.to_csv(path_lb, index=False, compression='gzip')
        cols.to_csv(path_cols, index=False, compression='gzip')
        mixrat_profiles.to_csv(path_profiles, index=False, compression='gzip')

def split_reaction_data(rates_data, int_rates_data, folder, react_names,
    flux='O2_flux_lb'):
    Path(folder).mkdir(exist_ok=True)
    Path(folder + '/surface').mkdir(exist_ok=True)
    Path(folder + '/column').mkdir(exist_ok=True)
    Path(folder + '/profiles').mkdir(exist_ok=True)
    if flux == 'O2_flux_lb':
        rates_data = rates_data[rates_data.O2_flux_lb > 1e11]
        rates_data = rates_data[rates_data.O2_flux_lb < 6.3e12]
        int_rates_data = int_rates_data[int_rates_data.O2_flux_lb > 1e11]
        int_rates_data = int_rates_data[int_rates_data.O2_flux_lb < 6.3e12]
    for r in react_names:
        print(r)
        new_rates_data = rates_data[['alt', 'temp_lb', 'converged',
            flux, 'relh_lb' ,r]]
        int_rates = int_rates_data[['temp_lb', 'converged',
            flux, 'relh_lb' ,r]]
        rates_lb = new_rates_data[new_rates_data.alt == 0.25]
        fluxes = new_rates_data[flux].unique()   
        idxs = np.round(np.linspace(0, len(fluxes) - 1, 30)).astype(int)
        fluxes = fluxes[idxs]
        rates_profiles = new_rates_data[new_rates_data[flux].isin(fluxes)]
        path_lb = os.path.join(folder, 'surface', r.replace(' ', '')) + '.csv'
        path_int_rates = os.path.join(folder, 'column', r.replace(' ', '')) + '.csv'
        path_profiles = os.path.join(folder, 'profiles', r.replace(' ', '')) + '.csv'
        rates_lb.to_csv(path_lb, index=False, compression='gzip')
        int_rates.to_csv(path_int_rates, index=False, compression='gzip')
        rates_profiles.to_csv(path_profiles, index=False, compression='gzip')

def split_flux_data(flux_data, folder, alts, flux='O2_flux_lb'):
    Path(folder).mkdir(exist_ok=True)
    if flux == 'O2_flux_lb':
        flux_data = flux_data[flux_data.O2_flux_lb > 1e11]
        flux_data = flux_data[flux_data.O2_flux_lb < 6.3e12]
    for alt in alts:
        print(alt)
        new_data = flux_data[['wavl', 'temp_lb', 'relh_lb', 'converged',
            flux, alt]]
        new_data = new_data.rename(columns = {alt:f'flux_{alt}km'})
        fluxes = new_data[flux].unique()   
        idxs = np.round(np.linspace(0, len(fluxes) - 1, 30)).astype(int)
        fluxes = fluxes[idxs]
        flux_profiles = new_data[new_data[flux].isin(fluxes)]
        path = os.path.join(folder, f'{alt}km') + '.csv'
        flux_profiles.to_csv(path, index=False, compression='gzip')
