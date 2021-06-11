from utils import Others


class Attacker(Others):
	def processing_goal(self, data:dict):
		if self.ball['x'] < self.x:
			self.catch_ball_around()
		else:
			self.catch_ball()





