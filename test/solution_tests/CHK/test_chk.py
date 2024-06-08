from solutions.CHK import checkout_solution

# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+

class TestChk():
    def test_parse(self):
        assert checkout_solution.parse_skus('ABCAC') == {'A':2, 'B': 1, 'C': 2}
    
    def test_chk(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_multiples(self):
        assert checkout_solution.checkout('ABCACD') == 185

    def test_special_a(self):
        assert checkout_solution.checkout('ABCACDA') == 215

    def test_special_b(self):
        assert checkout_solution.checkout('ABCACDB') == 200