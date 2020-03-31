# covid-19-schiphol
This is a simulation of the spread of Covid-19 in neighbourhoods around Schiphol. 
For more info, refer to the markdown cells in `post.ipynb` or see the blogpost at [http://jvlanalytics.nl/blog](http://jvlanalytics.nl/blog).

# To reproduce
 
- Create an env with Python 3.8 using `requirements.txt`
- Run `collect_population_data.ipynb` to download and pre-process data from Statistics Netherlands (CBS).
- See `post.ipynb` - this should all run now.

# Other files in this dir

- `sim-10.ipynb` 
- `sim-20.ipynb`

These contain the same simulations as `post.ipynb`, except with radius changed from 30 km to 10 and 20 km respectively. These notebooks have been stripped of blog text.

