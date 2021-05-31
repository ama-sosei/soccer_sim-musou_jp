from utils import Others

class Attacker(Others):
	def processing_goal(self,data):
		if self._operation['ball']['x'] < self.x:
			self.catch_ball_around()
		else:
			self.catch_ball()





