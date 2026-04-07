# ============================================
# ATWOOD MACHINE SIMULATION (WITH INCLINE)
# This program simulates motion using forces,
# friction, and Newton’s 2nd law.
# ============================================
Web VPython 3.2
# Create the simulation window
scene = canvas(title='Atwood Machine: Interactive Simulation',
               width=1450, height=780,
               center=vector(3.2, 2.2, 0),
               background=color.white)

# ============================================================
# Physics constants (gravity, time step, time)
# ============================================================
g, dt, t, t_max = 9.8, 0.001, 0, 20
running = True

# ============================================================
# INPUT RANGES(to prevent invalid values)
# ============================================================
M_MIN, M_MAX = 0.1, 10.0
MU_MIN, MU_MAX = 0.0, 1.0
THETA_MIN, THETA_MAX = 5, 85

# ============================================================
# USER PARAMETERS(change these to test different cases)
# ============================================================
m1, m2 = 2.5o, 2.3o
mu_k = 0.18
mu_s = mu_k * 1.2  
theta_deg = 30
theta = radians(theta_deg)
x, v = 0.0, 0.0

# ============================================================
# Scene geometry (sizes and positions of objects)
# ============================================================
table_length, table_width, table_thick, table_top_y = 12.0, 4.6, 0.35, 1.4
ground_y = -1.8
ramp_length, ramp_width, ramp_height = 4.8, 1.4, 0.08 
pulley_radius, vertical_drop0 = 0.22, 2.3

Z_ACTION = 0
Z_TABLE = -2.5

incline_axis, normal_dir = vector(1,0,0), vector(0,1,0)
ramp_start_line, pulley_center = vector(0,0,0), vector(0,0,0)

s0, s_min, s_max = 1.2, 0.7, 3.9
x_min, x_max = s_min - s0, s_max - s0

# ============================================================
# HELPERS to keep values within limits
# ============================================================
def clamp(val, low, high):
    if val < low: return low
    if val > high: return high
    return val
# Adjust block size based on mass for visualization
def block1_size_from_mass(m):
    scale = sqrt(m)
    return vector(clamp(0.35 + 0.16*scale, 0.40, 1.00), clamp(0.14 + 0.10*scale, 0.18, 0.60), clamp(0.22 + 0.09*scale, 0.25, 0.70))

def block2_size_from_mass(m):
    side = clamp(0.16 + 0.12*sqrt(m), 0.22, 0.75)
    return vector(side, side, side)

def set_warning(msg):
    warning_text.text = 'Warning: ' + msg if msg != '' else ''

def update_top_status():
    top_status.text = 'Current values -> m1 = ' + str(round(m1,2)) + ' kg,   m2 = ' + str(round(m2,2)) + ' kg,   mu_k = ' + str(round(mu_k,2)) + ',   theta = ' + str(round(theta_deg,1)) + ' deg'

def apply_mass_input(which_mass, value):
    global m1, m2
    if value == None or value < M_MIN or value > M_MAX:
        set_warning(which_mass + ' invalid (0.1 - 10kg).')
        return
    if which_mass == 'm1': m1 = value
    else: m2 = value
    set_warning('')
    update_top_status()

def m1_input_bind(box): apply_mass_input('m1', box.number)
def m2_input_bind(box): apply_mass_input('m2', box.number)

def slider_update(s):
    global mu_k, mu_s, theta_deg, theta
    mu_k, theta_deg = mu_slider.value, theta_slider.value
    mu_s = mu_k * 1.2
    theta = radians(theta_deg)
    set_warning('')
    update_top_status()

def reset_motion(btn):
    global x, v, t, running, vel_curve, accel_curve
    x, v, t, running = 0, 0, 0, True
    vel_curve.delete()
    vel_curve = gcurve(graph=vel_graph, color=color.blue)
    accel_curve.delete()
    accel_curve = gcurve(graph=accel_graph, color=color.red)
    update_geometry(); update_block_sizes(); update_positions(); update_rope()

def toggle_running(btn):
    global running
    running = not running

