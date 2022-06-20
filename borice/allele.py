class Allele(object):
	"""An Allele is an object representing an allele in the population. It has a y value.
	"""
	def __init__(self, allele, locus):
		self.name = allele
		self.locus = locus
		self.y = 1.0
		self.af_list = []
	
	def __str__(self):
		"""Returns an allele string with the allele name and the locus name separated by a comma.
		"""
		return repr(self.name) + ', locus' + repr(self.locus)