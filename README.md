# Advanced Atwood Machine: 3D Physics Simulation
**St. John Baptist De La Salle Catholic School - Grade 11 Physics**

## Project Overview
This project is a 3D computational model of an Advanced Atwood Machine featuring a coupled system on a rough inclined plane. Instead of using standard algebraic kinematics, this simulation utilizes **Euler’s Numerical Integration** to calculate motion dynamically over infinitesimal time steps ($dt = 0.001s$).

![Simulation Demo](simulation.gif) 

## Key Features
* **Interactive Parameters:** Real-time adjustment of masses ($m1$, $m2$), coefficient of friction ($\mu$), and incline angle ($\theta$).
* **Numerical Calculus:** Uses a discrete integration loop to update acceleration, velocity, and position.
* **Friction Logic:** Accurately models the transition between Static and Kinetic friction, including a breakout threshold.
* **Live Graphing:** Real-time plots for Velocity vs. Time and Acceleration vs. Time.

## The Calculus Behind the Model
The simulation solves the following differential equation for acceleration ($a$) at every time step:
Where:

* **Velocity Update:** $v_{new} = v_{old} + a \cdot dt$
* **Position Update:** $x_{new} = x_{old} + v_{new} \cdot dt$

##  Simulation Analysis
Our 3D model reveals several key physical behaviors that align with theoretical expectations:

### 1. The Static Friction Breakout
The simulation demonstrates that if $m_2g < m_1g\sin(\theta) + f_{static}$, the system remains at rest (Acceleration = 0). This confirms the "threshold" nature of friction modeled in our `compute_acceleration` function.

### 2. Numerical Precision
By using a time step of $dt = 0.001s$, we achieve high precision in our velocity curves. A larger $dt$ would cause "overshoot" errors, but our Euler integration remains stable even at high acceleration, showing a smooth linear increase in velocity.

### 3. Effect of the Incline ($\theta$)
As the user increases the incline angle $\theta$ via the slider, the simulation dynamically reduces the Normal Force ($F_n = mg\cos(\theta)$), which in turn reduces the kinetic friction. This real-time feedback loop is the core achievement of our computational model.

$$a = \frac{m_2g - m_1g\sin(\theta) - f_{fric}}{m_1 + m_2}$$

## How to Run
1. Copy the source code from `main.py`.
2. Navigate to [Web VPython](https://webvpython.org/).
3. Paste the code into a new script and click **Run**.

## Contributors
* **Section B: Group 2 & 8**
* Submitted: March 23, 2026
