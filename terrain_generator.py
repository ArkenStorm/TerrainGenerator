# from numba import cuda

# cuda.select_device(0)

import pyglet
from pyglet.gl import glLoadIdentity, glRotatef, glViewport, glMatrixMode, GL_PROJECTION, gluPerspective, GL_MODELVIEW, glFlush
from noise import pnoise2
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from bisect import bisect
import random


def generate_2d_noise(field_range, divisor, octaves, persistence=0.5, lacunarity=2.0):
	# basic noise field
	# Divisor should be such that a float is passed into pnoise2
	noise_field = []
	for row in field_range:
		noise_row = []
		for col in field_range:
			noise_row.append(pnoise2(row / divisor, col / divisor, octaves=octaves,
									 persistence=persistence, lacunarity=lacunarity))
		noise_field.append(noise_row)
	noise_field = np.array(noise_field)

	return noise_field


def generate_ridged_noise(field_range, divisor, octaves=1, threshold=0.1):
	# ridged noise field
	noise_field = generate_2d_noise(field_range, divisor, octaves)

	return threshold_field(noise_field, threshold)


def threshold_field(noise_field, threshold=0.1):
	# ridge thickness is directly proportional to threshold value
	return np.select([noise_field > threshold, noise_field < -threshold,
			   noise_field <= threshold, noise_field >= -threshold], [0, 0, 1, 1])


def render_pyplot(terrain):
	heightmap = plt.figure().add_subplot(111, projection='3d')
	heightmap.plot_surface(x, y, terrain, cmap=cm.terrain, linewidth=0, antialiased=False)
	plt.axis("off")
	plt.show()


x_angle = y_angle = 0

terrain_dimension = 1000
terrain_range = range(1, terrain_dimension + 1)
x, y = np.meshgrid(terrain_range, terrain_range)

# cool multiplied ridged generation
terrain_map = generate_2d_noise(terrain_range, 357, 15)
terrain_map *= generate_ridged_noise(terrain_range, 157)
terrain_map *= generate_2d_noise(terrain_range, 750, 14)
terrain_map *= generate_2d_noise(terrain_range, 463, 7)
terrain_map *= 1000

render_pyplot(terrain_map)

# Pyglet window setup
# win = pyglet.window.Window(width=1000, height=800, resizable=False, visible=False,
# 						   config=pyglet.gl.Config(sample_buffers=1, samples=4, double_buffer=True, depth_size=24))
#
# # change to have multiple colors per layer?
# # grass, trees, stone, snow
# color_list = [[72, 135, 54], [35, 89, 21], [80, 80, 80], [255, 255, 255]]
# # construct list of vertices and list of corresponding colors
# dim = range(terrain_dimension)
#
# terrain_max = terrain_map.max()
# terrain_min = terrain_map.min()
# color_range = np.linspace(terrain_min, terrain_max, len(color_list) * 2)
#
# graphical_vertices = []
# vertex_colors = []
# for row in dim:
# 	for col in dim:
# 		height = terrain_map[row, col]
# 		graphical_vertices.extend((row, height, col))
# 		# choose vertex color from dict
# 		bound = bisect(color_range, height)
# 		if bound == 0:
# 			vertex_colors.extend(color_list[0])
# 		elif bound // 2 == len(color_list) - 1 or bound // 2 == len(color_list):
# 			vertex_colors.extend(color_list[-1])
# 		elif bound % 2 == 0:
# 			# randomly choose between two colors
# 			vertex_colors.extend(color_list[random.choice([(bound//2), (bound//2)+1])])
# 		else:
# 			vertex_colors.extend(color_list[bound//2])

# vertex_list = pyglet.graphics.vertex_list(terrain_map.size, 'v3f', 'c3B')
# vertex_list.vertices = graphical_vertices
# vertex_list.colors = vertex_colors

# vertex_list = pyglet.graphics.vertex_list(3,
#     ('v2i', (10, 15, 30, 35, 45, 50)),
#     ('c3B', (0, 0, 255, 0, 255, 0, 255, 0, 0))
# )
#
#
# label = pyglet.text.Label('Terrain Generator',
# 						  font_name='Times New Roman',
# 						  font_size=16,
# 						  color=(255,255,255,255),
# 						  x=win.width // 2, y=win.height,
# 						  anchor_x='center', anchor_y='top')
#
#
# @win.event
# def on_mouse_drag(mx, my, dx, dy, buttons, modifiers):
# 	global x_angle, y_angle
# 	x_angle += dx * 0.3
# 	y_angle += dy * 0.3
#
#
# @win.event
# def on_draw():
# 	global x_angle, y_angle
# 	win.clear()
# 	label.draw()
# 	vertex_list.draw(pyglet.gl.GL_POINTS)
# 	# glMatrixMode(GL_PROJECTION)
# 	# glLoadIdentity()
# 	# gluPerspective(90, 1, 0.1, 10000)
# 	# glMatrixMode(GL_MODELVIEW)
# 	# glRotatef(x_angle, 1.0, 0, 0)
# 	# glRotatef(y_angle, 0, 1.0, 0)
#
#
# win.set_visible()
# pyglet.app.run()

