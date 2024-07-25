import unittest

from main import new_gen, get_final


class TestNewGen(unittest.TestCase):

  def setUp(self):
    self.chr_1 = 'A'
    self.chr_2 = 'B'
    self.rule_1 = 'A-/B|+A+/B|-A'
    self.rule_2 = 'BB'

  def test_a(self):
    self.assertEqual(new_gen("A", self.chr_1, self.chr_2, self.rule_1, self.rule_2), "A-/B|+A+/B|-A")

  def test_b(self):
    self.assertEqual(new_gen("B", self.chr_1, self.chr_2, self.rule_1, self.rule_2), "BB")

  def test_ab(self):
    self.assertEqual(new_gen("AB", self.chr_1, self.chr_2, self.rule_1, self.rule_2), "A-/B|+A+/B|-ABB")

class TestGetFinal(unittest.TestCase):

  def setUp(self):
    self.chr_1 = 'A'
    self.chr_2 = 'B'
    self.rule_1 = 'A-B+A+B-A'
    self.rule_2 = 'BB'

  def test_work(self):
    self.assertEqual(get_final("A-B-B", 2, self.chr_1, self.chr_2, self.rule_1, self.rule_2), "A-B+A+B-A-BB+A-B"
                                                                                              "+A+B-A+BB-A-B+A+B"
                                                                                              "-A-BBBB-BBBB")

if __name__ == "__main__":
  unittest.main()