# -*- coding: utf-8 -*-
"""Project1_ECE590.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SBx6IND3UU6j-ubcB38_tCqOqBlWmc1b
"""

# Commented out IPython magic to ensure Python compatibility.
# %reset
import numpy as np
import matplotlib.pyplot as plt

def square_mutual_inductance(segments:int):

  # Initialize Variables
  side = int(segments / 4) # segments per side
  N = segments
  a = 0.02 # m (Side length)
  b = 0.005 # m (Distance between loops)
  M = 0 # mutual inductance initialized to 0


  # Coordinates for loop 1 segments (Peacewise concatenation)
  L1_x = np.concatenate([np.linspace(0, a, side+1,endpoint=False)[1:],                              # First Peacewise varies values between 0 to a
                         np.full(side, a),                                                          # second peacewise sets values = a
                         np.linspace(0, a, side+1,endpoint=False)[::-1][:-1],                       # third peacewise varies values between a to 0
                         np.full(side, 0)])                                                         # fourth peacewise sets values equal to 0

  L1_y = np.concatenate([np.full(side, a),                                                          # sets y to a
                         np.linspace(0, a, side,endpoint=False)[::-1],                              # varys y from a to 0
                         np.full(side, 0),                                                          # sets values to 0
                         np.linspace(0, a, side,endpoint=False)                                     # varys values from 0 to a
                         ])
  L1_z = 0

  # Coordinates for loop 2 segments (Peacewise concatenation)
  L2_x = np.concatenate([np.linspace(a + b, (2 * a) + b, side+1,endpoint=False)[1:],                # First Peacewise varies x between a + b to 2a + b
                         np.full(side, (2 * a) + b),                                                # second peacewise sets values = 2a + b
                         np.linspace((a + b), ((2 * a) + b),side+1,endpoint=False)[::-1][:-1],      # third Peacewise varies x between 2a + b to a + b
                         np.full(side, a + b)                                                       # fourth peacewise sets values = a + b
                         ]) # X coordinates of Loop 2 starting top left

  L2_y = np.concatenate([np.full(side, a),                                                          # ...
                         np.linspace(0, a, side, endpoint=False)[::-1],
                         np.full(side, 0),
                         np.linspace(0, a, side, endpoint=False)
                         ])

  L2_z = 0

  M = 0
  for i in range(N): # Summation for loop 1
    dl1 = np.array([L1_x[(i+1) % N]-L1_x[i], L1_y[(i+1) % N]-L1_y[i], L1_z])
    for j in range(N): # Summation for loop 2
      dl2 = np.array([L2_x[(j+1) % N]-L2_x[j], L2_y[(j+1) % N]-L2_y[j], L2_z])
      r = np.array([L2_x[(j)%N]-L1_x[(i)%N], L2_y[(j)%N]-L1_y[(i)%N], b])
      M += (dl1 @ dl2) / np.linalg.norm(r)

  # Multiply Constants
  M *= (4*np.pi*(10**-7)) / (4 * np.pi)

  return M



def circle_mutual_inductance(segments:int, a, b):
  N = segments

  # Gen evenly spaced theta
  theta = np.linspace(0, 2 * np.pi, N, endpoint=False)

  # Loop 1
  L1_x = a * np.cos(theta)
  L1_y = a * np.sin(theta)
  L1_z = 0

  # Loop 2
  L2_x = a * np.cos(theta) + b
  L2_y = a * np.sin(theta)
  L2_z = 0

  M = 0
  for i in range(N): # Summation for loop 1
    dl1 = np.array([L1_x[(i+1) % N]-L1_x[i], L1_y[(i+1) % N]-L1_y[i], L1_z])
    for j in range(N): # Summation for loop 2
      dl2 = np.array([L2_x[(j+1) % N]-L2_x[j], L2_y[(j+1) % N]-L2_y[j], L2_z])
      r = np.array([L2_x[(j+1)%N]-L1_x[(i+1)%N], L2_y[(j+1)%N]-L1_y[(i+1)%N], b])
      M += (dl1 @ dl2) / np.linalg.norm(r)

  # Multiply Constants
  M *= (4*np.pi*(10**-7)) / (4 * np.pi)

  return M

def coaxial_mutual_inductance(segments:int,a,b):
  N = segments
  M = 0 # mutual inductance initialized to 0

  #Gen evenly spaced theta
  theta = np.linspace(0, 2 * np.pi, N, endpoint=False)

  # Loop 1
  L1_x = a * np.cos(theta)
  L1_y = a * np.sin(theta)
  L1_z = 0
  # Loop 2
  L2_x = a * np.cos(theta)
  L2_y = a * np.sin(theta)
  L2_z = b

  M = 0
  for i in range(N): # Summation for loop 1
    dl1 = np.array([L1_x[(i+1) % N]-L1_x[i], L1_y[(i+1) % N]-L1_y[i], L1_z])
    for j in range(N): # Summation for loop 2
      dl2 = np.array([L2_x[(j+1) % N]-L2_x[j], L2_y[(j+1) % N]-L2_y[j], L2_z])
      r = np.array([L2_x[(j+1)%N]-L1_x[(i+1)%N], L2_y[(j+1)%N]-L1_y[(i+1)%N], b])
      M += (dl1 @ dl2) / np.linalg.norm(r)

  # Multiply Constants
  M *= (4*np.pi*(10**-7)) / (4 * np.pi)

  return M

def plot_convergence(N,M):

  # Set plotting Parameters
  plt.figure(figsize=(4, 2))
  plt.plot(N, M, color='blue', linewidth=2)

  # Labelling
  plt.title('Mutual Inductance Convergence')
  plt.xlabel('Number of Segments')
  plt.ylabel('Mutual Inductance')

  # Display Plot
  plt.show

# Parameters
a = 0.02  # Side length of the square loops
b = 0.005  # Distance between the loops

# Coordinates for Loop 1
x1 = np.array([0, 0, a, a, 0])
y1 = np.array([0, a, a, 0, 0])

# Coordinates for Loop 2
x2 = x1 + (a + b)
y2 = y1

# Plot the loops
plt.figure(figsize=(4, 2))
plt.plot(x1, y1, label='Loop 1', color='blue')
plt.plot(x2, y2, label='Loop 2', color='red')

# Plot settings
plt.title('Two Square Loops in X/Y plane')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()

"""Problem Overview:

Part 1: Two square loops in X/Y plane
"""

M = []
N = []
for i in range(1,50):
  segments = 4*i
  M.append(square_mutual_inductance(segments))
  N.append(segments)
plot_convergence(N,M)

"""Problem Overview:

Part 2: Two circular loops in X/Y plane
"""

M = []
N = []
a = 2 / 100 * np.sqrt(np.pi) # m (Loop Radius)
b = 0.025 # m (Distance between center of loops)
for i in range(1,50):
  segments = 4*i
  M.append(circle_mutual_inductance(segments,a,b))
  N.append(segments)
plot_convergence(N,M)

"""

```
Problem Overview:

Part 2: Two coaxial loops in X/Y plane seperated in Z plane
```

"""

M = []
N = []
a = 0.02 # m (Loop Radius)
b = 0.02 # m (Distance between center of loops)
for i in range(1,50):
  segments = 4*i
  M.append(coaxial_mutual_inductance(segments,a,b))
  N.append(segments)
plot_convergence(N,M)