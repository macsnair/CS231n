import numpy as np


def affine_forward(x, w, b):
  """
  Computes the forward pass for an affine (fully-connected) layer.

  The input x has shape (N, d_1, ..., d_k) and contains a minibatch of N
  examples, where each example x[i] has shape (d_1, ..., d_k). We will
  reshape each input into a vector of dimension D = d_1 * ... * d_k, and
  then transform it to an output vector of dimension M.

  Inputs:
  - x: A numpy array containing input data, of shape (N, d_1, ..., d_k)
  - w: A numpy array of weights, of shape (D, M)
  - b: A numpy array of biases, of shape (M,)
  
  Returns a tuple of:
  - out: output, of shape (N, M)
  - cache: (x, w, b)
  """
  out = None
  #############################################################################
  # TODO: Implement the affine forward pass. Store the result in out. You     #
  # will need to reshape the input into rows.                                 #
  #############################################################################
  N = x.shape[0]
  out = np.reshape(x, (N,-1)).dot(w) + b
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x, w, b)
  return out, cache


def affine_backward(dout, cache):
  """
  Computes the backward pass for an affine layer.

  Inputs:
  - dout: Upstream derivative, of shape (N, M)
  - cache: Tuple of:
    - x: Input data, of shape (N, d_1, ... d_k)
    - w: Weights, of shape (D, M)

  Returns a tuple of:
  - dx: Gradient with respect to x, of shape (N, d1, ..., d_k)
  - dw: Gradient with respect to w, of shape (D, M)
  - db: Gradient with respect to b, of shape (M,)
  """
  x, w, b = cache
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the affine backward pass.                                 #
  #############################################################################
  N = x.shape[0]  
  dx = dout.dot(w.T).reshape(x.shape)
  dw = np.reshape(x, (N,-1)).T.dot(dout)
  db = np.sum(dout, axis = 0)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def relu_forward(x):
  """
  Computes the forward pass for a layer of rectified linear units (ReLUs).

  Input:
  - x: Inputs, of any shape

  Returns a tuple of:
  - out: Output, of the same shape as x
  - cache: x
  """
  out = None
  #############################################################################
  # TODO: Implement the ReLU forward pass.                                    #
  #############################################################################
  out = np.copy(x)  ## Attention! if do not use copy, then modify out can modify x!
  out[x < 0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = x
  return out, cache


def relu_backward(dout, cache):
  """
  Computes the backward pass for a layer of rectified linear units (ReLUs).

  Input:
  - dout: Upstream derivatives, of any shape
  - cache: Input x, of same shape as dout

  Returns:
  - dx: Gradient with respect to x
  """
  dx, x = None, cache
  #############################################################################
  # TODO: Implement the ReLU backward pass.                                   #
  #############################################################################
  dx = np.copy(dout)
  dx[x < 0] = 0
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def batchnorm_forward(x, gamma, beta, bn_param):
  """
  Forward pass for batch normalization.
  
  During training the sample mean and (uncorrected) sample variance are
  computed from minibatch statistics and used to normalize the incoming data.
  During training we also keep an exponentially decaying running mean of the mean
  and variance of each feature, and these averages are used to normalize data
  at test-time.

  At each timestep we update the running averages for mean and variance using
  an exponential decay based on the momentum parameter:

  running_mean = momentum * running_mean + (1 - momentum) * sample_mean
  running_var = momentum * running_var + (1 - momentum) * sample_var

  Note that the batch normalization paper suggests a different test-time
  behavior: they compute sample mean and variance for each feature using a
  large number of training images rather than using a running average. For
  this implementation we have chosen to use running averages instead since
  they do not require an additional estimation step; the torch7 implementation
  of batch normalization also uses running averages.

  Input:
  - x: Data of shape (N, D)
  - gamma: Scale parameter of shape (D,)
  - beta: Shift paremeter of shape (D,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features

  Returns a tuple of:
  - out: of shape (N, D)
  - cache: A tuple of values needed in the backward pass
  """
  mode = bn_param['mode']
  eps = bn_param.get('eps', 1e-5)
  momentum = bn_param.get('momentum', 0.9)

  N, D = x.shape
  running_mean = bn_param.get('running_mean', np.zeros(D, dtype=x.dtype))
  running_var = bn_param.get('running_var', np.zeros(D, dtype=x.dtype))

  out, cache = None, None
  if mode == 'train':
    #############################################################################
    # TODO: Implement the training-time forward pass for batch normalization.   #
    # Use minibatch statistics to compute the mean and variance, use these      #
    # statistics to normalize the incoming data, and scale and shift the        #
    # normalized data using gamma and beta.                                     #
    #                                                                           #
    # You should store the output in the variable out. Any intermediates that   #
    # you need for the backward pass should be stored in the cache variable.    #
    #                                                                           #
    # You should also use your computed sample mean and variance together with  #
    # the momentum variable to update the running mean and running variance,    #
    # storing your result in the running_mean and running_var variables.        #
    #############################################################################
    mu = np.mean(x, axis = 0)
    sigma = np.var(x, axis = 0)

    running_mean = momentum * running_mean + (1 - momentum) * mu
    running_var = momentum * running_var + (1 - momentum) * sigma
    
    inv_sqrt_sigma = 1./np.sqrt(sigma + eps)
    x_cen = x - mu
    x_hat = x_cen * inv_sqrt_sigma
    out = gamma * x_hat + beta
    cache = (gamma, x_cen, inv_sqrt_sigma, eps, x_hat, x)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  elif mode == 'test':
    #############################################################################
    # TODO: Implement the test-time forward pass for batch normalization. Use   #
    # the running mean and variance to normalize the incoming data, then scale  #
    # and shift the normalized data using gamma and beta. Store the result in   #
    # the out variable.                                                         #
    #############################################################################
    sample_mean = running_mean   # here we should use 'running mean'
    sample_var = running_var
    x_hat = (x - sample_mean) / (np.sqrt(sample_var + eps))
    out = gamma * x_hat + beta
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################
  else:
    raise ValueError('Invalid forward batchnorm mode "%s"' % mode)

  # Store the updated running means back into bn_param
  bn_param['running_mean'] = running_mean
  bn_param['running_var'] = running_var

  return out, cache


def batchnorm_backward(dout, cache):
  """
  Backward pass for batch normalization.
  
  For this implementation, you should write out a computation graph for
  batch normalization on paper and propagate gradients backward through
  intermediate nodes.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, D)
  - cache: Variable of intermediates from batchnorm_forward.
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs x, of shape (N, D)
  - dgamma: Gradient with respect to scale parameter gamma, of shape (D,)
  - dbeta: Gradient with respect to shift parameter beta, of shape (D,)
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #############################################################################
  gamma, x_cen, inv_sqrt_sigma, eps, x_hat, x = cache
  m = x.shape[0]
  dx_hat = dout  * gamma
  dvar = -0.5 * np.sum(dx_hat * x_cen * inv_sqrt_sigma**3, axis = 0)
  dmu = -np.sum(dx_hat * inv_sqrt_sigma, axis = 0) -2 * dvar * np.sum(x_cen, axis = 0) / m
  dx = dx_hat *inv_sqrt_sigma + (dvar * 2 * x_cen + dmu) / m
  dgamma = np.sum(dout * x_hat, axis = 0)
  dbeta = np.sum(dout, axis = 0)  
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta


def batchnorm_backward_alt(dout, cache):
  """
  Alternative backward pass for batch normalization.
  
  For this implementation you should work out the derivatives for the batch
  normalizaton backward pass on paper and simplify as much as possible. You
  should be able to derive a simple expression for the backward pass.
  
  Note: This implementation should expect to receive the same cache variable
  as batchnorm_backward, but might not use all of the values in the cache.
  
  Inputs / outputs: Same as batchnorm_backward
  """
  dx, dgamma, dbeta = None, None, None
  #############################################################################
  # TODO: Implement the backward pass for batch normalization. Store the      #
  # results in the dx, dgamma, and dbeta variables.                           #
  #                                                                           #
  # After computing the gradient with respect to the centered inputs, you     #
  # should be able to compute gradients with respect to the inputs in a       #
  # single statement; our implementation fits on a single 80-character line.  #
  #############################################################################
  pass 
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  
  return dx, dgamma, dbeta


def dropout_forward(x, dropout_param):
  """
  Performs the forward pass for (inverted) dropout.

  Inputs:
  - x: Input data, of any shape
  - dropout_param: A dictionary with the following keys:
    - p: Dropout parameter. We drop each neuron output with probability p.
    - mode: 'test' or 'train'. If the mode is train, then perform dropout;
      if the mode is test, then just return the input.
    - seed: Seed for the random number generator. Passing seed makes this
      function deterministic, which is needed for gradient checking but not in
      real networks.

  Outputs:
  - out: Array of the same shape as x.
  - cache: A tuple (dropout_param, mask). In training mode, mask is the dropout
    mask that was used to multiply the input; in test mode, mask is None.
  """
  p, mode = dropout_param['p'], dropout_param['mode']
  if 'seed' in dropout_param:
    np.random.seed(dropout_param['seed'])

  mask = None
  out = None

  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase forward pass for inverted dropout.   #
    # Store the dropout mask in the mask variable.                            #
    ###########################################################################
    mask = np.random.rand(*x.shape) < p
    out = x * mask / p
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    ###########################################################################
    # TODO: Implement the test phase forward pass for inverted dropout.       #
    ###########################################################################
    # When using inverted dropout, just let output equals with the input
    out = x
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################

  cache = (dropout_param, mask)
  out = out.astype(x.dtype, copy=False)

  return out, cache


def dropout_backward(dout, cache):
  """
  Perform the backward pass for (inverted) dropout.

  Inputs:
  - dout: Upstream derivatives, of any shape
  - cache: (dropout_param, mask) from dropout_forward.
  """
  dropout_param, mask = cache
  mode = dropout_param['mode']
  
  dx = None
  if mode == 'train':
    ###########################################################################
    # TODO: Implement the training phase backward pass for inverted dropout.  #
    ###########################################################################
    p = dropout_param['p']
    dx = dout * mask / p
    ###########################################################################
    #                            END OF YOUR CODE                             #
    ###########################################################################
  elif mode == 'test':
    dx = dout
  return dx


def conv_simple_naive(x, w, b):
  """
  A naive method to calculate the convolution of x and w, b
  Input:
  - x: Input data after padding of shape (C, HH, WW)
  - w: Filter weights of shape (C, HH, WW)
  - b: Biase, a scalar
  Returns the result of conv(x, w, b)
  """
  return np.sum(x * w) + b

def conv_forward_naive(x, w, b, conv_param):
  """
  A naive implementation of the forward pass for a convolutional layer.

  The input consists of N data points, each with C channels, height H and width
  W. We convolve each input with F different filters, where each filter spans
  all C channels and has height HH and width HH.

  Input:
  - x: Input data of shape (N, C, H, W)
  - w: Filter weights of shape (F, C, HH, WW)
  - b: Biases, of shape (F,)
  - conv_param: A dictionary with the following keys:
    - 'stride': The number of pixels between adjacent receptive fields in the
      horizontal and vertical directions.
    - 'pad': The number of pixels that will be used to zero-pad the input.

  Returns a tuple of:
  - out: Output data, of shape (N, F, H', W') where H' and W' are given by
    H' = 1 + (H + 2 * pad - HH) / stride
    W' = 1 + (W + 2 * pad - WW) / stride
  - cache: (x, w, b, conv_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the convolutional forward pass.                           #
  # Hint: you can use the function np.pad for padding.                        #
  #############################################################################

  stride = conv_param['stride']
  pad = conv_param['pad']
  (N, C, H, W) = x.shape
  (F, CC, HH, WW) = w.shape
  assert C == CC
  H_ = 1 + (H + 2 * pad - HH) / stride
  W_ = 1 + (W + 2 * pad - WW) / stride
  out_dim = (N, F, H_, W_)
  out = np.zeros(out_dim, dtype = x.dtype)
  # padding the input
  x_pad = np.lib.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)), \
  'constant', constant_values = 0)
  # [delta_H, HH-delta_H + center_y) is the desired x which
  # will convolute with the weight
  delta_H = (HH - 1) / 2   
  delta_W = (WW - 1) / 2
  """
  # This is implemented by myself.
  # some parameters we can easily get or calculate  
  # for each input data
  for n in xrange(N):
    x_1 = x_pad[n, :, :, :]
    # for each filter    
    for f in xrange(F):
      f_1 = w[f, :, :, :]
      for i in xrange(0, H_):
        for j in xrange(0, W_):
          # the center position of current x data          
          # the position should be shifted to get the true position
          # after padding          
          center = (i * stride + pad, j * stride + pad)
          x_conv = x_1[:, \
          center[0] - delta_H : HH - delta_H + center[0], 
          center[1] - delta_W : WW - delta_W + center[1]]
          out[n, f, i, j] = conv_simple_naive(x_conv, f_1, b[f])
  """  
  """
  This implementation is introduced in the slide.
  More memory, but more efficient.
  """
  x_conv = np.zeros((HH * WW * C, H_ * W_))
  # for each input image
  for n in xrange(N):
    cnt_win = 0   # the number of windows that have done convolution
    for i in xrange(H_):
      for j in xrange(W_):
        center = (i * stride + pad, j * stride + pad)
        x_conv[:, cnt_win] = x_pad[n, :, \
        center[0] - delta_H: HH - delta_H + center[0], \
        center[1] - delta_W: WW - delta_W + center[1]].\
        reshape((-1, 1)).squeeze()
        cnt_win += 1
    res_conv = np.dot(w.reshape(F, -1), x_conv) + b.reshape(F, -1)  
    out[n, :, :, :] = res_conv.reshape((F, H_, W_)) 
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  # Add an assertion  
  assert out_dim == out.shape
  cache = (x, w, b, conv_param)
  return out, cache

