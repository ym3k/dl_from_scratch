# coding: utf-8
import numpy as np

class SGD:

    """確率的勾配降下法（Stochastic Gradient Descent）"""

    def __init__(self, lr=0.01):
        self.lr = lr
        
    def update(self, params, grads):
        for key in params.keys():
            params[key] -= self.lr * grads[key] 


class Momentum:

    """Momentum SGD"""

    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None
        
    def update(self, params, grads):
        if self.v is None:
            self.v = {}
            for key, val in params.items():                                
                self.v[key] = np.zeros_like(val)
                
        for key in params.keys():
            self.v[key] = self.momentum*self.v[key] - self.lr*grads[key] 
            params[key] += self.v[key]


class Nesterov:

    """Nesterov's Accelerated Gradient (http://arxiv.org/abs/1212.0901)"""

    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.v = None
        
    def update(self, params, grads):
        if self.v is None:
            self.v = {}
            for key, val in params.items():
                self.v[key] = np.zeros_like(val)
            
        for key in params.keys():
            self.v[key] *= self.momentum
            self.v[key] -= self.lr * grads[key]
            params[key] += self.momentum * self.momentum * self.v[key]
            params[key] -= (1 + self.momentum) * self.lr * grads[key]


class AdaGrad:

    """AdaGrad"""

    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None
        
    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            for key, val in params.items():
                self.h[key] = np.zeros_like(val)
            
        for key in params.keys():
            self.h[key] += grads[key] * grads[key]
            params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key]) + 1e-7)


class RMSprop:

    """RMSprop (lr is 0.001 is the best.)"""

    def __init__(self, lr=0.001, decay_rate = 0.99):
        self.lr = lr
        self.decay_rate = decay_rate
        self.h = None
        
    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            for key, val in params.items():
                self.h[key] = np.zeros_like(val)
            
        for key in params.keys():
            self.h[key] *= self.decay_rate
            self.h[key] += (1 - self.decay_rate) * grads[key] * grads[key]
            params[key] -= self.lr * grads[key] / (np.sqrt(self.h[key]) + 1e-7)


class Adam:

    """Adam (http://arxiv.org/abs/1412.6980v8)"""

    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.iter = 0
        self.m = None
        self.v = None
        
    def update(self, params, grads):
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)
        
        self.iter += 1
        lr_t  = self.lr * np.sqrt(1.0 - self.beta2**self.iter) / (1.0 - self.beta1**self.iter)         
        
        for key in params.keys():
            #self.m[key] = self.beta1*self.m[key] + (1-self.beta1)*grads[key]
            #self.v[key] = self.beta2*self.v[key] + (1-self.beta2)*(grads[key]**2)
            self.m[key] += (1 - self.beta1) * (grads[key] - self.m[key])
            self.v[key] += (1 - self.beta2) * (grads[key]**2 - self.v[key])
            
            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + 1e-7)
            
            #unbias_m += (1 - self.beta1) * (grads[key] - self.m[key]) # correct bias
            #unbisa_b += (1 - self.beta2) * (grads[key]*grads[key] - self.v[key]) # correct bias
            #params[key] += self.lr * unbias_m / (np.sqrt(unbisa_b) + 1e-7)

class SDprop:
    
    """SDProp
    Adaptive Learning Rate via Covariance Matrix Based Preconditioning for Deep Neural Networks
    (https://www.ijcai.org/proceedings/2017/0267.pdf)
    """
    
    def __init__(self, lr=0.001, gamma=0.99, bias_correction=True):
        self.lr = lr
        self.gamma = gamma
        self.bs = bias_correction
        # m : μ,  c : C**2, iter: timestep
        self.m = None
        self.c = None
        self.iter = 0
    
    def update(self, params, grads):
        if self.m is None:
            self.m, self.c = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.c[key] = np.zeros_like(val)
        
        if self.bs is True:
            self.iter += 1
            lr_t = self.lr * np.sqrt(1.0 - self.gamma**self.iter)
        
        for key in params.keys():
            self.c[key] *= self.gamma
            self.c[key] += self.gamma * (1 - self.gamma) * (grads[key] - self.m[key])**2
            # c(i,t) に代入しているのが μ(i,t-1)のため、cを更新したあとでmを更新する
            self.m[key] *= self.gamma
            self.m[key] += (1 - self.gamma) * grads[key]
            if self.bs is True:
                params[key] -= lr_t * grads[key] / (np.sqrt(self.c[key]) + 1e-8)
            else:
                params[key] -= self.lr * grads[key] / (np.sqrt(self.c[key]) + 1e-8)
                
class Adastand:

    """Adastand"""

    def __init__(self, lr=0.001, beta1=0.7, beta2=0.99, epsilon=1e-7):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.iter = 0
        self.m = None
        self.v = None
        
    def update(self, params, grads):
        if self.m is None:
            self.m, self.v = {}, {}
            for key, val in params.items():
                self.m[key] = np.zeros_like(val)
                self.v[key] = np.zeros_like(val)
        
        self.iter += 1
        lr_t  = self.lr * np.sqrt(1.0 - self.beta2**self.iter) / (1.0 - self.beta1**self.iter)         
        
        for key in params.keys():
            # m, vのインクリメント処理はAdamと逆
            #self.v[key] = self.beta2*self.v[key] + self.beta2*(1-self.beta2)*(grads[key]-self.m[key])
            #self.m[key] = self.beta1*self.m[key] + (1-self.beta1)*(grads[key]-self.m[key])
            self.v[key] += (1 - self.beta2) * (self.beta2 * (grads[key] - self.m[key])**2 - self.v[key])
            self.m[key] += (1 - self.beta1) * (grads[key] - 2 * self.m[key])
            
            params[key] -= lr_t * self.m[key] / (np.sqrt(self.v[key]) + self.epsilon)
            
            #unbias_m += (1 - self.beta1) * (grads[key] - self.m[key]) # correct bias
            #unbisa_b += (1 - self.beta2) * (grads[key]*grads[key] - self.v[key]) # correct bias
            #params[key] += self.lr * unbias_m / (np.sqrt(unbisa_b) + 1e-7)