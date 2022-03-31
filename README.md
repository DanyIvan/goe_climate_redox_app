# Climate-Redox evolution of the Great Oxidation Event

![Alt Text](https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/plot-species.gif)

This flask web application allows exploring the effect of temperature and relative humidity variations on the Great Oxidation Event with interactive plots made with [plotly](https://plotly.com/python/).

You can also use this application here: <https://danielgardunoruiz.com/projects/goe_climate_redox/>

# Requirements

- python version >= 3.8

# Installation

- Create a python environment with all the dependencies specified in `requirements.txt`: For example, with [virtualenv](https://virtualenv.pypa.io/en/latest/):

```
virtualenv goe_climate_redox_app
```

- Activate your new environment and install the dependencies:
  
```
source goe_climate_redox_app/bin/activate
pip install -r requirements.txt
```

- Run the application:

```
python app.py
```

- Go to <http://localhost:3000/projects/goe_climate_redox/> and explore!

# How to use

### Plot species

 See the gif above to see how to plot species.

### Plot reactions

![Alt Text](https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/plot-reactions.gif)

### Plot radiative flux

![Alt Text](https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/plot-radiative-flux.gif)

### Plot atmospheric boundary conditions

![Alt Text](https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/plot-atm-bcs.gif)

### Plot species flux boundary conditions

![Alt Text](https://filedn.com/lAPYsgzcix0SyzxXsLrqQpS/goe_climate_redox/plot-species-bcs.gif)