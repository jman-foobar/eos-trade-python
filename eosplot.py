from eosstats import EOSStats
import matplotlib.pyplot as plt
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
import threading

"""
Plot some history of the EOS Sales
"""

class EOSPlot:

    def __init__(self):
        self.stats = EOSStats(offline=True, verbose=True)

    """
    Plot daily ETH sales
    """
    def plot_daily_total_eth(self):
        eth_totals = self.stats.el.eth_values(1,-1)
        start_dates = self.stats.el.start_date_values(1, -1)

        #plot data
        fig = plt.figure(dpi=128, figsize=(10, 6))
        plt.plot(start_dates, eth_totals, linewidth=1)

        #set title and axis
        plt.title("Daily Ethereum Totals", fontsize=24)

        plt.xlabel("", fontsize=14)
        fig.autofmt_xdate() #draws date labels diagonally

        plt.ylabel("Ethereum (ETH)", fontsize=14)

        #set size of tick parameters
        plt.tick_params(axis='both', which='major', labelsize=14)

        plt.show()

    def bar_daily_ico(self):
        #get values
        plot_dicts, start_dates = [], []
        for ico in self.stats.el.list(1,-1):
            start_dates.append(ico.ends)
            plot_dict = {
                'value' : int(ico.daily_total_eth),
                'label' : "Daily Total ETH"
                }
            plot_dicts.append(plot_dict)

        #set config
        my_style = LS('#333366', base_style=LCS)
        my_config = pygal.Config()
        my_config.x_label_rotation = 45
        my_config.show_legend = False
        my_config.title_font_size = 24
        my_config.label_font_size = 14
        my_config.major_label_font_size = 18
        my_config.truncate_label = 15
        my_config.show_y_guides = False
        my_config.width = 1000

        chart = pygal.Bar(my_config, style=my_style)

        #make visualization

        chart.title = "Daily Ethereum Total (All)"
        chart.x_labels = start_dates


        chart.add('', plot_dicts)
        chart.render_to_file('eth_totals.svg')

    """
    Plot daily formaula sales
    """
    def plot_daily_eos_formula(self):
        eos_formulas = self.stats.el.eos_formula_values(1, self.stats.el.length()-1)
        start_dates = self.stats.el.start_date_values(1, self.stats.el.length()-1)

        #plot data
        fig = plt.figure(dpi=128, figsize=(10, 6))
        plt.plot(start_dates, eos_formulas, linewidth=1)

        #set title and axis
        plt.title("Daily EOS per ETH", fontsize=24)

        plt.xlabel("", fontsize=14)
        fig.autofmt_xdate() #draws date labels diagonally

        plt.ylabel("EOS Tokens", fontsize=14)

        #set size of tick parameters
        plt.tick_params(axis='both', which='major', labelsize=14)

        plt.show()


    """
    Plot daily formaula sales and price
    """
    def plot_daily_eos_formula_price(self):
        eos_formulas = self.stats.el.eos_formula_values(1, self.stats.el.length()-1)
        eos_prices = self.stats.el.eos_values(1, self.stats.el.length()-1)
        start_dates = self.stats.el.start_date_values(1, self.stats.el.length()-1)

        #plot data
        fig = plt.figure(dpi=128, figsize=(10, 6))
        plt.plot(start_dates, eos_formulas, linewidth=1)
        plt.plot(start_dates, eos_prices, linewidth=1)

        #set title and axis
        plt.title("Daily EOS per ETH", fontsize=24)

        plt.xlabel("", fontsize=14)
        fig.autofmt_xdate() #draws date labels diagonally

        plt.ylabel("EOS Tokens", fontsize=14)

        #set size of tick parameters
        plt.tick_params(axis='both', which='major', labelsize=14)

        plt.show()

plotter = EOSPlot()
#plotter.plot_daily_eos_formula_price()
plotter.bar_daily_ico()

#t1 = threading.Thread(target=plotter.plot_daily_total_eth)
#t2 = threading.Thread(target=plotter.plot_daily_eos_formula)

#t1.start()
#t2.start()