def conv_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a convolutional layer.

  Inputs:
  - dout: Upstream derivatives.
  - cache: A tuple of (x, w, b, conv_param) as in conv_forward_naive

  Returns a tuple of:
  - dx: Gradient with respect to x
  - dw: Gradient with respect to w
  - db: Gradient with respect to b
  """
  dx, dw, db = None, None, None
  #############################################################################
  # TODO: Implement the convolutional backward pass.                          #
  #############################################################################
  (x, w, b, conv_param) = cache
  stride = conv_param['stride']
  pad = conv_param['pad']
  (N, C, H, W) = x.shape
  (F, CC, HH, WW) = w.shape
  assert C == CC
  H_ = 1 + (H + 2 * pad - HH) / stride
  W_ = 1 + (W + 2 * pad - WW) / stride
  out_dim = (N, F, H_, W_)
  assert out_dim == dout.shape
  delta_H = (HH - 1) / 2   
  delta_W = (WW - 1) / 2
  center_in_template = (delta_H, delta_W)
  # calculate dx
  dx = np.zeros(x.shape)
  for n in xrange(N):
    for c in xrange(C):
      for im_h in xrange(H):
        for im_w in xrange(W):
          # print 'im_h = ', im_h, ' im_w = ', im_w
          dx_1 = 0.0
          # get the templates centers which involves         
          centers = []
          for yy in xrange(im_h - delta_H, im_h - delta_H + HH):
            if yy < 0 or yy >= H:
              continue
            for xx in xrange(im_w - delta_W, im_w - delta_W + WW):
              if xx >= 0 and xx < W:
                centers.append((yy, xx))
          
          for center in centers:
              #print 'center = ', cen
              ii = center[0] / stride
              jj = center[1] / stride
              #print 'ii = ', ii, ' jj = ', jj
              for f in xrange(F):
                # assert ii < H_ and ii >= 0
                # assert jj < W_ and jj >= 0
                row_in_template = center_in_template[0] - (center[0] - im_h)
                col_in_template = center_in_template[1] - (center[1] - im_w)
                #print 'i = ', i, ' j = ', j
                dx_1 += dout[n, f, ii, jj] * w[f, c, row_in_template, col_in_template]
            
          dx[n, c, im_h, im_w] = dx_1
  
  # calculate dw
  dw = np.zeros(w.shape)
  for f in xrange(F):
    for c in xrange(C):
      for t_h in xrange(HH):
        for t_w in xrange(WW):
          dw_1 = 0.0
          diff = (t_h - center_in_template[0], t_w - center_in_template[1])
          # slide the template in the image
          for i in xrange(H_):
            for j in xrange(W_):
              center = (i * stride, j * stride)
              x_position = (center[0] + diff[0], center[1] + diff[1])
              if x_position[0] >= 0 and x_position[0] < H \
              and x_position[1] >= 0 and x_position[1] < W:
                for n in xrange(N):
                  dw_1 += dout[n, f, i, j] * x[n, c, x_position[0], x_position[1]]
          dw[f, c, t_h, t_w] = dw_1
  
  # calculate db
  db = np.sum(np.sum(np.sum(dout, axis = 0), axis = 1), axis = 1)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx, dw, db


def max_pool_forward_naive(x, pool_param):
  """
  A naive implementation of the forward pass for a max pooling layer.

  Inputs:
  - x: Input data, of shape (N, C, H, W)
  - pool_param: dictionary with the following keys:
    - 'pool_height': The height of each pooling region
    - 'pool_width': The width of each pooling region
    - 'stride': The distance between adjacent pooling regions

  Returns a tuple of:
  - out: Output data
  - cache: (x, pool_param)
  """
  out = None
  #############################################################################
  # TODO: Implement the max pooling forward pass                              #
  #############################################################################
  ph = pool_param['pool_height']
  pw = pool_param['pool_width']
  stride = pool_param['stride']  
  
  N, C, H, W = x.shape
  H_, W_ = (H - ph) / stride + 1, (W - pw) / stride + 1  
  out = np.zeros((N, C, H_, W_), dtype = x.dtype)
  max_idx = np.zeros((N, C, H_, W_, 2))
  
  for n in xrange(N):
    for c in xrange(C):
      for ih in xrange(H_):
        tl_y = stride * ih
        for iw in xrange(W_):
          tl_x = stride * iw
          data = x[n, c, tl_y: tl_y + stride, tl_x : tl_x + stride]
          # we can record the position of the maximum element for backward
          max_cnt = np.argmax(data)
          max_pos = max_cnt / pw + tl_y, max_cnt % pw + tl_x
          max_idx[n, c, ih, iw, 0], max_idx[n, c, ih, iw, 1] = max_pos[0], max_pos[1]
          out[n, c, ih, iw] = x[n, c, max_pos[0], max_pos[1]]
                    
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  cache = (x.shape, max_idx)
  return out, cache


def max_pool_backward_naive(dout, cache):
  """
  A naive implementation of the backward pass for a max pooling layer.

  Inputs:
  - dout: Upstream derivatives
  - cache: A tuple of (x, pool_param) as in the forward pass.

  Returns:
  - dx: Gradient with respect to x
  """
  dx = None
  #############################################################################
  # TODO: Implement the max pooling backward pass                             #
  #############################################################################
  x_shape, max_idx = cache
 
  N, C, H_, W_, _ = max_idx.shape
  
  dx = np.zeros(x_shape)
  for n in xrange(N):
    for c in xrange(C):
      for fh in xrange(H_):
        for fw in xrange(W_):
          row, col = max_idx[n, c, fh, fw, 0], max_idx[n, c, fh, fw, 1]
          dx[n, c, row, col] = dout[n, c, fh, fw]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  return dx


def spatial_batchnorm_forward(x, gamma, beta, bn_param):
  """
  Computes the forward pass for spatial batch normalization.
  
  Inputs:
  - x: Input data of shape (N, C, H, W)
  - gamma: Scale parameter, of shape (C,)
  - beta: Shift parameter, of shape (C,)
  - bn_param: Dictionary with the following keys:
    - mode: 'train' or 'test'; required
    - eps: Constant for numeric stability
    - momentum: Constant for running mean / variance. momentum=0 means that
      old information is discarded completely at every time step, while
      momentum=1 means that new information is never incorporated. The
      default of momentum=0.9 should work well in most situations.
    - running_mean: Array of shape (D,) giving running mean of features
    - running_var Array of shape (D,) giving running variance of features
    
  Returns a tuple of:
  - out: Output data, of shape (N, C, H, W)
  - cache: Values needed for the backward pass
  """
  out, cache = None, None

  #############################################################################
  # TODO: Implement the forward pass for spatial batch normalization.         #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N, C, H, W = x.shape  
  x_tran = np.transpose(x, (0, 2, 3, 1)).reshape(N * H * W, C)
  out, cache = batchnorm_forward(x_tran, gamma, beta, bn_param)
  out = np.reshape(out, (N, H, W, C)).transpose((0, 3, 1, 2))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return out, cache


def spatial_batchnorm_backward(dout, cache):
  """
  Computes the backward pass for spatial batch normalization.
  
  Inputs:
  - dout: Upstream derivatives, of shape (N, C, H, W)
  - cache: Values from the forward pass
  
  Returns a tuple of:
  - dx: Gradient with respect to inputs, of shape (N, C, H, W)
  - dgamma: Gradient with respect to scale parameter, of shape (C,)
  - dbeta: Gradient with respect to shift parameter, of shape (C,)
  """
  dx, dgamma, dbeta = None, None, None

  #############################################################################
  # TODO: Implement the backward pass for spatial batch normalization.        #
  #                                                                           #
  # HINT: You can implement spatial batch normalization using the vanilla     #
  # version of batch normalization defined above. Your implementation should  #
  # be very short; ours is less than five lines.                              #
  #############################################################################
  N, C, H, W = dout.shape   
  dout = dout.transpose((0, 2, 3, 1)).reshape((N * H * W, C))
  dx, dgamma, dbeta = batchnorm_backward(dout, cache)
  dx = dx.reshape((N, H, W, C)).transpose((0, 3, 1, 2))
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return dx, dgamma, dbeta
  

def svm_loss(x, y):
  """
  Computes the loss and gradient using for multiclass SVM classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  N = x.shape[0]
  correct_class_scores = x[np.arange(N), y]
  margins = np.maximum(0, x - correct_class_scores[:, np.newaxis] + 1.0)
  margins[np.arange(N), y] = 0
  loss = np.sum(margins) / N
  num_pos = np.sum(margins > 0, axis=1)
  dx = np.zeros_like(x)
  dx[margins > 0] = 1
  dx[np.arange(N), y] -= num_pos
  dx /= N
  return loss, dx


def softmax_loss(x, y):
  """
  Computes the loss and gradient for softmax classification.

  Inputs:
  - x: Input data, of shape (N, C) where x[i, j] is the score for the jth class
    for the ith input.
  - y: Vector of labels, of shape (N,) where y[i] is the label for x[i] and
    0 <= y[i] < C

  Returns a tuple of:
  - loss: Scalar giving the loss
  - dx: Gradient of the loss with respect to x
  """
  probs = np.exp(x - np.max(x, axis=1, keepdims=True))
  probs /= np.sum(probs, axis=1, keepdims=True)
  N = x.shape[0]
  
  loss = -np.sum(np.log(probs[np.arange(N), y])) / N
  dx = probs.copy()
  dx[np.arange(N), y] -= 1
  dx /= N
  return loss, dx
