import matplotlib.pyplot as plt
import pandas as pd

from .state import PersonState


class SimulationResult:
    def __init__(self, pop_size, n_days, travel_restriction_day, 
                 social_distancing_day):
        self.pop_size = pop_size
        self.n_days = n_days
        self.travel_restriction_day = travel_restriction_day 
        self.social_distancing_day = social_distancing_day

        self.daily_counts_per_hood = []
        self.overall_counts = None
 
        self.num_deceased = None
        self.peak_affected = None
        self.total_affected = None

    def add_day_results(self, df: pd.DataFrame):
        res = (df
               .assign(**{
                   # pivot doesn't play well if state isn't a str
                   "state": lambda df_: df_["state"].map(str),
                   "count": 1
               })
               .groupby(["hood_id", "state"])
               .sum()
               .reset_index()
               .pivot(index="hood_id", columns="state", values="count")
               # This column order happens to give appropriate colors to each 
               # series with matplotlib 2.0's default colors. 
               # Statement also serves to add missing columns.
               .reindex(columns=["PersonState.untouched", 
                                 "PersonState.infected",
                                 "PersonState.recovered", 
                                 "PersonState.deceased"])
               .fillna(0)
               # Undo mapping to str:
               .rename(columns={
                   "PersonState.untouched": PersonState.untouched,
                   "PersonState.infected": PersonState.infected,
                   "PersonState.recovered": PersonState.recovered,
                   "PersonState.deceased": PersonState.deceased
               })
        )

        self.daily_counts_per_hood.append(res)

    def finalize(self):
        last_day = self.daily_counts_per_hood[-1].sum(axis=0)
        self.num_deceased = int(last_day[PersonState.deceased])
        self.total_affected = self.pop_size - int(last_day[PersonState.untouched])

        peak_inf = 0
        for count_per_hood in self.daily_counts_per_hood:
            day_inf_count = count_per_hood[PersonState.infected].sum()
            if day_inf_count > peak_inf:
                peak_inf = day_inf_count

        self.peak_infected = int(peak_inf)

        self._determine_overall_counts()

    def _determine_overall_counts(self):
        res = []

        for day, df in enumerate(self.daily_counts_per_hood):
            counts = df.sum(axis=0).to_dict()
            counts["day"] = day
            res.append(counts)

        self.overall_counts = pd.DataFrame(res).set_index("day")

    @property
    def perc_deceased(self):
        return self.num_deceased / self.pop_size * 100

    @property
    def perc_peak_infected(self):
        return self.peak_infected / self.pop_size * 100
    
    @property
    def perc_total_affected(self):
        return self.total_affected / self.pop_size * 100

    def print_summary(self):
        print(f"Population:     {self.pop_size:10,d}")
        print(f"Deceased:       {self.num_deceased:10,d} "
              f"({self.perc_deceased:4.1f} %)")
        print(f"Peak infected:  {self.peak_infected:10,d} "
              f"({self.perc_peak_infected:4.1f} %)")
        print(f"Total affected: {self.total_affected:10,d} "
              f"({self.perc_total_affected:4.1f} %)")

    def plot_count_curves(self, log=False):
        self.overall_counts.plot(figsize=(12, 4))
        
        title = "Simulation of Covid-19 spread "
        if isinstance(self.travel_restriction_day, int):
            title += f"with travel restriction on day {self.travel_restriction_day}"
            plt.vlines(self.travel_restriction_day, 0, self.pop_size, linestyle="--", 
                       color="C5", linewidth=3, label="travel restriction start")
        else:
            title += "without travel restrictions."
            
        if isinstance(self.social_distancing_day, int):
            title += "\nSocial Distancing in effect from day " \
                     f"{self.social_distancing_day} onwards."
            plt.vlines(self.social_distancing_day, 0, self.pop_size, linestyle="--", 
                       color="C6", linewidth=3, label="social distancing start")
            
        plt.legend(loc="best")
        plt.grid()
        plt.ylabel("Number of persons")
        plt.xlabel("Day")
        if log:
            title = "LOG SCALE - " + title
            plt.yscale("log")
        plt.title(title)
        plt.show()

    def __str__(self):
        return (self.__class__.__name__ + "("
                f"n_days={self.n_days}, tr_day={self.travel_restriction_day}, "
                f"sd_day={self.social_distancing_day})")

    def __repr__(self):
        return str(self)


class SimulationResultStorage:
    def __init__(self):
        self.results = {}

    def add(self, res: SimulationResult):
        self.results[str(res)] = res

    def keys(self):
        return self.results.keys()

    def save(self, base_save_path: str):
        base_save_path = Path(base_save_path)
        for result_key in self.keys():
            result_save_path = base_save_path / result_key.replace(" ", "")
            result_save_path.mkdir(exist_ok=True, parents=True)
            result = self[result_key]
            result.overall_counts.to_csv(result_save_path / "overall-counts.csv")
            for day, df in enumerate(result.daily_counts_per_hood):
                df.to_csv(result_save_path / f"daily_counts_per_hood-day{day:03d}.csv")

    def __getitem__(self, key):
        return self.results[key]

    def __str__(self):
        return self.__class__.__name__ + "(\n    " + \
                ",\n    ".join(str(k) for k in self.keys()) + "\n)"

    def __repr__(self):
        return str(self)

