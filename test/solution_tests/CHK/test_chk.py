from solutions.CHK import checkout_solution

class TestChk():
    def test_invalid(self):
        assert checkout_solution.checkout('ABCxAC') == -1
    
    def test_parse(self):
        assert checkout_solution.parse_skus('ABCAC') == {'A':2, 'B': 1, 'C': 2}
    
    def test_chk(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_multiples(self):
        assert checkout_solution.checkout('ABCACD') == 185

    def test_special_a(self):
        assert checkout_solution.checkout('ABCACDA') == 215

    def test_special_a5(self):
        assert checkout_solution.checkout('ABACACADA') == 285

    def test_special_a7(self):
        assert checkout_solution.checkout('ABACACADAAA') == 385

    def test_special_b(self):
        assert checkout_solution.checkout('ABCACDB') == 200

