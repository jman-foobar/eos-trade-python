from eosstats import EOSStats
import matplotlib.pyplot as plt
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

"""
Leverages the statistics to provide an answer to buy or not buy EOS today
"""

class EOSDecisionMaker:

    def __init__(self):
        self.stats = EOSStats(offline=False, verbose=True)

        self.decide_based_on_eth()

    """
    Print options based on statistics
    Return True == Yes or False == No
    """
    def decide_based_on_eth(self):
        score = 0
        tot_eth = self.stats.todays_eth()
        avg_eth = self.stats.daily_avg_eth()
        med_eth = self.stats.daily_median_eth()
        max_eth = self.stats.daily_highest_eth()
        min_eth = self.stats.daily_lowest_eth()

        print """
        *** Decision Based on ETH Submitted Today ***
        """
        if tot_eth >= avg_eth:
            print "\033[91mBAD  => Total ETH greater than Average ETH: %s > %s\033[0m" % (tot_eth, avg_eth)
        else:
            print "\033[92mGOOD => Total ETH less than Average ETH: %s < %s\033[0m" % (tot_eth, avg_eth)
            score += 1

        if tot_eth >= med_eth:
            print "\033[91mBAD  => Total ETH greater than Median ETH: %s > %s\033[0m" % (tot_eth, med_eth)
        else:
            print "\033[92mGOOD => Total ETH less than Median ETH: %s < %s\033[0m" % (tot_eth, med_eth)
            score += 1

        if tot_eth >= max_eth:
            print "\033[91mBAD  => Total ETH greater than Maximum ETH: %s > %s\033[0m" % (tot_eth, max_eth)
        else:
            print "\033[92mGOOD => Total ETH less than Max ETH: %s < %s\033[0m" % (tot_eth, max_eth)
            score += 1

        if tot_eth < min_eth:
            print "\033[92mGOOD => Total ETH less than Minimum ETH: %s < %s\033[0m" % (tot_eth, min_eth)
            score += 1
        else:
            print "\033[91mBAD  => Total ETH greater than Min ETH: %s < %s\033[0m" % (tot_eth, max_eth)

        print
        print "\033[1m" + "Score: %i / 4" % (score)
        if score < 2:
            print "\033[1m" + "Better buy on another day."
        if score == 2:
            print "\033[1m" + "OK, but may not be great."
            self.check_time()
        elif score == 3:
            print "\033[1m" + "Looking good."
            self.check_time()
        else:
            print "\033[1m" + "Perfect Score."
            self.check_time()

    def check_time(self):
        delta = self.stats.time_left()
        seconds = delta.total_seconds()
        minutes = int(seconds/60)
        hours = int(minutes/60)

        if hours > 2:
            print "Wait %s hours and come back again." % (hours)
        elif hours > 1:
            print "Looking good keep an eye on the clock. %s hours to go." % (hours)
        elif minutes > 30:
            print "Getting closer. %s minutes to go." % (minutes)
        elif minutes:
            print "Only %s minutes to go. Time to buy!" % (minutes)

decision = EOSDecisionMaker()

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

plotter = EOSPlot()
plotter.bar_daily_ico()
print "Use your browser to open eth_totals.svg for an interactive chart."
