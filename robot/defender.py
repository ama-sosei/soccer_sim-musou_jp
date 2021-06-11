from utils import Others

class Defender(Others):

	def processing_defence(self,data):
		return self.go_point_use_coordinate(2,0)
		if self.chk_position():#守備範囲外の場合
			if self.chk_ball_position(): #自陣にボール
				self.catch_ball()
			else: #敵陣にボール
				if self.team == "B":
					if self._operation["ball"]['x'] > self._get_min_x():
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
					return self.go_point_use_coordinate(self.x,self._operation["ball"]['y'])
				else:
					return self.go_point_use_coordinate(self.x,0)

	def chk_position(self):
		if self.team == "B":
			return False if (self.x > 0.1 and self.x > 0.4) else True
		else:
			return False if (self.x < -0.1 and self.x < -0.4) else True







