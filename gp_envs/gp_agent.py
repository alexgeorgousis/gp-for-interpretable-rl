import gym
import numpy as np

class GPAgent:
    """
    GP template class. Implements all the functionality of a GP agent 
    for a gym environment and is parameterised by a data object with
    the parameters for a specific environment. 
    """

    def __init__(self, info):
        self.env_name = info["env_name"]
        
        # Program structure params
        self.T = info["T"]
        self.F = info["F"]
        self.max_d = info["max_depth"]
        self.growth_rate = info["term_growth_rate"]  # probability of growing a terminal instead of a function
        
        # GP experiment params
        self.n = info["pop_size"]
        self.num_eps = info["num_eps"]
        self.max_gens = info["max_gens"]
        self.term_fit = info["term_fit"]

    def run(self):
        best_program = self._train()
        
        env = gym.make(self.env_name)
        obs = env.reset()
        net_reward = 0
        done = False

        while not done:
            # env.render()
            action = self._eval(best_program, obs)
            obs, rew, done, _ = env.step(action)
            net_reward += rew
        
        print("Net reward: {}".format(net_reward))
        env.close()

    def _train(self):
        best_program = []

        # Generate initial population
        init_pop = [self._gen_prog(self.max_d, 'grow') for _ in range(self.n)]
        for p in init_pop:
            print(p)

        # Evolution loop

        return best_program

    def _eval(self, p, obs):
        return 0

    def _gen_prog(self, max_d, method, type="Action"):
        """
        Generates a random program with a fixed max depth using the terminal and function sets. 
        Supported methods: full and growth.

        max_d: maximum program depth
        method: "grow" | "full"
        """
        
        prog = None

        # Pick random terminal
        if max_d == 0 or (method == "grow" and self.growth_rate > np.random.rand()):
            # Only choose from the terminals that have the correct type
            filt_terms = list(dict(filter(lambda term: term[1]["type"]==type, self.T.items())).keys())
            prog = np.random.choice(filt_terms)
        else:
            # Pick random function and recursively generate random arguments for it
            func = np.random.choice(list(self.F.keys()))
            arity = self.F[func]["arity"]
            args = [self._gen_prog(max_d-1, method) for _ in range(arity)]
            prog = [func] + args

        return prog
