from typing import NoReturn


class Attacker:
	def processing_goal(self, data:dict) -> NoReturn:
		if self.ball['x'] < self.x:
			self.catch_ball_around()
		else:
			self.catch_ball()



