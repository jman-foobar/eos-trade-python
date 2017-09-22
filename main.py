from eosstats import EOSStats

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

