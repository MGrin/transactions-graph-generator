import uuid

class Node:
	def toRow(self, headers):
		row = []
		for field in headers: row.append(str(getattr(self, field)))
		return '|'.join(row)
