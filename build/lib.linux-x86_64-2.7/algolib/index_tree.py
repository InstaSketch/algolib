
class index_tree(object):
	def __init__(self, is_rg):
		self.left = None
		self.right = None
		self.is_rg = is_rg
		self.median = None
		self.parent = None
		self.images = []
		# self.data = None

	def height(self):
		if (self.left):
			left_height = self.left.height()
		else:
			left_height = 0

		if (self.right):
			right_height = self.right.height()
		else:
			right_height = 0

		if (left_height > right_height):
			return 1 + left_height
		else:
			return 1 + right_height