import math
import struct
from typing import Tuple
from controller import Robot
from attacker import Attacker
from defender import Defender

TIME_STEP = 64
ROBOT_NAMES = ["B1", "B2", "B3", "Y1", "Y2", "Y3"]
N_ROBOTS = len(ROBOT_NAMES)


class RCJSoccerRobot(Attacker,Defender):
	def __init__(self):
		self.robot = Robot()
		self.name = self.robot.getName()
		self.team = self.name[0]
		self.player_id = int(self.name[1])

		self.receiver = self.robot.getDevice("receiver")
		self.receiver.enable(TIME_STEP)

		self.left_motor = self.robot.getDevice("left wheel motor")
		self.right_motor = self.robot.getDevice("right wheel motor")

		self.left_motor.setPosition(float('+inf'))
		self.right_motor.setPosition(float('+inf'))

		self.left_motor.setVelocity(0.0)
		self.right_motor.setVelocity(0.0)

	def parse_supervisor_msg(self, packet: str) -> dict:
		struct_fmt = 'ddd' * N_ROBOTS + 'dd' + '?'

		unpacked = struct.unpack(struct_fmt, packet)

		data = {}
		for i, r in enumerate(ROBOT_NAMES):
			data[r] = {
				"x": unpacked[3 * i],
				"y": unpacked[3 * i + 1],
				"orientation": unpacked[3 * i + 2]
			}
		ball_data_index = 3 * N_ROBOTS
		data["ball"] = {
			"x": unpacked[ball_data_index],
			"y": unpacked[ball_data_index + 1]
		}

		waiting_for_kickoff_data_index = ball_data_index + 2
		data["waiting_for_kickoff"] = unpacked[waiting_for_kickoff_data_index]
		return data

	def get_new_data(self) -> dict:
		packet = self.receiver.getData()
		self.receiver.nextPacket()

		return self.parse_supervisor_msg(packet)

	def is_new_data(self) -> bool:
		return self.receiver.getQueueLength() > 0

	def get_angles(self, ball_pos: dict, robot_pos: dict) -> Tuple[float, float]:
		robot_angle: float = robot_pos['orientation']

		# Get the angle between the robot and the ball
		angle = math.atan2(
			ball_pos['y'] - robot_pos['y'],
			ball_pos['x'] - robot_pos['x'],
		)

		if angle < 0:
			angle = 2 * math.pi + angle

		if robot_angle < 0:
			robot_angle = 2 * math.pi + robot_angle

		robot_ball_angle = math.degrees(angle + robot_angle)
		robot_ball_angle -= 90
		if robot_ball_angle > 360:
			robot_ball_angle -= 360

		return robot_ball_angle, robot_angle

	def run(self):
		while self.robot.step(TIME_STEP) != -1:
			data=self.fetch_operation()
			if data:
				if self.x == self._get_min_x():
					func = self.processing_defence
				else:
					func = self.processing_goal
				func(data)

	def _get_min_x(self):
		if self.team == 'Y':
			return min([self._operation[i]['x'] for i in self._operation if i[0] == self.team])
		else:
			return max([self._operation[i]['x'] for i in self._operation if i[0] == self.team])


RCJSoccerRobot().run()