def update_geometry():
    global incline_axis, normal_dir, ramp_start_line, pulley_center, x_min, x_max, s_max
    incline_axis, normal_dir = vector(cos(theta), sin(theta), 0), vector(-sin(theta), cos(theta), 0)
    pulley_center = vector(table.pos.x + table.size.x/2 - 0.25, table_top_y + ramp_length*sin(theta), Z_ACTION)
    ramp_start_line = vector(pulley_center.x - ramp_length*cos(theta), table_top_y, Z_ACTION)
    ramp_body.axis = incline_axis
    ramp_body.size = vector(ramp_length, ramp_height, ramp_width)
    ramp_body.pos = ramp_start_line + 0.5*ramp_length*incline_axis + 0.5*ramp_height*normal_dir
    pulley.pos = pulley_center + vector(0,0,-0.22)
    axle.pos = pulley_center
    support_height = max(pulley_center.y - table_top_y, 0.15)
    support.pos, support.size = vector(pulley_center.x, table_top_y + support_height/2, Z_ACTION), vector(0.10, support_height, 0.10)
    s_max = ramp_length - 0.65
    x_min, x_max = s_min - s0, s_max - s0

def update_block_sizes():
    block1.size, block2.size = block1_size_from_mass(m1), block2_size_from_mass(m2)
# Update positions of the blocks
def update_positions():
    s = clamp(s0 + x, s_min, s_max)
    block1.pos = ramp_start_line + s*incline_axis + (ramp_height/2 + block1.size.y/2)*normal_dir
    block1.axis, block1.up = incline_axis, normal_dir
    block2.pos = vector(pulley_center.x, pulley_center.y - vertical_drop0 - x - block2.size.y/2, Z_ACTION)
# Update rope connection between objects
def update_rope():
    p1, p2 = block1.pos + 0.47*block1.size.x*incline_axis, pulley_center + vector(-pulley_radius*cos(theta), -pulley_radius*sin(theta), 0)
    p3, p4 = pulley_center + vector(0, -pulley_radius, 0), block2.pos + vector(0, block2.size.y/2, 0)
    string1.clear(); string1.append(pos=p1); string1.append(pos=p2)
    string_arc.clear()
    for i in range(17):
        ang = -(pi-theta) + i*(-(pi/2) - (-(pi-theta)))/16
        string_arc.append(pos=pulley_center + pulley_radius*vector(cos(ang), sin(ang), 0))
    string2.clear(); string2.append(pos=p3); string2.append(pos=p4)

def update_pulley_rotation():
    phi = -x/pulley_radius
    spoke.pos, spoke.axis = pulley_center + vector(0,0,0.01), vector(pulley_radius*cos(phi), pulley_radius*sin(phi), 0)

def hanging_block_hits_ground(): return (block2.pos.y - block2.size.y/2) <= ground_y
# Main physics function (calculates acceleration using forces)
def compute_acceleration(v_now):
  # Driving force (difference between hanging and incline forces)
    drive = m2*g - m1*g*sin(theta)
  # Normal force on the inclined surface
    fn = m1*g*cos(theta)
  # Kinetic friction (acts when object is moving)
    fk = mu_k * fn
  # Maximum static friction (prevents motion)
    fs_max = mu_s * fn
    
    # Static logic
  # Check if object is nearly at rest#
    if abs(v_now) < 1e-5:
        if abs(drive) <= fs_max: return 0
        else:
            f_direction = 1 if drive > 0 else -1
          # Newton’s Second Law: acceleration = net force / total mass
            return (drive - f_direction * fk) / (m1 + m2)
    
    # Moving logic (Friction opposes velocity)
    f_friction = -fk if v_now > 0 else fk
    return (drive + f_friction) / (m1 + m2)

def compute_motion_state(a_now, v_now, is_running):
    if hanging_block_hits_ground(): return 'Stopped: reached ground'
    if x >= x_max: return 'Stopped: reached pulley'
    if not is_running or (abs(v_now) < 1e-4 and abs(a_now) < 1e-4):
        return 'At rest'
    return 'Moving: m1 up, m2 down' if v_now > 0 else 'Moving: m1 down, m2 up'

