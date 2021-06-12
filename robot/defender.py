from utils import Others

class Defender(Others):
	i=0
	def processing_defence(self, data:dict):
		if self.team=="B":
			print(f"{self.i}:{self.chk_attack()}")
			self.i+=1
		a, _=self.chk_attack()
		if a:
			return self.catch_ball()
		elif self.chk_position():#守備範囲外の場合
			if self.chk_ball_position(): #自陣にボール
				self.catch_ball()
			else: #敵陣にボール
				if self.team == "B":
					if self.ball['x'] > self._get_min_x():
						self.catch_ball()
					else:
						return self.go_point_use_coordinate(0.4,0)
				else:
					return self.go_point_use_coordinate(-0.4,0)
		else:
			if self.chk_ball_position():
				self.catch_ball()
			else:
				if self.y < 0.3 and self.y > -0.3: #ゴールの範囲内のみ
					return self.go_point_use_coordinate(self.x,self.ball['y'])
				else:
					return self.go_point_use_coordinate(self.x,0)

	def chk_position(self):
		if self.team == "B":
			return False if (self.x > 0.1 and self.x > 0.4) else True
		else:
			return False if (self.x < -0.1 and self.x < -0.4) else True


	def chk_attack(self):
		other_robo_x=[self._operation[i]["x"] for i in ["B1", "B2", "B3", "Y1", "Y2", "Y3"] if i != self.name]
		print(other_robo_x,self.ball["x"])
		if self.chk_ball_position():
			return False, 1
		elif (
			(self.team == "B" and max(other_robo_x) < self.ball["x"]) or 
			(self.team == "Y" and min(other_robo_x) > self.ball["x"])
		):
			return True , 0
		else:
			return False, 2



