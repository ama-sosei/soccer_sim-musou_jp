from typing import Tuple, Union, NoReturn

def get_direction(ball_angle: float) -> int:
	if ball_angle >= 345 or ball_angle <= 15:
		return 0
	return -1 if ball_angle < 180 else 1

class Others:
	_operation=None

	def display_operation(self) -> NoReturn:
		print(f"----{self.name}----")
		print(f"x:{self.x}")
		print(f"y:{self.y}")
		print(f"ball_angle:{self.ball_angle}")
		print(f"robot_angle:{self.robot_angle}")
		print(f"orientation:{self.orientation}")
		print(f"direction:{self.direction}")
		print(f"ball:{self.ball}")


	def motor(self,left:int, right:int) -> int:
		self.left_motor.setVelocity(left*-1)
		self.right_motor.setVelocity(right*-1)
		return 0

	def fetch_operation(self) -> Union[int, None]:
		#データ取得andインスタンス変数の設定
		if self.is_new_data():
			self._operation=self.get_new_data()
			self.x, self.y, self.ball = self._operation[self.name]["x"], self._operation[self.name]["y"], self._operation['ball']
			self.ball_angle, self.robot_angle=self.get_angles(self.ball,self._operation[self.name])
			if self._operation[self.name]["orientation"]*-1 < 0:
				self.orientation = True
			else:
				self.orientation = False
			self.direction = get_direction(self.ball_angle)
			return self._operation
		else:
			return None

	def get_ball_angle(self) -> float:
		result, _ = self.get_angles(self.ball,self._operation[self.name])
		return result

	def get_robot_angle(self) -> float:
		_, result = self.get_angles(self.ball,self._operation[self.name])
		return result

	def catch_ball(self) -> int:
		if self.direction:
			return self.motor(self.direction * -5, self.direction * 5)
		else:
			return self.motor(5,5)

	def catch_ball_around(self) -> int:
		direction=self.ball_angle*(2/3)
		if direction>360:
			direction-=360
		direction=get_direction(direction)
		if direction:
			return self.motor(direction * -5, direction * 5)
		else:
			return self.motor(5,5)



	def chk_ball_position(self) -> bool:#自陣True 敵陣False
		if self.team=="B":
			return True if self.ball["x"]>0 else False
		else:
			return True if self.ball["x"]<0 else False

	def go_point_use_coordinate(self, x:float, y:float) -> int:
		angle, _ =self.get_angles({'x':x,'y':y},self._operation[self.name])
		direction = get_direction(angle)
		if direction:
			return self.motor(direction * -5, direction * 5)
		else:
			return self.motor(5,5)

	def _get_min_x(self) -> float:
		if self.team == 'Y':
			return min([self._operation[i]['x'] for i in self._operation if i[0] == self.team])
		else:
			return max([self._operation[i]['x'] for i in self._operation if i[0] == self.team])