def update_info_panel(a, T):
    state = compute_motion_state(a, v, running)
    info.text = "SIMULATION DATA\n\n" + \
                "t = " + str(round(t,2)) + " s\n" + \
                "a = " + str(round(a,3)) + " m/s^2\n" + \
                "v = " + str(round(v,3)) + " m/s\n" + \
                "x = " + str(round(x,3)) + " m\n" + \
                "T = " + str(round(T,3)) + " N\n" + \
                "m1 = " + str(round(m1,2)) + " kg\n" + \
                "m2 = " + str(round(m2,2)) + " kg\n" + \
                "mu_k = " + str(round(mu_k,2)) + "\n" + \
                "theta = " + str(round(theta_deg,1)) + " deg\n\n" + \
                "STATE: " + state

# ============================================================
# UI & OBJECTS
# ============================================================
scene.append_to_caption('\nAtwood Machine Controls\n')
warning_text = wtext(text='')
scene.append_to_caption('\nm1 [kg]: '); m1_input = winput(bind=m1_input_bind, type='numeric', text='2.5')
scene.append_to_caption('  m2 [kg]: '); m2_input = winput(bind=m2_input_bind, type='numeric', text='2.3')
scene.append_to_caption('\nmu_k: '); mu_slider = slider(min=MU_MIN, max=MU_MAX, value=mu_k, length=260, bind=slider_update)
scene.append_to_caption('\ntheta [deg]: '); theta_slider = slider(min=THETA_MIN, max=THETA_MAX, value=theta_deg, length=260, bind=slider_update)
scene.append_to_caption('\n\n'); top_status = wtext(text='')
scene.append_to_caption('\n\n'); button(text='Pause / Resume', bind=toggle_running); button(text='Reset Motion', bind=reset_motion)

ground = box(pos=vector(2.2, ground_y - 0.12, -3.0), size=vector(18, 0.24, 6), color=vector(0.5,0.5,0.5))
table = box(pos=vector(1.2, table_top_y - table_thick/2, -2.4), size=vector(12, table_thick, 4.6), color=vector(0.28,0.28,0.30))
ramp_body = box(size=vector(ramp_length, ramp_height, 1.4), color=color.gray(0.7), shininess=0.8)
support = box(size=vector(0.10, 1.0, 0.10), color=color.gray(0.45))
pulley = cylinder(axis=vector(0,0,0.44), radius=pulley_radius, color=color.orange)
axle, spoke = sphere(radius=0.045, color=color.black), cylinder(radius=0.025, color=color.black)
block1, block2 = box(color=color.green), box(color=color.red)
string1, string_arc, string2 = curve(radius=0.024, color=color.black), curve(radius=0.024, color=color.black), curve(radius=0.024, color=color.black)

vel_graph = graph(title='Velocity vs Time', xtitle='t (s)', ytitle='v (m/s)', width=450, height=220)
vel_curve = gcurve(graph=vel_graph, color=color.blue)
accel_graph = graph(title='Acceleration vs Time', xtitle='t (s)', ytitle='a (m/s^2)', width=450, height=220)
accel_curve = gcurve(graph=accel_graph, color=color.red)

panel_bg = box(size=vector(4.2, 6.6, 0.04), color=vector(0.96,0.96,0.96))
info = label(text='', box=False, height=11, color=color.black, line=False)

update_geometry(); update_block_sizes(); update_positions()
# Main simulation loop (runs continuously)
while True:
    rate(900)
    update_geometry(); update_block_sizes()
    
    # Calculate current acceleration and Tension
    a = compute_acceleration(v)
    current_T = m2 * (g - a)
    
    if running and t < t_max:
        # Check if the system is at a standstill due to friction
        if abs(v) < 1e-5 and a == 0:
            pass # Running but not moving yet
        else:
            v += a*dt
            x += v*dt
            t += dt # Only increment time when motion is active
            
            # Boundary conditions
            if x <= x_min or x >= x_max or hanging_block_hits_ground():
                v, a = 0, 0
                running = False 
            
            update_positions()
            vel_curve.plot(t, v); accel_curve.plot(t, a)
    else:
        update_positions()
    
    update_rope(); update_pulley_rotation(); update_top_status()
    px, py = scene.center.x + 1.35*scene.range, scene.center.y + 0.45*scene.range
    panel_bg.pos, info.pos = vector(px, py - 1.5, -0.25), vector(px, py + 0.7, 0)
    update_info_panel(a, current_T)
