# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 17:13:20 2021

@author: chris
"""
from abc import ABC, abstractmethod
import random
import logic.helper as hlp

MAX_POOLS = 10  # max number of pools that a stakeholder can open (when pool splitting is allowed)


class Strategy(ABC):

    @abstractmethod
    def __init__(self, stake_allocations, is_pool_operator):
        self.stake_allocations = stake_allocations
        self.is_pool_operator = is_pool_operator

    @abstractmethod
    def create_random_operator_strategy(self, pools, player_id, player_stake):
        pass

    @abstractmethod
    def create_random_delegator_strategy(self, pools, player_id, player_stake):
        pass


class SinglePoolStrategy(Strategy):
    def __init__(self, pledge=-1, margin=-1, stake_allocations=[], is_pool_operator=False):
        super().__init__(stake_allocations, is_pool_operator)
        self.pledge = pledge
        self.margin = margin
        # maybe also have a "last_update" field? to perform updates more easily

    def create_random_operator_strategy(self, pools, player_id, player_stake):
        margin = random.random()
        stake_allocations = [0 for i in range(len(pools))]
        pledge = stake_allocations[player_id] = player_stake  # assume that pledge == α_i
        return SinglePoolStrategy(pledge, margin, stake_allocations, True)

    def create_random_delegator_strategy(self, pools, player_id, player_stake):
        # stake allocations must sum to (at most) the player's stake
        stake_allocations = [random.random() if (i != player_id and pool is not None) else 0
                             for i, pool in enumerate(pools)]
        stake_allocations = hlp.normalize_distr(stake_allocations, normal_sum=player_stake)
        return SinglePoolStrategy(stake_allocations=stake_allocations, is_pool_operator=False)

    def set_random_strategy(self, n_pools):
        self.pledge = random.random()
        self.margin = random.random()
        self.stake_allocations = [random.random() for pool in range(n_pools)]
        # maybe stake allocations better as hashmap/dict? otherwise very sparse

        return self

    def print_(self):
        print("Pledge: {} \n Margin: {} \n Allocations: {}"
              .format(self.pledge, self.margin, self.stake_allocations))


class MultiPoolStrategy(Strategy):
    def __init__(self, number_of_pools=0, pool_pledges=[], pool_margins=[], stake_allocations=[], is_pool_operator=False):
        super().__init__(stake_allocations, is_pool_operator)
        self.number_of_pools = number_of_pools
        self.pool_pledges = pool_pledges
        self.pool_margins = pool_margins
        # maybe also have a "last_update" field? to perform updates more easily 

    def create_random_operator_strategy(self, pools, player_id, player_stake):
        num_of_player_pools = random.randint(0, MAX_POOLS)
        # pledges = [random.random() for pool in range(num_of_player_pools)]
        margins = [random.random() for pool in range(num_of_player_pools)]
        # todo sums <= self.stake
        pools_tmp = pools.copy()
        pools_tmp[player_id] = [None for pool in range(num_of_player_pools)]
        # stake alloations must sum to (at most) the player's stake
        stake_allocations = [[random.random() if (i == player_id or pool is not None) else 0
                              for pool in pool_group] for i, pool_group in enumerate(pools_tmp)]
        # todo normalize allocations properly (respecting the #pools of each player)
        # stake_allocations = hlp.normalize_distr(stake_allocations, normal_sum=player_stake)
        pledges = stake_allocations[player_id]  # assume that pledge == α_i
        return MultiPoolStrategy(num_of_player_pools, pledges, margins, stake_allocations)

    def create_random_delegator_strategy(self, pools, player_id, player_stake):
        num_of_player_pools = random.randint(0, MAX_POOLS)
        # pledges = [random.random() for pool in range(num_of_player_pools)]
        margins = [random.random() for pool in range(num_of_player_pools)]
        # todo sums <= self.stake
        pools_tmp = pools.copy()
        pools_tmp[player_id] = [None for pool in range(num_of_player_pools)]
        # stake alloations must sum to (at most) the player's stake
        stake_allocations = [[random.random() if (i == player_id or pool is not None) else 0
                              for pool in pool_group] for i, pool_group in enumerate(pools_tmp)]
        # todo normalize allocations properly (respecting the #pools of each player)
        # stake_allocations = hlp.normalize_distr(stake_allocations, normal_sum=player_stake)
        pledges = stake_allocations[player_id]  # assume that pledge == α_i
        return MultiPoolStrategy(num_of_player_pools, pledges, margins, stake_allocations)

    ''' 
    Creates a random **not necessarily valid** strategy
    '''

    def set_random_strategy(self, n_pools):
        self.number_of_pools = random.randint(0, MAX_POOLS)
        self.pool_pledges = [random.random() for pool in range(self.number_of_pools)]
        self.pool_margins = [random.random() for pool in range(self.number_of_pools)]
        self.stake_allocations = [random.random() for pool in range(n_pools)]

        return self

    def print_(self):
        print("Number of pools owned: {} \n Pledges: {} \n Margins: {} \n Allocations: {}"
              .format(self.number_of_pools, self.pool_pledges, self.pool_margins, self.stake_allocations))
