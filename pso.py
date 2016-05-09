import random
import copy
from evalfuncs import *


class Particle:
	def __init__(self, evalFunc, minx, maxx):
		axes = evalFunc.axes
		self.position = [0.0 for i in range(axes)]
		self.velocity = [0.0 for i in range(axes)]
		self.best_pos = [0.0 for i in range(axes)]

		for i in range(axes):
			self.position[i] = ((maxx - minx) * random.random() + minx)
			self.velocity[i] = ((maxx - minx) * random.random() + minx)

		self.eval = evalFunc.eval(self.position)
		self.best_pos = copy.copy(self.position)
		self.best_eval = self.eval


def PSO(iterations, n, evalFunc, minx, maxx, w1, w2, w3):
	"""
	w1 - inertia factor
	w2 - cognitive factor for a particle
	w3 - social swarm factor
	"""
	axes = evalFunc.axes
	rnd = random.Random(0)
	particles = [Particle(evalFunc, minx, maxx) for i in range(n)]
	overall_best_pos = [0.0 for i in range(axes)]
	overall_best_eval = None

	for i in range(n):
		if particles[i].eval < overall_best_eval or overall_best_eval is None:
			overall_best_eval = particles[i].eval
			overall_best_pos = copy.copy(particles[i].position)

	iteration = 0
	while True: #iteration < iterations:
		# if iteration % 10 == 0 and iteration > 1:
		# 	print("Iteration: %d Best: %.3f" % (iteration, overall_best_eval))

		for i in range(n):
			for k in range(axes):
				particles[i].velocity[k] = ((w1 * particles[i].velocity[k]) +
										(w2 * rnd.random() * (particles[i].best_pos[k] - particles[i].position[k])) +
										(w3 * rnd.random() * (overall_best_pos[k] - particles[i].position[k])) )

				if particles[i].velocity[k] < minx:
					particles[i].velocity[k] = minx
				elif particles[i].velocity[k] > maxx:
					particles[i].velocity[k] = maxx

			for k in range(axes):
				particles[i].position[k] += particles[i].velocity[k]


			particles[i].eval = evalFunc.eval(particles[i].position)

			if particles[i].eval < particles[i].best_eval:
				particles[i].best_eval = particles[i].eval
				particles[i].best_pos = copy.copy(particles[i].position)

			if particles[i].eval < overall_best_eval:
				overall_best_eval = particles[i].eval
				overall_best_pos = copy.copy(particles[i].position)


			try:
				EvaluationOverflow.check()
			except EvaluationOverflow:
				return overall_best_pos

		iteration += 1
	return overall_best_pos


if __name__ == "__main__":
	#evalFunc = Sixhump()
	evalFunc = Rastrigin(axes=2)
	#evalFunc = Rosenbrock()
	#evalFunc = Griewangk()
	axes = evalFunc.axes
	maxParticles = 200
	maxIterations = 1000
	evalFunc.info()

	w1 = 0.7  # inertia
	w2 = 1.6  # cognitive
	w3 = 1.5  # social

	print("Particles: %d" % maxParticles)
	print("Axes: %d\nMax iterations: %d" % (axes, maxIterations))
	print ("Inertia: %f\nCognitive: %f\nSocial:%f" % (w1, w2, w3))
	print evalFunc.info()

	best_position = PSO(maxIterations, maxParticles, evalFunc, evalFunc.start, evalFunc.end, w1, w2, w3)

	print("Swarm position %s" % map(float2e, best_position))
	print("Solution for best found position: %.6f" % evalFunc.eval(best_position))
