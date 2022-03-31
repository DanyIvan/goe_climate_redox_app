from flask import render_template, abort, Blueprint
import pandas as pd
import os
import numpy as np
from GOE_app.make_plots import *

results_app = Blueprint('results_app',__name__)

base_route = '/projects/goe_climate_redox/'
data_url = 'https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/'

# lists of acceptable options
plot_type_options = ['species', 'reactions', 'radiativeflux', 'atm_bcs',
    'species_bcs']
by_options = ['rh', 'temp']
by_value_options = ['0.2', '0.6', '1.0', '250', '260', '270', '280',
    '290', '300', '310', '320', '330', '340', '350', '360']
scenario_options = ['0', '1']
fratio_options = ['0.094', '0.3', '0.45']


@results_app.route(base_route, methods=["GET"])
def GOE_climate_index(): 
    return render_template('GOE_app_index.html')

@results_app.route(base_route + "<plot_type>/<by>/",methods=["GET"])
def GOE_climate_options(plot_type, by):
    # abort if url contains not acceptable options
    if plot_type not in plot_type_options or by not in by_options:
        abort(404)
    # get option_list
    species_list = np.genfromtxt('GOE_app/data/species.txt', dtype='str')
    reaction_list = np.genfromtxt('GOE_app/data/reactions.txt',
        dtype='str', delimiter='\n')
    altitude_list = [f'{x}km' for x in np.arange(0.25, 100, 10)]
    if plot_type == 'species':
        options_list = species_list
    elif plot_type == 'reactions':
        options_list = reaction_list
    elif plot_type == 'radiativeflux':
        options_list = altitude_list
    # retutn boundary conditions plots
    if plot_type == 'atm_bcs':
        bcs_html = '/static/atm_bcs.html' if by == 'temp' else\
            '/static/atm_bcs_rh.html'
        return render_template('bcs.html', bcs_html=bcs_html, bcs_co=None)
    elif plot_type == 'species_bcs':
        bcs_html = '/static/increase_O2_species_flux_bcs.html'
        bcs_co = '/static/decrease_CO_species_flux_bcs.html'
        return render_template('bcs.html', bcs_html=bcs_html, bcs_co=bcs_co)
    else:
        # return options template
        return render_template('GOE_app_options.html',
            plot_type=plot_type,
            by=by,
            options_list=options_list,
            surface_html=None,
            columns_html=None,
            profile_html=None)

@results_app.route(base_route + "<plot_type>/<by>/<by_value>/<scenario>/<fratio>/<variable>",
    methods=["GET"])
def GOE_climate_plot_results(plot_type, by, by_value, scenario, fratio, variable): 
    # abort if url contains not acceptable options
    if plot_type not in plot_type_options or\
        by not in by_options or\
        by_value not in by_value_options or\
        scenario not in scenario_options or\
        fratio not in fratio_options:
        abort(404)

    species_list = np.genfromtxt('GOE_app/data/species.txt', dtype='str')
    reaction_list = np.genfromtxt('GOE_app/data/reactions.txt', 
        dtype='str', delimiter='\n')
    altitude_list = [f'{x}km' for x in np.arange(0.25, 100, 10)]
    
    # include spaces in reaction names
    if plot_type == 'reactions':
        variable = variable.replace('+', ' + ').replace('=', ' = ')

    # abort if url contains not acceptable options
    if plot_type == 'species' and variable not in species_list:
        abort(404)
    if plot_type == 'reactions' and variable not in reaction_list:
        abort(404)
    if plot_type == 'radiativeflux' and variable not in altitude_list:
        abort(404)
    
    # get list of  options according to plot type
    if plot_type == 'species':
        options_list = species_list
    elif plot_type == 'reactions':
        options_list = reaction_list
    elif plot_type == 'radiativeflux':
        options_list = altitude_list

    # get paths of data for plot
    data_folder = 'increase_O2_flux/' if scenario == '0' else 'decrease_CO_flux/'
    flux = 'O2_flux_lb'if scenario == '0' else 'CO_flux_lb'
    color = 'temp_lb' if  by == 'temp' else 'relh_lb'
    by_var = 'relh_lb' if  by == 'temp' else 'temp_lb'  
    data_folder = data_url + data_folder

    # read and filter data for plots
    if plot_type != 'radiativeflux':
        surface_file = os.path.join(data_folder, fratio, plot_type,
            'surface', variable.replace(' ', '').replace('+', '%2B').\
                replace('=', '%3D')) + '.csv'
        column_file = os.path.join(data_folder, fratio, plot_type,
            'column', variable.replace(' ', '').replace('+', '%2B').\
                replace('=', '%3D')) + '.csv'
        profile_file = os.path.join(data_folder, fratio, plot_type,
            'profiles', variable.replace(' ', '').replace('+', '%2B').\
                replace('=', '%3D')) + '.csv'

        surface = pd.read_csv(surface_file, compression='gzip')
        column = pd.read_csv(column_file, compression='gzip')
        profile = pd.read_csv(profile_file, compression='gzip')
    
        surface = surface[surface[by_var] == float(by_value)]
        column = column[column[by_var] == float(by_value)]
        profile = profile[profile[by_var] == float(by_value)]
    else:
        radiation_file = os.path.join(data_folder, fratio, plot_type,
            variable) + '.csv'
        radiation = pd.read_csv(radiation_file, compression='gzip')
        radiation = radiation[radiation[by_var] == float(by_value)]

    
    # make plots
    if plot_type == 'species':
        fig1 = plot_O2_flux_lb_vs_atm_cols(column, variable, color, flux,
            fratio=fratio)
        fig2 = plot_O2_flux_lb_vs_mixrat(surface, variable, color, flux,
            fratio=fratio)
        fig3 = plot_vars_vs_alt_by_flowO2(profile, variable, color, flux)
    elif plot_type == 'reactions':
        fig1 = plot_O2_flux_lb_vs_integrated_rates(column, variable, color, flux,
            fratio=fratio)
        fig2 = plot_O2_flux_lb_vs_rates(surface, variable, color, flux,
            fratio=fratio)
        fig3 = plot_rates_vs_alt(profile, variable, color, flux)        
    elif plot_type == 'radiativeflux':
        alt = f'flux_{variable}'
        fig1 = plot_radiative_flux(radiation, alt, color, flux)
    
    # write plots html
    if plot_type != 'radiativeflux':
        surface_html = fig1.to_html(full_html=False, auto_play=False,
            default_height='600px')
        columns_html = fig2.to_html(full_html=False, auto_play=False,
            default_height='600px')
        profile_html = fig3.to_html(full_html=False, auto_play=False,
            default_height='600px')
    else:
        surface_html = fig1.to_html(full_html=False, auto_play=False,
            default_height='600px')
        columns_html = None
        profile_html = None

    # send plots
    scenario_sel = 'Increase O2 flux' if scenario == '0' else 'Decrease CO flux'
    return render_template('GOE_app_options.html',
        plot_type=plot_type,
        by=by,
        options_list=options_list,
        surface_html=surface_html,
        columns_html=columns_html,
        profile_html=profile_html, 
        variable_sel=variable,
        scenario_sel=scenario_sel,
        fratio=fratio,
        by_value_sel=by_value)
