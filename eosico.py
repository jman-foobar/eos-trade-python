
"""
Description - Class to capture the ICO values found in the json file from eos.io website
"""

class EosIco():
    def __init__(self, sale_id, eos_created_on_day, daily_total_eth, price, begins, ends):
        self.sale_id = sale_id			        #int
        self.eos_created_on_day = eos_created_on_day    #int
	self.daily_total_eth = daily_total_eth 	        #float
        self.price = price                              #float
	self.begins = begins	                        #datetime
	self.ends = ends	                        #datetime

    def __repr__(self):
        return "id: %i, total eos created %i, daily total eth: %f, price: %f, begins: %s, ends: %s" % (
                                                        self.sale_id,
							self.eos_created_on_day,
                                                        self.daily_total_eth,
                                                        self.price,
							self.begins,
							self.ends,
                                                        )
    """
    Returns the EOS formula a * (b/c)
    a = Total ETH contributed by an authorized purchaser during the period.
    b = Total number of EOS Tokens available for distribution in the period.
    c = Total ETH contributed by all authorized purchasers during the period.
    With no values provided calculates what 1 ETH purchased on that period.
    """
    def eos_formula(self, individual_eth_contributed=1, eos_created_on_day=None, daily_total_eth=None):
        if eos_created_on_day == None:
            eos_created_on_day = self.eos_created_on_day
        if daily_total_eth == None:
            daily_total_eth = self.daily_total_eth
        return individual_eth_contributed * (eos_created_on_day/daily_total_eth)
